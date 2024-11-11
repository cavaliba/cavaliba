# app_log - views.py
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
from django.core.paginator import Paginator
from django.utils.translation import gettext as _
from django.db.models import Q


from app_user.aaa import start_view
from app_user.aaa import get_aaa 
from app_home.configuration import get_configuration

from .log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL
from .log import purge

from .models import SireneLog



# return redirect("anonymous")
# context={}
# return render(request, 'app_log/index.html', context)




def private(request, level="debug"):

    context = start_view(request, app="log", view="private", noauth="app_sirene:index", perm="p_log_view", noauthz="app_home:index")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]

    log(DEBUG, aaa=aaa, app="log", view="private", action="access", status="OK")


    # purge ?
    if request.method == "POST":
        if request.POST.get('purge'):
            if 'p_log_manage' in aaa["perms"]:
                count = purge(aaa=aaa, keep_days=0)
                messages.add_message(request, messages.SUCCESS, _("All Log purged: ") + str(count) )
                log(WARNING, aaa=aaa, app="log", view="private", action="purge", status="OK", data=f"{count} removed")
                return redirect("app_log:private")


    # bigset or not
    count = SireneLog.objects.count()
    bigset = True
    context["bigset"] = bigset
    context["count"] = count



    # Filter POST (form)
    # -------------------
    #query = request.GET.get("q", "")
    query = ""
    if request.method == "POST":
        if request.POST.get('query'):
            query = request.POST.get('query')
    if request.method == "GET":
        if request.GET.get('query'):
            query = request.GET.get('query')
    if query:
        m = re.compile(r'[a-zA-Z0-9()_/.-]*$')
        if not m.match(query):
            query = ""
    context["query"] = query


    # partial query + paginate if bigset
    try:
        size = int(request.GET.get("size", 100))
        page = int(request.GET.get("page",1))
    except:
        return redirect("app_log:private")

    if page < 1 or size > 10000 or size < 1:
        return redirect("app_log:private")


    offset = (page-1) * size
    limit = offset + size

    if len(query) > 0:

        if level not in ["debug","info","warning","error","critical"]:
            level = "debug"

        if level == "info":
            level_display = _('INFO')
            logs = SireneLog.objects.all().order_by("-id").filter(level__in=['info','warning','error','critical']).filter(
                    Q(app__icontains=query) |
                    Q(username__icontains=query) |
                    Q(view__icontains=query) |
                    Q(action__icontains=query) |
                    Q(data__icontains=query) |
                    Q(status__icontains=query) |
                    Q(user_ip__icontains=query)\
                    )[offset:limit]

        elif level == "warning":
            level_display = _('WARNING')
            logs = SireneLog.objects.all().order_by("-id").filter(level__in=['warning','error','critical']).filter(
                    Q(app__icontains=query) |
                    Q(username__icontains=query) |
                    Q(view__icontains=query) |
                    Q(action__icontains=query) |
                    Q(data__icontains=query) |
                    Q(status__icontains=query) |
                    Q(user_ip__icontains=query)\
                    )[offset:limit]                
            

        elif level == "error":
            level_display = _('ERROR')
            logs = SireneLog.objects.all().order_by("-id").filter(level__in=['error','critical']).filter(
                    Q(app__icontains=query) |
                    Q(username__icontains=query) |
                    Q(view__icontains=query) |
                    Q(action__icontains=query) |
                    Q(data__icontains=query) |
                    Q(status__icontains=query) |
                    Q(user_ip__icontains=query)\
                    )[offset:limit]                
            

        elif level == "critical":
            level_display = _('CRITICAL')
            logs = SireneLog.objects.all().order_by("-id").filter(level='critical').filter(
                    Q(app__icontains=query) |
                    Q(username__icontains=query) |
                    Q(view__icontains=query) |
                    Q(action__icontains=query) |
                    Q(data__icontains=query) |
                    Q(status__icontains=query) |
                    Q(user_ip__icontains=query)\
                    )[offset:limit]                        

        else:
            level_display = _('DEBUG')
            logs = SireneLog.objects.all().order_by("-id").filter(
                    Q(app__icontains=query) |
                    Q(username__icontains=query) |
                    Q(view__icontains=query) |
                    Q(action__icontains=query) |
                    Q(data__icontains=query) |
                    Q(status__icontains=query) |
                    Q(user_ip__icontains=query)\
                    )[offset:limit]
    else:

        if level not in ["debug","info","warning","error","critical"]:
            level = "debug"

        if level == "info":
            level_display = _('INFO')
            logs = SireneLog.objects.all().order_by("-id").filter(level__in=['info','warning','error','critical'])[offset:limit]
            
        elif level == "warning":
            level_display = _('WARNING')
            logs = SireneLog.objects.all().order_by("-id").filter(level__in=['warning','error','critical'])[offset:limit]

        elif level == "error":
            level_display = _('ERROR')
            logs = SireneLog.objects.all().order_by("-id").filter(level__in=['error','critical'])[offset:limit]

        elif level == "critical":
            level_display = _('CRITICAL')
            logs = SireneLog.objects.all().order_by("-id").filter(level='critical')[offset:limit]

        else:
            level_display = _('DEBUG')
            logs = SireneLog.objects.all().order_by("-id")[offset:limit]
                
    
    # PREV | FIRST || CURRENT or ... || LAST | NEXT
    context["size"] = size
    context["page"] = page
    page_last = int (count / size) + 1
    
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






    context["level"] = level_display
    context["logs"] = logs
    return render(request, 'app_log/private.html', context)

