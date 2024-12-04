# export.py
# Export DB to JSON / YAML /CSV



import os
from datetime import datetime, timedelta
import time
import base64
import random

import csv
import json
import yaml

from django.http import HttpResponse
from django.forms.models import model_to_dict

from app_home.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL

from .models import Category
from .models import PublicPage
from .models import MessageTemplate



# -------------------------------------------------
#  EXPORT - all
# -------------------------------------------------
# YAML
class MyYamlDumper(yaml.SafeDumper):
    def write_line_break(self, data=None):
        super().write_line_break(data)
        if len(self.indents) < 2:
            super().write_line_break()
            super().write_line_break()

def full_yaml_response():

    data = full_export_dict()
    filedata = yaml.dump(data, allow_unicode=True, Dumper=MyYamlDumper, sort_keys=False)
    response = HttpResponse(filedata, content_type='text/yaml')  
    response['Content-Disposition'] = 'attachment; filename="sirene_notification.yaml"'
    return response

# json
def full_json_response(categories):

    data = full_export_dict()
    filedata = json.dumps(data, indent=4)
    response = HttpResponse(filedata, content_type='text/json')  
    response['Content-Disposition'] = 'attachment; filename="sirene_notification.json"'
    return response


def full_export_dict():

    data = {}

    # category
    r = []
    mylist = Category.objects.all()
    for item in mylist:
        m = category_dict_format(item)
        name = item.name
        data[f'_sirene_category:{name}'] = m
    #     r.append(m)
    # data['_sirene_category'] = r

    # publicpages
    r = []
    mylist = PublicPage.objects.all()
    for item in mylist:
        m = publicpage_dict_format(item)
        name = item.name
        data[f'_sirene_public:{name}'] = m
    #     r.append(m)
    # data['_sirene_public'] = r

    # templates
    r = []
    mylist = MessageTemplate.objects.all()
    for item in mylist:
        m = template_dict_format(item)
        name = item.name
        data[f'_sirene:{name}'] = m
    #     r.append(m)
    # data['_sirene_template'] = r

    return data


# -------------------------------------------------
#  EXPORT - Templates
# -------------------------------------------------

def template_dict_format(item):

    if not item:
        return

    dict_attributs =  [  "severity", "title", "body", "description", 
        "is_enabled", "has_publicpage", "has_privatepage", "has_email", "has_sms",
        # "name",
        ] 

    # standard attibuts
    m = model_to_dict(item, fields=dict_attributs)

    # remove null values
    m2= {}
    for k,v in m.items():
        if v:
            m2[k] = v

    # special attibuts
    m2["category"]= str(item.category)
    m2["publicpage"]= str(item.publicpage)
    m2["notify_site"] = [i.keyname for i in item.notify_site.all()]
    m2["notify_app"] = [i.keyname for i in item.notify_app.all()]
    m2["notify_sitegroup"] = [i.keyname for i in item.notify_sitegroup.all()]
    m2["notify_customer"] = [i.keyname for i in item.notify_customer.all()]
    m2["notify_group"] = [i.keyname for i in item.notify_group.all()]


    return m2


# -------------------------------------------------
#  EXPORT - Public Pages
# -------------------------------------------------

def publicpage_dict_format(item):

    if not item:
        return

    dict_attributs =  [ "title", "body", "severity", "is_enabled", "is_default",
    #"name", 
    ] 

    # standard attibuts
    m = model_to_dict(item, fields=dict_attributs)

    # remove null values
    m2= {}
    for k,v in m.items():
        if v:
            m2[k] = v

    return m2



# -------------------------------------------------
#  EXPORT - Category
# -------------------------------------------------

def category_dict_format(category):

    if not category:
        return

    dict_attributs =  [ "longname", "is_enabled", "description",
    # "name",
    ] 

    # standard attibuts
    m = model_to_dict(category, fields=dict_attributs)

    # remove null values
    m2= {}
    for k,v in m.items():
        if v:
            m2[k] = v

    return m2



# def category_listdict_format(categories):
#     ''' list of  Models to  list of dict '''
#     mylist = []
#     for category in categories:
#         m = category_dict_format(category)
#         mylist.append(m)
#     return mylist



# def category_yaml_response(categories):

#     mystruct = category_listdict_format(categories)
#     data = { 'categories': mystruct}
#     filedata = yaml.dump(data, allow_unicode=True, Dumper=MyYamlDumper, sort_keys=False)
#     response = HttpResponse(filedata, content_type='text/yaml')  
#     response['Content-Disposition'] = 'attachment; filename="sirene_category.yaml"'
#     return response


# # json
# def category_json_response(categories):

#     mystruct = category_listdict_format(categories)
#     data = { 'categories': mystruct}
#     filedata = json.dumps(data, indent=4)
#     response = HttpResponse(filedata, content_type='text/json')  
#     response['Content-Disposition'] = 'attachment; filename="sirene_category.json"'
#     return response

