# (c) cavaliba.com - sirene - export.py



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


def sirene_export_dict(category=True, template=True, public=True):

    datalist = []

    # category
    if category:
        mylist = Category.objects.all()
        for item in mylist:
            m = category_dict_format(item)
            datalist.append(m)

    # publicpages
    if public:
        mylist = PublicPage.objects.all()
        for item in mylist:
            m = publicpage_dict_format(item)
            datalist.append(m)

    # templates
    if template:
        mylist = MessageTemplate.objects.all()
        for item in mylist:
            m = template_dict_format(item)
            datalist.append(m)

    return datalist


#  EXPORT - Templates
def template_dict_format(item):

    if not item:
        return

    dict_attributs =  [  "severity", "title", "body", "description", 
        "is_enabled", "has_publicpage", "has_privatepage", "has_email", "has_sms",
        # "name",
        ] 

    # standard attibuts
    m = model_to_dict(item, fields=dict_attributs)
    m["classname"] = "_sirene_template"
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



#  EXPORT - Public Pages
def publicpage_dict_format(item):

    if not item:
        return

    dict_attributs =  [ "title", "body", "severity", "is_enabled", "is_default",
    #"name", 
    ] 

    # standard attibuts
    m = model_to_dict(item, fields=dict_attributs)
    m["classname"] = "_sirene_public"
    # remove null values
    m2= {}
    for k,v in m.items():
        if v:
            m2[k] = v

    return m2



#  EXPORT - Category
def category_dict_format(category):

    if not category:
        return

    dict_attributs =  [ "longname", "is_enabled", "description",
    # "name",
    ] 

    # standard attibuts
    m = model_to_dict(category, fields=dict_attributs)
    m["classname"] = "_sirene_category"
    # remove null values
    m2= {}
    for k,v in m.items():
        if v:
            m2[k] = v

    return m2

