# app_data - views.py
# (c) cavaliba.com 

import os
from datetime import datetime, timedelta
import time
import base64
import random
import csv
import re

from pprint import pprint

from django.utils import timezone
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.utils.translation import gettext as _
from django.db.models import Q
from django.core.paginator import Paginator


from app_log.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL
from app_user.aaa import start_view
from app_user.aaa import get_aaa 
from app_home.configuration import get_configuration

from .models import DataInstance

from .data import Instance

from .data import get_classes
from .data import get_class_by_name
from .data import get_instances
from .data import get_schema

from .forms import DataUploadForm
from .data import data_import_csv 
from .data import data_import_json
from .data import data_import_yaml

from .data import export_data
from .data import data_yaml_response
from .data import data_json_response

from .data import update_bigset

from .dataview import get_dataview_content_by_name
from .dataview import get_dataviews_for_class
from .dataview import DataView

# return redirect("anonymous")
# context={}
# return render(request, 'app_data/index.html', context)



# -----------------------------------------
# private / Class List
#-----------------------------------------

def is_user_in_group(aaa=None, gname=None):

    if gname in aaa["groups"] + aaa["groups_indirect"]:
        return True
    return False


def check_class_action(aaa=None, classobj=None, action=None):
    '''
    Returns True/False
    Check if aaa user can perform action on class Classobj.
    '''


    if not aaa:
        return False

    if aaa["is_admin"]:
        return True

    # role (security group) allowing the requested action
    gname = None

    # display link to class in Classlist UI
    if action == "show":
        if "p_schema_ro" in aaa["perms"]:
            if classobj.role_show:
                gname = classobj.role_show.keyname

    elif action == "access":
        if "p_schema_ro" in aaa["perms"]:
            if classobj.role_access:
                gname = classobj.role_access.keyname

    elif action == "read":
        if "p_schema_ro" in aaa["perms"]:
            if classobj.role_read:
                gname = classobj.role_read.keyname

    elif action == "create":
        if "p_schema_rw" in aaa["perms"]:
            if classobj.role_create:
                gname = classobj.role_create.keyname    

    elif action == "update":
        if "p_schema_rw" in aaa["perms"]:
            if classobj.role_update:
                gname = classobj.role_update.keyname

    elif action == "delete":
        if "p_schema_rw" in aaa["perms"]:
            if classobj.role_delete:
                gname = classobj.role_delete.keyname

    elif action == "onoff":
        if "p_schema_rw" in aaa["perms"]:
            if classobj.role_onoff:
                gname = classobj.role_onoff.keyname

    elif action == "import":
        if "p_data_admin" in aaa["perms"]:
            if classobj.role_import:
                gname = classobj.role_import.keyname

    elif action == "export":
        if "p_data_admin" in aaa["perms"]:
            if classobj.role_export:
                gname = classobj.role_export.keyname

    if not gname:
        return False

    if is_user_in_group(aaa=aaa, gname=gname):
        return True

    return False

# ----------------------------------------------
# list of Classes
# ----------------------------------------------
def private(request):

    context = start_view(request, app="data", view="private", noauth="app_sirene:index", 
        perm="p_data_access", noauthz="app_home:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]

    if "p_schema_ro" not in aaa["perms"]:
        return redirect("app_home:index")



    dataclasses = get_classes()

    # # export mode ?
    # output = request.GET.get("o","")
    # if output != "":
    #     if not 'p_data_admin' in aaa["perms"]:
    #         log(WARNING, aaa=aaa, app="data", view="private", action="export", status="KO", data=_("Not allowed")) 
    #         messages.add_message(request, messages.ERROR, _("Not allowed"))
    #         return redirect("app_data:private")

    filtered = []

    for classobj in dataclasses:

        # # export mode ?
        # if output != "":
        #     if not check_class_action(classobj=classobj, aaa=aaa, action="export"):
        #         continue 

        # else:
        if not check_class_action(classobj=classobj, aaa=aaa, action="show"):
            continue

        if not classobj.is_enabled:
            if not check_class_action(classobj=classobj, aaa=aaa, action="onoff"):
                continue

        if check_class_action(classobj=classobj, aaa=aaa, action="access"):
            classobj.p_access = True
            filtered.append(classobj)
        else:
            classobj.p_access = False
            filtered.append(classobj)


    #filtered = list(set(filtered))


    # page/order for UI
    # [  [page1, [class1, class2,  ...] , [ page2, [...] ] ,  ... ]
    paginated = []
    pagelist = []
    index = {} # page => [class1, class2]
    default_name = get_configuration("home", "GLOBAL_APPNAME")

    for element in filtered:
        order = element.order
        page = element.page
        if not page:
            page = default_name
        if len(page) == 0:
            page = default_name
        if page not in index:
            index[page] = []
            pagelist.append(page)
        index[page].append(element)    
    for p in pagelist:
        paginated.append( [p, index[p] ])

    #pprint(paginated)

    upload_form = DataUploadForm()

    # Exports 
    # if output == "csv":
    #     log(DEBUG, aaa=aaa, app="user", view="user_list", action="export_csv", status="OK", data=f"") 
    #     response = user_csv_response(users)
    #     return response   


    # #export_data(classes=["app"])
    # if output == "yaml":
    #     log(INFO, aaa=aaa, app="data", view="private", action="export", status="OK", data=f"yaml") 
    #     response = data_yaml_response(classes = [i.keyname for i in filtered])
    #     return response 
    
    # elif output == "json":
    #     log(INFO, aaa=aaa, app="data", view="private", action="export", status="OK", data=f"json") 
    #     response = data_json_response(classes = [i.keyname for i in filtered])
    #     return response   

    log(DEBUG, aaa=aaa, app="data", view="private", action="list", status="OK", data="{} classes".format(len(filtered)))


    context["dataclasses"] = filtered
    context["paginated"] = paginated
    context["upload_form"] = upload_form

    return render(request, 'app_data/private.html', context)

# -------------------------------------------------------------------------
# Instance List 
# -------------------------------------------------------------------------
# V3.10 : always bigset

def instance_list(request, classname=None):

    context = start_view(request, app="data", view="instance_list", noauth="app_sirene:index", 
        perm="p_instance_ro", noauthz="app_data:private")
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


    # NEXT: faster = use precomputed bigset attribut from class
    bigset_size = int(get_configuration("data","DATA_BIGSET_SIZE"))
    count = classobj.datainstance_set.count()
    context["count"] = count


    # export mode ? (export all)
    output = request.GET.get("o","")
    if output != "":

        if not ('p_data_admin' in aaa["perms"] and check_class_action(classobj=classobj, aaa=aaa, action="export")):
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
            log(INFO, aaa=aaa, app="data", view="instance_list", action="export", status="OK", data=f"yaml") 
            response = data_yaml_response(classes = [classname])
            return response 
        
        elif output == "json":
            log(INFO, aaa=aaa, app="data", view="instance_list", action="export", status="OK", data=f"json") 
            response = data_json_response(classes = [classname])
            return response   


    # Filter POST (form)
    #query = request.GET.get("q", "")
    query = ""
    if request.method == "POST":
        if request.POST.get('query'):
            query = request.POST.get('query')
            m = re.compile(r'[a-zA-Z0-9()_/.-]*$')
            if not m.match(query):
                #return redirect("app_data:private")
                query = ""
    context["query"] = query


    try:
        size = int(request.GET.get("size", bigset_size))
        page = int(request.GET.get("page",1))
    except:
        return redirect("app_data:private")

    if page < 1 or size > 10000 or size < 1:
        return redirect("app_data:private")

    offset = (page-1) * size
    limit = offset + size


    # HERE, Get Instances
    if len(query) > 0:
        # filter on displayname Q() | Q()
        instances = DataInstance.objects.filter(classobj=classobj, keyname__icontains=query)[offset:limit]
    else:
        instances = DataInstance.objects.filter(classobj=classobj)[offset:limit]
    
    # PAGINATOR
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

    
    log(DEBUG, aaa=aaa, app="data", view="instance_list", action="get", status="OK", data="{}, {} items".format(classname, len(instances)))


    # DATAVIEW

    # Transform to a DATAVIEW structure (subset of columns, widgets, ...)
    # 1. get available dataviews (default, global, per user)
    # 2. get requested dataview (or default dataview)
    # 3. loop over instances / extract columns / build structure

    # beta_preview = get_configuration("home","BETA_PREVIEW")
    # if beta_preview == "yes":

    dataview = None

    #dataview_default_content = { 'columns' : ['keyname', 'displayname','last_update']}
    #context["dataview"] = True    
    
    # selector 
    dv_selector = get_dataviews_for_class(classname)
    context["dataview_selector"] = dv_selector

    # Per user data views
    # dv_selector2 = get_dataviews_for_user(classname,aaa)
    # context["dataview_selector2"] = dv_selector2


    req_dataview = request.GET.get("dv",None)
    if req_dataview:
        m = re.compile(r'[a-zA-Z0-9()_/.-]*$')
        if not m.match(req_dataview):
            req_dataview = None

    dataview = DataView(dataview_name = req_dataview)
    dataview_content = dataview.content
    dataview_name = dataview.dataview_name

    #dataview.print()

    # extract columns
    schema = get_schema(classname=classname)
    for iobj in instances:
        instance = Instance(iobj=iobj, classname=classname, schema=schema)
        iobj.dataview = dataview.filter(instance=instance)


    context["dataview_name"] = dataview_name
    context["dataview_heads"] = dataview.get_heads()
    context["instances"] = instances
    return render(request, 'app_data/instance_list.html', context)


# -------------------------------------------------------------------------
# Instance Detail
# -------------------------------------------------------------------------

def instance_detail(request, classname=None, keyname=None):
    ''' '''

    context = start_view(request, app="data", view="instance_detail", noauth="app_sirene:index", 
        perm="p_instance_ro", noauthz="app_data:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]

    if not keyname:
        return redirect("app_data:private")


    classobj = get_class_by_name(classname)
    context["classobj"] = classobj

    dataclasses = get_classes()
    context["dataclasses"] = dataclasses

    instance = Instance(classname=classname, iname=keyname)
    #instance.print()
    form_ui = instance.get_dict_for_ui_detail()

    context["keyname"] = keyname
    context["instance"] = form_ui

    log(DEBUG, aaa=aaa, app="data", view="instance", action="detail", status="OK", data=f"{classname} / {keyname}")

    return render(request, 'app_data/instance_detail.html', context)


# -------------------------------------------------------------------------
# Instance EDIT
# -------------------------------------------------------------------------

def instance_edit(request, classname=None, keyname=None):
    ''' '''
    pass
    context = start_view(request, app="data", view="instance_edit", noauth="app_sirene:index", 
        perm="p_instance_rw", noauthz="app_data:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]

    dataclasses = get_classes()
    context["dataclasses"] = dataclasses

    classobj = get_class_by_name(classname)
    if not classobj:
        return redirect("app_data:private")

    instance = Instance(classname=classname, iname=keyname)
    if not instance:
        return redirect("app_data:instance_list", classname)

    if request.method == "POST":

        instance.merge_edit_post_request(request)

        if instance.is_valid():
            r = instance.update()
            if r:
                messages.add_message(request, messages.SUCCESS, _("Instance updated"))
                log(INFO, aaa=aaa, app="data", view="instance_edit", action="post", status="OK", data=f"{classname}:{keyname}") 
                #return redirect("app_data:instance_list", classname)
                return redirect("app_data:instance_detail", classname, keyname)
            else:
                messages.add_message(request, messages.ERROR, _("Failed to update"))
                log(ERROR, aaa=aaa, app="data", view="instance_edit", action="post", status="KO", data=f"{classname}:{keyname}") 
        else:
            err = '; '.join(instance.errors)
            messages.add_message(request, messages.ERROR, _("Invalid form") + ': ' + err)
            log(ERROR, aaa=aaa, app="data", view="instance_edit", action="post", status="KO", data=f"{err}") 

        form_ui = instance.get_dict_for_ui()

    else:
        form_ui = instance.get_dict_for_ui()
        log(DEBUG, aaa=aaa, app="data", view="instance_edit", action="get", status="OK", data=f"{classname} / {keyname}")


    #pprint(form_ui)
    context["keyname"] = keyname
    context["classobj"] = classobj
    context["formular"] = form_ui

    #pprint(context)
    return render(request, 'app_data/instance_edit.html', context)


# -------------------------------------------------------------------------
# Instance NEW
# -------------------------------------------------------------------------

def instance_new(request, classname=None):
    ''' '''

    context = start_view(request, app="data", view="instance_new", noauth="app_sirene:index", 
        perm="p_instance_rw", noauthz="app_data:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]

    dataclasses = get_classes()
    context["dataclasses"] = dataclasses

    classobj = get_class_by_name(classname)
    if not classobj:
        return redirect("app_data:private")

    instance = Instance(classname=classname)
    if not instance:
        return redirect("app_data:instance_list", classname)

    #instance.print()

    if request.method == "POST":

        instance.merge_new_post_request(request)
        #instance.print()

        if instance.is_valid():
            r = instance.create()
            if r:
                messages.add_message(request, messages.SUCCESS, _("Instance created"))
                log(INFO, aaa=aaa, app="data", view="instance_new", action="post", status="OK", data=f"{classname}")                 
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


    return render(request, 'app_data/instance_new.html', context)



# -------------------------------------------------------------------------
# Instance DELETE
# -------------------------------------------------------------------------

def instance_delete(request, classname=None, keyname=None):
    ''' '''
    
    context = start_view(request, app="data", view="instance_edit", noauth="app_sirene:index", 
        perm="p_instance_rw", noauthz="app_data:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]

    dataclasses = get_classes()
    context["dataclasses"] = dataclasses

    classobj = get_class_by_name(classname)
    if not classobj:
        log(ERROR, aaa=aaa, app="data", view="instance_delete", action="find", status="KO", data=f"class not found {classname}")
        return redirect("app_data:private")

    instance = Instance(classname=classname, iname=keyname)
    if not instance:
        log(ERROR, aaa=aaa, app="data", view="instance_delete", action="find", status="KO", data=f"instance not found {classname}:{keyname}")
        return redirect("app_data:instance_list", classname)


    if request.method == "POST":

        r = instance.delete()
        if r:
            messages.add_message(request, messages.SUCCESS, _("Instance deleted"))
            log(INFO, aaa=aaa, app="data", view="instance_delete", action="post", status="OK", data=f"{classname}:{keyname}")

        else:
            messages.add_message(request, messages.ERROR, _("Failed to delete"))
            log(ERROR, aaa=aaa, app="data", view="instance_delete", action="post", status="KO", data=f"{classname}:{keyname}")
    else:
            messages.add_message(request, messages.ERROR, _("Invalid request"))
            log(WARNING, aaa=aaa, app="data", view="instance_delete", action="get", status="KO", data=f"invalid request")


    return redirect("app_data:instance_list", classname)



# -------------------------------------------------------------------------
# IMPORT
# -------------------------------------------------------------------------

def data_import(request):
    ''' '''

    context = start_view(request, app="data", view="data_import", noauth="app_sirene:index", 
        perm="p_data_admin", noauthz="app_data:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]

    if request.method == "POST":

        form = DataUploadForm(request.POST, request.FILES)
        if form.is_valid():

            file = request.FILES["file"]

            if file.multiple_chunks():
                messages.add_message(request, messages.ERROR, _("Import failed - file too big"))
                log(ERROR, aaa=aaa, app="data", view="import", action="post", status="KO", data=_("Import failed - file too big"))
                return redirect("app_data:private")          


            if file.name.endswith(".csv"):
                err = data_import_csv(file)

            elif file.name.endswith(".json"):
                err = data_import_json(file)

            elif file.name.endswith(".yaml"):
                err = data_import_yaml(file)

            elif file.name.endswith(".yml"):
                err = data_import_yaml(file)

            else:
                messages.add_message(request, messages.ERROR, _("Import failed - unknown file type"))
                log(ERROR, aaa=aaa, app="data", view="import", action="post", status="KO", data=_("Import failed - unknown file type"))
                return redirect("app_data:private")          

            # OK
            messages.add_message(request, messages.SUCCESS, _("Import successful") )    
            log(INFO, aaa=aaa, app="data", view="import", action="post", status="OK", data=_("Import successful"))
            return redirect("app_data:private")


    # Failed
    messages.add_message(request, messages.ERROR, _("Import failed"))
    log(ERROR, aaa=aaa, app="data", view="import", action="post", status="KO", data=_("Import failed - not a POST"))
    
    return redirect("app_data:private")
