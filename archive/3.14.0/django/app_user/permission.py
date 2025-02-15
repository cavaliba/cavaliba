# (c) cavaliba.com
# app_user - permission.py

import re
import json
import yaml

from django.http import HttpResponse
from django.forms.models import model_to_dict

from app_home.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL
from .models import SirenePermission



def permission_get_by_id(pid):
    return SirenePermission.objects.filter(pk=pid).first()


def permission_get_by_name(keyname):
    return SirenePermission.objects.filter(keyname=keyname).first()


def permission_get_by_data(data):
    
    keyname = data.get('keyname', None)
    if not keyname:
        return
    return  permission_get_by_name(keyname)




def permission_set(keyname=None, appname=None, displayname=None, description=None, default=False):
    
    ''' create/update a single permission in Database '''

    if not keyname:
        return

    p = permission_get_by_name(keyname)
    if not p:
        p = SirenePermission()
        p.keyname = keyname

    if appname:
        p.appname = appname

    if displayname:
        p.displayname = displayname

    if description:        
        p.description = description

    p.default = default
    p.save()

    return p



def permission_init(data):

    keyname = data.get('keyname', None)
    if not keyname:
        return

    # skip if exists
    entry = permission_get_by_name(keyname)
    if entry:
        return entry

    entry = SirenePermission()
    entry = permission_update(entry, data)

    return entry



def permission_create(data):

    keyname = data.get('keyname', None)
    if not keyname:
        return

    # create or update
    entry = permission_get_by_name(keyname)
    if not entry:
        entry = SirenePermission()

    entry = permission_update(entry, data)

    return entry


def permission_update(iobj, data):
    ''' update Object with data dict info'''

    attributs =  [
        "keyname", "appname", "displayname", "description","is_builtin", "default",
    ] 

    if not iobj:
        return

    if not data:
        return

    for attrib in attributs:
        if attrib in data:
            try:
                setattr(iobj, attrib, data[attrib])
            except:
                pass

    #iobj.last_update = timezone.now()
    iobj.save()
    return iobj


def permission_update_by_data(data):

    iobj = permission_get_by_data(data)
    if iobj:
        return permission_update(iobj, data)



def permission_delete(iobj):

    if not iobj:
        return False

    if iobj.is_builtin:
        return False
    
    try:
        iobj.delete()
        return True
    except Exception as e:
        print("permission_delete failed : ",e)
        return False


def permission_delete_by_id(pid):

    iobj = permission_get_by_id(pid)
    permission_delete(iobj)
    return iobj



def permission_delete_by_data(data):

    iobj = permission_get_by_data(data)
    if iobj:
        return permission_delete_by_id(iobj.id)


# -------------------------------------------------------
# IMPORTS
# -------------------------------------------------------
def load_permission(datadict=None, verbose=None):

    if not datadict:
        return

    keyname = datadict.get("keyname", None)
    if not keyname: 
        return

    action = datadict.get("_action", "create")

    r = None

    if action == "init":
        r = permission_init(datadict)

    elif action == "create":
        r = permission_create(datadict)
        #r = permission_update_by_data(datadict)

    elif action == "update":
        r = permission_update_by_data(datadict)

    elif action == "delete":
        r = permission_delete_by_data(datadict)

    # elif action == "enable":
    #     r = permission_enable_by_data(data)

    # elif action == "disable":
    #     r = permission_disable_by_data(data)
    else:
        pass

    if r:
        if verbose:
            print(f"permission: {action} - {keyname}")
    # else:
    #     print(f"permission action {action} KO")
        
    return r

# -------------------------------------------------------
# EXPORT
# -------------------------------------------------------

def permission_listdict_format(permissions):
    ''' list of  Models to  list of dict '''

    dict_attributs =  ["keyname", "appname", "is_builtin", "default", "displayname", "is_enabled","description" ] 

    datalist = []
    for permission in permissions:
        m = model_to_dict(permission, fields=dict_attributs)
        m["classname"] = "_permission"
        # remove null values
        m2= {}
        for k,v in m.items():
            if v:
                m2[k] = v
        datalist.append(m2)

    return datalist


# JSON
def permission_json_response(items):
    datalist = permission_listdict_format(items)
    filedata = json.dumps(datalist, indent=4, ensure_ascii = False)
    response = HttpResponse(filedata, content_type='text/json')  
    response['Content-Disposition'] = 'attachment; filename="permissions.json"'
    return response

# YAML
class MyYamlDumper(yaml.SafeDumper):
    def write_line_break(self, data=None):
        super().write_line_break(data)
        if len(self.indents) < 2:
            super().write_line_break()


def permission_yaml_response(items):
    datalist = permission_listdict_format(items)
    filedata = yaml.dump(datalist, allow_unicode=True, Dumper=MyYamlDumper, sort_keys=False)
    response = HttpResponse(filedata, content_type='text/yaml')  
    response['Content-Disposition'] = 'attachment; filename="permissions.yaml"'
    return response
