# app_home - load.py

import yaml
import json
import os
import re
import pprint

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

