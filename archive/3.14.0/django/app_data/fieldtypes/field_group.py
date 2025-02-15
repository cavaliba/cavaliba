

from .field import Field

from app_user.group import group_all_filtered
from app_user.group import group_get_by_name

# -------------
# GROUP
# -------------
class FieldGroup(Field):

    def __init__(self, fieldname, fieldschema, alljson):
        super().__init__(fieldname, fieldschema, alljson)

        if not type(self.value) is list:
            self.value = []


    def get_attribute(self):
        ''' return list of SireneGroup '''
        # self.value = ["a", "b", ..."]

        reply = []

        for groupname in self.value:
            groupobj = group_get_by_name(groupname)
            reply.append(groupobj)
        return reply


    def get_datapoint_ui_detail(self):
        
        datapoint = super().get_datapoint_ui_detail()
        try:
            #datapoint["value"] = ', '.join(self.value)
            datapoint["value"] = self.value
        except:
            datapoint["value"] = ''
        return datapoint        


    def get_datapoint_ui_edit(self):

        # value: [ { 'key':'keyname' , 'selected':True/False }, ...    ]

        datapoint = super().get_datapoint_ui_edit()
        datapoint["value"] = self.value
        datapoint["value"] = []

        # classname = datapoint["dataformat_ext"]
        # all_instances_obj = get_instances(classname=classname, is_enabled=True)
        all_instances_obj = group_all_filtered(is_enabled=True)

        for i in all_instances_obj:
            if i.keyname in self.value:
                selected = True
            else:
                selected = False
            item = { "key":i.keyname, "selected":selected}
            datapoint["value"].append( item )

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


    def get_json(self):
        return self.value

    def is_valid(self):
        r = super().is_valid()
        # TODO
        return r