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


from app_log.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL
#log(INFO, aaa=aaa, app="home", view="private", action="update_dashboard", status="OK", data="")


from .models import DashboardApp

from .home import update_dashboard 
from app_data.data import update_bigset

from .home import get_applist

from .load import load_dict

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
            update_dashboard()
            update_bigset()
            messages.add_message(request, messages.SUCCESS, _("Dashboard updated"))
            log(INFO, aaa=aaa, app="home", view="private", action="update_dashboard", status="OK", data="")

        else:
            messages.add_message(request, messages.ERROR, _("Not allowed"))
            log(ERROR, aaa=aaa, app="home", view="dashboard", action="update", status="KO", data=f"not allowed")
            return render(request, 'app__sirene:index')    

    apps = get_applist(aaa)
    for x in apps:
        if x.keyname=='home':
            apps.remove(x)
            break

    context['apps'] = apps
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
