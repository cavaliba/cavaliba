# -------------
# SIRENE STATIC
# -------------

import json 
import yaml 
import copy

from .field import Field

from app_data.models import DataClass
from app_data.models import DataInstance

from app_home.configuration import get_configuration


from app_home.cache import cache_enum



global widget_map
widget_map = {
        "red_circle":    "&#x1f534;",
        "orange_circle": "&#x1F7E0;",
        "yellow_circle": "&#x1F7E1;",
        "green_circle":  "&#x1F7E2;",
        "purple_circle": "&#1F7E3;",
        "brown_circle":  "&#1F7E4;",
        "blue_circle":   "&#x1F535;",
        "white_circle":  "&#x25EF;",
        "black_circle":  "&#11044;",
        "default" : ""
    }



def get_enum_content(enumname):

    # cache
    global cache_enum
    if cache_enum:
        if type(cache_enum) is dict:
            if enumname in cache_enum:
                # hit
                a = cache_enum[enumname]
                return copy.deepcopy(a)
            else:
                # miss
                pass
        else:
            cache_enum = {}
    else:
        cache_enum = {}

    # global_enum[enumname] = None
    # print("**** ", enumname,  global_enum)

    classobj = DataClass.objects.filter(keyname="data_enumerate", is_enabled=True).first()
    if not classobj:
        cache_enum[enumname] = None
        return

    enumobj = DataInstance.objects.filter(classobj=classobj, keyname=enumname, is_enabled=True).first()
    if not enumobj:
        cache_enum[enumname] = None
        return

    jsondata = json.loads(enumobj.data_json) 
    rawdata = jsondata["content"]
    data = yaml.safe_load(rawdata[0])
    
    # [  {} , {},  ...]
    cache_enum[enumname] = copy.deepcopy(data)
    return data
    
    # - value: "A - good"
    #   is_enabled: True
    #   widget: "green_circle"
    #   description: "Use if very good"
    # - value: "B - average"
    #   is_enabled: True
    #   widget: "orange_circle"
    # - value: "C - bad"
    #   is_enabled: True
    #   widget: "red_circle"
    # - value: "n/a"
    #   is_enabled: True
    #   widget: ""
    # - value: "?"
    #   is_enabled: True
    #   widget: "blue_circle"


def convert_widget(values):

    global widget_map

    if not values:
        return

    for entry in values:
        w = entry.get("widget", "default")
        w2 = widget_map.get(w)
        entry["widget"] = w2

    return values



class FieldEnumerate(Field):

    def __init__(self, fieldname, fieldschema, alljson):

        super().__init__(fieldname, fieldschema, alljson)

        if not type(self.value) is list:
            self.value = []


    def get_datapoint_ui_edit(self):

        datapoint = super().get_datapoint_ui_edit()

        datapoint["value"] = []
        values = get_enum_content(datapoint["dataformat_ext"])
        #print(values)
        #[{'value': 'A - good', 'is_enabled': True, 'widget': 'green_box', 'description': 'Use if very good'}, 
        # {'value': 'B - average', 'is_enabled': True, 'widget': 'orange_box'}, 
        # {'value': 'C - bad', 'is_enabled': True, 'widget': 'red_box'}, 
        # {'value': 'n/a', 'is_enabled': True, 'widget': 'empty'}, 
        # {'value': '?', 'is_enabled': True, 'widget': 'grey_circle'}]

        values = convert_widget(values)

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

        #print("****", datapoint["value"])    
        return datapoint        



    def get_datapoint_ui_detail(self):

        datapoint = super().get_datapoint_ui_detail()


        values = get_enum_content(datapoint["dataformat_ext"])
        
        values = convert_widget(values)
        if not values:
            return datapoint

        datapoint["value"] = []
        for i in values:
            if i["value"] in self.value:
                #w2 = convert_widget2(i["widget"])
                datapoint["value"].append(i)

        return datapoint   


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