# (c) cavaliba.com  -  app_data - api.py

import json
import yaml
import csv
from io import StringIO

from pprint import pprint

from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from django.utils.translation import gettext as _

from app_home.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL
from app_home.configuration import get_configuration

from app_user.api import start_api

from app_data.data import get_classes
from app_data.data import get_instances
from app_data.data import Instance

from app_data.loader import load_broker
from app_data.pipeline import apply_pipeline
from app_data.pipeline import get_pipeline



# ----------------------------------------------------------------------------
# /data/api/
# ----------------------------------------------------------------------------
@csrf_exempt
def index(request):


    # reply = {}
    # reply["is_allowed"] = False
    # reply["keyname"] = None
    # reply["is_readonly"] = True
    # reply["error"] = "no action performed"
    # reply["user_ip"] = None
    # reply["acl_filter"] = None
    # reply["permissions"] = []

    reply = start_api(request)

    if not reply["is_allowed"]:
        print("Not allowed !", reply["error"])
        return HttpResponse(status=401)    # unauthorized

    if request.method == "POST" and reply["is_readonly"]:
        print("POST not allowed for read-only key")
        return HttpResponse(status=401)    # unauthorized

    #pprint(reply)

    reply = {"status":"OK"}
    myjson = json.dumps(reply, indent=4, ensure_ascii = False).encode('utf8')
    return HttpResponse(myjson)
    #return render(request, 'app_data/api.html')


# ----------------------------------------------------------------------------
# /data/api/classes/
# GET
# ----------------------------------------------------------------------------
@csrf_exempt
def classes(request):

    context = start_api(request)
    reply = {}

    if not context["is_allowed"]:
        print("Not allowed !", context["error"])
        return HttpResponse(status=401)    # unauthorized

    # permission 
    if "p_api_get_classes" not in context["permissions"]:
        print("Not allowed !", context["error"])
        return HttpResponse(status=401)    # unauthorized

    if request.method == "GET": 
        # qs
        cls = get_classes()
        for c in cls:
            reply[c.keyname] = c.displayname

    else:
        return HttpResponse(status=401)    # unauthorized

    myjson = json.dumps(reply, indent=4, ensure_ascii = False).encode('utf8')
    return HttpResponse(myjson)


# ----------------------------------------------------------------------------
# /data/api/c/CLASSNAME/
# GET
# ----------------------------------------------------------------------------
@csrf_exempt
def classname(request, classname):

    context = start_api(request)
    reply = {}

    if not context["is_allowed"]:
        print("Not allowed !", context["error"])
        return HttpResponse(status=401)    # unauthorized

    # permission 
    if "p_api_get_classname" not in context["permissions"]:
        print("Not allowed !", context["error"])
        return HttpResponse(status=401)    # unauthorized

    if request.method == "GET": 
        # qs
        instances = get_instances(classname=classname)
        for c in instances:
            reply[c.keyname] = c.displayname

    else:
        return HttpResponse(status=401)    # unauthorized

    myjson = json.dumps(reply, indent=4, ensure_ascii = False).encode('utf8')
    return HttpResponse(myjson)


# ----------------------------------------------------------------------------
# /data/api/c/CLASSNAME/i/INSTANCE/
# GET
# ----------------------------------------------------------------------------
@csrf_exempt
def instance(request, classname, keyname):

    context = start_api(request)
    reply = {}

    if not context["is_allowed"]:
        print("Not allowed !", context["error"])
        return HttpResponse(status=401)    # unauthorized

    # permission 
    if "p_api_get_instance" not in context["permissions"]:
        print("Not allowed !", context["error"])
        return HttpResponse(status=401)    # unauthorized

    if request.method == "GET": 
        # qs
        instance = Instance(classname=classname, iname=keyname)
        reply = instance.get_dict_for_ui_detail()
    else:
        return HttpResponse(status=401)    # unauthorized

    myjson = json.dumps(reply, indent=4, ensure_ascii = False).encode('utf8')
    return HttpResponse(myjson)


# ----------------------------------------------------------------------------
# POST /data/api/import/
# ----------------------------------------------------------------------------
@csrf_exempt
def api_import(request):

    context = start_api(request)

    if not context["is_allowed"]:
        print("Not allowed !", context["error"])
        return HttpResponse(status=401)    # unauthorized

    if request.method != "POST":
        return HttpResponse(status=401)    # unauthorized

    # API Key read-only ?
    if context["is_readonly"]:
        print("POST not allowed for read-only key")
        return HttpResponse(status=401)    # unauthorized

    # permission 
    if "p_api_import" not in context["permissions"]:
        print("Not allowed !", context["error"])
        return HttpResponse(status=401)    # unauthorized
    
    body = request.body

    # application/yaml / application/x-yaml / text/x-yaml / text/yaml
    # application/json / ...
    if 'yaml' in request.content_type:
        data = yaml.safe_load(body)
    elif 'json' in request.content_type: 
        data = json.loads(body)
    else:
        data = ''

    # get pipeline
    pipeline = request.GET.get("pipeline", None)
    pipeline_data = {}
    if pipeline:
        pipeline_data = get_pipeline(pipeline)
    if not pipeline_data:
        pipeline_data = {}

    # apply pipeline
    if pipeline:
        datalist = apply_pipeline(pipeline=pipeline, datalist=data)

    # process import data (2 pass)
    count1 = load_broker(datalist=datalist, verbose=False)
    count2 = load_broker(datalist=datalist, verbose=False)

    reply = {"ok pass 1": count1 , "ok pass 2": count2}

    myjson = json.dumps(reply, indent=4, ensure_ascii = False).encode('utf8')
    return HttpResponse(myjson)


# ----------------------------------------------------------------------------
# POST /data/api/csv/CLASSNAME/?pipeline=PIPENAME&delimiter=|
# ----------------------------------------------------------------------------
@csrf_exempt
def api_csv(request, classname):

    context = start_api(request)

    if not context["is_allowed"]:
        print("Not allowed !", context["error"])
        return HttpResponse(status=401)    # unauthorized

    if request.method != "POST":
        return HttpResponse(status=401)    # unauthorized

    # API Key read-only ?
    if context["is_readonly"]:
        print("POST not allowed for read-only key")
        return HttpResponse(status=401)    # unauthorized

    # permission 
    if "p_api_csv" not in context["permissions"]:
        print("Not allowed !", context["error"])
        return HttpResponse(status=401)    # unauthorized
    
    # text/csv
    csvdata = ''
    if request.content_type == 'text/csv':
        csvdata = request.body.decode("utf-8")

    # get pipeline
    pipeline = request.GET.get("pipeline", None)
    pipeline_data = {}
    if pipeline:
        pipeline_data = get_pipeline(pipeline)
    if not pipeline_data:
        pipeline_data = {}

    # csv delimiter : URL >> pipeline >> configuration >> default=','
    csv_delimiter = request.GET.get("delimiter", None)
    if not csv_delimiter:
        csv_delimiter = pipeline_data.get("csv_delimiter", None)
        if not csv_delimiter:
            csv_delimiter = get_configuration(appname="home", keyname="CSV_DELIMITER")

    data = []
    csvfile = StringIO(csvdata)
    csv_reader = csv.DictReader(csvfile, delimiter=csv_delimiter)

    for entry in csv_reader:
        entry["classname"] = classname
        data.append(entry)
        # key = None
        # if classname == "_user":
        #     keyname = entry.get("login", None)
        #     if keyname:
        #         key = f"_user:{keyname}"
        # else:
        #     keyname = entry.get("keyname", None)                
        #     if keyname:
        #         key = f"{classname}:{keyname}"
        # if key:
        #     data[key] = entry

    # apply pipeline
    if pipeline:
        datalist = apply_pipeline(pipeline=pipeline, datalist=data)


    count = load_broker(datalist=datalist, verbose=False)

    reply = {"status": "ok", "count_ok": count}

    myjson = json.dumps(reply, indent=4, ensure_ascii = False).encode('utf8')
    return HttpResponse(myjson)


