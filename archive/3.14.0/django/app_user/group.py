# cavaliba.com - sirene - app_user - group.py

import os
from datetime import datetime, timedelta
import time
import base64
import random
import re

import csv
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

from .forms import GroupForm

from .user import user_get_by_id
from .user import user_get_by_login

from .permission import permission_get_by_name



def group_get_form(group=None):

    # blank
    if not group:
        return GroupForm(initial={})

    attributs =  [
        "keyname", "displayname", "description", "is_enabled", "is_builtin",
        ] 

    initial = {}
    for attrib in attributs:
        try:
            initial[attrib] = getattr(group,attrib, "")
        except:
            pass

    initial["users"] = [i for i in group.users.all()]
    initial["subgroups"] = [i for i in group.subgroups.all()]
    initial["permissions"] = [i for i in group.permissions.all()]

    return GroupForm(initial=initial) 





def group_all_filtered(is_enabled=None, filter=None):
    # prefetch_related('').
    if is_enabled:
        return SireneGroup.objects.filter(is_enabled=True, is_role=False).all()
    else:
        return SireneGroup.objects.filter(is_role=False).all()

# X
def group_get_by_id(gid):
    # prefetch_related('').
    return SireneGroup.objects.filter(pk=gid, is_role=False).first()

# X
def group_get_by_name(name):
    return SireneGroup.objects.filter(keyname=name, is_role=False).prefetch_related('users').first()

# X
def group_get_by_data(data):
    
    keyname = data.get('keyname', None)
    if not keyname:
        return
    return  group_get_by_name(keyname)



# OBJECTS
def group_get_subgroups(group, done=[]):
    ''' Recurse  group Object to get all subgroups Objects'''

    reply = []
    for g in group.subgroups.all():
        if g in done:
            continue
        done.append(g)
        reply.append(g)
        reply += group_get_subgroups(g, done)
        
    reply = list(set(reply))
    return reply


# ------------------------------------
# expand group(s) objects to users
# Recursive
# ------------------------------------
# OBJECTS
def group_expand_to_users(groups_processed, new_groups):

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
            subreply = group_expand_to_users(groups_processed, [sg])
            reply += subreply

    # remove duplicate users
    reply = list(set(reply))
    return reply   



# def group_register_builtin(appname, data):

#     if not appname:
#         return False

#     for gname, gdata in data.items():
        
#         # already exists ?
#         gobj = group_get_by_name(gname)
#         if not gobj:
#             gobj = SireneGroup()
#         gobj.is_builtin = True
#         gobj.is_role = False
#         gobj.is_enabled = True
#         gobj.keyname = gname
#         gobj.displayname = f"{appname} {gname} built-in group"
#         gobj.description = f"Built-in User Group for {appname}"
#         gobj.save()

#         for perm in gdata:
#             pobj = permission_get_by_name(perm)
#             if pobj:
#                 gobj.permissions.add(pobj)
        
#         gobj.last_update = timezone.now()
#         gobj.save()
#         #print(f"Registered built-in User Group {gname} for app {appname}")

#     return True



def group_init(data):

    keyname = data.get('keyname', None)
    if not keyname:
        return

    # check if exists as role (not group)
    entry0 = SireneGroup.objects.filter(keyname=keyname, is_role=True).first()
    if entry0:
        return

    # skip if exists
    entry = group_get_by_name(keyname)
    if entry:
        return entry

    entry = SireneGroup(is_role=False)
    entry = group_update(entry, data)

    return entry


def group_create(data):

    keyname = data.get('keyname', None)
    if not keyname:
        return

    # check if exists as role (not group)
    entry0 = SireneGroup.objects.filter(keyname=keyname, is_role=True).first()
    if entry0:
        return

    # create or update
    entry1 = group_get_by_name(keyname)
    if not entry1:
        entry1 = SireneGroup(is_role=False)

    entry = group_update(entry1, data)

    return entry


def group_update(group, data):
    ''' update Object with data dict info'''

    attributs =  [
        "keyname", "displayname", "is_enabled","description",
    ] 

    special_attributs = ["users", "subgroups", "permissions"]


    if not data:
        return

    for attrib in attributs:
        if attrib in data:
            try:
                setattr(group, attrib, data[attrib])
            except:
                pass
    
    group.last_update = timezone.now()
    group.save()


    # users
    if 'users' in data:
        # can be a Queryset (form) or list of login (import)
        group.users.clear()
        if data["users"]:
            for user in data["users"]:
                if type(user) is SireneUser:
                    group.users.add(user)
                else:
                    user2 = user_get_by_login(user)
                    if user2:
                        group.users.add(user2)
        group.last_update = timezone.now()                        
        group.save()       
    
    # subgroups
    if 'subgroups' in data:
        # can be a Queryset (form) or list of keynames (import)
        group.subgroups.clear()
        if data["subgroups"]:
            for subgroup in data["subgroups"]:
                if type(subgroup) is SireneGroup:
                    group.subgroups.add(subgroup)
                else:
                    subgroup2 = group_get_by_name(subgroup)
                    if subgroup2:
                        group.subgroups.add(subgroup2)
        group.last_update = timezone.now()
        group.save()       

    # NO permissions in groups ; use Role (groups w/ is_role=True)
    # if 'permissions' in data:
    #     # can be a Queryset (form) or list of keynames (import)
    #     group.permissions.clear()
    #     for perm in data["permissions"]:
    #         if type(perm) is SirenePermission:
    #             group.permissions.add(perm)
    #         else:
    #             perm2 = permission_get_by_name(perm)
    #             if perm2:
    #                 group.permissions.add(perm2)
    #     group.save()    

    return group



def group_update_by_data(data):

    group = group_get_by_data(data)
    if group:
        return group_update(group, data)


# X
def group_delete(gobj):

    if not gobj:
        return False

    if gobj.is_builtin:
        return False

    if gobj.is_role:
        return False
    
    try:
        gobj.delete()
        return True
    except Exception as e:
        print("group_delete failed : ",e)
        return False

# X
def group_delete_by_id(gid):

    gobj = group_get_by_id(gid)
    r = group_delete(gobj)
    return gobj


# X
def group_delete_by_data(data):

    group = group_get_by_data(data)
    if group:
        return group_delete_by_id(group.id)

# 0
def group_enable_by_data(data):
    group = group_get_by_data(data)
    if group:
        group.is_enabled = True
        group.save()
        return group

# 0
def group_disable_by_data(data):
    group = group_get_by_data(data)
    if group:
        group.is_enabled = False
        group.save()
        return group
    
# -------------------------------------------------------
# IMPORTS
# -------------------------------------------------------
#def load_groups(filedata, force_action=None, verbose=None):
def load_group(datadict=None, verbose=None):

    if not datadict:
        return

    keyname = datadict.get("keyname", None)
    if not keyname: 
        return

    action = datadict.get("_action", "create")

    r = None

    if action == "init":
        # create/update only if not already exists
        r = group_init(datadict)

    elif action == "create":
        # create and/or update
        r = group_create(datadict)
        #r = group_update_by_data(datadict)

    elif action == "update":
        # update only if exists
        r = group_update_by_data(datadict)

    elif action == "delete":
        r = group_delete_by_data(datadict)

    elif action == "enable":
        r = group_enable_by_data(datadict)

    elif action == "disable":
        r = group_disable_by_data(datadict)
    else:
        pass

    if r:
        if verbose:
            print(f"group: {action} - {keyname}")

    return r


# -------------------------------------------------------
# EXPORTs
# -------------------------------------------------------



def group_listdict_format(groups):
    ''' groups to listdict = [ {}, {} .. ] '''

    dict_attributs =  ["keyname", "displayname", "is_enabled","description"] 

    datalist = []
    for group in groups:
        m = model_to_dict(group, fields=dict_attributs)
        m["classname"] = "_group"
        # remove null values
        m2= {}
        for k,v in m.items():
            if v:
                m2[k] = v
        m2["subgroups"]= [i.keyname for i in group.subgroups.all()]
        m2["users"] = [i.login for i in group.users.all()]
        #m2["permissions"] = [i.keyname for i in group.permissions.all()]
        datalist.append(m2)

    return datalist


# JSON
def group_json_response(groups):
    datalist = group_listdict_format(groups)
    filedata = json.dumps(datalist, indent=4, ensure_ascii = False)
    response = HttpResponse(filedata, content_type='text/json')  
    response['Content-Disposition'] = 'attachment; filename="groups.json"'
    return response

# YAML
class MyYamlDumper(yaml.SafeDumper):
    def write_line_break(self, data=None):
        super().write_line_break(data)
        if len(self.indents) < 2:
            super().write_line_break()

def group_yaml_response(groups):
    datalist = group_listdict_format(groups)
    filedata = yaml.dump(datalist, allow_unicode=True, Dumper=MyYamlDumper, sort_keys=False)
    response = HttpResponse(filedata, content_type='text/yaml')  
    response['Content-Disposition'] = 'attachment; filename="groups.yaml"'
    return response


# CSV
def group_csv_response(groups):

    csv_attributs =  [
        "classname", "keyname", "displayname", "is_enabled","description","users", "subgroups",
    ] 

    special_attributs = ["classname", "users", "subgroups","permissions"]

    delimiter = get_configuration(keyname="CSV_DELIMITER")

    response = HttpResponse(content_type='text/csv')  
    response['Content-Disposition'] = 'attachment; filename="groups.csv"'
    writer = csv.writer(response, delimiter=delimiter)

    # headers = []
    # for attrib in csv_attributs:
    #     headers.append(attrib)

    writer.writerow(csv_attributs)

    for item in groups:
        mye = ["_group"]
        # standard attributs
        for attrib in csv_attributs:
            if attrib in special_attributs:
                continue
            myvalue = getattr(item,attrib, "")
            mye.append(myvalue)


        # users - special attribut
        mystr = '+'.join([i.login for i in item.users.all()])
        mye.append(mystr)

        # subgroups - special attribut
        mystr = '+'.join([i.keyname for i in item.subgroups.all()])
        mye.append(mystr)

        # NO permissions directly in groups ; use Roles
        # permissions - special attribut
        # mystr = '+'.join([i.keyname for i in item.permissions.all()])
        # mye.append(mystr)


        writer.writerow(mye)

    return response

