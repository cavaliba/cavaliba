# cavaliba.com - app_user - role.py


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



# def role_all_filtered(is_enabled=None, filter=None):

#     if is_enabled:
#         return SireneGroup.objects.filter(is_enabled=True, is_role=True)\
#             .all()
#     else:
#         return SireneGroup.objects.filter(is_role=True)\
#             .all()        


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



# def role_register_builtin(appname, data):

#     if not appname:
#         return False

#     for gname, gdata in data.items():
        
#         # already exists ?
#         gobj = role_get_by_name(gname)
#         if not gobj:
#             gobj = SireneGroup()
#         gobj.is_builtin = True
#         gobj.is_role = True
#         gobj.is_enabled = True
#         gobj.keyname = gname
#         gobj.displayname = f"{appname} {gname} built-in role"
#         gobj.description = f"Built-in Role for {appname}"
#         gobj.save()

#         for perm in gdata:
#             pobj = permission_get_by_name(perm)
#             if pobj:
#                 gobj.permissions.add(pobj)

#         gobj.last_update = timezone.now()
#         gobj.save()
#         #print(f"Registered built-in Role {gname} for app {appname}")

#     return True


def role_init(data):

    keyname = data.get('keyname', None)
    if not keyname:
        return

    entry = role_get_by_name(keyname)
    if entry:
        return

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

    special_attributs = ["users", "subgroups", "permissions"]

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


# -------------------------------------------------------
# LOADER / IMPORTS
# -------------------------------------------------------
def load_roles(filedata, force_action=None, verbose=None):

    count = 0

    # _role:rolename: {}
    for item,data in filedata.items():
        if not item.startswith("_role:"):
            continue

        keyname = re.sub("^_role:", '', item)
        if keyname == "":
            continue
        if not data:
            data = {}
        data["keyname"] = keyname

        action = force_action
        if not action:
            action = data.get("_action", "create")

        if action == "init":
            role = role_init(data)

        elif action == "create":
            role = role_create(data)
            role = role_update_by_data(data)

        elif action == "update":
            role = role_update_by_data(data)

        elif action == "delete":
            role = role_delete_by_data(data)

        elif action == "enable":
            role = role_enable_by_data(data)

        elif action == "disable":
            role = role_disable_by_data(data)
        else:
            pass

        if role:
            count += 1
            if verbose:
                print(f"role: {action} - {keyname}")

    return count



def role_import_dictlist(rows):

    line_total = 0
    line_ok = 0

    for rowdict in rows:
        
        
        line_total += 1
        count = load_roles(rowdict)
        line_ok += count

    return line_total, line_ok



def role_import_json(file):

    filedata = json.load(file) 

    data = filedata.get("_role", '')
    line_total1, line_ok1 = role_import_dictlist(data)

    return line_total1, line_ok1


def role_import_yaml(file):

    filedata = yaml.load(file, Loader=yaml.SafeLoader)

    data = filedata.get("_role", '')
    line_total1, line_ok1 = role_import_dictlist(data)
    
    return line_total1, line_ok1


# -------------------------------------------------------
# EXPORTs
# -------------------------------------------------------


def role_dict_format(role):

    dict_attributs =  [
        "keyname", "displayname", "is_enabled","description",
    ] 


    # standard attibuts
    m = model_to_dict(role, fields=dict_attributs)

    # remove null values
    m2= {}
    for k,v in m.items():
        if v:
            m2[k] = v

    # special_attributs = ["subgroups", "users", "permissions"]
    m2["subgroups"]= [i.keyname for i in role.subgroups.all()]
    m2["users"] = [i.login for i in role.users.all()]
    m2["permissions"] = [i.keyname for i in role.permissions.all()]

    return m2


def role_listdict_format(items):
    ''' list of  Models to  list of dict '''
    mylist = []
    for item in items:
        m = role_dict_format(item)
        mylist.append(m)
    return mylist


# json
def role_json_response(items):

    mystruct = role_listdict_format(items)
    data = { '_role': mystruct}
    filedata = json.dumps(data, indent=4)
    response = HttpResponse(filedata, content_type='text/json')  
    response['Content-Disposition'] = 'attachment; filename="sirene_roles.json"'
    return response

# YAML
class MyYamlDumper(yaml.SafeDumper):
    def write_line_break(self, data=None):
        super().write_line_break(data)
        if len(self.indents) < 3:
            super().write_line_break()


def role_yaml_response(items):

    mystruct = role_listdict_format(items)
    data = { '_role': mystruct}
    filedata = yaml.dump(data, allow_unicode=True, Dumper=MyYamlDumper, sort_keys=False)
    response = HttpResponse(filedata, content_type='text/yaml')  
    response['Content-Disposition'] = 'attachment; filename="sirene_roles.yaml"'
    return response
