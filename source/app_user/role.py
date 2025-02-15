# (c) - cavaliba.com - IAM - role.py


import os
from datetime import datetime, timedelta
import time
import base64
import random
import re
import json
import yaml

from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.utils import timezone


from app_home.configuration import get_configuration
from app_home.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL

from .models import SireneUser
from .models import SireneGroup
from .models import SirenePermission
from .forms import RoleForm
from .user import user_get_by_id
from .user import user_get_by_login
from .group import group_get_by_name
from .permission import permission_get_by_name



def role_get_by_id(gid, enabled_only=False):

    if enabled_only:
        return SireneGroup.objects.filter(pk=gid, is_role=True, is_enabled=True)\
            .prefetch_related('users')\
            .prefetch_related('subgroups')\
            .prefetch_related('permissions')\
            .first()
    else:
        return SireneGroup.objects.filter(pk=gid, is_role=True)\
            .prefetch_related('users')\
            .prefetch_related('subgroups')\
            .prefetch_related('permissions')\
            .first()


def role_get_by_name(name, enabled_only=False):

    if enabled_only:
        return SireneGroup.objects.filter(keyname=name, is_role=True, is_enabled=True)\
            .prefetch_related('users')\
            .prefetch_related('subgroups')\
            .prefetch_related('permissions')\
            .first()
    else:
        return SireneGroup.objects.filter(keyname=name, is_role=True)\
            .prefetch_related('users')\
            .prefetch_related('subgroups')\
            .prefetch_related('permissions')\
            .first()


def role_get_by_data(data, enabled_only=False):
    
    keyname = data.get('keyname', None)
    if not keyname:
        return
    return  role_get_by_name(keyname, enabled_only=enabled_only)



# OBJECTS
def role_get_subgroups(role, done=[]):
    ''' Recurse  group Object to get all subgroups Objects'''

    reply = []
    for g in role.subgroups.all():
        if g in done:
            continue
        done.append(g)
        reply.append(g)
        reply += role_get_subgroups(g, done)
        
    reply = list(set(reply))
    return reply



def role_get_form(item=None):

    # blank
    if not item:
        return RoleForm(initial={})

    attributs =  [
        "keyname", "displayname", "description", "is_enabled", "is_builtin", 
        ] 

    initial = {}
    for attrib in attributs:
        try:
            initial[attrib] = getattr(item,attrib, "")
        except:
            pass

    initial["users"] = [i for i in item.users.all()]
    initial["subgroups"] = [i for i in item.subgroups.all()]
    initial["permissions"] = [i for i in item.permissions.all()]

    return RoleForm(initial=initial) 



# ------------------------------------
# expand group(s) objects to users
# Recursive
# ------------------------------------
# OBJECTS
def role_expand_to_users(groups_processed, new_groups):

    reply = []

    if not new_groups:
        return []

    if len(new_groups) == 0:
        return []

    for g in new_groups:

        if g in groups_processed:
            # already done
            continue

        groups_processed.append(g)

        # add all users from group g
        for user in g.users.all():
            reply.append(user)

        # recurse to subgroups 
        for sg in g.subgroups.all():
            subreply = role_expand_to_users(groups_processed, [sg])
            reply += subreply


    # remove duplicate users
    reply = list(set(reply))
    return reply   


def role_init(data):

    keyname = data.get('keyname', None)
    if not keyname:
        return

    entry = role_get_by_name(keyname)
    if entry:
        return entry

    entry = SireneGroup(is_role=True)
    entry = role_update(entry, data)
    return entry


def role_create(data):

    keyname = data.get('keyname', None)
    if not keyname:
        return

    # check if exists as group (not role)
    entry0 = SireneGroup.objects.filter(keyname=keyname, is_role=False).first()
    if entry0:
        return

    # create or update
    entry1 = role_get_by_name(keyname)
    if not entry1:
        entry1 = SireneGroup(is_role=True)

    entry = role_update(entry1, data)

    return entry


def role_update(role, data):
    ''' update Object with data dict info'''

    attributs =  [
        "keyname", "displayname", "is_enabled","description","is_builtin",
    ] 

    # special_attributs = ["users", "subgroups", "permissions"]

    if not data:
        return

    for attrib in attributs:
        if attrib in data:
            try:
                setattr(role, attrib, data[attrib])
            except:
                pass
    role.last_update = timezone.now()
    role.save()


    # users
    if 'users' in data:
        # can be a Queryset (form) or list of login (import)
        role.users.clear()
        if data["users"]:
            for user in data["users"]:
                if type(user) is SireneUser:
                    role.users.add(user)
                else:
                    user2 = user_get_by_login(user)
                    if user2:
                        role.users.add(user2)
        role.last_update = timezone.now()
        role.save()       
    
    # subgroups
    if 'subgroups' in data:
        # can be a Queryset (form) or list of keynames (import)
        role.subgroups.clear()
        if data["subgroups"]:
            for subgroup in data["subgroups"]:
                if type(subgroup) is SireneGroup:
                    role.subgroups.add(subgroup)
                else:
                    # TODO - also get Role ...
                    subgroup2 = group_get_by_name(subgroup)
                    if subgroup2:
                        role.subgroups.add(subgroup2)
        role.last_update = timezone.now()
        role.save()       

    # permissions
    if 'permissions' in data:
        # can be a Queryset (form) or list of keynames (import)
        role.permissions.clear()
        if data["permissions"]:
            for perm in data["permissions"]:
                if type(perm) is SirenePermission:
                    role.permissions.add(perm)
                else:
                    perm2 = permission_get_by_name(perm)
                    if perm2:
                        role.permissions.add(perm2)
        role.last_update = timezone.now()
        role.save()    

    return role



def role_update_by_data(data):

    role = role_get_by_data(data)
    if role:
        return role_update(role, data)


# 0
def role_delete(gobj):

    if not gobj:
        return False

    if gobj.is_builtin:
        return False
    
    if not gobj.is_role:
        return False

    try:
        gobj.delete()
        return True
    except Exception as e:
        print("role_delete failed : ",e)
        return False

# 0
def role_delete_by_id(gid):

    robj = role_get_by_id(gid)
    r = role_delete(robj)
    return robj


# X
def role_delete_by_data(data):

    role = role_get_by_data(data)
    if role:
        return role_delete_by_id(role.id)

# 0
def role_enable_by_data(data):
    role = role_get_by_data(data)
    if role:
        role.is_enabled = True
        role.save()
        return role

# 0
def role_disable_by_data(data):
    role = role_get_by_data(data)
    if role:
        role.is_enabled = False
        role.save()
        return role


# -------------------------------------------------------
# LOADER / IMPORTS
# -------------------------------------------------------
def load_role(datadict=None, verbose=None):

    if not datadict:
        return

    keyname = datadict.get("keyname", None)
    if not keyname: 
        return

    action = datadict.get("_action", "create")

    r = None

    if action == "init":
        # if missing, create
        # if already exists, don't update
        r = role_init(datadict)

    elif action == "create":
        # create and/or update with provided data
        r = role_create(datadict)

    elif action == "update":
        # update only if exists ; don't create
        r = role_update_by_data(datadict)

    elif action == "delete":
        r = role_delete_by_data(datadict)

    elif action == "enable":
        r = role_enable_by_data(datadict)

    elif action == "disable":
        r = role_disable_by_data(datadict)
    else:
        pass

    if r:
        if verbose:
            print(f"role: {action} - {keyname}")

    return r



# -------------------------------------------------------
# EXPORTs
# -------------------------------------------------------

def role_listdict_format(roles):
    ''' list of  Models to  list of dict '''

    dict_attributs =  ["keyname", "displayname", "is_enabled","description" ] 


    datalist = []
    for role in roles:
        m = model_to_dict(role, fields=dict_attributs)
        m["classname"] = "_role"
        # remove null values
        m2= {}
        for k,v in m.items():
            if v:
                m2[k] = v
        # special_attributs = ["subgroups", "users", "permissions"]
        m2["subgroups"]= [i.keyname for i in role.subgroups.all()]
        m2["users"] = [i.login for i in role.users.all()]
        m2["permissions"] = [i.keyname for i in role.permissions.all()]
        datalist.append(m2)

    return datalist


# JSON
def role_json_response(items):

    datalist = role_listdict_format(items)
    filedata = json.dumps(datalist, indent=4, ensure_ascii = False)
    response = HttpResponse(filedata, content_type='text/json')  
    response['Content-Disposition'] = 'attachment; filename="roles.json"'
    return response

# YAML
class MyYamlDumper(yaml.SafeDumper):
    def write_line_break(self, data=None):
        super().write_line_break(data)
        if len(self.indents) < 2:
            super().write_line_break()


def role_yaml_response(items):

    datalist = role_listdict_format(items)
    filedata = yaml.dump(datalist, allow_unicode=True, Dumper=MyYamlDumper, sort_keys=False)
    response = HttpResponse(filedata, content_type='text/yaml')  
    response['Content-Disposition'] = 'attachment; filename="roles.yaml"'
    return response
