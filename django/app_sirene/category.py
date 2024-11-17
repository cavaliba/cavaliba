# category.py


import os
from datetime import datetime, timedelta
import time
import base64
import random

import csv
import json
import yaml

from django.forms.models import model_to_dict

from app_home.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL
from .models import Category


# -------------------------------------------------------
# category
# -------------------------------------------------------

def category_get_by_name(name):
    return Category.objects.filter(name=name).first()


# -------------------------------------------------------
# # EXPORTs
# # -------------------------------------------------------

# def category_dict_format(category):

#     if not category:
#         return

#     dict_attributs =  [
#         "name", "longname", "is_enabled", "description",
#     ] 

#     #special_attributs = ["permissions"]

#     # standard attibuts
#     m = model_to_dict(category, fields=dict_attributs)

#     # remove null values
#     m2= {}
#     for k,v in m.items():
#         if v:
#             m2[k] = v

#     return m2



# def category_listdict_format(categories):
#     ''' list of  Models to  list of dict '''
#     mylist = []
#     for category in categories:
#         m = category_dict_format(category)
#         mylist.append(m)
#     return mylist


# # json
# def category_json_response(categories):

#     mystruct = category_listdict_format(categories)
#     data = { 'categories': mystruct}
#     filedata = json.dumps(data, indent=4)
#     response = HttpResponse(filedata, content_type='text/json')  
#     response['Content-Disposition'] = 'attachment; filename="sirene_category.json"'
#     return response

# # YAML
# class MyYamlDumper(yaml.SafeDumper):
#     def write_line_break(self, data=None):
#         super().write_line_break(data)
#         if len(self.indents) < 3:
#             super().write_line_break()


# def category_yaml_response(categories):

#     mystruct = category_listdict_format(categories)
#     data = { 'categories': mystruct}
#     filedata = yaml.dump(data, allow_unicode=True, Dumper=MyYamlDumper, sort_keys=False)
#     response = HttpResponse(filedata, content_type='text/yaml')  
#     response['Content-Disposition'] = 'attachment; filename="sirene_category.yaml"'
#     return response

