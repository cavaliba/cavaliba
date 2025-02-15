# (c) cavaliba.com - home - export.py


import json
import yaml

from django.http import HttpResponse
from django.forms.models import model_to_dict

from app_home.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL

from .models import DashboardApp


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

    data = sirene_export_dict()
    filedata = yaml.dump(data, allow_unicode=True, Dumper=MyYamlDumper, sort_keys=False)
    response = HttpResponse(filedata, content_type='text/yaml')  
    response['Content-Disposition'] = 'attachment; filename="sirene.yaml"'
    return response

# json
def full_json_response(categories):

    data = sirene_export_dict()
    filedata = json.dumps(data, indent=4, ensure_ascii = False)
    response = HttpResponse(filedata, content_type='text/json')  
    response['Content-Disposition'] = 'attachment; filename="sirene.json"'
    return response


def home_export_dict(keyname=None):

    datalist = []

    dict_attributs =  ["keyname", "displayname", "is_enabled", "description", 
        "icon","page","url","order"
        ] 
    
    if keyname:
        apps = DashboardApp.objects.filter(keyname=keyname).prefetch_related("permission")
    else:
        apps = DashboardApp.objects.all().prefetch_related("permission").order_by("order")

    for item in apps:
        m = model_to_dict(item, fields=dict_attributs)
        m["classname"] = "_home"
        m["permission"] = item.permission.keyname
        m2= {}
        for k,v in m.items():
            if v:
                m2[k] = v
        datalist.append(m2)
    return datalist



