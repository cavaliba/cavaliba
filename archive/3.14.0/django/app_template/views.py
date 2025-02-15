# {{ app_name }} - views.py
# (c) cavaliba.com 

import os
from datetime import datetime, timedelta
import time
import base64
import random
import csv

from pprint import pprint

from django.utils import timezone
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.utils.translation import gettext as _



from app_home.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL
from app_user.aaa import start_view
from app_user.aaa import get_aaa 
from app_home.configuration import get_configuration


# -----------

# return redirect("anonymous")
# context={}
# return render(request, '{{ app_name }}/index.html', context)

# log(DEBUG, aaa=aaa, app="log", view="private", action="list", status="OK", data="")


# -----------------------------------------
# index - public page
#-----------------------------------------
# def index(request):

# 	context={}
# 	return render(request, '{{ app_name }}/index.html', context)
    

# def anonymous(request):

#     context={}
#     return render(request, '{{ app_name }}/anonymous.html', context)


def private(request):

    context = start_view(request, app="xxxxxxx", view="private", noauth="app_sirene:index", perm="pxxxx", noauthz="app_sirene:index")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]



    log(DEBUG, aaa=aaa, app="TEMPLATE", view="private", action="list", status="OK", data="")

    return render(request, '{{ app_name }}/private.html', context)



# def list(request):

#     context={}
#     return render(request, '{{ app_name }}/list.html', context)


# def detail(request):

#     context={}
#     return render(request, '{{ app_name }}/detail.html', context)

 
# edit
# new
# api