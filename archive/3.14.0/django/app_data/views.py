# app_data - views.py
# (c) cavaliba.com 

import re
import yaml 
import json 

from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext as _

from app_home.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL
from app_user.aaa import start_view
from app_home.configuration import get_configuration

from .models import DataInstance

from .data import Instance
from .data import get_classes
from .data import get_class_by_name
from .data import get_instance_by_handle
from .data import get_schema
# export
from .data import data_yaml_response
from .data import data_json_response

from app_data.loader import load_broker

from app_data.pipeline import list_pipelines
from app_data.pipeline import apply_pipeline

from .forms import DataUploadForm

from .dataview import get_dataviews_for_class
from .dataview import DataView

from .permissions import has_read_permission_on_class
from .permissions import has_read_permission_on_instance
from .permissions import has_delete_permission_on_class
from .permissions import has_delete_permission_on_instance
from .permissions import has_edit_permission_on_instance
from .permissions import has_create_permission_on_class


# -----------------------------------------
# helper
#-----------------------------------------

# def is_user_in_group(aaa=None, gname=None):

#     if gname in aaa["groups"] + aaa["groups_indirect"]:
#         return True
#     return False



# def has_read_permission_on_class(aaa=None, classobj=None):
#     # classobj is a DB object

#     if not aaa:
#         return False
    
#     if not classobj:
#         return False

#     if '*' in aaa['perms']:
#         return True
    
#     # global p_data_admin
#     if "p_data_admin" in aaa["perms"]:
#         return True

#     # p_admin on classobj
#     if classobj.p_admin:
#         if classobj.p_admin in aaa["perms"]:
#             return True

#     # p_read  
#     if classobj.p_read:
#         if classobj.p_read in aaa["perms"]:
#             return True
#         else:
#             return False
    
#     # default    
#     if "p_data_read" in aaa["perms"]:
#         return True

#     return False


# def has_read_permission_on_instance(aaa=None, iobj=None):
#     # iobj is a DB object

#     if not aaa:
#         return False
    
#     if not iobj:
#         return False

#     if '*' in aaa['perms']:
#         return True

#     if "p_data_admin" in aaa["perms"]:
#         return True

#     # class permission ?
#     if not has_read_permission_on_class(aaa, classobj=iobj.classobj):
#         return False
    
#     # p_admin on classobj ? (allow direct & stop inheritance)
#     if iobj.classobj.p_admin:
#         if iobj.classobj.p_admin in aaa["perms"]:
#             return True
            
#     # instance permission
#     if iobj.p_read:
#         if iobj.p_read in aaa["perms"]:
#             return True
#         else:
#             return False

#     # default    
#     if "p_data_read" in aaa["perms"]:
#         return True

#     return False

# # -- delete

# def has_delete_permission_on_class(aaa=None, classobj=None):
#     # classobj is a DB object

#     if not aaa:
#         return False
    
#     if not classobj:
#         return False

#     if '*' in aaa['perms']:
#         return True

#     # global p_data_admin: allow all on data
#     if "p_data_admin" in aaa["perms"]:
#         return True

#     # p_admin on classobj : allow all on this class
#     if classobj.p_admin:
#         if classobj.p_admin in aaa["perms"]:
#             return True

#     # p_delete: allow delete on this class
#     if classobj.p_delete:
#         if classobj.p_delete in aaa["perms"]:
#             return True
#         else:
#             return False
    
#     # default: allow delete on class / all instances ; overridable
#     if "p_data_delete" in aaa["perms"]:
#         return True

#     return False


# def has_delete_permission_on_instance(aaa=None, iobj=None):
#     # iobj is a DB object

#     if not aaa:
#         return False
    
#     if not iobj:
#         return False

#     if '*' in aaa['perms']:
#         return True

#     if "p_data_admin" in aaa["perms"]:
#         return True

#     # class permission needed
#     if not has_delete_permission_on_class(aaa, classobj=iobj.classobj):
#         return False
    
#     # p_admin on classobj: allow all on this class; no override 
#     if iobj.classobj.p_admin:
#         if iobj.classobj.p_admin in aaa["perms"]:
#             return True
            
#     # instance permission
#     if iobj.p_delete:
#         if iobj.p_delete in aaa["perms"]:
#             return True
#         else:
#             return False

#     # default: class level overridable
#     if "p_data_delete" in aaa["perms"]:
#         return True

#     return False

# ----------------------------------------------
# list of Classes
# ----------------------------------------------
def private(request):

    context = start_view(request, app="data", view="private", noauth="app_sirene:index", 
        perm="p_data_read", noauthz="app_home:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]

    dataclasses = get_classes(is_enabled=True)
    filtered = []

    # Permission
    for classobj in dataclasses:    
        if has_read_permission_on_class(aaa=aaa, classobj=classobj):
            filtered.append(classobj)


    # page/order for UI
    # -----------------
    # [  [page1, [class1, class2,  ...] , [ page2, [...] ] ,  ... ]
    paginated = []
    pagelist = []
    index = {}   # page => [class1, class2]
    default_name = get_configuration("home", "GLOBAL_APPNAME")

    for classobj in filtered:
        # order = element.order
        page = classobj.page
        if not page:
            page = default_name
        if len(page) == 0:
            page = default_name
        if page not in index:
            index[page] = []
            pagelist.append(page)
        index[page].append(classobj)    

    for p in pagelist:
        paginated.append( [p, index[p] ])


    log(DEBUG, aaa=aaa, app="data", view="private", action="list", status="OK", data="{} classes".format(len(filtered)))

    context["dataclasses"] = filtered
    context["paginated"] = paginated
    return render(request, 'app_data/private.html', context)

# -------------------------------------------------------------------------
# Instance List 
# -------------------------------------------------------------------------
# V3.10 : always bigset

def instance_list(request, classname=None):

    context = start_view(request, app="data", view="instance_list", noauth="app_sirene:index", 
        perm="p_data_read", noauthz="app_data:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]

    if not classname:
        return redirect("app_data:private")
    context["classname"] = classname

    classobj = get_class_by_name(classname)
    if not classobj:
        redirect("app_data:private")
    context["classobj"] = classobj

    # Permission on Class ?
    if not has_read_permission_on_class(aaa=aaa, classobj=classobj):
        log(WARNING, aaa=aaa, app="data", view="instance", action="list", status="KO", data=_("Not allowed")) 
        messages.add_message(request, messages.ERROR, _("Not allowed"))
        return redirect("app_data:private")        


    # size
    # NEXT: faster = use precomputed bigset attribut from class
    # bigset_size = int(get_configuration("data","DATA_BIGSET_SIZE"))
    count = classobj.datainstance_set.count()
    context["count"] = count

    # export mode ? (export all)
    # TODO: filter permissions per exported instance
    output = request.GET.get("o","")
    if output != "":

        # TODO - update permission check (global built-in / per-class )
        if not ('p_data_admin' in aaa["perms"] or 'p_data_export' in aaa["perms"]):
            log(WARNING, aaa=aaa, app="data", view="instance_list", action="export", status="KO", data=_("Not allowed")) 
            messages.add_message(request, messages.ERROR, _("Not allowed"))
            return redirect("app_data:private")

        # refuse to export too big
        try:
            export_max = int(get_configuration("data","EXPORT_INTERACTIVE_MAX_SIZE"))
        except:
            export_max = 1000

        if count > export_max:
            log(ERROR, aaa=aaa, app="data", view="instance", action="export", status="KO", data=f"Export too big for {classname}") 
            messages.add_message(request, messages.ERROR, _("Export too large for interactive export."))
            return redirect("app_data:instance_list", classname)


        #export_data(classes=["app"])
        if output == "yaml":
            log(INFO, aaa=aaa, app="data", view="instance_list", action="export", status="OK", data="yaml") 
            response = data_yaml_response(classes = [classname])
            return response 
        
        elif output == "json":
            log(INFO, aaa=aaa, app="data", view="instance_list", action="export", status="OK", data="json") 
            response = data_json_response(classes = [classname])
            return response   


    # QUERY
    query = ""
    if request.method == "POST":
        if request.POST.get('query'):
            query = request.POST.get('query')
            m = re.compile(r'[a-zA-Z0-9()_/.-]*$')
            if not m.match(query):
                #return redirect("app_data:private")
                query = ""
    context["query"] = query

    # PAGE SIZE / OFFSET
    # ------------------
    max_size = int(get_configuration("data","DATA_MAX_SIZE"))
    default_size = int(get_configuration("data","DATA_DEFAULT_SIZE"))
    default_page = 1
    
    # # session ?
    session_size = request.session.get(classname+"_size", default_size)
    session_page = request.session.get(classname+"_page", default_page)
    try:
        size = int(request.GET.get("size", session_size))
        page = int(request.GET.get("page",session_page))
    except:
        return redirect("app_data:private")


    if page < 1 or size < 1:
        request.session[classname+"_size"] = default_size
        request.session[classname+"_page"] = default_page
        return redirect("app_data:private")

    if size > max_size:
        size = default_size

    if (page-1) * size > count:
        page = 1
        size = default_size

    offset = (page-1) * size
    limit = offset + size
    # # session
    request.session[classname+"_size"] = size
    request.session[classname+"_page"] = page

    # HERE, Get Instances
    # -------------------
    if len(query) > 0:
        # filter on displayname Q() | Q()
        instances = DataInstance.objects.filter(classobj=classobj, keyname__icontains=query)[offset:limit]
    else:
        instances = DataInstance.objects.filter(classobj=classobj)[offset:limit]

    # Filter PERMISSIONS
    # ------------------
    filtered = []
    for i in instances:
        if has_read_permission_on_instance(aaa=aaa, iobj=i):
            filtered.append(i)

    # PAGINATOR
    # ---------
    # PREV | FIRST || CURRENT or ... || LAST | NEXT
    context["size"] = size
    context["page"] = page
    page_last = int (count / size) + 1
    # if count * size <= page_last:
    #     page_last = page_last + 1

    if page > 1:
        context["page_prev"] = page - 1
    else:
        context["page_prev"] = page
    
    if page == 1:
        context["page_first"] = True
    else:
        context["page_first"] = False

    if page > 1 and page < page_last:
        context["page_current"] = True
    else:
        context["page_current"] = False

    context["page_last"] = page_last
    if page < page_last:
        context["page_last_active"] = False
    else:
        context["page_last_active"] = True

    if page < page_last:
        context["page_next"] = page + 1
    else:
        context["page_next"] = page

    # list of valid size_for template
    default_size_list = [1,5,10,20, 50,100,200,500,1000,2000, 5000,10000,50000,100000,500000]
    size_list = []
    for i in default_size_list:
        if i <= max_size:
            size_list.append(i)
    
    log(DEBUG, aaa=aaa, app="data", view="instance_list", action="get", status="OK", data="{}, {} items".format(classname, len(filtered)))


    # DATAVIEW
    # --------
    # Transform to a DATAVIEW structure (subset/superset of columns, widgets, ...)
    # 1. get available dataviews (default, global, per user)
    # 2. get requested dataview (or default dataview)
    # 3. loop over instances / extract columns / build structure

    # beta_preview = get_configuration("home","BETA_PREVIEW")
    # if beta_preview == "yes":

    # 1. Get Dataview :  request > session > single > _default > DEFAULT built-in
    dataview_name = None 
    dv_found = False

    # default dataview for this class
    dataview_default = classname + "_default"

    # available dataviews (list of DB keynames)
    dataview_selector = get_dataviews_for_class(target_class = classname)
    
    # in request ?
    try:
        dataview_name = request.GET.get("dv")
        m = re.compile(r'[a-zA-Z0-9()_/.-]*$')
        if m.match(dataview_name):
            if dataview_name in dataview_selector:
                dv_found = True
            else:
                dataview_name = dataview_default
                dv_found = True
    except:
        pass

    # in session ?
    if not dv_found:
        try:
            dataview_name = request.session["dataviews"][classname]
            if dataview_name:
                m = re.compile(r'[a-zA-Z0-9()_/.-]*$')
                if m.match(dataview_name):
                    if dataview_name in dataview_selector:
                        dv_found = True
        except:
            pass

    # single entry in selector ?
    if not dv_found:
        if len(dataview_selector) == 1:
            dataview_name = dataview_selector[0]
            dv_found = True

    # CLASSNAME_default
    if not dv_found:
        if dataview_default in dataview_selector:
            dataview_name = dataview_default
            dv_found = True
        
    # get or built-in default
    if dv_found:
        dataview = DataView(keyname = dataview_name)
        if dataview.target_class != classname:
            # wrong class, use a default view
            dataview=DataView()
    else:
        dataview=DataView()

    # store dataview in user session
    if dataview_name:
        if "dataviews" not in request.session:
            request.session["dataviews"] = {classname: dataview_name}
            #request.session.modified = True
        else:
            request.session["dataviews"][classname] = dataview_name
            request.session.modified = True


    # apply dataview to instances ; extract columns
    schema = get_schema(classname=classname)
    for iobj in filtered:
        instance = Instance(iobj=iobj, classobj=classobj, classname=classname, schema=schema)
        iobj.dataview = dataview.filter(instance=instance)

    dataview_selector_no_default = []
    for i in dataview_selector:
        if i != dataview_default:
            dataview_selector_no_default.append(i)

    context["dataview_selector"] = dataview_selector_no_default
    context["dataview_default"] = dataview_default
    context["dataview_name"] = dataview.displayname
    context["dataview_columns"] = dataview.columns
    context["instances"] = filtered
    context["size_list"] = size_list

    return render(request, 'app_data/instance_list.html', context)


# -------------------------------------------------------------------------
# Instance Detail
# -------------------------------------------------------------------------

def instance_detail(request, classname=None, handle=None):
    ''' '''
    context = start_view(request, app="data", view="instance_detail", noauth="app_sirene:index", 
        perm="p_data_read", noauthz="app_data:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]


    classobj = get_class_by_name(classname)
    if not classobj:
        return redirect("app_data:private")
   
    instance = Instance(classobj=classobj, handle=handle)
    if not instance.iobj:
        return redirect("app_data:private")
    
    # Check PERMISSIONS
    if not has_read_permission_on_instance(aaa=aaa, iobj=instance.iobj):
        return redirect("app_data:private")

    form_ui = instance.get_dict_for_ui_detail()


    log(DEBUG, aaa=aaa, app="data", view="instance", action="detail", status="OK", 
        data=f"{classname} / {handle} /  {instance.keyname}")

    context["instance"] = form_ui
    context["classobj"] = classobj
    context["dataclasses"] = get_classes()
    return render(request, 'app_data/instance_detail.html', context)


# -------------------------------------------------------------------------
# Instance EDIT
# -------------------------------------------------------------------------

def instance_edit(request, classname=None, handle=None):
    
    context = start_view(request, app="data", view="instance_edit", noauth="app_sirene:index", 
        perm="p_data_update", noauthz="app_data:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]

    classobj = get_class_by_name(classname)
    if not classobj:
        return redirect("app_data:private")

    instance = Instance(classobj=classobj, handle=handle)
    if not instance.iobj:
        return redirect("app_data:instance_list", classname)

    # Check PERMISSIONS
    if not has_edit_permission_on_instance(aaa=aaa, iobj=instance.iobj):
        return redirect("app_data:private")



    if request.method == "POST":
        instance.merge_edit_post_request(request)
        if instance.is_valid():
            r = instance.update()
            if r:
                messages.add_message(request, messages.SUCCESS, _("Instance updated"))
                log(INFO, aaa=aaa, app="data", view="instance_edit", action="post", status="OK", data=f"{classname}:{instance.keyname}") 
                #return redirect("app_data:instance_list", classname)
                return redirect("app_data:instance_detail", classname, instance.handle)
            else:
                messages.add_message(request, messages.ERROR, _("Failed to update"))
                log(ERROR, aaa=aaa, app="data", view="instance_edit", action="post", status="KO", data=f"{classname}:{instance.keyname}") 
        else:
            err = '; '.join(instance.errors)
            messages.add_message(request, messages.ERROR, _("Invalid form") + ': ' + err)
            log(ERROR, aaa=aaa, app="data", view="instance_edit", action="post", status="KO", data=f"{err}") 

        form_ui = instance.get_dict_for_ui()

    else:
        form_ui = instance.get_dict_for_ui()
        log(DEBUG, aaa=aaa, app="data", view="instance_edit", action="get", status="OK", 
            data=f"{classname} / {instance.keyname}")

    context["classobj"] = classobj
    context["formular"] = form_ui
    context["dataclasses"] = get_classes()
    return render(request, 'app_data/instance_edit.html', context)


# -------------------------------------------------------------------------
# Instance NEW
# -------------------------------------------------------------------------

def instance_new(request, classname=None):
    ''' '''

    context = start_view(request, app="data", view="instance_new", noauth="app_sirene:index", 
        perm="p_data_create", noauthz="app_data:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]

   
    classobj = get_class_by_name(classname)
    if not classobj:
        return redirect("app_data:private")

    # Check PERMISSIONS
    if not has_create_permission_on_class(aaa=aaa, classobj=classobj):
        return redirect("app_data:private")

    # new Data Structure
    instance = Instance(classname=classname)
    if not instance:
        return redirect("app_data:instance_list", classname)


    if request.method == "POST":

        instance.merge_new_post_request(request)

        if instance.is_valid():
            r = instance.create()
            if r:
                messages.add_message(request, messages.SUCCESS, _("Instance created"))
                log(INFO, aaa=aaa, app="data", view="instance_new", action="post", status="OK", data=f"{classname}/{instance.keyname}")                 
                return redirect("app_data:instance_list", classname)
            else:
                messages.add_message(request, messages.ERROR, _("Failed to create."))
                log(ERROR, aaa=aaa, app="data", view="instance_new", action="post", status="KO", data=f"{classname}")                 
        else:
            err = '; '.join(instance.errors)
            messages.add_message(request, messages.ERROR, _("Invalid form") + ': ' + err)
            log(ERROR, aaa=aaa, app="data", view="instance_new", action="post", status="KO", data=f"{err}") 

        form_ui = instance.get_dict_for_ui()


    else:
        form_ui = instance.get_dict_for_ui()
        log(DEBUG, aaa=aaa, app="data", view="instance_new", action="get", status="OK", data=f"{classname}")

    context["classobj"] = classobj
    context["formular"] = form_ui
    context["dataclasses"] = get_classes()
    return render(request, 'app_data/instance_new.html', context)



# -------------------------------------------------------------------------
# Instance DELETE
# -------------------------------------------------------------------------

def instance_delete(request, classname=None, handle=None):
    ''' '''
    
    context = start_view(request, app="data", view="instance_edit", noauth="app_sirene:index", 
        perm="p_data_delete", noauthz="app_data:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]

    
    classobj = get_class_by_name(classname)
    if not classobj:
        log(ERROR, aaa=aaa, app="data", view="instance_delete", action="find", status="KO", 
            data=f"class not found {classname}")
        return redirect("app_data:private")

    instance = Instance(classobj=classobj, handle=handle)
    if not instance.iobj:
        log(ERROR, aaa=aaa, app="data", view="instance_delete", action="find", status="KO", 
            data=f"instance not found {classname}:{instance.keyname}")
        return redirect("app_data:instance_list", classname)

    # Check PERMISSIONS
    if not has_delete_permission_on_instance(aaa=aaa, iobj=instance.iobj):
        return redirect("app_data:private")


    if request.method == "POST":

        r = instance.delete()
        if r:
            messages.add_message(request, messages.SUCCESS, _("Instance deleted"))
            log(INFO, aaa=aaa, app="data", view="instance_delete", action="post", status="OK", 
                data=f"{classname}:{instance.keyname}")

        else:
            messages.add_message(request, messages.ERROR, _("Failed to delete"))
            log(ERROR, aaa=aaa, app="data", view="instance_delete", action="post", status="KO", 
                data=f"{classname}:{instance.keyname}")
    else:
        messages.add_message(request, messages.ERROR, _("Invalid request"))
        log(WARNING, aaa=aaa, app="data", view="instance_delete", action="get", status="KO", 
            data="invalid request")

    context["dataclasses"] = get_classes()
    return redirect("app_data:instance_list", classname)



# -------------------------------------------------------------------------
# IMPORT
# -------------------------------------------------------------------------

# def data_import(request):
#     ''' '''

#     context = start_view(request, app="data", view="data_import", noauth="app_sirene:index", 
#         perm="p_data_admin", noauthz="app_data:private")
#     if context["redirect"]:
#         return redirect(context["redirect"])
#     aaa = context["aaa"]

#     if request.method == "POST":

#         form = DataUploadForm(request.POST, request.FILES)
#         if form.is_valid():

#             file = request.FILES["file"]

#             if file.multiple_chunks():
#                 messages.add_message(request, messages.ERROR, _("Import failed - file too big"))
#                 log(ERROR, aaa=aaa, app="data", view="import", action="post", status="KO", data=_("Import failed - file too big"))
#                 return redirect("app_data:private")          


#             if file.name.endswith(".csv"):
#                 err = data_import_csv(file)

#             elif file.name.endswith(".json"):
#                 err = data_import_json(file)

#             elif file.name.endswith(".yaml"):
#                 err = data_import_yaml(file)

#             elif file.name.endswith(".yml"):
#                 err = data_import_yaml(file)

#             else:
#                 messages.add_message(request, messages.ERROR, _("Import failed - unknown file type"))
#                 log(ERROR, aaa=aaa, app="data", view="import", action="post", status="KO", data=_("Import failed - unknown file type"))
#                 return redirect("app_data:private")          

#             # OK
#             messages.add_message(request, messages.SUCCESS, _("Import successful") )    
#             log(INFO, aaa=aaa, app="data", view="import", action="post", status="OK", data=_("Import successful"))
#             return redirect("app_data:private")


#     # Failed
#     messages.add_message(request, messages.ERROR, _("Import failed"))
#     log(ERROR, aaa=aaa, app="data", view="import", action="post", status="KO", data=_("Import failed - not a POST"))
    
#     return redirect("app_data:private")


# -----------------------------------------
# import tool
#-----------------------------------------


def data_import(request):

    context = start_view(request, app="data", view="import", 
        noauth="app_sirene:private", perm="p_data_import", noauthz="app_home:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]

    rawdata = ""

    if request.method == "POST":

        valid = False
        rawdata = request.POST["rawdata"]
        datalist = None

        # Get TextArea
        try:
            datalist = yaml.safe_load(rawdata)
            valid = True
        except Exception as e:
            messages.add_message(request, messages.ERROR, e)


        # File provided ?
        fileform = DataUploadForm(request.POST, request.FILES)
        
        if fileform.is_valid():
            file = request.FILES["file"]
            if file.multiple_chunks():
                messages.add_message(request, messages.ERROR, _("Import failed - file too big"))
                log(ERROR, aaa=aaa, app="data", view="import", action="post", status="KO", data=_("Import failed - file too big"))
                return redirect("app_data:private")          


        #     if file.name.endswith(".csv"):
        #         err = data_import_csv(file)

        #     elif file.name.endswith(".json"):
        #         err = data_import_json(file)

        #     elif file.name.endswith(".yaml"):
        #         err = data_import_yaml(file)

        #     elif file.name.endswith(".yml"):
        #         err = data_import_yaml(file)

            #if file.name.endswith('.csv'):
            #    datalist = load_file_csv(file, pipeline=pipeline)

            if file.name.endswith('.yml') or file.name.endswith('.yaml'):
                datalist = yaml.load(file, Loader=yaml.SafeLoader)

            elif file.name.endswith('.json'):
                datalist = json.load(file) 

            if type(datalist) is not list:
                messages.add_message(request, messages.ERROR, _("Import failed - invalid file"))
                log(ERROR, aaa=aaa, app="data", view="import", action="file", status="KO", 
                    data=f"Content is not a list : {file.name}")
                datalist = []
            else:
                log(INFO, aaa=aaa, app="data", view="import", action="file", status="OK", 
                    data=f"loaded: {file.name}")
                valid = True

        # process content
        if valid:

            # apply pipeline if any
            pipeline = request.POST["pipeline"]
            datalist = apply_pipeline(pipeline=pipeline, datalist=datalist)

            if request.POST["submit"] == "import":
                # load twice for references
                count = load_broker(datalist, aaa=aaa)
                count = load_broker(datalist, aaa=aaa)
                messages.add_message(request, messages.SUCCESS, _("Import OK"))
                log(DEBUG, aaa=aaa, app="data", view="import", action="import", status="OK",
                    data=f"imported: {count} objects")
                return redirect("app_home:private")

            else:
                # TODO : check
                messages.add_message(request, messages.SUCCESS, _("Check ok"))
                log(DEBUG, aaa=aaa, app="data", view="import", action="check", status="OK")
                # no redirect, keep editing

    context["upload_form"] = DataUploadForm()
    context["rawdata"] = rawdata
    context["pipelines"] = list_pipelines(is_enabled=True)
    return render(request, 'app_data/import.html', context)


# -----------------------------------------
# export tool
#-----------------------------------------
def data_export(request):

    context = start_view(request, app="data", view="export", 
        noauth="app_sirene:private", perm="p_data_export", noauthz="app_home:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]
   
    return render(request, 'app_data/export.html', context)
