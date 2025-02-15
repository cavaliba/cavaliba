# (c) cavaliba.com - sirene - views.py

import os
from datetime import datetime
from datetime import timedelta
import time
import base64
import random

from django.utils import timezone
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.utils.translation import gettext as _


from app_home.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL

from app_user.aaa import start_view
from app_user.aaa import get_aaa


from .models import PublicPage
from .models import PublicPageJournal

from .publicpage_forms import PublicPageForm

from .common import get_bootstrap_colors2

#---------------------------------------------
# PUBLICPAGE :  CRUD for templates
#---------------------------------------------

    
def selector(request):
    ''' display  list '''

    context = start_view(request, app="sirene", view="publicpage_selector", 
        noauth="app_sirene:index", perm="p_sirene_public_read", noauthz="app_sirene:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]


    publicpages = PublicPage.objects.all()

    for page in publicpages:
        (bgcolor, fgcolor)= get_bootstrap_colors2(page.severity)
        page.bgcolor=bgcolor
        page.fgcolor=fgcolor


    context["publicpages"] = publicpages
    return render(request, 'app_sirene/publicpage_selector.html', context)


def preview(request , ppid):

    context = start_view(request, app="sirene", view="publicpage_preview", 
        noauth="app_sirene:index", perm="p_sirene_public_read", noauthz="app_sirene:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]


    publicpage = PublicPage.objects.filter(pk=ppid).first()
    if not publicpage:
        log(WARNING, aaa=aaa, app="sirene", view="public", action="preview", status="KO", data=_("Not allowed")) 
        messages.add_message(request, messages.ERROR, _("Not allowed"))
        return redirect("app_sirene:publicpage_list")

    (bgcolor, fgcolor) = get_bootstrap_colors2(publicpage.severity)

    context["title"] = f"PagePublique: {publicpage.name}"
    context["publicpage"] = publicpage
    context["bgcolor"] = bgcolor
    context["fgcolor"] = fgcolor
    context["ppid"] = ppid

    return render(request, 'app_sirene/publicpage_preview.html', context)

    

def push(request, ppid):
    """ push publicpage to Journal for public display """


    context = start_view(request, app="sirene", view="publicpage_push", 
        noauth="app_sirene:index", perm="p_sirene_public_push", noauthz="app_sirene:publicpage_list")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]


    if request.method == "POST":

        publicpage = PublicPage.objects.filter(pk=ppid).first()
        if not publicpage:
            log(WARNING, aaa=aaa, app="sirene", view="public", action="push", status="KO", data=_("Not allowed"))             
            messages.add_message(request, messages.ERROR, _("Not allowed"))
            return redirect("app_sirene:publicpage_list")

        # default  page => reset
        if publicpage.is_default:
            PublicPageJournal.reset(aaa=aaa)
            log(INFO, aaa=aaa, app="sirene", view="public", action="push", status="KO", data=_("Default pushed")) 
            messages.add_message(request, messages.SUCCESS, _("Public page reset to default"))

        # standard publicpage
        else:
            journal = PublicPageJournal.add(publicpage=publicpage, aaa=aaa)
            if journal:
                log(INFO, aaa=aaa, app="sirene", view="public", action="push", status="OK", data=f"{publicpage.name}") 
                messages.add_message(request, messages.SUCCESS, _("Public page published: ") + publicpage.name)
            else:
                log(ERROR, aaa=aaa, app="sirene", view="public", action="push", status="KO", data=_("Push public page")) 
                messages.add_message(request, messages.ERROR, _("Failed to publish public page"))

    else:
        log(ERROR, aaa=aaa, app="sirene", view="public", action="push", status="KO", data=_("Not a POST")) 
        messages.add_message(request, messages.ERROR, _("Not allowed"))

    return redirect("app_sirene:publicpage_selector")




def list(request):
    ''' display  list '''

    context = start_view(request, app="sirene", view="publicpage_list", 
        noauth="app_sirene:index", perm="p_sirene_public_read", noauthz="app_sirene:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]


    publicpages = PublicPage.objects.all()


    for page in publicpages:
        (bgcolor, fgcolor)= get_bootstrap_colors2(page.severity)
        page.bgcolor=bgcolor
        page.fgcolor=fgcolor


    context["title"] = "Pages Publiques"
    context["publicpages"] = publicpages
    return render(request, 'app_sirene/publicpage_list.html', context)




def delete(request, ppid):
    ''' delete model '''

    context = start_view(request, app="sirene", view="publicpage_delete", 
        noauth="app_sirene:index", perm="p_sirene_public_cud", noauthz="app_sirene:publicpage_list")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]


    if request.method == "POST":

        try: 
            publicpage = PublicPage.objects.get(id = ppid)
            publicpage.delete()
            messages.add_message(request, messages.SUCCESS, _("Public Page deleted :") + publicpage.name)
            log(INFO, aaa=aaa, app="sirene", view="public", action="delete", status="OK", data=f"{publicpage.name}") 

        except Exception as e:
            messages.add_message(request, messages.ERROR, _("Failed to delete public page"))
            log(ERROR, aaa=aaa, app="sirene", view="public", action="delete", status="FAIL", data=_("Failed to delete publicpage")) 
            return redirect("app_sirene:publicpage_list")

    return redirect("app_sirene:publicpage_list")




# publicapge
def edit(request, ppid=None):
    ''' pp edit form'''

    context = start_view(request, app="sirene", view="publicpage_edit", 
        noauth="app_sirene:index", perm="p_sirene_public_cud", noauthz="app_sirene:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]

    if request.method == "POST":

        form = PublicPageForm(request.POST)
        if form.is_valid():
            if ppid:
                publicpage = PublicPage.objects.get(pk=ppid)
            else:
                publicpage = PublicPage()

            cd = form.cleaned_data
            publicpage.name             = cd["name"]
            publicpage.title            = cd["title"]
            publicpage.body             = cd["body"]
            publicpage.severity         = cd["severity"]
            publicpage.is_default       = cd["is_default"]
            publicpage.is_enabled       = cd["is_enabled"]

            try:
                publicpage.save()
            except:
                messages.add_message(request, messages.ERROR, _("Failed to save public page"))
                log(ERROR, aaa=aaa, app="sirene", view="public", action="edit", status="KO", data="Failed to save public page") 
                return redirect("app_sirene:publicpage_list")

            messages.add_message(request, messages.SUCCESS, _("Public page saved"))
            log(INFO, aaa=aaa, app="sirene", view="public", action="edit", status="OK", data=f"saved {publicpage.name}") 

            return redirect("app_sirene:publicpage_list")

        else:
            messages.add_message(request, messages.ERROR, _("Invalid"))
            log(ERROR, aaa=aaa, app="sirene", view="public", action="edit", status="KO", data="Invalid form")
    # GET
    else:
        if ppid:
            publicpage = PublicPage.objects.get(pk=ppid)
            initial = {}

            initial["name"]             = publicpage.name
            initial["title"]            = publicpage.title
            initial["body"]             = publicpage.body
            initial["severity"]         = publicpage.severity
            initial["is_default"]       = publicpage.is_default
            initial["is_enabled"]       = publicpage.is_enabled
            form = PublicPageForm(initial=initial)
            context["ppid"] = ppid
        else:
            form = PublicPageForm()

        log(DEBUG, aaa=aaa, app="sirene", view="public", action="edit", status="OK", data="get form")

    context["form"] = form
    return render(request, 'app_sirene/publicpage_edit.html', context)


