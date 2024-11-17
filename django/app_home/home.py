# app_home - home.py

import os
import re
import yaml
import json
import csv

from .cavaliba import GLOBAL_BUILTIN_DATA

from app_home.configuration import init_configuration
from app_home.configuration import update_configuration

from .configuration_default import CONFIGURATION_DEFAULT
from .models import DashboardApp


import app_home.register as app_home
import app_data.register as app_data
import app_user.register as app_user
import app_sirene.register as app_sirene


from app_data.data import load_data
from app_sirene.load import load_sirene
from app_user.user  import load_users
from app_user.group import load_groups
from app_user.role  import load_roles
from app_user.permission import load_permissions

from app_user.permission import permission_get_by_name


#from app_user.user import user_create
#from app_data.data import get_instance_by_name
from app_data.data import Instance 



from .models import DashboardApp

from .pipeline import get_pipeline
from .pipeline import apply_pipeline

# --------------------------------------------
# Cavaliba Apps
# --------------------------------------------

def get_cavaliba_apps():

    reply = []

    appnames = [ i for i in CONFIGURATION_DEFAULT ]
    for appname in appnames:
        appobj = DashboardApp.objects.filter(keyname=appname).first()
        if appobj:
            reply.append(appobj)

    return reply



def get_app_by_name(appname):
    app = DashboardApp.objects.filter(keyname=appname).first()
    return app



def get_applist(aaa=None):
    '''   filter: enabled + perm = True'''
    
    apps = DashboardApp.objects.all().prefetch_related("permission").order_by("order")

    reply = []

    for app in apps:

        if not app.is_enabled:
            continue
            
        app.is_allowed = False
        try:
            if app.permission.keyname in aaa["perms"]:
                app.is_allowed = True
        except:
            pass

        reply.append(app)
            
    return reply


# --------------------------------------------
# load / init / update
# --------------------------------------------

def cavaliba_init(verbose=True):
    ''' init cavaliba to factory default '''

    init_configuration()

    load_builtin(force_action="init", verbose=verbose)

     


def cavaliba_update(verbose=True):

    update_configuration()

    load_builtin(force_action="init", verbose=verbose)




def load_builtin(force_action="init", verbose=True):
    
    builtins = [
            GLOBAL_BUILTIN_DATA,
            app_user.BUILTIN_DATA,
            app_home.BUILTIN_DATA,
            app_data.BUILTIN_DATA,
            app_sirene.BUILTIN_DATA,
        ]

    # aggregate
    raw = '\n'.join(builtins)
    content = yaml.safe_load(raw)

    # split 
    content_permission = {}
    content_role = {}
    content_group = {}
    content_user = {} 
    content_schema = {}
    content_home = {}
    content_other = {}

    for item,value in content.items():

        if item.startswith("_permission:"):
            content_permission[item] = value

        elif item.startswith("_role:"):
            content_role[item] = value

        elif item.startswith("_group:"):
            content_group[item] = value

        elif item.startswith("_user:"):
            content_user[item] = value

        elif item.startswith("_schema:"):
            content_schema[item] = value

        elif item.startswith("_home:"):
            content_home[item] = value

        else:
            content_other[item] = value


    # load
    r = load_dict(content_permission, force_action=force_action, verbose=verbose)
    r = load_dict(content_role, force_action=force_action, verbose=verbose)
    r = load_dict(content_group, force_action=force_action, verbose=verbose)
    r = load_dict(content_user, force_action=force_action, verbose=verbose)
    r = load_dict(content_schema, force_action=force_action, verbose=verbose)
    r = load_dict(content_home, force_action=force_action, verbose=verbose)
    r = load_dict(content_other, force_action=force_action, verbose=verbose)





# ---------------------------------------------------------------------
# Load broker for one or more objects provided as a DICT
# ---------------------------------------------------------------------
#
# { 
# '_user:LOGIN': {OBJ}
# '_group:GROUPNAME': {OBJ}
# '_role:ROLENAME': {OBJ}
#
# '_schema:CLASSNAME': {OBJ}
# '_static:KEYNAME': {OBJ}
# 'CLASSNAME:KEYNAME:': {OBJ}
#
# '_sirene:TEMPLATENAME': {OBJ}
# '_sirene_public:KEYNAME': {OBJ}
# '_sirene_category:KEYNAME': {OBJ}
#
# '_home': 
#
# -- 
# OBJ:
# _action: create|create_or_update|update|delete|enable|disable
# field: value
# }

def load_dict(data, aaa=None, pipeline=None, force_action=None, verbose=None):


    if not data:
        return
        
    if not type(data) is dict:
        return


    # each loader will pick its keys
    if aaa:

        if 'p_permission_import' in aaa['perms']:
            count = load_permissions(data, force_action=force_action, verbose=verbose)
            print(f"{count} loaded.")

        if 'p_role_import' in aaa['perms']:
            count = load_roles(data, force_action=force_action, verbose=verbose)
            print(f"{count} loaded.")

        if 'p_home_import' in aaa['perms']:
            count = load_home(data, force_action=force_action, verbose=verbose)
            print(f"{count} loaded.")

        if 'p_user_import' in aaa['perms']:
            count = load_users(data, force_action=force_action, verbose=verbose)
            print(f"{count} loaded.")

        if 'p_group_import' in aaa['perms']:
            count = load_groups(data, force_action=force_action, verbose=verbose)
            print(f"{count} loaded.")

        if 'p_data_import' in aaa['perms']:
            count = load_data(data, force_action=force_action, verbose=verbose)
            print(f"{count} loaded.")

        if 'p_sirene_import' in aaa['perms']:
            count = load_sirene(data, force_action=force_action, verbose=verbose)
            print(f"{count} loaded.")

    # CLI / server operation
    else:
        count = load_permissions(data, force_action=force_action, verbose=verbose)
        if count and  count > 0:
            print(f"Loaded: {count} permission objects")
        
        count = load_users(data, force_action=force_action, verbose=verbose)
        if count and  count > 0:
            print(f"Loaded: {count} user objects")

        count = load_home(data, force_action=force_action, verbose=verbose)
        if count and  count > 0:
            print(f"Loaded: {count} home objects")

        count = load_groups(data, force_action=force_action, verbose=verbose)
        if count and  count > 0:
            print(f"Loaded: {count} group objects")

        count = load_roles(data, force_action=force_action, verbose=verbose)
        if count and  count > 0:
            print(f"Loaded: {count} role objects")
        
        count = load_data(data, force_action=force_action, verbose=verbose)
        if count and count > 0:
            print(f"Loaded: {count} data objects")
        
        count = load_sirene(data, force_action=force_action, verbose=verbose)
        if count and  count > 0:
            print(f"Loaded: {count} sirene objects")
    
    return count


# ---------------------------------------------------------------------
# CSV File to DATA
# ---------------------------------------------------------------------

# custom processing of CSV file with header line and composit field
def make_dictlist_from_csv(filedata,  splitfields=[]):

    lines = filedata.splitlines()
    header = []
    rows = []
    line_count = 0

    delimiter = get_configuration(appname="home", keyname="CSV_DELIMITER") 

    for line in lines:
        #print("** ", line)
        entry = {}                    
        fields = line.split(delimiter)
        if line_count == 0:
            header = fields
            line_count = 1
        else:
            line_count += 1
            for i in range(0,len(header)):
                hi = header[i]
                if hi in splitfields:
                    try:
                        a = fields[i].split("+")
                        entry[hi] = a
                    except:
                        pass
                else:
                    try:
                        entry[hi] = fields[i]
                    except:
                        pass
            rows.append(entry)        

    return rows



def load_file_csv_to_data(filename, pipeline=None, classname=None, csv_delimiter=None,  verbose=True):

    ''' CSV filename => dict {} 
        # {
        # _user:login: {}
        # classname:keyname: {}
        # ...
        # }
     '''

    if not os.path.isfile(filename):
        print(f"SKIP - not a file ({filename})")
        return

    if not (filename.endswith('.csv')):
        print(f"SKIP - not a CSV file ({filename})")
        return

    pipeline_data = {}
    if pipeline:
        pipeline_data = get_pipeline(pipeline)
    if not pipeline_data:
        pipeline_data = {}


    if not classname:
        classname = pipeline_data.get("classname", None)
        if not classname:
            print("SKIP - no classname provided")
            return


    if not csv_delimiter:
        csv_delimiter = pipeline_data.get("csv_delimiter", None)
        if not csv_delimiter:
            csv_delimiter = get_configuration(appname="home", keyname="CSV_DELIMITER") 

    data = {}

    with open(filename, encoding="utf-8") as file:

        # NEXT : handle CSV withou header line (use pipeline structure)
        #filedata = file.read().decode("utf-8") 
        #

        csv_reader = csv.DictReader(file, delimiter=csv_delimiter)
        
        for entry in csv_reader:

            key = None

            if classname == "_user":
                keyname = entry.get("login", None)
                if keyname:
                    key = f"_user:{keyname}"
            else:
                keyname = entry.get("keyname", None)                
                if keyname:
                    key = f"{classname}:{keyname}"

            if key:
                data[key] = entry

    return data


# ---------------------------------------------------------------------
# JSON to DATA
# ---------------------------------------------------------------------

def load_file_json_to_data(filename, pipeline=None, verbose=None ):

    data= {}

    if not os.path.isfile(filename):
        print(f"SKIP - not a file ({filename})")
        return

    if not (filename.endswith('.json')):
        print(f"SKIP - not a JSON file ({filename})")
        return

    pipeline_data = {}
    if pipeline:
        pipeline_data = get_pipeline(pipeline)
    if not pipeline_data:
        pipeline_data = {}


    with open(filename) as f:
        data = json.load(f)
        #print(json.dumps(filedata, indent=2))

    if not type(data) is dict:
        print(f"SKIP - invalid JSON, not a dict ({filename})")
        return

    return data

# ---------------------------------------------------------------------
# YAML File to DATA
# ---------------------------------------------------------------------


def load_file_yaml_to_data(filename, pipeline=None, verbose=None ):


    data= {}

    if not os.path.isfile(filename):
        print(f"SKIP - not a file ({filename})")
        return

    if not (filename.endswith('.yml') or filename.endswith('.yaml')):
        print(f"SKIP - not a YAML file ({filename})")
        return

    pipeline_data = {}
    if pipeline:
        pipeline_data = get_pipeline(pipeline)
    if not pipeline_data:
        pipeline_data = {}


    with open(filename) as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
        #print(json.dumps(filedata, indent=2))

    if not type(data) is dict:
        print(f"SKIP - invalid YAML, not a dict ({filename})")
        return

    return data


# ---------------------------------------------------------------------
# HOME data struct
# ---------------------------------------------------------------------
TRUE_LIST = ('on', 'On', 'ON', True, 'yes', 'Yes', 'YES', 'True', 'true', 'TRUE', 1, "1")



def load_home(filedata, force_action=None, verbose=None):

    count = 0

    for item,data in filedata.items():
        if not item.startswith("_home:"):
            continue

        keyname = re.sub("^_home:", '', item)
        if keyname == "":
            continue
        if not data:
            data = {}
        data["keyname"] = keyname

        dbentry = get_app_by_name(keyname)

        action = force_action
        if not action:
            action = data.get("_action", "create")

        if action == "delete":
            if dbentry:
                dbentry.delete()

        elif action == "enable":
            if dbentry:
                dbentry.is_enabled = True
                dbentry.save() 

        elif action == "disable":
            if dbentry:
                dbentry.is_enabled = False
                dbentry.save() 

        elif action == "update":
            if dbentry:
                dbentry.keyname     = keyname
                dbentry.displayname = data.get('displayname', keyname)
                dbentry.description = data.get('description', '')
                dbentry.url  = data.get('url', '/')
                dbentry.icon  = data.get('icon', 'fa-question')
                dbentry.page  = data.get('page', '')
                dbentry.order  = data.get('order', 999)
                dbentry.is_enabled = data.get('is_enabled', True) in TRUE_LIST
                dbentry.save() 

                # permissions
                if "permission" in data:
                    p = data['permission']
                    pobj = permission_get_by_name(p)
                    if pobj:
                        dbentry.permission = pobj
                        dbentry.save() 


        elif action == "create" or (action == "init" and not dbentry):

            if not dbentry:
                dbentry = DashboardApp()

            dbentry.keyname     = keyname
            dbentry.displayname = data.get('displayname', keyname)
            dbentry.description = data.get('description', '')
            dbentry.url  = data.get('url', '/')
            dbentry.icon  = data.get('icon', 'fa-question')
            dbentry.page  = data.get('page', '')
            dbentry.order  = data.get('order', 999)
            dbentry.is_enabled = data.get('is_enabled', True) in TRUE_LIST
            dbentry.save() 

            # permissions
            if "permission" in data:
                p = data['permission']
                pobj = permission_get_by_name(p)
                if pobj:
                    dbentry.permission = pobj
                    dbentry.save() 

        # TODO: update only provided fields and sub-elements (permissions)
        elif action == "append":
            pass

        if dbentry:
            count += 1
            if verbose:
                print(f"dashboard: {action} - {keyname}")


    return count





