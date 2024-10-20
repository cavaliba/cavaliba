# app_conf - views.py - 
# (c) cavaliba.com 

import os
from datetime import datetime, timedelta
import time
import base64
import random
import csv


from django.utils import timezone
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.utils.translation import gettext as _


# ---
from app_log.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL
from app_user.aaa import start_view
from app_user.aaa import get_aaa 

# --
from .configuration import get_configuration
from .configuration import get_initial_form
from .configuration import get_post_form
from .configuration import save_form


from app_home.home import get_app_by_name
from app_home.home import get_applist

# return redirect("anonymous")
# context={}
# return render(request, 'app_user/index.html', context)

# -----------------------------------------
# private
#-----------------------------------------

def private(request, appname=None):

    #context = start_view(request, app="home", view="private", noauth="app_sirene:index", perm="p", noauthz="app_sirene:index")
    context = start_view(request, app="conf", view="private", noauth="app_home:index", 
        perm="p_conf_access", noauthz="app_sirene:index")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]

    if appname:
        appobj = get_app_by_name(appname)
        if not appobj:
            return redirect("app_home:index")


    if request.method == "POST":

        form = get_post_form(request, appname=appname)

        if form.is_valid():
            save_form(form, appname=appname)
            messages.add_message(request, messages.SUCCESS, _("Configuration updated"))
            log(INFO, aaa=aaa, app="conf", view="private", action="update", status="OK", data=f"app {appname}")
            return redirect("app_conf:private", appname )
        else:
            messages.add_message(request, messages.ERROR, _("Invalid configuration"))
    
    else:
        form = get_initial_form(appname)

    if appname:
        context["appname"] = appobj.displayname

    apps = get_applist(aaa)
    context["apps"] = apps

    context["form"] = form
    return render(request, 'app_conf/private.html', context)

