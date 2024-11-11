# cavaliba.com

# ---------------------------------------------------------------------
# DataView
# ---------------------------------------------------------------------


import yaml

from .models import DataInstance

from .data import Instance 
from .data import get_instances
from .data import get_instances_raw_json



# ---------------------------------------------------------------------
# Helper
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


def get_dataview_content_by_name(dataview_name):

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
    
    return reply

# -------------------------------------------    
# DataView CLASS
# -------------------------------------------    
class DataView:

    def __init__(self, dataview_name=None):

        self.iobj = None
        self.classname = None
        self.dataview_name = "default_view"
        self.displayname = "Default View"
        self.is_enabled = True
        self.content = { 'columns' : ['keyname', 'displayname','last_update']}


        if not dataview_name:
            self.dataview_name = "Default View"
        
        # use default or DB data_view ?
        instance = Instance(classname="data_view", iname=dataview_name)
        if not instance.is_bound():
            self.dataview_name = "Default View"
            return

        self.iobj = instance.iobj
        self.classname = instance.classname
        self.dataview_name = instance.keyname
        self.displayname = instance.displayname
        self.is_enabled = instance.is_enabled
        try:
            raw = instance.fields["content"].value[0]
        except:
            raw = ""

        try:
            self.content = yaml.safe_load(raw)
        except Exception as e:
            print(f"ERR - can't parse dataview content ({dataview_name}): {e}")
            return



    def get_heads(self):

        reply = []

        heads = self.content.get("columns", ['keyname', 'displayname', 'last_update'])
        for head in heads:
            if type(head) is str:
                reply.append(head)
            elif type(head) is dict:
                for col, operators in head.items():
                    reply.append(col)

        return reply



    def filter(self, instance=None):

        if not instance:
            return

        data = []

        heads = self.content.get("columns", ['keyname', 'displayname', 'last_update'])

        for head in heads:

            if type(head) is str:
                if head == 'keyname':
                    data.append(instance.keyname)
                elif head == 'displayname':
                    data.append(instance.displayname)
                elif head == 'last_update':
                    data.append(instance.last_update)
                else:
                    # existing column
                    if head in instance.fields:
                        datapoint = instance.fields[head].get_datapoint_ui_detail()
                        data.append(datapoint)
                    # computed column
                    else:
                        # Strange : non-existent column but no compute primitive ; add anyway (empty)
                        data.append('')
            elif type(head) is dict:
                datapoint = ''
                for col, operators in head.items():
                    for operator, operator_value in operators.items():
                        if operator == "from":
                            if operator_value in instance.fields:
                                datapoint = instance.fields[operator_value].get_datapoint_ui_detail()
                        else:
                            # TODO / other operators
                            pass
                data.append(datapoint)

            else:
                data.append('')
                
        return data


    def print(self):
        print(f"data_view")
        print(f"    is_enabled:     {self.is_enabled}")
        print(f"    dataview_name:  {self.dataview_name}")
        print(f"    displayname:    {self.displayname}")
        print(f"    iobj:           {self.iobj}")
        print(f"    heads:          {self.get_heads()}")
        print(f"    content:        {self.content}")



