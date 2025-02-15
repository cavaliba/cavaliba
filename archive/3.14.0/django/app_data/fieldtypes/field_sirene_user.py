# Cavaliba / Field type sirene_user

from .field import Field

from app_home.configuration import get_configuration

from app_user.models import SireneUser

#from app_user.user import user_all
from app_user.user import user_get_by_login

# -------------
# SIRENE GROUP
# -------------
class FieldSireneUser(Field):

    def __init__(self, fieldname, fieldschema, alljson):
        super().__init__(fieldname, fieldschema, alljson)

        if not type(self.value) is list:
            self.value = []


    def get_attribute(self):
        ''' return list of SireneGroup '''
        # self.value = ["a", "b", ..."]

        reply = []

        for login in self.value:
            userobj = user_get_by_login(login)
            reply.append(userobj)
        return reply



    def get_datapoint_ui_detail(self):

        datapoint = super().get_datapoint_ui_detail()

        datapoint["value"] = []
        # for i in self.value:
        #     if len(i) > 0:
        #         datapoint["value"].append(i)

        users = SireneUser.objects.filter(login__in=self.value, is_enabled=True)
        for i in users:
            item = { "key":i.login, "display":i.displayname }
            datapoint["value"].append(item)

        return datapoint        



    def get_datapoint_ui_edit(self):

        # value: [ { 'key':'keyname' , 'selected':True/False }, ...    ]

        datapoint = super().get_datapoint_ui_edit()

        datapoint["value"] = []
    
        count = SireneUser.objects.count()
        bigset_size = int(get_configuration("data","DATA_BIGSET_SIZE"))
        if count > bigset_size:
            datapoint["bigset"] = True
        else:
            datapoint["bigset"] = False

        # NEW: always bigset now
        datapoint["bigset"] = True

        # bigset : select items only (ajax for the rest)
        if datapoint["bigset"]:

            users = SireneUser.objects.filter(login__in=self.value, is_enabled=True)
            for i in users:
                selected = True
                item = { "key":i.login, "display":i.displayname, "selected":selected}
                datapoint["value"].append(item)

        # DISABLED : bigset for SireneUser
        # # # no bigset : all available and selected items
        # else:
        #     #all_instances_obj = user_all(is_enabled=True)
        #     all_instances_obj = SireneUser.objects.filter(is_enabled=True)
        #     for i in all_instances_obj:
        #         select = False
        #         if i.login in self.value:
        #             selected = True
        #         item = { "key":i.login, "display":i.displayname, "selected":selected }
        #         datapoint["value"].append( item )

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