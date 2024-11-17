# sirene - user.py

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
from django.utils.translation import gettext as _
from django.utils import timezone


# ---

from app_home.configuration import get_configuration

from app_home.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL

from .models import SireneUser
from .models import SireneGroup

from .forms import UserForm

#from .user import load_user



def user_get_form_blank():

    initial = {}
    return UserForm(initial=initial)


def user_get_form(user):

    user_attributs =  [
        "login", "firstname","lastname","displayname","email","mobile",
        "external_id", "is_enabled","description",
        "want_notifications", "want_24", "want_email", "want_sms", 
        "secondary_email", "secondary_mobile"
    ] 


    initial = {}
    for attrib in user_attributs:
        try:
            initial[attrib] = getattr(user,attrib, "")
        except:
            pass

    # groups (helper field, not in model)
    groups = SireneGroup.objects.filter(is_enabled=True, users__in=[user])
    if groups:
        initial["groups"] = [i for i in groups]

    return UserForm(initial=initial) 


# def user_all(is_enabled=None):
#     # prefetch_related('').
#     if is_enabled:
#         return SireneUser.objects.filter(is_enabled=True).all()
#     else:
#         return SireneGroup.objects.all()



def user_get_by_id(userid):
    return SireneUser.objects.filter(pk=userid).first()
    #return SireneUser.objects.prefetch_related('roles__permissions').filter(pk=userid).first()
    ##return  SireneUser.objects.prefetch_related('roles__permissions').filter(login=login, is_enabled=True).first()


def user_get_by_login(login):
    #return SireneUser.objects.prefetch_related('roles__permissions').filter(login=login).first()
    return SireneUser.objects.filter(login=login).first()


def user_get_by_data(data):
    
    login = data.get('login', None)
    if not login:
        return

    return  user_get_by_login(login)


def user_get_email(user=None):

    if not user:
        return

    if user.secondary_email:
        if len(user.secondary_email) > 0:
            return user.secondary_email
    return user.email

def user_get_mobile(user):
    if not user:
        return

    if user.secondary_mobile:
        if len(user.secondary_mobile) > 0:
            return user.secondary_mobile
    return user.mobile


def user_init(data):

    login = data.get('login', None)
    if not login:
        return

    # skip if exists
    entry = user_get_by_login(login)
    if entry:
        return
        
    entry = SireneUser()
    entry = user_update(entry, data)
    return entry


def user_create(data):

    login = data.get('login', None)
    if not login:
        return

    # create or update
    entry1 = user_get_by_login(login)
    if not entry1:
        entry1 = SireneUser()

    entry = user_update(entry1, data)
    return entry


def user_update(user, data):
    ''' update user Object with data dict info'''

    user_attributs =  [
        "login", "firstname","lastname","displayname","email","mobile",
        "external_id", "is_enabled","description",
        "want_notifications", "want_24", "want_email", "want_sms", 
        "secondary_email", "secondary_mobile"
    ] 

    for attrib in user_attributs:
        if attrib in data:
            try:
                setattr(user, attrib, data[attrib])
            except:
                pass

    # save here to create object if new
    user.save()
    
    # groups helper field (not in model)
    if "groups" in data:

        # step 1: remove user from its previous groups
        user.sirenegroup_set.clear()

        # Step 2: add groups
        for gname in data["groups"]:
            #print("*** ", gname)
            gobj = SireneGroup.objects.filter(keyname=gname, is_role=False).first()
            if gobj:
                gobj.users.add(user)
                gobj.save()



    user.last_update = timezone.now()
    user.save()

    return user



def user_update_by_data(data):
    user = user_get_by_data(data)
    if user:
        return user_update(user,data)


# ---
def user_switch(user, is_enabled):
    if user:
        if is_enabled:
            user.is_enabled = True
        else:
            user.is_enabled = False
        user.last_update = timezone.now()
        user.save()
    return user

def user_enable_by_id(userid):
    user = user_get_by_id(userid)
    return user_switch(user, True)

def user_enable_by_data(data):
    user = user_get_by_data(data)
    return user_switch(user, True)


def user_disable_by_id(userid):
    user = user_get_by_id(userid)
    return user_switch(user, False)

def user_disable_by_data(data):
    user = user_get_by_data(data)
    return user_switch(user, False)

# ---

def user_delete(user):
    if user:
        if user.login == "admin":
            # built-in, can't delete ; disable instead
            return
        else:
            user.delete()
        return user        

def user_delete_by_id(userid):
    user = user_get_by_id(userid)
    return user_delete(user)


def user_delete_by_data(data):
    user = user_get_by_data(data)
    return user_delete(user)



# -------------------------------------------------------
# LOADER / IMPORT
# -------------------------------------------------------

def load_users(filedata, force_action=None, verbose=None):

    count = 0
    
    for item,data in filedata.items():

        if not item.startswith("_user:"):
            continue
        login = re.sub("^_user:", '', item)
        if login == "":
            continue
        if not data:
            data = {}
        data["login"] = login

        action = force_action
        if not action:
            action = data.get("_action", "create")

        if action == "init":
            user = user_init(data)

        elif action == "create":
            user = user_create(data)
            user = user_update_by_data(data)

        elif action == "update":
            user = user_update_by_data(data)

        elif action == "delete":
            user = user_delete_by_data(data)

        elif action == "enable":
            user = user_enable_by_data(data)

        elif action == "disable":
            user = user_disable_by_data(data)

        # NEXT : append only provided sub-elements

        else:
            # unknown action
            pass

        if user:
            count += 1
            if verbose:
                print(f"load_user: {action} - {login}")

        if count > 0 and count % 100 == 0:
            print(f"{count} done...")



    return count



def user_import_dictlist(rows):

    line_total = 0
    line_ok = 0

    for rowdict in rows:
        
        line_total += 1
        count = load_users(rowdict)
        line_ok += count

    return line_total, line_ok



def import_json(file):

    filedata = json.load(file) 
    data = filedata.get("users", '')
    line_total, line_ok = user_import_dictlist(data)
    return line_total, line_ok


def import_yaml(file):

    filedata = yaml.load(file, Loader=yaml.SafeLoader)
    data = filedata.get("users", '')
    line_total, line_ok = user_import_dictlist(data)
    return line_total, line_ok


# -------------------------------------------------------
# EXPORTs
# -------------------------------------------------------


def user_csv_response(users):

    csv_attributs =  [
        "login", "firstname","lastname", "displayname", "email","mobile", 
        "external_id", "is_enabled","description",
        "want_notifications", "want_24", "want_email", "want_sms", 
        "secondary_email", "secondary_mobile"
    ] 

    special_attributs = ["site", "roles"]

    delimiter = get_configuration(keyname="CSV_DELIMITER")


    response = HttpResponse(content_type='text/csv')  
    response['Content-Disposition'] = 'attachment; filename="sirene_users.csv"'
    writer = csv.writer(response, delimiter=delimiter)

    headers = []
    for attrib in csv_attributs:
        headers.append(attrib)

    writer.writerow(headers)

    for item in users:
        mye = []

        # standard attributs
        for attrib in csv_attributs:
            if attrib in special_attributs:
                continue;
            myvalue = getattr(item,attrib, "")
            mye.append(myvalue)

        writer.writerow(mye)

    return response


def user_dict_format(user):
    ''' user object to dict {} '''

    dict_attributs =  [
        "login", "firstname","lastname", "displayname", "email","mobile", 
        "external_id", "is_enabled", "description",
        "want_notifications", "want_24", "want_email", "want_sms", 
        "secondary_email", "secondary_mobile"
    ] 

    #special_attributs = ["roles", "site"]
    special_attributs = []

    # standard attibuts
    m = model_to_dict(user, fields=dict_attributs)

    # remove null values
    m2= {}
    for k,v in m.items():
        if v:
            m2[k] = v

    return m2


def user_listdict_format(users):
    ''' users Models to list of dict [ {}, {}, {}, ... ]'''
    mylist = []
    for user in users:
        m = user_dict_format(user)
        mylist.append(m)
    return mylist


# json
def user_json_format(users):
    mystruct = user_listdict_format(users)
    data = { '_user': mystruct}
    return json.dumps(data, indent=4)

def user_json_response(users):
    filedata = user_json_format(users)    
    response = HttpResponse(filedata, content_type='text/json')  
    response['Content-Disposition'] = 'attachment; filename="sirene_users.json"'
    return response

# YAML
class MyYamlDumper(yaml.SafeDumper):
    def write_line_break(self, data=None):
        super().write_line_break(data)
        if len(self.indents) < 3:
            super().write_line_break()


def user_yaml_response(users):

    mystruct = user_listdict_format(users)
    data = { '_user': mystruct}
    filedata = yaml.dump(data, allow_unicode=True, Dumper=MyYamlDumper, sort_keys=False)
    response = HttpResponse(filedata, content_type='text/yaml')  
    response['Content-Disposition'] = 'attachment; filename="sirene_users.yaml"'
    return response

