# app_home - load.py

import yaml
import json
# import os
# import re
# import pprint

from app_data.data import Instance 
from app_data.data import get_instances

# ---------------------------------------------------------------------
# Pipelines
# ---------------------------------------------------------------------

def list_pipelines(is_enabled=None):

    pipelines = get_instances(classname = "_pipeline", is_enabled=is_enabled)
    return pipelines


def get_pipeline(pipeline):

    pipeline_data = None

    instance = Instance(classname="_pipeline", iname=pipeline)
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




def apply_pipeline(pipeline=None, datalist=None):
    '''
    data is a list of dict [ {}, {} , ]
    '''

    if not pipeline:
        return datalist

    if not datalist:
        return

    if not type(datalist) is list:
        return

    pipeline_data = get_pipeline(pipeline)

    if not pipeline_data:       
        print(f"No pipeline data for {pipeline}")
        return datalist

    # tasks ?
    if "tasks" not in pipeline_data:
        return datalist

    #for dataname, datadict in data.items():
    for datadict in datalist:
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
                    try:
                        datadict[v2] = datadict[v1]
                    except:
                        datadict[v2] = ""

                if t == "field_rename":
                    (v1,v2) = v
                    try:
                        datadict[v2] = datadict[v1]
                        datadict.pop(v1)
                    #my_dict.pop('key', None)
                    except:
                        datadict[v2] = ""

                if t == "field_delete":
                    try:
                        datadict.pop(v, None)
                    except:
                        pass

                if t == "field_lower":
                    try:
                        datadict[v] = datadict[v].lower()
                    except:
                        pass

                if t == "field_upper":
                    try:
                        datadict[v] = datadict[v].upper()
                    except:
                        pass

    return datalist

