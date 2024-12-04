# views_category.py

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


from app_home.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL
from app_user.aaa import start_view
from app_user.aaa import get_aaa

from .models import Category
from .category_forms import CategoryForm




def list(request):
    ''' display Category list '''


    context = start_view(request, app="sirene", view="category_list", 
        noauth="app_sirene:index", perm="p_sirene_cat_read", noauthz="app_sirene:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]

    categories = Category.objects.all().order_by('id')

    log(DEBUG, aaa=aaa, app="sirene", view="category", action="list", status="OK", data="")

    context["categories"] = categories
    return render(request, 'app_sirene/category_list.html', context)



def delete(request, cid):
    ''' delete category '''

    context = start_view(request, app="sirene", view="category_delete", 
        noauth="app_sirene:index", perm="p_sirene_cat_cud", noauthz="app_sirene:category_list")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]


    if request.method == "POST":

        try: 
            category = Category.objects.get(id = cid)
            category.delete()
            messages.add_message(request, messages.SUCCESS, _("Category deleted"))
            log(INFO, aaa=aaa, app="sirene", view="category", action="delete", status="OK", data=f"{category.name}")
        except Exception as e:
            messages.add_message(request, messages.ERROR, _("Failed"))
            log(ERROR, aaa=aaa, app="sirene", view="category", action="delete", status="KO", data=f"{e}")

    return redirect("app_sirene:category_list")



def edit(request, cid=None):
    ''' category edit form'''

    context = start_view(request, app="sirene", view="category_edit", 
        noauth="app_sirene:index", perm="p_sirene_cat_read", noauthz="app_sirene:category_list")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]


    if request.method == "POST":

        if 'p_sirene_cat_cud' not in aaa["perms"]:
            messages.add_message(request, messages.WARNING, _("Not allowed"))
            log(WARNING, aaa=aaa, app="sirene", view="category", action="edit", status="KO", data="not allowed")
            return redirect("app_sirene:category_list")

        form = CategoryForm(request.POST)
        if form.is_valid():
            if cid:
                category = Category.objects.get(pk=cid)
            else:
                category = Category()

            cd = form.cleaned_data
            category.name        = cd["name"]
            category.longname    = cd["longname"]
            category.is_enabled  = cd["is_enabled"]
            category.description = cd["description"]

            try:
                category.save()
            except Exception as e:
                messages.add_message(request, messages.ERROR, _("Failed"))
                log(ERROR, aaa=aaa, app="sirene", view="category", action="save", status="KO", data=f"{e}")
                return redirect("app_sirene:category_list")

            messages.add_message(request, messages.SUCCESS, _("Category saved"))
            log(INFO, aaa=aaa, app="sirene", view="category", action="save", status="OK", data=f"<{category.name}>")
            return redirect("app_sirene:category_list")

        else:
            messages.add_message(request, messages.ERROR, _("Invalid form"))
            log(WARNING, aaa=aaa, app="sirene", view="category", action="edit", status="KO", data="Invalid form")
    # GET
    else:
        if cid:
            category = Category.objects.get(pk=cid)
            initial = {}
            initial["name"]        = category.name
            initial["longname"]    = category.longname
            initial["is_enabled"]  = category.is_enabled
            initial["description"] = category.description
            form = CategoryForm(initial=initial)
            context["cid"] = cid
            log(INFO, aaa=aaa, app="sirene", view="category", action="edit", status="OK", data=f"<{category.name}>")
        else:
            form = CategoryForm()
            log(INFO, aaa=aaa, app="sirene", view="category", action="edit", status="OK", data="new")

    context["form"] = form
    return render(request, 'app_sirene/category_edit.html', context)


