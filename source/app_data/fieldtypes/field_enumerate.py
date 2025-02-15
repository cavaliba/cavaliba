# -------------
# SIRENE STATIC
# -------------

import json 
import yaml 
import copy

from app_home.cavaliba import TRUE_LIST


from .field import Field

from app_data.models import DataClass
from app_data.models import DataInstance

from app_home.configuration import get_configuration

import app_home.cache as cache



widget_map = {
        "red_circle":    "&#x1f534;",
        "orange_circle": "&#x1F7E0;",
        "yellow_circle": "&#x1F7E1;",
        "green_circle":  "&#x1F7E2;",
        "purple_circle": "&#1F7E3;",
        "brown_circle":  "&#1F7E4;",
        "blue_circle":   "&#x1F535;",
        "white_circle":  "&#x25EF;",
        #"black_circle":  "&#11044;",
        #"black_circle":  "&#x25CF;",
        "black_circle":  "&#x2B24;",      # large
        "default" : ""
    }



def get_enumerate(enumname):

    ''' return list of values for enumerate Instance enumname'''
    global widget_map

    # cache
    if enumname in cache.cache_enum:
        a = cache.cache_enum[enumname]
        return copy.deepcopy(a)

    classobj = DataClass.objects.filter(keyname="_enumerate", is_enabled=True).first()
    if not classobj:
        cache.cache_enum[enumname] = None
        return

    enumobj = DataInstance.objects.filter(classobj=classobj, keyname=enumname, is_enabled=True).first()
    if not enumobj:
        cache.cache_enum[enumname] = None
        return

    jsondata = json.loads(enumobj.data_json) 
    rawcontent = jsondata["content"]
    content = yaml.safe_load(rawcontent[0])

    # - classname: _enumerate
    #   keyname: enum_os
    #   is_enabled: True
    #   displayname: "OS Values"
    #   description: "Enumeration of OS"
    #   content: |
    #     - value: "Debian 10"
    #       long: string Debian 10
    #       num: int 1
    #       family: string Linux
    #       widget: green_circle
    #       price: float 9.50
    #       supported: boolean yes
    #     - value: "Win XP"
    #       long: string Windows XP
    #       num: int 2
    #       family: string Windows
    #       widget: red_circle
    #       price: float 99.95
    #       supported: boolean no

   
    # convert Widget to HTML string
    data2 = []
    for entry in content:
        w = entry.get("widget","default")      
        if w.startswith("html"):
            w2 = w[5:]
        else:
            w2 = widget_map.get(w, entry.get("value","") )
        entry["widget"] = w2
        data2.append(entry)

    cache.cache_enum[enumname] = copy.deepcopy(data2)
    return data2
    

   


class FieldEnumerate(Field):

    def __init__(self, fieldname, fieldschema, alljson):

        super().__init__(fieldname, fieldschema, alljson)

        if not type(self.value) is list:
            self.value = []



    def get_datapoint_ui_detail(self):

        datapoint = super().get_datapoint_ui_detail()

        dataformat_ext = self.fieldschema["dataformat_ext"]
        if dataformat_ext in ["string","int","boolean","float"]:
            return datapoint
        
        enum_values = get_enumerate(dataformat_ext)

        if not enum_values:
            return datapoint

        datapoint["value"] = []
        for entry in enum_values:
            if entry["value"] in self.value:
                datapoint["value"].append(entry["value"])

        if len(datapoint["value"]) == 1:
            datapoint["value"] = datapoint["value"][0]
        elif len(datapoint["value"]) > 1:
            datapoint["value"] = ', '.join(datapoint["value"])

        return datapoint   



    def get_datapoint_ui_edit(self):

        datapoint = super().get_datapoint_ui_edit()
    
        dataformat_ext = self.fieldschema["dataformat_ext"]
        if dataformat_ext in ["string","int","boolean","float"]:
            return datapoint
        
        values = get_enumerate(dataformat_ext)

        datapoint["value"] = []

        if not values:
            return datapoint

        for i in values:

            if "is_enabled" in i:
                if not i["is_enabled"]:
                    continue
            if i["value"] in self.value:
                i["selected"] = True
            else:
                i["selected"] = False


            datapoint["value"].append(i)

        return datapoint        




    def get_datapoint_for_export(self):

        if not self.fieldschema["is_multi"]:
            try:
                return self.value[0]
            except:
                # empty
                return ''
        return self.value



    def get_subfields(self):

        enumerate_name = self.fieldschema["dataformat_ext"]
        values = get_enumerate(enumerate_name)

        if not values:
            return {}
        
        if self.fieldschema["is_multi"]:
            return {}

        reply = {}
        for entry in values:
            if entry["value"] in self.value:
                for subkey,subval in entry.items():

                    if subkey == "value":
                        continue
                    v = subval                    

                    if type(subval) is str:

                        if subval.startswith("string"):
                            v = subval[7:]

                        elif subval.startswith("int"):
                            try:
                                v = int(subval[4:])
                            except:
                                v = None
                        elif subval.startswith("float"):
                            try:
                                v = float(subval[6:])
                            except:
                                v = None
                        
                        elif subval.startswith("boolean"):
                            try:
                                v = subval[8:] in TRUE_LIST
                            except:
                                v = False
                        else:
                            v = subval
                    
                    reply[subkey]=v


        #   content: |
        #     - value: "Debian 10"
        #       long: string Debian 10
        #       num: int 1
        #       family: string Linux
        #       widget: green_circle
        #       price: float 9.50
        #       supported: boolean yes
        #     - value: "Win XP"
        #       long: string Windows XP
        #       num: int 2
        #       family: string Windows
        #       widget: red_circle
        #       price: float 99.95
        #       supported: boolean no    

        return reply



    def merge_edit_data(self, data):
        self.value = []
        for i in data:
            if len(i) > 0:
                self.value.append(i)

    def merge_new_data(self, data):
        self.value = []
        for i in data:
            if len(i) > 0:
                self.value.append(i)

    # def get_json(self):
    #     return self.value

    def is_valid(self):
        r = super().is_valid()
        # TODO
        return r