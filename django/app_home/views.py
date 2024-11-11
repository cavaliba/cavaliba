# app_home - views.py - # (c) cavaliba.com 

import yaml


from django.utils import timezone
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.utils.translation import gettext as _


from app_user.aaa import start_view
from app_user.aaa import get_aaa 
from .configuration import get_configuration
from app_log.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL


from .configuration import get_initial_form
from .configuration import get_post_form
from .configuration import save_form

from .home import get_app_by_name
from .home import get_applist
from .home import get_cavaliba_apps
from .home import cavaliba_update
from .home import get_applist
from .home import load_dict

from .models import DashboardApp

from app_data.data import update_bigset



# return redirect("anonymous")
# context={}
# return render(request, 'app_home/index.html', context)


# -----------------------------------------
# private - private_page
#-----------------------------------------

def private(request):

    context = start_view(request, app="home", view="private", 
        noauth="app_sirene:index", perm="p_home_access", noauthz="app_sirene:index")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]

    if request.method == "POST":

        if 'p_home_update' in aaa["perms"]:
            cavaliba_update()
            update_bigset()
            messages.add_message(request, messages.SUCCESS, _("Dashboard updated"))
            log(INFO, aaa=aaa, app="home", view="private", action="cavaliba_update", status="OK", data="")

        else:
            messages.add_message(request, messages.ERROR, _("Not allowed"))
            log(ERROR, aaa=aaa, app="home", view="dashboard", action="update", status="KO", data=f"not allowed")
            return render(request, 'app__sirene:index')    

    apps = get_applist(aaa)
    for x in apps:
        if x.keyname=='home':
            apps.remove(x)
            break


    # page/order for UI
    # [  [page1, [item1, item22,  ...] , [ page2, [...] ] ,  ... ]
    paginated = []
    pagelist = []
    index = {} # page => [class1, class2]
    default_name = get_configuration("home", "GLOBAL_APPNAME")

    for element in apps:
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
        default_name = page
    for p in pagelist:
        paginated.append( [p, index[p] ])


    #context['apps'] = apps
    context['paginated'] = paginated
    return render(request, 'app_home/private.html', context)



# -----------------------------------------
# YAML import tool
#-----------------------------------------


def yaml_import(request):

    context = start_view(request, app="home", view="yaml_import", 
        noauth="app_sirene:private", perm="p_home_import_yaml", noauthz="app_home:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]

    rawdata = ""

    if request.method == "POST":

        valid = False
        rawdata = request.POST["rawdata"]
        cleandata = ""

        try:
            cleandata = yaml.safe_load(rawdata)
            valid = True
        except Exception as e:
            messages.add_message(request, messages.ERROR, e)


        #print(yaml.dump(cleandata))

        if valid:
            if request.POST["submit"] == "import":
                # load twice for references
                status = load_dict(cleandata, aaa=aaa)
                status = load_dict(cleandata, aaa=aaa)
                messages.add_message(request, messages.SUCCESS, _("YAML loaded"))
                return redirect("app_home:private")

            else:
                # TODO : check
                messages.add_message(request, messages.SUCCESS, _("Check ok"))
                # no redirect, keep editing


    context["rawdata"] = rawdata
    return render(request, 'app_home/import_yaml.html', context)







# -----------------------------------------
# configuration
#-----------------------------------------


# import os
# from datetime import datetime, timedelta
# import time
# import base64
# import random
# import csv


# from django.utils import timezone
# from django.conf import settings
# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from django.contrib import messages
# from django.utils.translation import gettext as _


# # ---
# from app_log.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL
# from app_user.aaa import start_view
# from app_user.aaa import get_aaa 

# # --




def configuration(request, appname=None):

    #context = start_view(request, app="home", view="private", noauth="app_sirene:index", perm="p", noauthz="app_sirene:index")
    context = start_view(request, app="home", view="configuration", noauth="app_home:index", 
        perm="p_conf_admin", noauthz="app_sirene:index")
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
            log(INFO, aaa=aaa, app="home", view="configuration", action="update", status="OK", data=f"app {appname}")
            return redirect("app_home:configuration", appname )
        else:
            messages.add_message(request, messages.ERROR, _("Invalid configuration"))
    
    else:
        form = get_initial_form(appname)

    if appname:
        context["appname"] = appobj.displayname

    context["apps"] = get_cavaliba_apps()
    context["form"] = form
    return render(request, 'app_home/configuration.html', context)

