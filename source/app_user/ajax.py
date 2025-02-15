# (c) cavaliba.com - IAM - ajax.py

import json
import re
from pprint import pprint

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.translation import gettext as _

from django.views.decorators.csrf import csrf_protect

from app_home.configuration import get_configuration

from app_user.aaa import start_ajax

from app_user.models import SireneUser




# Security: authenticated (oauth2), GET / read-only
@csrf_protect
def ajax_user(request):

    # GET /user/private/ajax/?q=query
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

    query = request.GET.get("q", "")
    if not m.match(query):
        return response

    bigset_size = int(get_configuration("data","DATA_BIGSET_SIZE"))
    users = SireneUser.objects.filter(is_enabled=True, login__icontains=query)[0:bigset_size]

    data = {}
    data['results'] = []
    for item in users:
        dsp = f"{item.login} ({item.displayname})"
        data['results'].append({'id':item.login, 'text':dsp})

    #respdata = json.dumps(data, indent=4)
    respdata = json.dumps(data, indent=4, ensure_ascii = False).encode('utf8')
    #pprint(data)
    response = HttpResponse(respdata, content_type='text/json')  
    return response     


