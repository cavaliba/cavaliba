# # (c) cavaliba.com - sirene - messagetemplate_views

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


from .common import get_bootstrap_colors2

from app_user.aaa import start_view
from app_user.aaa import get_aaa
from app_home.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL

from app_data.models import DataClass
from app_data.models import DataInstance


from .models import MessageTemplate
from .models import Category
from .models import PublicPage

from .template_forms import MessageTemplateForm



#--------------------------------------------
# selector
#--------------------------------------------

def selector(request):

    context = start_view(request, app="sirene", view="template_selector", 
        noauth="app_sirene:index", perm="p_sirene_new", noauthz="app_sirene:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]


    pages = MessageTemplate.objects.filter(is_enabled=True).select_related('category').order_by('id')
    
    for page in pages:
        (bgcolor, fgcolor)= get_bootstrap_colors2(page.severity)
        page.bgcolor=bgcolor
        page.fgcolor=fgcolor

    context["pages"] = pages
    context["title"] = "Messages disponibles"

    return render(request, 'app_sirene/template_selector.html', context)


# --------------------------------------------------------------------    
def list(request):
    ''' display message templates list '''

    context = start_view(request, app="sirene", view="template_list", 
        noauth="app_sirene:index", perm="p_sirene_template_read", noauthz="app_sirene:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]


    templates = MessageTemplate.objects.all().select_related('category').select_related('publicpage').order_by('name')

    for item in templates:
        (bgcolor, fgcolor)= get_bootstrap_colors2(item.severity)
        item.bgcolor=bgcolor
        item.fgcolor=fgcolor

    log(DEBUG, aaa=aaa, app="sirene", view="template", action="list", status="OK")


    context["templates"] = templates
    return render(request, 'app_sirene/template_list.html', context)


# --------------------------------------------------------------------
def delete(request, tid):
    ''' delete template '''

    context = start_view(request, app="sirene", view="template_delete", 
        noauth="app_sirene:index", perm="p_sirene_template_cud", noauthz="app_sirene:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]
  

    if request.method == "POST":

        try: 
            template = MessageTemplate.objects.get(id = tid)
            template.delete()
            messages.add_message(request, messages.SUCCESS, _("Template deleted"))
            log(INFO, aaa=aaa, app="sirene", view="template", action="delete", status="OK", data=f"{template.name}")

        except Exception as e:
            messages.add_message(request, messages.ERROR, _("Failed to delete template"))
            log(ERROR, aaa=aaa, app="sirene", view="template", action="delete", status="KO", data=f"id: {tid}")

    return redirect("app_sirene:template_list")


# --------------------------------------------------------------------
def edit(request, tid=None):
    ''' template  edit form'''

    context = start_view(request, app="sirene", view="template_edit", 
        noauth="app_sirene:index", perm="p_sirene_template_read", noauthz="app_sirene:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]


    if request.method == "POST":

        if "p_sirene_template_cud" not in aaa["perms"]:
            messages.add_message(request, messages.ERROR, _("Not allowed"))
            return redirect("app_sirene:template_list")

        form = MessageTemplateForm(request.POST)

        if form.is_valid():
            if tid:
                template = MessageTemplate.objects.get(pk=tid)
            else:
                template = MessageTemplate()

            cd = form.cleaned_data

            template.name             = cd["name"]
            template.title            = cd["title"]
            template.severity         = cd["severity"]
            template.is_enabled       = cd["is_enabled"]
            template.description      = cd["description"]
            template.body             = cd["body"]

            if cd["publicpage"]:
                template.has_publicpage   = True
                publicpage_name = cd["publicpage"]
                try:
                    publicpage = PublicPage.objects.get(name=publicpage_name)
                except Exception as e:
                    publicpage = None
                template.publicpage = publicpage     
            else:
                template.has_publicpage   = False
                template.publicpage = None

            template.has_privatepage  = cd["has_privatepage"]
            template.has_email        = cd["has_email"]
            template.has_sms          = cd["has_sms"]

            try:
                template.save()
            except:
                messages.add_message(request, messages.ERROR, "Création/modification échouée")
                return redirect("app_sirene:template_list")

            # category
            try:
                catname = cd["category"]
                item = Category.objects.get(name=catname)
                template.category = item
            except:
                pass

            # notify_xxxxx
            template.notify_app.clear()
            for item in cd["notify_app"]:
                template.notify_app.add(item)

            template.notify_site.clear()
            for item in cd["notify_site"]:
                template.notify_site.add(item)

            template.notify_sitegroup.clear()
            for item in cd["notify_sitegroup"]:
                template.notify_sitegroup.add(item)

            template.notify_customer.clear()
            for item in cd["notify_customer"]:
                template.notify_customer.add(item)

            template.notify_group.clear()
            for item in cd["notify_group"]:
                template.notify_group.add(item)


            template.save()  
            messages.add_message(request, messages.SUCCESS, _("Template saved"))
            log(INFO, aaa=aaa, app="sirene", view="template", action="save", status="OK", data=f"{template.name}")
            return redirect("app_sirene:template_list")

        else:
            messages.add_message(request, messages.ERROR, "Failed to save template")
            log(ERROR, aaa=aaa, app="sirene", view="template", action="save", status="KO")


    # GET
    else:
        if tid:
            template = MessageTemplate.objects.get(pk=tid)
            initial = {}

            initial["is_enabled"]       = template.is_enabled
            initial["name"]             = template.name
            initial["title"]            = template.title
            initial["category"]         = template.category
            initial["severity"]         = template.severity
            initial["description"]      = template.description
            initial["body"]             = template.body
            initial["publicpage"]       = template.publicpage
            initial["has_publicpage"]   = template.has_publicpage
            initial["has_privatepage"]  = template.has_privatepage
            initial["has_email"]        = template.has_email
            initial["has_sms"]          = template.has_sms

            # notify_xxxx
            initial["notify_group"]     = [g for g in template.notify_group.all()]
            initial["notify_site"]      = [i for i in template.notify_site.all()]
            initial["notify_app"]       = [i for i in template.notify_app.all()]
            initial["notify_sitegroup"] = [i for i in template.notify_sitegroup.all()]
            initial["notify_customer"]  = [i for i in template.notify_customer.all()]

            form = MessageTemplateForm(initial=initial)
            context["tid"] = tid

        else:
            # if not "p_sirene_template_cud" in aaa["perms"]:
            #     messages.add_message(request, messages.ERROR, _("Not allowed"))
            #     return redirect("app_sirene:template_list")

            form = MessageTemplateForm()

    context["form"] = form
    context['publicpages'] = PublicPage.objects.filter(is_enabled=True)

    return render(request, 'app_sirene/template_edit.html', context)


