# group_views.py

import os
from datetime import datetime, timedelta
import time
import base64
import random

from django.utils import timezone
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.utils.translation import gettext as _
from django.db.models import Count

from .aaa import get_aaa
from .aaa import start_view

from app_home.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL
#log(DEBUG, aaa=aaa, app="log", view="private", action="list", status="OK", data="")


from .models import SireneGroup

# forms
from .forms import GroupForm
from .forms import GroupUploadForm


from .group import group_csv_response
from .group import group_json_response
from .group import group_yaml_response
#from .group import group_import_csv 
from .group import group_import_json
from .group import group_import_yaml
from .group import group_get_by_id
from .group import group_get_by_name
from .group import group_delete

from .group import group_update
from .group import group_create # or update
from .group import group_get_form
from .group import group_get_subgroups
from .group import group_expand_to_users

# ----------------------------------------------------------
# GROUPS
# ----------------------------------------------------------    

def list(request):
    ''' display group list '''


    context = start_view(request, app="user", view="group_list", 
        noauth="app_home:index", perm="p_group_ro", noauthz="app_sirene:index")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]



    # bigset or not
    count = SireneGroup.objects.filter(is_role=False).count()
    context["count"] = count

    # bigset_size = int(get_configuration("data","DATA_BIGSET_SIZE"))
    # bigset = True
    # context["bigset"] = bigset
    
    groups = SireneGroup.objects\
        .filter(is_role=False)\
        .prefetch_related("users")\
        .prefetch_related("subgroups")\
        .order_by('keyname')


    output = request.GET.get("o","")
    if output != "":

        if not 'p_group_export' in aaa["perms"]:
            log(WARNING, aaa=aaa, app="user", view="group_list", action="export", status="FAIL", data=_("Not allowed")) 
            messages.add_message(request, messages.ERROR, _("Not allowed"))
            return redirect("app_sirene:private")

        export_max = int(get_configuration("data","EXPORT_INTERACTIVE_MAX_SIZE"))
        if count > export_max:
            log(ERROR, aaa=aaa, app="group", view="list", action="export", status="KO", data=f"Export too big") 
            messages.add_message(request, messages.ERROR, _("Export too large for interactive export."))
            return redirect("app_user:group_list")

        if output == "csv":
            log(INFO, aaa=aaa, app="user", view="group_list", action="export_csv", status="OK", data="")
            response = group_csv_response(groups)
            return response   

        elif output == "json":
            log(INFO, aaa=aaa, app="user", view="group_list", action="export_json", status="OK", data="")
            response = group_json_response(groups)
            return response   

        elif output == "yaml":
            log(INFO, aaa=aaa, app="user", view="group_list", action="export_yaml", status="OK", data="")
            response = group_yaml_response(groups)
            return response   


    context["groups"] = groups
    context["upload_form"] = GroupUploadForm()

    return render(request, 'app_user/group_list.html', context)


# --------------------------------------------
# delete
# --------------------------------------------


def delete(request, gid):
    ''' delete user Group '''

    context = start_view(request, app="user", view="group_delete", 
        noauth="app_user:private", perm="p_group_rw", noauthz="app_sirene:index")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]

    # TODO : check perms / security groups

    gobj = group_get_by_id(gid)
    if not gobj:
        log(ERROR, aaa=aaa, app="user", view="group_delete", action="find", status="FAIL", data=_("Group not found"))
        messages.add_message(request, messages.ERROR, _("Group not found"))
        return redirect("app_user:group_list")


    if request.method == "POST":

        r = group_delete(gobj)

        if r:
            messages.add_message(request, messages.SUCCESS, _("Group deleted ") )
            log(INFO, aaa=aaa, app="user", view="group_delete", action="delete", status="OK", data=f"deleted: group.keyname" )

        else:
            log(ERROR, aaa=aaa, app="user", view="group_delete", action="delete", status="FAIL", data=_("Failed to delete group") )
            messages.add_message(request, messages.ERROR, _("Failed to delete group"))

    return redirect("app_user:group_list")


# --------------------------------------------
# detail
# --------------------------------------------

def detail(request, gid=None, gname=None):
    ''' display group detail '''

    context = start_view(request, app="user", view="group_detail", 
        noauth="app_user:private", perm="p_group_ro", noauthz="app_user:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]

    group = None
    if gid:
        group = group_get_by_id(gid)
    elif gname:
        group = group_get_by_name(gname)

    if not group:
        messages.add_message(request, messages.ERROR, _("Not allowed"))
        log(WARNING, aaa=aaa, app="user", view="group", action="detail", status="KO", data=_("Not allowed") )
        return redirect("app_user:group_list")

    subgroups_indirect = group_get_subgroups(group, done=[])
    tmp = group.subgroups.all()
    subgroups_indirect = [i for i in subgroups_indirect if i not in tmp]
    context["subgroups_indirect"] = subgroups_indirect

    users_indirect = group_expand_to_users([], [group])
    tmp = group.users.all() 
    users_indirect = [i for i in users_indirect if i not in tmp ]
    context["users_indirect"] = users_indirect

    context["group"] = group
    return render(request, 'app_user/group_detail.html', context)

# --------------------------------------------
# edit
# --------------------------------------------
def edit(request, gid=None, keyname=None):
    ''' usergroup  edit form'''

    context = start_view(request, app="user", view="group.edit", 
        noauth="app_user:private", perm="p_group_rw", noauthz="app_sirene:index")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]

    group = None

    if gid:
        group = group_get_by_id(gid)
        if not group:
            messages.add_message(request, messages.ERROR, _("Not allowed"))
            log(WARNING, aaa=aaa, app="user", view="group", action="edit", status="FAIL", data=_("Not allowed") )
            return redirect("app_user:group_list")
    elif keyname:
        group = group_get_by_name(keyname)
        if not group:
            messages.add_message(request, messages.ERROR, _("Not allowed"))
            log(WARNING, aaa=aaa, app="user", view="group", action="edit", status="FAIL", data=_("Not allowed") )
            return redirect("app_user:group_list")

    if request.method == "POST":

        form = GroupForm(request.POST)

        if form.is_valid():
            
            # data + add users (outside managed django form)
            data = form.cleaned_data
            users = request.POST.getlist("users",default=[])
            data["users"] = users

            # update
            if group:
                group = group_update(group, data)

            # create                
            else:   
                group = group_create(data)
    
            if group:
                messages.add_message(request, messages.SUCCESS, _("Group saved") )
                log(INFO, aaa=aaa, app="user", view="group", action="save", status="OK", data=f"saved: group.keyname")
          
            else:
                messages.add_message(request, messages.ERROR, _("Failed to save group"))
                log(ERROR, aaa=aaa, app="user", view="group", action="save", status="KO", data=_("Failed to save group"))

            return redirect("app_user:group_detail", group.keyname)

        else:
            # error, keep editing
            messages.add_message(request, messages.ERROR, _("Invalid group form") )
            log(DEBUG, aaa=aaa, app="user", view="group", action="save", status="KO", data=_("Invalid group form"))
            # add out of form users attribute
            context["users"] = []
            users = request.POST.getlist("users",default=[])
            for i in users:
                item = { "key":i, "display":i, "selected":True}
                context["users"].append(item)
    # GET
    else:
        if group:
            form = group_get_form(group)
            context["users"] = []
            users = group.users.all()
            for i in users:
                item = { "key":i.login, "display":i.displayname , "selected":True}
                context["users"].append(item)

        else: 
            context["users"] = []
            form = group_get_form()


    context["form"] = form
    if group:
        context["group"] = group

    return render(request, 'app_user/group_edit.html', context)


# --------------------------------------------
# import
# --------------------------------------------

def group_import(request):

    context = start_view(request, app="user", view="group.import", 
        noauth="app_user:private", perm="p_group_import", noauthz="app_sirene:index")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]


    if request.method == "POST":
        form = GroupUploadForm(request.POST, request.FILES)
        if form.is_valid():

            file = request.FILES["file"]

            if file.multiple_chunks():
                messages.add_message(request, messages.ERROR, _("File too big"))
                log(ERROR, aaa=aaa, app="user", view="group_import", action="POST", status="FAIL", data="File too big")   
                return redirect("app_user:group_list")          


            # if file.name.endswith(".csv"):
            #     line_total, line_ok = group_import_csv(file)

            elif file.name.endswith(".json"):
                line_total, line_ok = group_import_json(file)

            elif file.name.endswith(".yaml"):
                line_total, line_ok = group_import_yaml(file)

            elif file.name.endswith(".yml"):
                line_total, line_ok = group_import_yaml(file)

            else:
                messages.add_message(request, messages.ERROR, _("Import failed - unknown file type"))
                log(ERROR, aaa=aaa, app="user", view="group_import", action="POST", status="FAIL", data=f"Unknown file type {file}")
                return redirect("app_user:group_list")          

            # OK
            messages.add_message(request, messages.SUCCESS, _("Import OK") )
            log(INFO, aaa=aaa, app="user", view="group_import", action="POST", status="OK", data=f"{file} - {line_ok}/{line_total} entries")
            return redirect("app_user:group_list")


    # Failed
    messages.add_message(request, messages.ERROR, _("Import failed"))
    log(ERROR, aaa=aaa, app="user", view="group_import", action="POST", status="FAIL", data=f"import failed, not a POST")
    return redirect("app_user:group_list")

