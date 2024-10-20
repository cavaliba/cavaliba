# app_home - load.py

import yaml
import json
import os
import csv
import pprint

from app_home.models import DashboardApp
from app_home.home import get_app_by_name

from app_user.permission import permission_get_by_name
from app_conf.configuration import get_configuration



# data
from app_data.data import load_data

# sirene
from app_sirene.load import load_sirene

# user
from app_user.load import load_user
from app_user.load import load_user2
from app_user.load import load_group
from app_user.load import load_role

from app_user.user import user_create


from app_data.data import get_instance_by_name
from app_data.data import Instance 


# ---------------------------------------------------------------------
# Pipelines
# ---------------------------------------------------------------------

def get_pipeline(pipeline):

    pipeline_data = None

    instance = Instance(classname="data_pipeline", iname=pipeline)
    if not instance:
        return

    content = {}
    try:
        content = instance.fields["content"].value[0]
    except Exception as e:
        print(f"ERR - can't access pipeline : {e}")
        return
    
    if content:
        try:
            pipeline_data = yaml.safe_load(content)
        except Exception as e:
            print(f"ERR - invalid pipeline content ({pipeline}): {e}")
            return

    # pipeline_data = {
    #     #"csv_delimiter":'|',
    #     #"classname": "_user",
    #     #"force_action": "create",
    #     "tasks": [
    #         {"field_add": "test"},

    #     ]
    # }
    return pipeline_data




def apply_pipeline(pipeline=None, data=None, verbose=None):

    if not pipeline:
        return data

    if not data:
        return

    pipeline_data = get_pipeline(pipeline)


    if not pipeline_data:
        
        print(f"No pipeline data for {pipeline}")
        return data

    if verbose:
        print(f"Pipeline: {pipeline}")
        #print(type(pipeline_data))
        print(json.dumps(pipeline_data, indent=2))




    # tasks ?
    if not "tasks" in pipeline_data:
        return data

    for dataname, datadict in data.items():
        # classname:keyname: => datadict{}
        for task in pipeline_data["tasks"]:
            #print(f"* pipeline task: {task}")
            # dict: taskname: {}
            if not type(task) is dict:
                continue
            for t,v in task.items():
                #print(f"{t} => {v}")

                if t == "field_add":
                    datadict[v] = ""

                if t == "field_copy":
                    (v1,v2) = v
                    datadict[v2] = datadict[v1]

                if t == "field_rename":
                    (v1,v2) = v
                    datadict[v2] = datadict[v1]
                    datadict.pop(v1)
                    #my_dict.pop('key', None)

                if t == "field_delete":
                    datadict.pop(v, None)

                if t == "field_lower":
                    datadict[v] = datadict[v].lower()

                if t == "field_upper":
                    datadict[v] = datadict[v].upper()

    return data

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

        if 'p_user_import' in aaa['perms']:
            count = load_user2(data, force_action=force_action, verbose=verbose)

        if 'p_home_import' in aaa['perms']:
            count = load_home(data)


        if 'p_group_import' in aaa['perms']:
            count = load_group(data)

        if 'p_role_import' in aaa['perms']:
            count = load_role(data)

        if 'p_sirene_import' in aaa['perms']:
            count = load_sirene(data)

        if 'p_data_import' in aaa['perms']:
            count = load_data(data)

    # CLI / server operation
    else:
        count = load_user2(data, force_action=force_action, verbose=verbose)
        #count = load_user(data)
        
        count = load_home(data)
        count = load_group(data)
        count = load_role(data)
        count = load_sirene(data)
        count = load_data(data)
    
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
        print(f"ERR - not a file ({filename}), skipping.")
        return

    if not (filename.endswith('.csv')):
        print(f"ERR - not a CSV file ({filename}), skipping.")
        return

    pipeline_data = {}
    if pipeline:
        pipeline_data = get_pipeline(pipeline)
    if not pipeline_data:
        pipeline_data = {}


    if not classname:
        classname = pipeline_data.get("classname", None)
        if not classname:
            print("ERR - missing classname, skipping.")
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
        print(f"ERR - not a file ({filename}), skipping.")
        return

    if not (filename.endswith('.json')):
        print(f"ERR - not a JSON file ({filename}), skipping.")
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
        print(f"ERR - invalid JSON, not a dict ({filename}), skipping.")
        return

    return data

# ---------------------------------------------------------------------
# YAML File to DATA
# ---------------------------------------------------------------------


def load_file_yaml_to_data(filename, pipeline=None, verbose=None ):


    data= {}

    if not os.path.isfile(filename):
        print(f"ERR - not a file ({filename}), skipping.")
        return

    if not (filename.endswith('.yml') or filename.endswith('.yaml')):
        print(f"ERR - not a YAML file ({filename}), skipping.")
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
        print(f"ERR - invalid YAML, not a dict ({filename}), skipping.")
        return

    return data


# ---------------------------------------------------------------------
# HOME data struct
# ---------------------------------------------------------------------


def load_home(filedata):

    # NEXT: singleton format
    
    if not '_home' in filedata:
        return

    for keyname, data in filedata["_home"].items():

        entry = get_app_by_name(keyname)

        # if delete == true, remove & done!
        must_delete  = data.get('delete', False)
        if must_delete:
            if entry:
                entry.delete()
                print(f"  deleted app {keyname}")
            return


        is_new = False
        if not entry:
            entry = DashboardApp()
            is_new = True

       
        # create / update
        entry.keyname     = keyname
        entry.displayname = data.get('displayname', keyname)
        entry.description = data.get('description', '')
        entry.url  = data.get('url', '/')
        entry.icon  = data.get('icon', 'fa-question')
        entry.page  = data.get('page', '')
        entry.order  = data.get('order', 999)
        entry.state  = data.get('state', 'enabled')
        entry.version  = data.get('version', '1.0')
        entry.save() 

        if is_new:
            print(f"  created app {keyname}")
        else:
            print(f"  updated app {keyname}")


        # permissions
        if "permission" in data:
            p = data['permission']
            pobj = permission_get_by_name(p)
            if pobj:
                entry.permission = pobj
                print(f"    + added access permission {p} to app {entry.keyname}")
            else:
                print(f"    !!err invalid access permission {p} for app {entry.keyname}")

            entry.save() 

    return





