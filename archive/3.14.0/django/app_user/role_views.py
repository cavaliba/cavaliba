# role_views.py

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

from app_home.configuration import get_configuration

from app_home.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL
#log(DEBUG, aaa=aaa, app="log", view="private", action="list", status="OK", data="")


from .models import SireneGroup

# forms
#from .forms import GroupForm
from .forms import RoleForm
from .forms import RoleUploadForm


from .role import role_json_response
from .role import role_yaml_response

# from .role import role_import_json
# from .role import role_import_yaml

from .role import role_get_by_id
from .role import role_get_by_name
from .role import role_delete
from .role import role_update
from .role import role_create     # or update
from .role import role_get_form
from .role import role_get_subgroups
from .role import role_expand_to_users


# ----------------------------------------------------------
# role list
# ----------------------------------------------------------    

def list(request):
    ''' display role (security group) list '''


    context = start_view(request, app="iam", view="role_list", noauth="app_home:index", 
        perm="p_role_read", noauthz="app_home:index")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]


    # bigset or not
    count = SireneGroup.objects.filter(is_role=True).count()
    context["count"] = count

    # bigset_size = int(get_configuration("data","DATA_BIGSET_SIZE"))
    # bigset = True
    # context["bigset"] = bigset


    # Role is SireneGroup with is_role=True
    roles = SireneGroup.objects\
        .filter(is_role=True)\
        .prefetch_related("permissions")\
        .prefetch_related("users")\
        .prefetch_related("subgroups")\
        .order_by('keyname')
        
        # .annotate(num_perms=Count('permissions'))\
        # .annotate(num_users=Count('users'))\
        # .annotate(num_subgroups=Count('subgroups'))\

        
    output = request.GET.get("o","")
    if output != "":

        # NO CSV for roles
        # if output == "csv":
        #     log(INFO, aaa=aaa, app="iam", view="role_list", action="export_csv", status="OK", data="")
        #     response = group_csv_response(groups)
        #     return response   

        if 'p_role_export' not in aaa["perms"]:
            log(WARNING, aaa=aaa, app="iam", view="role", action="export", status="FAIL", data=_("Not allowed")) 
            messages.add_message(request, messages.ERROR, _("Not allowed"))
            return redirect("app_user:role_list")


        export_max = int(get_configuration("data","EXPORT_INTERACTIVE_MAX_SIZE"))
        if count > export_max:
            log(ERROR, aaa=aaa, app="iam", view="role", action="export", status="KO", data="Export too big") 
            messages.add_message(request, messages.ERROR, _("Export too large for interactive export."))
            return redirect("app_user:role_list")

        if output == "json":
            log(INFO, aaa=aaa, app="iam", view="role_list", action="export_json", status="OK", data="")
            response = role_json_response(roles)
            return response   

        elif output == "yaml":
            log(INFO, aaa=aaa, app="iam", view="role_list", action="export_yaml", status="OK", data="")
            response = role_yaml_response(roles)
            return response   


    context["roles"] = roles
    context["upload_form"] = RoleUploadForm()

    return render(request, 'app_user/role_list.html', context)

# --------------------------------------------
# detail
# --------------------------------------------

def detail(request, rid=None, rname=None):
    ''' display role detail '''

    context = start_view(request, app="iam", view="role_detail", 
        noauth="app_user:private", perm="p_role_read", noauthz="app_user:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]

    role = None
    if rid:
        role = role_get_by_id(rid)
    elif rname:
        role = role_get_by_name(rname)

    if not role:
        messages.add_message(request, messages.ERROR, _("Not allowed"))
        log(WARNING, aaa=aaa, app="iam", view="role", action="detail", status="KO", data=_("Not allowed") )
        return redirect("app_user:role_list")



    subgroups_indirect = role_get_subgroups(role, done=[])
    tmp = role.subgroups.all()
    subgroups_indirect = [i for i in subgroups_indirect if i not in tmp]
    context["subgroups_indirect"] = subgroups_indirect

    users_indirect = role_expand_to_users([], [role])
    tmp = role.users.all() 
    users_indirect = [i for i in users_indirect if i not in tmp]
    context["users_indirect"] = users_indirect

    context["role"] = role
    return render(request, 'app_user/role_detail.html', context)


# --------------------------------------------
# role delete
# --------------------------------------------

def delete(request, gid=None):
    ''' delete user Group '''

    context = start_view(request, app="iam", view="role_delete", 
        noauth="app_user:private", perm="p_role_delete", noauthz="app_sirene:index")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]

    if gid:
        gobj = role_get_by_id(gid)
        if not gobj:
            log(ERROR, aaa=aaa, app="iam", view="role_delete", action="find", status="KO", data=_("Role not found"))
            messages.add_message(request, messages.ERROR, _("Role not found"))
            return redirect("app_user:role_list")

    # role ?
    if not gobj.is_role:
        log(ERROR, aaa=aaa, app="iam", view="role_delete", action="find", status="KO", data=_("Not a role"))
        messages.add_message(request, messages.ERROR, _("Not a role"))
        return redirect("app_user:role_list")

    if request.method == "POST":

        r = role_delete(gobj)

        if r:
            messages.add_message(request, messages.SUCCESS, _("Role deleted") )
            log(INFO, aaa=aaa, app="iam", view="role_delete", action="delete", status="OK", data=f"Role deleted : {gobj.keyname}" )

        else:
            log(ERROR, aaa=aaa, app="iam", view="role_delete", action="delete", status="KO", data=_("Failed to delete role") )
            messages.add_message(request, messages.ERROR, _("Failed to delete role"))

    return redirect("app_user:role_list")


# --------------------------------------------
# edit
# --------------------------------------------
def edit(request, gid=None, keyname=None):
    ''' usergroup  edit form'''

    context = start_view(request, app="iam", view="role_edit", 
        noauth="app_user:private", perm="p_role_update", noauthz="app_sirene:index")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]


    group = None


    if gid:
        group = role_get_by_id(gid)
        if not group:
            messages.add_message(request, messages.ERROR, _("Not allowed"))
            log(WARNING, aaa=aaa, app="iam", view="role", action="edit", status="KO", data=_("Not allowed") )
            return redirect("app_user:role_list")

    elif keyname:
        group = role_get_by_name(keyname)
        if not group:
            messages.add_message(request, messages.ERROR, _("Not allowed"))
            log(WARNING, aaa=aaa, app="iam", view="role", action="edit", status="KO", data=_("Not allowed") )
            return redirect("app_user:role_list")

    else:
        if "p_role_create" not in aaa["perms"]:
            messages.add_message(request, messages.ERROR, _("Not allowed"))
            log(WARNING, aaa=aaa, app="iam", view="role", action="create", status="KO", data=_("Not allowed") )
            return redirect("app_user:role_list")

    if request.method == "POST":

        form = RoleForm(request.POST)

        if form.is_valid():

            # data + add users (outside managed django form)
            data = form.cleaned_data
            users = request.POST.getlist("users",default=[])
            data["users"] = users

            # update
            if group:
                group = role_update(group, data)

            # create                
            else:   
                group = role_create(data)

            # success ?
            if group:
                messages.add_message(request, messages.SUCCESS, _("Role saved") )
                log(INFO, aaa=aaa, app="iam", view="role_edit", action="POST", status="OK", data=f"Role saved : {group.keyname}")
          
            else:
                messages.add_message(request, messages.ERROR, _("Failed to save role"))
                log(ERROR, aaa=aaa, app="iam", view="role_edit", action="POST", status="KO", data=_("Failed to save role"))

            return redirect("app_user:role_detail", group.keyname)

        else:
            messages.add_message(request, messages.ERROR, _("Invalid role form") )
            log(DEBUG, aaa=aaa, app="iam", view="role_edit", action="POST", status="KO", data=_("Invalid role form"))
            # keep editing, add out of form users attribute
            context["users"] = []
            users = request.POST.getlist("users",default=[])
            for i in users:
                item = { "key":i, "display":i, "selected":True}
                context["users"].append(item)
    # GET
    else:
        if group:
            form = role_get_form(group)
            context["users"] = []
            users = group.users.all()
            for i in users:
                item = { "key":i.login, "display":i.displayname , "selected":True}
                context["users"].append(item)
        else: 
            form = role_get_form()
            context["users"] = []


    context["form"] = form
    if group:
        context["role"] = group

    return render(request, 'app_user/role_edit.html', context)

