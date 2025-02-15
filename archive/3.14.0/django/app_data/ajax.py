# app_data - ajax.py

# import os
# from datetime import datetime, timedelta
# import time
# import base64
# import random
import json
import re
# from pprint import pprint

# from django.utils import timezone
# from django.conf import settings
# from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.contrib import messages
# from django.utils.translation import gettext as _

from django.views.decorators.csrf import csrf_protect

from app_home.configuration import get_configuration
from app_user.aaa import start_ajax
# from app_data.models import DataClass
from app_data.models import DataInstance

# Security: authenticated (oauth2), GET / read-only
@csrf_protect
def ajax_instance(request):

    # GET /data/private/ajax/?q=query&c=classname
    # respdata = """
    # {
    #   "results": [
    #     { "id": "ajax1", "text": "ajax1"},
    #     { "id": "ajax2", "text": "ajax2"}
    #   ]
    # }
    # """
    response = HttpResponse("{}", content_type='text/json')  

    context = start_ajax(request)
    if not context:
        return response

    m = re.compile(r'[a-zA-Z0-9()_/.-]*$')

    classname = request.GET.get("c")
    if not classname:
        return response
    if not m.match(classname):
        return response

    query = request.GET.get("q", "")
    if not m.match(query):
        return response

    bigset_size = int(get_configuration("data","DATA_BIGSET_SIZE"))
    instances = DataInstance.objects.filter(classobj__keyname=classname, is_enabled=True, keyname__icontains=query)[0:bigset_size]

    data = {}
    data['results'] = []
    for item in instances:
        data['results'].append({'id':item.keyname, 'text':item.keyname})

    respdata = json.dumps(data, indent=4)

    #pprint(data)
    response = HttpResponse(respdata, content_type='text/json')  
    return response     