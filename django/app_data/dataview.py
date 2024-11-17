# cavaliba.com

# ---------------------------------------------------------------------
# DataView
# ---------------------------------------------------------------------


import yaml

from django.utils.translation import gettext as _


from .models import DataInstance

from .data import Instance 
from .data import get_instances
from .data import get_instances_raw_json



# ---------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------
# return a list of available dataview objects available for classname
# [ dataview_keyname1, ... ]


 
def get_dataviews_for_class(classname=None):

    reply = []  

    qs_iobj = get_instances_raw_json(classname='data_view', is_enabled=True, fieldname='classname')
    for dv_keyname, dv_classname in qs_iobj.items():
        if dv_classname[0] == classname:
            reply.append(dv_keyname)

    return reply
# qs_iobj = get_instances_raw_json(classname='data_view', is_enabled=True)
# 'default_dataview': 
#   {'description': ['DataView ....'], 'classname': ['data_view'], 
#   'content': ['columns:\n  - keyname\n  - displayname\n  - classname\n  - last_update']
#   }


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

    def __init__(self, keyname=None):

        self.iobj = None
        self.classname = None
        self.keyname = keyname
        self.displayname = _("Default View")
        self.is_enabled = True
        self.content = { 'columns' : ['keyname', 'displayname','last_update']}
        self.columns = ['keyname', 'displayname','last_update']
        
        if not keyname:
            return
        
        # query data_view Schema for keyname 
        instance = Instance(classname="data_view", iname=keyname)
        if not instance.is_bound():
            return


        self.iobj = instance.iobj
        try:
            self.classname = instance.fields["classname"].value[0]
        except:
            self.classname = None
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

        # Extract columns
        # columns:
        #   - nice name:
        #       from: keyname
        #   - col1
        #   - site:
        #       from: mysitename_col2
        # 
        yaml_columns = self.content.get("columns", None)
        computed_columns = []
        if yaml_columns:
            for head in yaml_columns:
                if type(head) is str:
                    computed_columns.append(head)
                elif type(head) is dict:
                    for col, operators in head.items():
                        computed_columns.append(col)
        self.columns = computed_columns

        # NEXT: if no keyname/displayname , add keyname ?


    def filter(self, instance=None):

        if not instance:
            return

        data = []

        columns_array = self.content.get("columns")
        if not columns_array:
            return
        
        for head in columns_array:
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
                for col, operator_line in head.items():
                    if operator_line:
                        for operator, operator_value in operator_line.items():
                            if operator == "from":
                                if operator_value in instance.fields:
                                    datapoint = instance.fields[operator_value].get_datapoint_ui_detail()
                            else:
                                # NEXT / other operators
                                pass
                data.append(datapoint)

            else:
                data.append('')
                
        return data


    def print(self):
        print(f"data_view")
        print(f"    keyname:        {self.keyname}")
        print(f"    iobj:           {self.iobj}")
        print(f"    classname:      {self.classname}")
        print(f"    is_enabled:     {self.is_enabled}")
        print(f"    displayname:    {self.displayname}")
        print(f"    columns:        {self.columns}")
        print(f"    content:        {self.content}")



