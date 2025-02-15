# app_user - views.py
# (c) cavaliba.com 

import os
from datetime import datetime, timedelta
import time
import base64
import random
import csv
import jwt
import json
import re

import pprint

from django.utils import timezone
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.utils.translation import gettext as _
from django.db.models import Q
from django.contrib.auth import logout as django_logout

from app_home.configuration import get_configuration
from app_home.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL

from .models import SireneUser
from .models import SireneGroup

from .aaa import start_view
from .aaa import get_aaa

from .aaa import get_all_groups_for_login

from .user import user_get_by_login
from .user import user_csv_response
from .user import user_json_response
from .user import user_yaml_response
# from .user import import_json
# from .user import import_yaml
from .user import user_get_by_id
from .user import user_delete_by_id
from .user import user_update
from .user import user_create   # or update
from .user import user_get_form_blank 
from .user import user_get_form

from .user import user_get_mobile
from .user import user_get_email

from .forms import UserForm
from .forms import UserPrefForm
from .forms import UserUploadForm

from app_sirene.sms import sms_check_valid_number
from app_sirene.sms import get_sms_quota
# Celery tasks
from app_sirene.tasks import task_send_mail
from app_sirene.tasks import task_send_sms


# -----------------------------------------
# private
#-----------------------------------------

def private(request):

    context = start_view(request, app="iam", view="private", noauth="app_home:private", 
        perm="p_iam_access", noauthz="app_home:index")
    if context["redirect"]:
        return redirect(context["redirect"])

    return redirect("app_user:user_list")


# ----------------------------------------------------------
# USER list
# ----------------------------------------------------------    
def list(request):
    '''  display user list - ?o=csv to export as CSV (yaml, json)  '''

    context = start_view(request, app="iam", view="list", noauth="app_home:index", 
        perm="p_user_read", noauthz="app_sirene:index")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]

    

    # bigset or not
    bigset_size = int(get_configuration("data","DATA_BIGSET_SIZE"))
    count = SireneUser.objects.count()
    bigset = True
    context["bigset"] = bigset
    context["count"] = count
    
    # Filter POST (form)
    #query = request.GET.get("q", "")
    query = ""
    if request.method == "POST":
        if request.POST.get('query'):
            query = request.POST.get('query')
            m = re.compile(r'[a-zA-Z0-9()_/.-]*$')
            if not m.match(query):
                #return redirect("app_user:user_list")
                query = ""
    context["query"] = query


    # # partial query + paginate if bigset
    # if bigset:
    try:
        size = int(request.GET.get("size", bigset_size))
        page = int(request.GET.get("page",1))
    except Exception as e:
        print(e)
        return redirect("app_user:user_list")

    if page < 1 or size > 10000 or size < 1:
        return redirect("app_user:user_list")


    offset = (page-1) * size
    limit = offset + size

    if len(query) > 0:
        users = SireneUser.objects\
            .filter( Q(displayname__icontains=query) | Q(login__icontains=query) | Q(mobile__icontains=query) | Q(email__icontains=query) | Q(external_id__icontains=query) )\
            .order_by('login')[offset:limit]
    else:
        users = SireneUser.objects.order_by('login')[offset:limit]

    # export requested (o=xxxx)
    output = request.GET.get("o","")
    if output != "":

        # permission
        if 'p_user_export' not in aaa["perms"]:
            log(WARNING, aaa=aaa, app="iam", view="list", action="export", status="FAIL", data=_("Not allowed")) 
            messages.add_message(request, messages.ERROR, _("Not allowed"))
            return redirect("app_sirene:private")

        # NEXT : partial export (selection only)

        # size max for interactive export ?
        export_max = int(get_configuration("data","EXPORT_INTERACTIVE_MAX_SIZE"))

        if count > export_max:
            log(ERROR, aaa=aaa, app="iam", view="list", action="export", status="KO", data="Export too big") 
            messages.add_message(request, messages.ERROR, _("Export too large for interactive export."))
            return redirect("app_user:user_list")

        if output == "csv":
            log(DEBUG, aaa=aaa, app="iam", view="user_list", action="export_csv", status="OK", data="") 
            response = user_csv_response(users)
            return response   

        elif output == "json":
            log(DEBUG, aaa=aaa, app="iam", view="user_list", action="export_json", status="OK", data="") 
            response = user_json_response(users)
            return response   

        elif output == "yaml":
            log(DEBUG, aaa=aaa, app="iam", view="user_list", action="export_yaml", status="OK", data="") 
            response = user_yaml_response(users)
            return response   

    
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

    # else:
    #     users = SireneUser.objects.all().order_by('login')
    #     # users = SireneUser.objects.all().exclude(login='admin').prefetch_related('roles').order_by('login')   
    
    upload_form = UserUploadForm()
    
    log(DEBUG, aaa=aaa, app="iam", view="list", action="get", status="OK", data=f"{count} users")


    context["users"] = users
    context["upload_form"] = upload_form
    return render(request, 'app_user/user_list.html', context)


# ----------------------------------------------------------
# User delete
# ----------------------------------------------------------    
    
def delete(request, userid):
    ''' delete user  '''

    context = start_view(request, app="iam", view="user_delete", noauth="app_home:index", 
        perm="p_user_delete", noauthz="app_sirene:index")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]

    if request.method == "POST":

        user = user_delete_by_id(userid=userid) 

        if user:
            messages.add_message(request, messages.SUCCESS, _("User deleted"))
            log(INFO, aaa=aaa, app="iam", view="user_delete", action="delete", status="OK", data=f"{user.login}") 
        else:
            messages.add_message(request, messages.ERROR, _("Failed to delete user"))
            log(ERROR, aaa=aaa, app="iam", view="user_delete", action="delete", status="FAIL", data="") 

    return redirect("app_user:user_list")


# ----------------------------------------------------------
# User detail
# ----------------------------------------------------------    

def detail(request, userid=None, login=None):
    ''' display role detail '''

    context = start_view(request, app="iam", view="user_detail", 
        noauth="app_user:private", perm="p_user_read", noauthz="app_user:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]

    user = None
    if userid:
        user = user_get_by_id(userid)
    elif login:
        user = user_get_by_login(login)

    if not user:
        messages.add_message(request, messages.ERROR, _("Not allowed"))
        log(WARNING, aaa=aaa, app="iam", view="user", action="detail", status="KO", data=_("Not allowed") )
        return redirect("app_user:user_list")

    log(DEBUG, aaa=aaa, app="iam", view="user", action="detail", status="OK", data=user.login )


    direct,indirect = get_all_groups_for_login(user.login)
    context["direct"] = direct
    context["indirect"] = indirect

    permissions = []
    for g in direct:
        for p in g.permissions.all():
            if p not in permissions:
                permissions.append(p)
    for g in indirect:
        for p in g.permissions.all():
            if p not in permissions:
                permissions.append(p)
    context["permissions"] = permissions

    context["user"] = user
    return render(request, 'app_user/user_detail.html', context)



# ----------------------------------------------------------
# User edit
# ----------------------------------------------------------    

def edit(request, userid=None, login=None):
    ''' user  edit form'''

    context = start_view(request, app="iam", view="user.edit", noauth="app_home:index", 
        perm="p_user_update", noauthz="app_user:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]


    user = None

    # if user is provided, it's an update
    if userid:
        user = user_get_by_id(userid)
        if not user:
            messages.add_message(request, messages.ERROR, _("Not allowed"))
            log(WARNING, aaa=aaa, app="iam", view="user", action="edit", status="KO", data=_("Not allowed"))
            return redirect("app_user:user_list")

    elif login:
        user = user_get_by_login(login)
        if not user:
            messages.add_message(request, messages.ERROR, _("Not allowed"))
            log(WARNING, aaa=aaa, app="iam", view="user", action="edit", status="KO", data=_("Not allowed"))
            return redirect("app_user:user_list")

    # else, it's a create : check p_user_create
    else:
        if "p_user_create" not in aaa["perms"]:
            messages.add_message(request, messages.ERROR, _("Not allowed"))
            log(WARNING, aaa=aaa, app="iam", view="user", action="create", status="KO", data=_("Not allowed"))
            return redirect("app_user:user_list")


    if request.method == "POST":

        form = UserForm(request.POST)
        
        if form.is_valid():

            # update
            if user:
                user = user_update(user, form.cleaned_data)
            # create                
            else:
                user = user_create(data=form.cleaned_data)
            
            # success ?
            if user:
                messages.add_message(request, messages.SUCCESS, _("User saved : ") + user.login )
                log(INFO, aaa=aaa, app="iam", view="edit", action="save", status="OK", data=f"{user.login}")
            else:
                messages.add_message(request, messages.ERROR, _("Failed to save user"))
                log(WARNING, aaa=aaa, app="iam", view="edit", action="save", status="KO", data="")
            
            return redirect("app_user:user_detail", user.login)

        else:
            messages.add_message(request, messages.ERROR, _("Invalid User form"))
            log(DEBUG, aaa=aaa, app="iam", view="edit", action="save", status="KO", data="Invalid User form")

    else:

        if user:
            form = user_get_form(user)
            log(DEBUG, aaa=aaa, app="iam", view="edit", action="edit", status="OK", data=f"{user.login}")

        else: 
            form = user_get_form_blank()
            log(DEBUG, aaa=aaa, app="iam", view="edit", action="new", status="OK", data="")

    context["form"] = form
    if user:
        context["user"] = user

    return render(request, 'app_user/user_edit.html', context)


# # ----------------------------------------------------------
# # User Import
# # ----------------------------------------------------------    

# def user_import(request):

#     context = start_view(request, app="user", view="user_import", noauth="app_home:index", 
#         perm="p_user_import", noauthz="app_user:private")
#     if context["redirect"]:
#         return redirect(context["redirect"])
#     aaa = get_aaa(request)

#     if request.method == "POST":
#         form = UserUploadForm(request.POST, request.FILES)
#         if form.is_valid():

#             file = request.FILES["file"]

#             if file.multiple_chunks():
#                 messages.add_message(request, messages.ERROR, _("Import failed - file too big"))
#                 log(ERROR, aaa=aaa, app="user", view="user_import", action="POST", status="FAIL", data="File too big")   
#                 return redirect("app_user:user_list")          

#             elif file.name.endswith(".json"):
#                 line_total, line_ok = import_json(file)

#             elif file.name.endswith(".yaml"):
#                 line_total, line_ok = import_yaml(file)

#             elif file.name.endswith(".yml"):
#                 line_total, line_ok = import_yaml(file)

#             else:
#                 messages.add_message(request, messages.ERROR, _("Import failed - unknown file"))
#                 log(ERROR, aaa=aaa, app="user", view="user_import", action="POST", status="FAIL", data=f"Unknown file type {file}")
#                 return redirect("app_user:user_list")          

#             # OK
#             messages.add_message(request, messages.SUCCESS, _("Imported  : ") + f"{line_ok}/{line_total}" )    
#             log(INFO, aaa=aaa, app="user", view="user_import", action="POST", status="OK", data=f"{file} - {line_ok}/{line_total} entries")
#             return redirect("app_user:user_list")


#     # Failed
#     messages.add_message(request, messages.ERROR, _("Failed to import"))
#     log(ERROR, aaa=aaa, app="user", view="user_import", action="POST", status="FAIL", data="import failed, not a POST")
#     return redirect("app_user:user_list")


# ----------------------------------------------------------
# User Preferences
# ----------------------------------------------------------    

def preferences(request):
    ''' user  edit form'''

    context = start_view(request, app="iam", view="user_preferences", 
        noauth="app_sirene:index", perm="p_user_pref", noauthz="app_home:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]


    user = user_get_by_login(aaa["username"])
    if not user:
        return redirect("app_home:private")


    if request.method == "POST":

        form = UserPrefForm(request.POST)
        
        if form.is_valid():

            user.displayname = form.cleaned_data["displayname"]
            user.firstname = form.cleaned_data["firstname"]
            user.lastname = form.cleaned_data["firstname"]

            user.want_notifications = form.cleaned_data["want_notifications"]
            user.want_24 = form.cleaned_data["want_24"]
            user.want_email = form.cleaned_data["want_email"]
            user.want_sms = form.cleaned_data["want_sms"]
            user.secondary_email = form.cleaned_data["secondary_email"]
            user.secondary_mobile = form.cleaned_data["secondary_mobile"]

            user.last_update = timezone.now()
            
            try:
                user.save()
            except Exception as e:
                messages.add_message(request, messages.ERROR, _("Failed to edit preferences") )
                print(e)
                return redirect("app_home:private")

            messages.add_message(request, messages.SUCCESS, _("Preferences updated"))
            return redirect("app_home:private")

        else:
            messages.add_message(request, messages.ERROR, _("Invalid preferences"))

    else:

        initial = {}
        # won't be edited
        initial["is_enabled"] = user.is_enabled
        initial["email"] = user.email
        initial["mobile"] = user.mobile

        initial["firstname"] = user.firstname
        initial["lastname"] = user.lastname
        initial["displayname"] = user.displayname

        initial["want_notifications"] = user.want_notifications
        initial["want_24"] = user.want_24
        initial["want_email"] = user.want_email
        initial["want_sms"] = user.want_sms
        initial["secondary_email"] = user.secondary_email
        initial["secondary_mobile"] = user.secondary_mobile

        form = UserPrefForm(initial=initial)

    context["form"] = form
    context["user"] = user
    return render(request, 'app_user/user_pref_edit.html', context)


# -----------------------------------------
# logout
#-----------------------------------------

def logout(request):

    context = start_view(request, app="iam", view="logout", noauth="app_home:index")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]

    request.session.flush()

    # Django Auth mode
    if aaa["auth_mode"] == "local":
        django_logout(request)

    # basic / browser mode
    elif aaa["auth_mode"] == "basic":
        # HACK redirect with false credential
        #redirect("http://logout:logout@cavaliba.com")
        # user must erase his browser history
        pass

    # oauthé
    else:
        # already done by flush
        pass
            


    return redirect("app_home:index")


# -----------------------------------------
# debug user env
#-----------------------------------------
    
def debug_env(request):

    context = start_view(request, app="iam", view="debug_env", 
        noauth="app_sirene:index", perm="p_user_debug", noauthz="app_sirene:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]

    str_headers = '' 
    for header, value in request.headers.items():
        str_headers += f"{header}: {value}\n"

    # decode JWT Access Token if any
    # ------------------------------
    encoded = request.headers.get('X-Access-Token','')
    # encoded = request.META.get('X-Access-Token')

    try:
        jwt_header = jwt.get_unverified_header(encoded)
        jwt_payload = jwt.decode(encoded, options={"verify_signature": False})
        jwt_header = json.dumps(jwt_header, indent=4)
        jwt_payload = json.dumps(jwt_payload, indent=4)
    except Exception as e:
        print(e)
        jwt_header = "n/a"
        jwt_payload = "n/a"

    aaa_nice = pprint.pformat(aaa)


    # OIDC Authorization Bearer Token
    # -------------------------------
    # request.META.get('HTTP_AUTHORIZATION') 
    # request.headers.get('Authorization')
    try:
        # Authorization: Bearer {access_token_here}
        autz_header = request.headers.get('Authorization','')
        encoded = autz_header.split()[1]
        tokid_header  = jwt.get_unverified_header(encoded)
        tokid_payload = jwt.decode(encoded, options={"verify_signature": False})
        tokid_header  = json.dumps(tokid_header, indent=4)
        tokid_payload = json.dumps(tokid_payload, indent=4)
    except Exception as e:
        print(e)
        tokid_header = "n/a"
        tokid_payload = "n/a"


    context["title"] = "Debug ENV"
    context["env"] = str_headers
    context["jwt_header"] = jwt_header
    context["jwt_payload"] = jwt_payload
    context["tokid_header"] = tokid_header
    context["tokid_payload"] = tokid_payload
    context["aaa_nice"] = aaa_nice
    
    return render(request, 'app_user/debug.html', context)

#-----------------------------------------
#  Send test email
#-----------------------------------------
def email_test(request, userid=None):


    context = start_view(request, app="iam", view="email_test", 
        noauth="app_sirene:index", perm="p_user_email_test", noauthz="app_sirene:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]


    subject = get_configuration("sirene","EMAIL_TEST_SUBJECT")
    text_content = get_configuration("sirene", "EMAIL_TEST_CONTENT")
    html_content = None

    dest = ""
    if userid:
        user = user_get_by_id(userid)
        if not user:
            return redirect("app_user:private")

    if request.method == "POST":

        dest = user_get_email(user)

        task_send_mail.delay(subject, text_content, [dest], html_content=html_content, aaa=aaa)
        messages.add_message(request, messages.SUCCESS, _("Test Email sent"))
    
    return redirect("app_user:private")

        

#-----------------------------------------
#  SMS Test form User Edit Form
#-----------------------------------------    
def sms_test(request, userid=None):

    context = start_view(request, app="iam", view="sms_test", 
        noauth="app_sirene:index", perm="p_user_sms_test", noauthz="app_user:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]


    if get_sms_quota(aaa) < 1:
        messages.add_message(request, messages.ERROR, _("Insufficient SMS Quota"))
        return redirect("app_user:private")

    if request.method == "POST":

        dest = ""
        if userid:
            user = user_get_by_id(userid)
            if not user:
                return redirect("app_user:private")

        dest = user_get_mobile(user)

        if not sms_check_valid_number(dest):
            messages.add_message(request, messages.ERROR, _("Invalid SMS number"))
            return redirect("app_user:private")

        data = get_configuration("sirene", "SMS_TEST")

        task_send_sms.delay([dest], data, aaa=aaa)
        messages.add_message(request, messages.SUCCESS, _("Test SMS sent"))

    return redirect("app_user:private")

