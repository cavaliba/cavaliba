# -------------
# SIRENE STATIC
# -------------

from .field import Field

from app_data.models import DataClass
from app_data.models import DataInstance
from app_data.models import DataStatic
from app_data.models import DataStaticValue

from app_conf.configuration import get_configuration



class FieldSireneStatic(Field):

    def __init__(self, fieldname, fieldschema, alljson):

        super().__init__(fieldname, fieldschema, alljson)

        if not type(self.value) is list:
            self.value = []


    def get_datapoint_ui_edit(self):

        # value: [ { 'key':'keyname' , 'selected':True/False }, ...    ]

        datapoint = super().get_datapoint_ui_edit()

        datapoint["value"] = []
        staticname = datapoint["dataformat_ext"]
        staticobj = DataStatic.objects.filter(keyname=staticname, is_enabled=True).first()
        if not staticobj:
            return datapoint

        values_obj = DataStaticValue.objects.filter(datastatic=staticobj, is_enabled=True).all()
        for i in values_obj:
            #print("** ", staticname, i)
            if i.value in self.value:
                selected = True
            else:
                selected = False
            item = { "key":i.value, "selected":selected}
            datapoint["value"].append(item)
        #print(datapoint["value"])
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