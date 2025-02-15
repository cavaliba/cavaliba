# (c) cavaliba.com
# app_data/loader.py


import os
import re
import yaml
import json
import csv

from app_home.configuration import get_configuration


from app_data.data import load_schema
from app_data.data import load_instance

from app_user.user import load_user
from app_user.permission import load_permission
from app_user.group import load_group
from app_user.role import load_role

from app_home.load import load_home

from app_sirene.load import load_public
from app_sirene.load import load_template
from app_sirene.load import load_category


from app_data.pipeline import get_pipeline
# from .pipeline import apply_pipeline

# ---------------------------------------------------------------------
# Load broker for one or more objects provided as a LIST of DICTs
# ---------------------------------------------------------------------
def load_broker(datalist=None, aaa=None, force_action=None, verbose=False, progress=False):


    if not datalist:
        if verbose:
            print("ERR - load_broker - no data provided")
        return
        
    if not type(datalist) is list:
        print("ERR - load_broker - data provided is not a list")
        return

    if not aaa:
        print("ERR - load_broker - no aaa permission provided")
        return
    
    if 'perms' not in aaa:
        print("ERR - load_broker - invalid aaa permissions")
        return

    count = 0 

    for datadict in datalist:
        
        r = None

        if not type(datadict) is dict:
            print(f"ERR - load_broker - invalid entry: {datadict}")
            continue

        classname = datadict.get("classname", None)
        if not classname:
            # unknown object class : TODO : log error
            print(f"ERR - load_broker - no classname provided for {datadict}")
            continue
        if len(classname) == 0:
            # unknown object class : TODO : log error
            print(f"ERR - load_broker - bad classname provided for {datadict}")
            continue
        
        keyname = datadict.get("keyname", None)
        if not keyname:
            # special (compatibility) with _user
            if classname == "_user":
                login = datadict.get("login", None)
                if login:
                    datadict["keyname"] = login
                else:
                    print(f"ERR - load_broker - no keyname/login for {datadict}")
                    continue
            else:
                print(f"ERR - load_broker - no keyname for {datadict}")
                continue

        if force_action:
            datadict["_action"] = force_action

        if classname == "_user":
            if 'p_user_import' in aaa['perms'] or '*' in aaa['perms']:              
                r = load_user(datadict=datadict, verbose=verbose)

        elif classname == "_group":
            if 'p_group_import' in aaa['perms'] or '*' in aaa['perms']:
                r = load_group(datadict=datadict,verbose=verbose)

        elif classname == "_role":
            if 'p_role_import' in aaa['perms'] or '*' in aaa['perms']:
                r = load_role(datadict=datadict,verbose=verbose)

        elif classname == "_permission":
            if 'p_permission_import' in aaa['perms'] or '*' in aaa['perms']:
                r = load_permission(datadict=datadict,verbose=verbose)            

        elif classname == "_home":
            if 'p_home_import' in aaa['perms'] or '*' in aaa['perms']:              
                r = load_home(datadict=datadict, verbose=verbose)

        elif classname == "_schema":
            if 'p_schema_import' in aaa['perms'] or '*' in aaa['perms']:
                r = load_schema(datadict=datadict, verbose=verbose)

        elif classname == "_sirene_category":
            if 'p_sirene_import' in aaa['perms'] or '*' in aaa['perms']:              
                r = load_category(datadict=datadict, verbose=verbose)

        elif classname == "_sirene_public":
            if 'p_sirene_import' in aaa['perms'] or '*' in aaa['perms']:              
                r = load_public(datadict=datadict, verbose=verbose)

        elif classname == "_sirene_template":
            if 'p_sirene_import' in aaa['perms'] or '*' in aaa['perms']:              
                r = load_template(datadict=datadict, verbose=verbose)

        else:
            # user-defined Instance
            # TODO: check class-level permissions
            if 'p_data_import' in aaa['perms'] or '*' in aaa['perms']:                        
                r = load_instance(datadict=datadict, verbose=verbose)

        if r:
            count += 1
        else:
            print(f"ERR: invalid object or permission: {classname} >> {keyname}")

        if progress:
            if count % 100 == 0:
                print(f"{count} done")


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

def load_file_csv(filename, pipeline=None, first=1, last=0):
    ''' 
    pipeline = keyname of pipeline object

    output: list of dict = [ {} , {}, {} ... ] 
    {
        classname: _home|_user|_group|_role|_permisison|_schema|_enumerate|_dataview|_pipeline| ...
            _sirene_category|_sirene_public|_sirene_template
            CLASSNAME
        keyname: my key
        handle: my-handle
        displayname: "a nice display name"
        is_enabled: 
        (...)
    }
    '''

    if not os.path.isfile(filename):
        print(f"SKIP - not a file ({filename})")
        return

    if not (filename.endswith('.csv')):
        print(f"SKIP - not a CSV file ({filename})")
        return

    if not pipeline:
        print("SKIP - missing pipeline")
        return
    
    pipeline_data = get_pipeline(pipeline)
    if not pipeline_data:
        print("SKIP - invalid pipeline")
        return

    classname = pipeline_data.get("classname", None)
    if not classname:
        print("SKIP - missing classname")
        return

    keyfield = pipeline_data.get("keyfield", None)
    if not keyfield:
        print("SKIP - missing keyfield in pipeline")
        return

    csv_delimiter = pipeline_data.get("csv_delimiter", None)
    if not csv_delimiter:
        csv_delimiter = get_configuration(appname="home", keyname="CSV_DELIMITER")


    datalist = []

    with open(filename, encoding="utf-8") as file:

        # NEXT : handle CSV without header line (use pipeline structure)
        # filedata = file.read().decode("utf-8")

        csv_reader = csv.DictReader(file, delimiter=csv_delimiter)

        cursor = 0

        for entry in csv_reader:

            cursor += 1

            if cursor < first:
                continue

            if last > 0:
                if cursor > last:
                    break

            keyname = entry.get(keyfield, None)                
            if keyname:
                entry["classname"] = classname
                entry["keyname"] = keyname
                datalist.append(entry)

    return datalist

# ---------------------------------------------------------------------
# JSON to DATA
# ---------------------------------------------------------------------

def load_file_json(filename, pipeline=None, verbose=None):

    data = []

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

    if not type(data) is list:
        print(f"SKIP - invalid JSON, not a LIST ({filename})")
        return

    return data

# ---------------------------------------------------------------------
# YAML File to DATA
# ---------------------------------------------------------------------


def load_file_yaml(filename, pipeline=None, verbose=None):


    data = []

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

    if not type(data) is list:
        print(f"SKIP - invalid YAML, not a LIST ({filename})")
        return

    return data

