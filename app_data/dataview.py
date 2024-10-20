# cavaliba.com

import yaml
from .data import Instance 
from .data import get_instances
from .data import get_instances_raw_json
# ---------------------------------------------------------------------
# DataView
# ---------------------------------------------------------------------

def get_dataviews_for_class(classname):

    reply = []  
    
    #qs_iobj = get_instances(classname = "data_view", is_enabled=True)
    qs_iobj = get_instances_raw_json(classname='data_view', is_enabled=True, fieldname='classname')
    
    for dv_keyname, dv_classname in qs_iobj.items():
        #print("***** ",dv_keyname, dv_classname, classname)

        if dv_classname[0] == classname:
            reply.append(dv_keyname)

    return reply


def get_dataview(dataview_name):

    reply = None

    instance = Instance(classname="data_view", iname=dataview_name)
    if not instance:
        return

    content = {}
    try:
        content = instance.fields["content"].value[0]
        reply = yaml.safe_load(content)
    except Exception as e:
        print(f"ERR - can't access dataview content ({dataview_name}): {e}")
        return
    
    # if content:
    #     try:
    #         reply = yaml.safe_load(content)
    #     except Exception as e:
    #         print(f"ERR - invalid dataview content ({dataview}): {e}")
    #         return

    return reply