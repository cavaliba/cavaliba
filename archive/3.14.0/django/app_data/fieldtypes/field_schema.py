

from .field import Field

from app_data.models import DataClass
from app_data.models import DataInstance

from app_home.configuration import get_configuration

from app_home.cache import cache_classname


def local_get_class_by_name(keyname):

    #dataclass = DataClass.objects.filter(keyname=keyname).first()
    #return dataclass

    global cache_classname
    if not keyname in cache_classname:
        cache_classname[keyname] = DataClass.objects.filter(keyname=keyname).first()
    return cache_classname[keyname]


def local_get_instances(classobj = None, is_enabled=None):
    ''' class keyname => Queryset'''

    #dataclass = get_class_by_name(classname)
    if is_enabled:
        instances = DataInstance.objects.filter(classobj=classobj, is_enabled=is_enabled).select_related('classobj')
    else:
        instances = DataInstance.objects.filter(classobj=classobj).select_related('classobj')
    return instances


def local_get_instances_from_keylist(classobj = None, keylist=[], is_enabled=None):
    ''' class keyname => Queryset'''

    if is_enabled:
        instances = DataInstance.objects.filter(classobj=classobj, keyname__in=keylist, is_enabled=is_enabled).select_related('classobj')
    else:
        instances = DataInstance.objects.filter(classobj=classobj, keyname__in=keylist).select_related('classobj')
    return instances


def local_get_instance_by_name(iname=None, classobj=None, classname=None):
    
    if not classobj:
        classobj = local_get_class_by_name(classname)
    iobj = DataInstance.objects.filter(classobj=classobj, keyname=iname).select_related('classobj').first()
    return iobj

# -------------
#  SCHEMA
# -------------
class FieldSchema(Field):

    def __init__(self, fieldname, fieldschema, alljson):
        super().__init__(fieldname, fieldschema, alljson)

        if not type(self.value) is list:
            self.value = []


    def get_attribute(self):
        ''' returns list of DB obj '''
        # self.value = ["a", "b", ..."]

        reply = []
        classname = self.fieldschema["dataformat_ext"]

        for iname in self.value:
            iobj = local_get_instance_by_name(iname=iname, classname=classname)
            reply.append(iobj)
        return reply


    def get_classname(self):        
        return self.fieldschema["dataformat_ext"]


    def get_datapoint_ui_detail(self):
        ''' 
        Returns list of datapoints [ {}, {}, ...]
        datapoint["value"] = [ { key:, display:, handle:}  , ... ]
        '''
        # self.value = [keyname1, keyname2, ...]

        datapoint = super().get_datapoint_ui_detail()

        datapoint["value"] = []

        classname = datapoint["dataformat_ext"]
        classobj = local_get_class_by_name(classname)
        if not classobj:
            return datapoint
        
        # NEXT : use cache / reverse_propagate & store
        #instances = DataInstance.objects.filter(classobj=classobj, keyname__in=self.value).select_related('classobj')
        instances = DataInstance.objects.filter(classobj=classobj, keyname__in=self.value).values("keyname","displayname","handle")
        for i in instances:
            #item = { "key":i.keyname, "display":i.displayname, "handle": i.handle }
            item = { "key":i["keyname"], "display":i["displayname"], "handle": i["handle"] }
            datapoint["value"].append(item)

        return datapoint        



    def get_datapoint_ui_edit(self):

        # value: [ { 'key':'keyname' , 'selected':True/False }, ...    ]

        datapoint = super().get_datapoint_ui_edit()

        datapoint["value"] = []

        classname = datapoint["dataformat_ext"]
        classobj = local_get_class_by_name(classname)
        if not classobj:
            return datapoint
        count = classobj.datainstance_set.count()

        bigset_size = int(get_configuration("data","DATA_BIGSET_SIZE"))

        if count > bigset_size:
            datapoint["bigset"] = True
        else:
            datapoint["bigset"] = False
            # else False from super().

        # bigset : select items onlty (ajax for the rest)
        if datapoint["bigset"]:
            limited_instances_obj = local_get_instances_from_keylist(classobj=classobj, keylist=self.value, is_enabled=True)
            for i in limited_instances_obj:
                selected = True
                item = { "key":i.keyname, "display":i.displayname, "selected":selected}
                datapoint["value"].append(item)
            # selected = False
            # item = { "key":"test03232", "selected":selected}
            # datapoint["value"].append(item)


        # no bigset : all available and selected items
        else:
            all_instances_obj = local_get_instances(classobj=classobj, is_enabled=True)
            for i in all_instances_obj:
                if i.keyname in self.value:
                    selected = True
                    # item = { "key":i.keyname, "selected":selected}
                    # datapoint["value"].append( item )
                else:
                    selected = False
                item = { "key":i.keyname, "display":i.displayname, "selected":selected }
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