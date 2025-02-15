# (c) cavaliba.com - data - data.py

import json
import yaml
import copy

from pprint import pprint

from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.utils.translation import gettext as _
from django.utils import timezone


from app_home.configuration import get_configuration
from app_home.cavaliba import TRUE_LIST
import app_home.cache as cache

from .fieldtypes.field_string        import FieldString
from .fieldtypes.field_int           import FieldInt
from .fieldtypes.field_boolean       import FieldBoolean
from .fieldtypes.field_schema        import FieldSchema
from .fieldtypes.field_group         import FieldGroup
from .fieldtypes.field_ipv4          import FieldIPV4
from .fieldtypes.field_float         import FieldFloat
from .fieldtypes.field_date          import FieldDate
from .fieldtypes.field_user          import FieldUser
from .fieldtypes.field_text          import FieldText
from .fieldtypes.field_enumerate     import FieldEnumerate
from .fieldtypes.field_external      import FieldExternal

from .models import DataClass
from .models import DataSchema
from .models import DataInstance

from .handle import update_handle


# -------------------------------------------------------------------------
# Task : bigset/count update
# -------------------------------------------------------------------------
def update_bigset():

    dataclasses = get_classes()

    bigset_size = int(get_configuration("data","DATA_BIGSET_SIZE"))

    for classobj in dataclasses:
        count = classobj.datainstance_set.count()
        classobj.count_estimation = count
        if count > bigset_size:
            classobj.is_bigset = True
            # but no switch back to false
        classobj.save()            
        print(f"update_bigset: class={classobj.keyname} count={classobj.count_estimation} bigset={classobj.is_bigset}")



# -------------------------------------------------------------------------
# Class Helpers
# -------------------------------------------------------------------------

def get_classes(is_enabled=None):

    if is_enabled:
        return DataClass.objects.order_by("order").filter(is_enabled=is_enabled)
    else:
        return DataClass.objects.order_by("order").all()


def get_class_by_name(keyname):
  
    if keyname not in cache.cache_classname:
        obj = DataClass.objects.filter(keyname=keyname).first()
        if obj:
            cache.cache_classname[keyname] = obj
            return obj
    else:
        return cache.cache_classname[keyname]

    # Non-cached version
    #return  DataClass.objects.filter(keyname=keyname).first()




def get_class_by_id(id):

    if not id in cache.cache_classid:
        obj = DataClass.objects.filter(pk=id).first()
        if obj:
            cache.cache_classid[id] = obj
            return obj
    else:
        return cache.cache_classid[id]

    # Non-cached version
    # dataclass = DataClass.objects.filter(pk=id).first()
    # return dataclass


def get_class_obj(cid=None, iid=None, obj=None, classname=None, iname=None):

    ''' get DataClass object depending on input field '''
    
    # order of precedence
    # -------------------
    # cid: PK id DataClass
    # iid: DB pk for DataInstance
    # obj: a DataClass/DataSchema/DataInstance object
    # iname + classname : string w/ keyname value of DataClass  /!\ to be paire with classobj
    # classname : string w/ keyname value of DataClass

    if cid:
        return get_class_by_id(cid)

    if iid:
        iobj = get_instance_by_id(iid)
        if iobj:
            return iobj.classobj

    # obj
    if obj:
        if type(obj) is DataClass:
            return obj
        elif type(obj) is DataSchema:            
            return obj.classobj
        elif type(obj) is DataInstance:
            return obj.classobj
    if iname:
        if not classname:
            # missing classname, needed with instance name
            return
        iobj = get_instance_by_name(classname=classname, iname=iname)
        return iobj.classobj

    if classname:
        classobj = get_class_by_name(classname)
        return classobj 

    return


# -------------------------------------------------------------------------
# Instance Helpers
# -------------------------------------------------------------------------

def get_instances(classname = None, is_enabled=None):
    ''' class keyname => Queryset'''

    dataclass = get_class_by_name(classname)
    if is_enabled:
        instances = DataInstance.objects.filter(classobj=dataclass).select_related('classobj').filter(is_enabled=is_enabled)
    else:
        instances = DataInstance.objects.filter(classobj=dataclass).select_related('classobj')
    return instances


# fast query to select one field value 
# select keyname, fieldname from instance where classname = classname
# select keyname, *         from instance where classname = classname
def get_instances_raw_json(classname = None, is_enabled=True, fieldname = None):
    
    reply = {}

    classobj = get_class_by_name(classname)
    if is_enabled:
        instances = DataInstance.objects.filter(classobj=classobj).filter(is_enabled=is_enabled)
    else:
        instances = DataInstance.objects.filter(classobj=classobj)

    # extract json
    for iobj in instances:
        jsondata = json.loads(iobj.data_json)
        data = jsondata
        # filter ?
        if fieldname:
            if fieldname in jsondata:
                data = jsondata[fieldname]
        reply[iobj.keyname] = data
    return reply


def get_instance_by_id(iid):
    iobj = DataInstance.objects.filter(pk=iid).select_related('classobj').first()
    return iobj


def get_instance_by_name(iname=None, classobj=None, classname=None):
    
    if not classobj:
        classobj = get_class_by_name(classname)
    if not classobj:
        return
    if not iname:
        return
    
    key = f"{classobj.keyname}::{iname}"
    if not key in cache.cache_instance_name:
        obj = DataInstance.objects.filter(classobj=classobj, keyname=iname).select_related('classobj').first()
        if obj:
            cache.cache_instance_name[key] = obj
            return obj
    else:
        return cache.cache_instance_name[key]
    
    # iobj = DataInstance.objects.filter(classobj=classobj, keyname=iname).select_related('classobj').first()
    # return iobj


def get_instance_by_handle(handle=None, classobj=None, classname=None):

    if not classobj:
        classobj = get_class_by_name(classname)
    if not classobj:
        return
    if not handle:
        return 
    iobj= DataInstance.objects.filter(classobj=classobj, handle=handle).first()
    # NEXT / remove : if none, try with keyname
    if not iobj:
        iobj= DataInstance.objects.filter(classobj=classobj, keyname=handle).first()
    
    return iobj


# -------------------------------------------------------------------------
# Schema
# -------------------------------------------------------------------------

def get_schema(cid=None, iid=None, obj=None, classname=None, iname=None):

    # { 
    # 'fieldname':{
    #         'displayname':''
    #         'description':''
    #         'dataformat':''
    #         'dataformat_ext':''
    #         'order':
    #         'cardinal_min':
    #         'cardinal_max':
    #         'is_multi': True/False
    #         'default_value':
    #         'is_computed': False
    #  }, 
    #  ...
    # }
    

    reply_dict = {}

    classobj = get_class_obj(cid=cid, iid=iid, obj=obj, classname=classname, iname=iname)
    if not classobj:
        return {}

    if classobj.keyname in cache.cache_schema:
        return cache.cache_schema[classobj.keyname]

    db_schema = DataSchema.objects.filter(classobj=classobj).select_related('classobj').order_by("order")
    if not db_schema:
        return {}

    # convert to schema_dict !
    dict_attributs =  [ "displayname", "description", "dataformat", "dataformat_ext", "order", "page",
        "cardinal_min","cardinal_max", "default_value"  ]     

    for entry in db_schema:
        m = model_to_dict(entry, fields=dict_attributs)

        if m['cardinal_max'] != 1:
            m['is_multi'] = True
        else:
            m['is_multi'] = False

        # by default schema fields are not computed at schema creation time
        m['is_computed'] = False

        reply_dict[entry.keyname] = m

    cache.cache_schema[classobj.keyname] = copy.deepcopy(reply_dict)
    return reply_dict


def get_field_by_name(classobj, fieldname):

    fieldobj = DataSchema.objects.filter(classobj=classobj, keyname=fieldname).first()
    return fieldobj



# --------------------------------------------------------
# INSTANCE
# --------------------------------------------------------
class Instance:

    def __init__(self, 
                 iobj=None, iid=None, iname=None, handle=None, 
                 classname=None, 
                 classobj=None,
                 schema=None):

        self.iobj = None
        self.classname = None
        self.classobj = None
        self.schema = None
        self.keyname = None
        self.handle = None
        self.is_enabled = None     # True / False
        self.displayname = None
        self.p_read = None
        self.p_update = None
        self.p_delete = None
        self.last_update = None
        self.json = None
        self.fields = {}    # key = field keyname
        self.errors = []

        # store provided structures (no-recompute/requery in DB)
        if schema:
            self.schema = schema

        if classname:
            self.classname = classname

        if classobj:
            self.classobj = classobj
            self.classname = self.classobj.keyname


        # find existing by iobj , if  DataInstance
        if iobj:
            if not type(iobj) is DataInstance:
                return

        # find existing by iid > iname > handle
        if not iobj:
            if iid:
                iobj = get_instance_by_id(iid)
            elif classobj:
                if iname:
                    iobj = get_instance_by_name(iname=iname, classobj=classobj)
                elif handle:
                    iobj = get_instance_by_handle(handle=handle, classobj=classobj)
            elif classname:
                if iname:
                    iobj = get_instance_by_name(iname=iname, classname=classname)
                elif handle:
                    iobj = get_instance_by_handle(handle=handle, classname=classname)

        # if found in DB
        if iobj:
            self.iobj = iobj
            self.keyname = iobj.keyname
            self.handle = iobj.handle
            self.is_enabled = iobj.is_enabled
            self.displayname = iobj.displayname
            self.p_read = iobj.p_read
            self.p_update = iobj.p_update
            self.p_delete = iobj.p_delete
            self.last_update = iobj.last_update
            if not self.classobj:
                self.classobj = iobj.classobj
            if not self.classname:
                #self.classname = iobj.classobj.keyname
                self.classname = self.classobj.keyname
                
            if not self.schema:
                self.schema = get_schema(obj=iobj)
        
        # new emptyInstance : iobj is None
        else:
            self.keyname = iname
            self.is_enabled = True
            self.displayname = None
            self.classname = classname
            if not self.schema:
                self.schema = get_schema(classname=classname)
            # set classobj from classname
            if not self.classobj:
                self.classobj = get_class_by_name(self.classname)
            if self.classobj:
                if not self.classobj.is_enabled:
                    self.classobj = None

        # unpack existing iobj JSON structure     
        if iobj:
            try:
                self.json = json.loads(iobj.data_json)      
            except:
                self.json = ""

        # create fields, and fill with json if available
        for fieldname, fieldschema in self.schema.items():       
            
            if fieldschema["dataformat"] == "string":
                self.fields[fieldname] = FieldString(fieldname, fieldschema, self.json)

            elif fieldschema["dataformat"] == "int":
                self.fields[fieldname] = FieldInt(fieldname, fieldschema, self.json)

            elif fieldschema["dataformat"] == "boolean":
                self.fields[fieldname] = FieldBoolean(fieldname, fieldschema, self.json)

            elif fieldschema["dataformat"] == "schema":
                self.fields[fieldname] = FieldSchema(fieldname, fieldschema, self.json)

            elif fieldschema["dataformat"] == "group":
                self.fields[fieldname] = FieldGroup(fieldname, fieldschema, self.json)

            elif fieldschema["dataformat"] == "ipv4":
                self.fields[fieldname] = FieldIPV4(fieldname, fieldschema, self.json)

            elif fieldschema["dataformat"] == "float":
                self.fields[fieldname] = FieldFloat(fieldname, fieldschema, self.json)

            elif fieldschema["dataformat"] == "date":
                self.fields[fieldname] = FieldDate(fieldname, fieldschema, self.json)

            elif fieldschema["dataformat"] == "user":
                self.fields[fieldname] = FieldUser(fieldname, fieldschema, self.json)

            elif fieldschema["dataformat"] == "text":
                self.fields[fieldname] = FieldText(fieldname, fieldschema, self.json)

            elif fieldschema["dataformat"] == "enumerate":
                self.fields[fieldname] = FieldEnumerate(fieldname, fieldschema, self.json)

            elif fieldschema["dataformat"] == "external":
                self.fields[fieldname] = FieldExternal(fieldname, fieldschema, self.json)

            else:
                self.fields[fieldname] = FieldString(fieldname, fieldschema, self.json)

        # add computed fields 
        self.update_external()
        self.update_enumerate()



    def __str__(self):
        return f"{self.classname}:{self.keyname}"


    def is_bound(self):
        ''' if object from DB in self.iobj '''
        if self.iobj:
            return True
        return False


    def print(self):
   
        print(f"{self.classname}:{self.keyname}")
        print(f"    handle:      {self.handle}")
        print(f"    is_enabled:  {self.is_enabled}")
        print(f"    displayname: {self.displayname}")
        print(f"    iobj:        {self.iobj}")
        print(f"    is_bound:    {self.is_bound()}")
        print(f"    is_valid:    {self.is_valid()}")
        print(f"    p_read:      {self.p_read}")
        print(f"    p_update:    {self.p_update}")
        print(f"    p_delete:    {self.p_delete}")
        print( "    schema:")
        pprint(self.schema)
        for k,v in self.fields.items():
            v.print()
            pprint(v.fieldschema)
            print()
            # print("++ schema ", v.fieldschema)


    def ordered_fields(self):

        def sort_key(item):
            return self.fields[item].fieldschema["order"]
        
        return sorted(self.fields, key = sort_key)
        


    def get_attribute(self, fieldname):
        '''  
        Returns a List []  of attribute value(s) from instance. 
        Convert to obj if FieldSchema  or SireneGroup or User ...
        '''

        if fieldname == "displayname":
            return [self.displayname]

        if fieldname == "keyname":
            return [self.keyname]

        if fieldname == "handle":
            return [self.handle]

        if fieldname == "is_enabled":
            return [self.is_enabled]
        
        if fieldname not in self.schema:
            return

        if fieldname not in self.fields:
            return

        return self.fields[fieldname].get_attribute()



    def get_recursive_content(self, fieldname=None, fieldmember=None, fieldrecurse=None, done=[]):
        ''' get list of fieldname value (object) from 
        - self instance
        - fieldmember *.fieldname
        - recurse on fieldsubgroup : fieldname, member, sub-subgroups ...
        '''

        # Example
        # SiteGroup = { 
        #   sirene_notify =[ SireneGroup1, 2, ...]
        #   + members = [site1, site2] 
        #   + subgroups = [sitegroup1, sitegroup2 ...]
        #}

        # done[] contains list of iobj like self

        reply=[]

        # recursive: already done ?
        if self in done:
            return

        done.append(self)

        # get field values from self
        xlist1 = self.get_attribute(fieldname)
        for z in xlist1:
            if z:
                if z not in done:
                    reply.append(z)
        #reply +=  xlist1

        # get all members from self
        xlist2 = []
        if fieldmember:
            if fieldmember in self.schema:
                if fieldmember in self.fields:
                    xlist2 = self.fields[fieldmember].get_attribute()
        # get field values from members
        for item in xlist2:
            # try to get an instance struct
            # NOTA: won't work on SireneGroup objects ; use SireneGroups for that purpose
            if type(item) is DataInstance:
                instance = Instance(iobj=item)
                if instance:
                    xlist3 = instance.get_attribute(fieldname)
                    for z in xlist3:
                        if z:
                            if z not in done:
                                reply.append(z)

        # get all subgroup (fieldrecurse field content)
        xlist4 = []
        if fieldrecurse:
            if fieldrecurse in self.schema:
                if fieldrecurse in self.fields:
                    xlist4 = self.fields[fieldrecurse].get_attribute()
        # recurse
        for item in xlist4:
            if type(item) is DataInstance:
                if item in done:
                    continue
                instance = Instance(iobj=item)
                if instance:
                    xlist5 = instance.get_recursive_content(
                        fieldname=fieldname,
                        fieldmember=fieldmember,
                        fieldrecurse=fieldrecurse,
                        done=done
                        )
                    for z in xlist5:
                        if z:
                            if z not in done:
                                reply.append(z)
                    #reply += xlist5


        reply = list(set(reply))
        return reply



    # Update External values - recurse to access Origin value at create/update/read time
    # no cache / no write to DB
    def update_external(self):

        for fieldname, fieldschema in self.schema.items():           

            if fieldschema["dataformat"] == "external":
                self.fields[fieldname].value = self.get_external_value(fieldname, fieldschema)


    def get_external_value(self, fieldname, fieldschema):
      
        parent_fieldname = self.fields[fieldname].get_parent_fieldname()
        remote_fieldname = self.fields[fieldname].get_remote_fieldname()

        if not parent_fieldname:
            return []

        if not remote_fieldname:
            return []


        parent_classname = self.fields[parent_fieldname].get_classname()
        if not parent_classname:
            return []
        
        # parent_instance_name
        parent_instance_names = self.fields[parent_fieldname].value
        if type(parent_instance_names) is not list:
            return []
        if len(parent_instance_names) != 1:
            return []
        parent_instance_name = parent_instance_names[0]

        # get Parent Instance
        parent = Instance(classname=parent_classname, iname=parent_instance_name)
        if not parent.iobj:
            return []

        # get parent field value
        return parent.get_attribute(remote_fieldname)



    # Update Enumerate value_ext fields (computed fields)
    def update_enumerate(self):
        
        # remove all enumerate computed fields
        remove = []

        for fieldname in self.fields:

            field = self.fields[fieldname]
            if field.fieldschema["dataformat"] == "enumerate":
                if field.is_computed:
                    remove.append(fieldname)
        
        for v in remove:
            self.fields.pop(v)

        # loop over enumerate fields, identify fields to expand
        expand = []
        for fieldname in self.fields:
            field = self.fields[fieldname]
            if field.fieldschema["dataformat"] != "enumerate":
                continue
            expand.append(fieldname)

        # expand / compute fields
        for fieldname in expand:
            field = self.fields[fieldname]
            subfields = field.get_subfields()
            # { f1:v1, f2:v2 }

            for k,v in subfields.items():
                new_fieldname = fieldname + "__" + k
                self.add_computed_field(new_fieldname, v, field.fieldschema["page"], field.fieldschema["order"])



    def add_computed_field(self, new_fieldname, new_value, page, order):

        new_json = {new_fieldname:[new_value]}
        new_schema = {
            'displayname':new_fieldname, 
            'description':new_fieldname, 
            'is_multi': False,  
            'dataformat': 'enumerate',
            'dataformat_ext': 'string',
            'page': page,
            'order': order,
            }

        if type(new_value) is str:
                new_schema["dataformat_ext"] = "string"
                self.fields[new_fieldname] = FieldString(new_fieldname, new_schema, new_json)

        elif type(new_value) is int:
                new_schema["dataformat_ext"] = "int"
                self.fields[new_fieldname] = FieldInt(new_fieldname, new_schema, new_json)

        elif type(new_value) is bool:
                new_schema["dataformat_ext"] = "boolean"
                self.fields[new_fieldname] = FieldBoolean(new_fieldname, new_schema, new_json)

        elif type(new_value) is float:
                new_schema["dataformat_ext"] = "float"
                self.fields[new_fieldname] = FieldFloat(new_fieldname, new_schema, new_json)


        if new_fieldname in self.fields:
                self.fields[new_fieldname].is_computed = True




    def get_dict_for_ui_detail(self):
        ''' dict suited for list template '''

        # ui = { 
        #   keyname:"xxxx"
        #   displayname:"xxx"
        #   is_enabled:True/False"
        #   "PAGES": {  
        #     "(page)1": { "(order)100": { "attribname":{DATAPOINT}, "attribname":{}, ... }, 
        #                  "(order)101": {... }, ... }, 
        #     "(page)2": { }, 
        #    ... 
        # }
        # DATAPOINT = {
        #     displayname:
        #     description:
        #     VALUE:
        #     label:
        #     dataformat:
        #     dataformat_ext:
        #     widget;
        #     invalid:
        # }
        # VALUE : depend on field dataformat (ex. ", ".join(values)")



        instance_ui = {}

        # SPECIAL fields
        instance_ui["keyname"] = self.keyname
        instance_ui["handle"] = self.handle
        instance_ui["displayname"] = self.displayname
        instance_ui["p_read"] = self.p_read
        instance_ui["p_update"] = self.p_update
        instance_ui["p_delete"] = self.p_delete
        instance_ui["is_enabled"] = self.is_enabled



        # loop over instance.fields
        instance_ui["PAGES"] = {}
        instance_ui["PAGES"]["TEST"] = {}
        instance_ui["PAGES"]["TEST"][1] = []
        for fieldname in self.ordered_fields():
            field = self.fields[fieldname]

            order = field.fieldschema.get("order",1)
            page = field.fieldschema.get("page")
            if not page:
                page = self.keyname

            if page not in instance_ui["PAGES"]:
                instance_ui["PAGES"][page] = {}
            if order not in instance_ui["PAGES"][page]:
                instance_ui["PAGES"][page][order]= []

            datapoint = field.get_datapoint_ui_detail()
            #instance_ui["PAGES"]["TEST"][1].append(datapoint)
            instance_ui["PAGES"][page][order].append(datapoint)

        return instance_ui


    
    def get_dict_for_ui_form(self):
        # used for edit in form : new or edit    
        # ui = { 
        #   keyname:"xxxx"
        #   displayname:"xxx"
        #   is_enabled:True/False"
        #    "PAGES": {  
        #     "(page)1": { "(order)100": { "attribname":{DATAPOINT}, "attribname":{}, ... }, 
        #                  "(order)101": {... }, ... }, 
        #     "(page)2": { }, 
        #    ... 
        # }
        # DATAPOINT = {
        #     displayname:
        #     description:
        #     value:
        #     label:
        #     dataformat:
        #     dataformat_ext:
        #     widget;
        #     invalid:
        #     NEXT: multi, values stuct w/ allowed/checked
        # }
        # value : format depend on dataformat for the field


        # NEXT - merge errors


        instance_ui = {}

        # SPECIAL fields
        instance_ui["keyname"] = self.keyname
        instance_ui["handle"] = self.handle
        instance_ui["displayname"] = self.displayname
        instance_ui["p_read"] = self.p_read
        instance_ui["p_update"] = self.p_update
        instance_ui["p_delete"] = self.p_delete
        instance_ui["is_enabled"] = self.is_enabled


        # loop over instance.fields
        instance_ui["PAGES"] = {}
        for fieldname in self.ordered_fields():
            field = self.fields[fieldname]

            # don't edit computed fields
            if field.is_computed:
                continue

            order = field.fieldschema.get("order",1)
            page = field.fieldschema.get("page")
            if not page:
                page = self.keyname

            if page not in instance_ui["PAGES"]:
                instance_ui["PAGES"][page] = {}
            if order not in instance_ui["PAGES"][page]:
                instance_ui["PAGES"][page][order]= []

            datapoint = self.fields[fieldname].get_datapoint_ui_edit()
            instance_ui["PAGES"][page][order].append(datapoint)

        return instance_ui


    
    def get_dict_for_export(self):
        
        # classname:keyname: { 
        #   displayname:"xxx"
        #   is_enabled:True/False"
        #   "attribname": DATAPOINT, 
        #   "attribname": ... 
        # }

        # DATAPOINT = value / "value"
        # DATAPOINT = ["v1", "v2", ...]

        instance_export = {}

        # SPECIAL fields
        instance_export["classname"] = self.classname
        instance_export["keyname"] = self.keyname
        instance_export["handle"] = self.handle
        instance_export["displayname"] = self.displayname
        instance_export["p_read"] = self.p_read
        instance_export["p_update"] = self.p_update
        instance_export["p_delete"] = self.p_delete
        instance_export["is_enabled"] = self.is_enabled

        for fieldname in self.fields():
            field = self.fields[fieldname]
            datapoint = field.get_datapoint_for_export()
            cardinal, cardinal_min, cardinal_max = field.get_cardinal3()
            if not (cardinal_min == 0 and cardinal == 0):
                instance_export[fieldname] = datapoint

        return instance_export



    def merge_edit_post_request(self, request):
        
        # instance name: no change, not editable

        # handle is external & provided handle ?
        if self.classobj.handle_method == "external":
            if 'handle' in request.POST:
                self.handle = request.POST["handle"]

        # displayname
        self.displayname = request.POST.get("displayname", "")

        # is_enabled
        if "is_enabled" in request.POST:
            self.is_enabled = request.POST["is_enabled"] in TRUE_LIST
        else:
            self.is_enabled = False

        # TODO - check p_* CRUD permission
        if "p_read" in request.POST:
            self.p_read = request.POST["p_read"]
        if "p_update" in request.POST:
            self.p_update = request.POST["p_update"]
        if "p_delete" in request.POST:
            self.p_delete = request.POST["p_delete"]


        for fieldname, fieldschema in self.schema.items():

            # special case : Boolean are not in POST request if False
            postdata = request.POST.getlist(fieldname,default=[])
            self.fields[fieldname].merge_edit_data(postdata)

        # update handle 
        self.handle = update_handle(
            keyname=self.keyname, 
            method=self.classobj.handle_method, 
            current_handle=self.handle)
        
        # update external values
        self.update_external()
        self.update_enumerate()



    def merge_new_post_request(self, request):

        # instance name: no change, not editable
        self.keyname = request.POST.get("keyname", "")
        
        # external handle ?
        if self.classobj.handle_method == "external":
            if 'handle' in request.POST:
                self.handle = request.POST["handle"]

        # displayname (check in is_valid + template auto escaping)
        self.displayname = request.POST.get("displayname", "")

        # is_enabled
        if "is_enabled" in request.POST:
            self.is_enabled = request.POST["is_enabled"] in TRUE_LIST
        else:
            self.is_enabled = False

        # TODO - check p_* CRUD permission
        if "p_read" in request.POST:
            self.p_read = request.POST["p_read"]
        if "p_update" in request.POST:
            self.p_update = request.POST["p_update"]
        if "p_delete" in request.POST:
            self.p_delete = request.POST["p_delete"]


        for fieldname, fieldschema in self.schema.items():

            # special case : Boolean are not in POST request if False
            postdata = request.POST.getlist(fieldname, default=[])
            self.fields[fieldname].merge_new_data(postdata)


        # update handle 
        self.handle = update_handle(
            keyname=self.keyname, 
            method=self.classobj.handle_method, 
            current_handle=self.handle)

        # update external values
        self.update_external()
        self.update_enumerate()



    def merge_import_data(self, data):

        # instance name: mandatory and already loaded at obj creation

        # provided handle ?
        if self.classobj.handle_method == "external":
            if 'handle' in data:
                self.handle = data["handle"]

        # displayname
        if 'displayname' in data:
            self.displayname = data["displayname"]

        # is_enabled
        if "is_enabled" in data:
            self.is_enabled = data["is_enabled"] in TRUE_LIST
        #else:
        #    self.is_enabled = False

        # TODO - check p_* CRUD permission
        if "p_read" in data:
            self.p_read = data["p_read"]
        if "p_update" in data:
            self.p_update = data["p_update"]
        if "p_delete" in data:
            self.p_delete = data["p_delte"]


        for fieldname, fieldschema in self.schema.items():

            # special case : Boolean are not in POST request if False
            if fieldname in data:
                fielddata = data[fieldname] 
                self.fields[fieldname].merge_import_data(fielddata)

        # update handle last
        self.handle = update_handle(
            keyname=self.keyname, 
            method=self.classobj.handle_method, 
            current_handle=self.handle)
        
        # update external values
        self.update_external()
        self.update_enumerate()




    def is_valid(self):

        reply = True

        # keyname
        if not self.keyname:
            self.errors.append(_("missing keyname"))
            return False
        if len(self.keyname) == 0:
            self.errors.append(_("keyname empty"))
            return False

        # handle check
        if not self.handle:
            self.errors.append(_("missing handle"))
            return False
        if len(self.handle)==0:
            self.errors.append(_("empty handle"))
            return False
        # NEXT : unique handle
        # NEXT : handle in slug format

        # classobj
        if not self.classobj:
            self.errors.append(_("missing classobj"))
            return False
        if not self.classname:
            self.errors.append(_("missing classname"))
            return False
        if len(self.classname)==0:
            self.errors.append(_("empty classname"))
            return False
        if self.classobj.keyname != self.classname:
            self.errors.append(_("classname/classobj mismatch"))
            return False
        
        # NEXT : classname exist in DB ?
        # NEXT:  displayname = safe string for display ?

        # is_enabled
        if type(self.is_enabled) is not bool:
            return False

        # NEXT - check permissions ?

        for fieldname, fieldschema in self.schema.items():
            
            r = self.fields[fieldname].is_valid()
            if not r:
                reply = False
                #err = fieldname
                err = fieldschema["displayname"]
                self.errors.append(str(err))
                # NEXT:  use field.errors info

        return reply

    # ACTIONs

    def delete(self):
        if not self.is_bound():
            return False
        try:
            self.iobj.delete()
        except Exception as e:
            print(f"DB delete failed for {self.classname}:{self.keyname} - {e}")
            return False
        return True


    def enable(self):
        if not self.is_bound():
            return False
        self.iobj.is_enabled=True
        try:
            self.iobj.save()
        except Exception as e:
            print(f"DB enable failed for {self.classname}:{self.keyname} - {e}")
            return False
        return True


    def disable(self):
        if not self.is_bound():
            return False
        self.iobj.is_enabled=False
        try:
            self.iobj.save()
        except Exception as e:
            print(f"DB disable failed for {self.classname}:{self.keyname} - {e}")
            return False
        return True


    def update(self):
        ''' update self.iobj with Instance struct , and save'''

        if not self.iobj:
            return False

        self.iobj.keyname = self.keyname
        self.iobj.handle = self.handle
        self.iobj.displayname = self.displayname
        self.iobj.is_enabled = self.is_enabled
        self.iobj.p_read = self.p_read
        self.iobj.p_update = self.p_update
        self.iobj.p_delete = self.p_delete

        # set handle if missing
        self.handle = update_handle(
            keyname=self.keyname, 
            method=self.classobj.handle_method, 
            current_handle=self.handle)
        self.iobj.handle = self.handle

        data = {}

        for fieldname, fieldschema in self.schema.items():

            # don't store external fields (computed fields)
            if self.fields[fieldname].is_computed:
                continue

            field_datalist = self.fields[fieldname].get_json()

            # don't store empty fields in DB
            if len(field_datalist) > 0:
                data[fieldname] = field_datalist

        try:
            self.iobj.data_json = json.dumps(data, indent=2, ensure_ascii=False)
        except:
            print("Invalid JSON in update()")
            return False

        self.save()
        # NEXT - bulk write to DataInstanceSearch for searchable fields
        return True



    def create(self):
        ''' Create new Instance in DB from 'instance' '''

        # already exists in struct?
        if self.iobj:
            self.errors.append(_("create - already created - can't recreate"))
            return False

        # instance already in DB ?
        iobj = get_instance_by_name(iname=self.keyname, classname=self.classname)
        if iobj:
            self.errors.append(_("create - instance already in DB - can't recreate"))
            return False

        # create new instance
        self.iobj = DataInstance()
        self.iobj.classobj = self.classobj
        self.iobj.keyname = self.keyname
        # set handle if not provided externally
        self.handle = update_handle(
            keyname=self.keyname, 
            method=self.classobj.handle_method, 
            current_handle=self.handle)
        self.iobj.handle = self.handle
        
        self.iobj.displayname = self.displayname
        self.iobj.is_enabled = self.is_enabled
        self.iobj.p_read = self.p_read
        self.iobj.p_update = self.p_update
        self.iobj.p_delete = self.p_delete        

        data = {}
        for fieldname, fieldschema in self.schema.items():

            # don't store external fields (computed fields)
            if self.fields[fieldname].is_computed:
                continue

            field_datalist = self.fields[fieldname].get_json()

            # don't store empty fields in DB
            if len(field_datalist) > 0:
                data[fieldname] = field_datalist


        try:
            self.iobj.data_json = json.dumps(data, indent=4)
        except:
            print("Invalid JSON in create()")
            return False

        self.save()
        return True


    def save(self):
        # only place where save() to DB for instances !

        if not self.iobj:
            print("!! no iobj in save()")
            return False

        self.iobj.last_update = timezone.now()

        try:
            self.iobj.save()
        except Exception as e:
            print(f"save() to DB failed: {e}")
            return False
        



# --------------------------------------------------------
# LOADER / IMPORT
# Global LOADER : class, schema, instance, static
# --------------------------------------------------------

def load_schema(datadict=None, verbose=True):

    META = ["displayname", "is_enabled", "icon", "order", "page", "handle_method",
            "p_read", "p_create", "p_update", "p_delete", "p_import", "p_export", "p_admin"
            ]

    if not datadict:
        return

    keyname = datadict.get("keyname", None)
    if not keyname: 
        return

    classobj = load_class_part(keyname, datadict, verbose=verbose)
    if not classobj:
        return

    # fields
    for fieldname, fielddata in datadict.items():
        if fieldname in META:
            continue      
        load_field_definition(classobj, fieldname, fielddata, verbose=verbose)

    return classobj


# loads class definition (fields not loaded here)
def load_class_part(classname, classdata, verbose=True):

    if not type(classname) is str:
        return

    if not type(classdata) is dict:
        return

    if not len(classname)>0: 
        return

    # action = force_action
    # if not action:
    action = classdata.get("_action", "create")

    # No cache, direct access for Load
    classobj = DataClass.objects.filter(keyname=classname).first()

    if action == "delete":
        if classobj:
            classobj.delete()
            if verbose:
                print(f"class delete - {classname}")            
            return classobj
        else:
            if verbose:
                print(f"class delete - {classname} NO FOUND")            
            return


    elif action == "disable":
        if classobj:
            classobj.is_enabled = False
            classobj.save()
            if verbose:
                print(f"class disable - {classname}")            
            return classobj

    elif action == "enable":
        if classobj:
            classobj.is_enabled = True
            classobj.save()
            if verbose:
                print(f"class enable - {classname}")            
            return classobj

    elif action == "update":
        # no creation, see below
        pass

    elif action == "init": 
        # skip if alreay created
        if classobj:
            # return None to skip creating fields
            return classobj
        classobj=DataClass(keyname=classname)
        classobj.save()
        if verbose:
            print(f"class init - {classname}")            

    elif action == "create":
        if not classobj:    
            classobj=DataClass(keyname=classname)
            classobj.save()
            if verbose:
                print(f"class create - {classname}")
    else:
        # unknown action
        if verbose:
            print(f"  !!! unknown action {action} for class {classname}")
        return

    # update for all remaining actions
    # --------------------------------
    if not classobj:
        return

    if "displayname" in classdata:
        classobj.displayname = classdata.get("displayname","")

    if "icon" in classdata:
        classobj.icon = classdata.get("icon")

    if "order" in classdata:
        classobj.order = classdata.get("order",100)

    if "page" in classdata:
        classobj.page = classdata.get("page")

    if "is_enabled" in classdata:
        classobj.is_enabled = classdata.get("is_enabled") in TRUE_LIST

    if "handle_method" in classdata:
        classobj.handle_method = classdata.get("handle_method")

    # update permissions
    # ------------------
    if "p_read" in classdata:
        classobj.p_read = classdata.get("p_read")
    if "p_create" in classdata:
        classobj.p_create = classdata.get("p_create")
    if "p_update" in classdata:
        classobj.p_update = classdata.get("p_update")
    if "p_delete" in classdata:
        classobj.p_delete = classdata.get("p_delete")
    if "p_import" in classdata:
        classobj.p_import = classdata.get("p_import")
    if "p_export" in classdata:
        classobj.p_export = classdata.get("p_export")
    if "p_admin" in classdata:
        classobj.p_admin = classdata.get("p_admin")

    classobj.save()
    if verbose:
        print(f"class update - {classname}")
    return classobj



# load Schema fields in DB
def load_field_definition(classobj, fieldname, fielddata, verbose=True):

    if not classobj:
        return

    if not type(fieldname) is str:
        return

    if not type(fielddata) is dict:
        return

    if not len(fieldname)>0: 
        return

    # action = force_action
    # if not action:
    action = fielddata.get("_action", "create")

    fieldobj = get_field_by_name(classobj, fieldname)

    if action == "delete":
        if fieldobj:
            fieldobj.delete()
            if verbose:
                print(f"  field delete - {classobj.keyname}:{fieldname}")            
            return fieldobj

    elif action == "disable":
        if fieldobj:
            fieldobj.is_enabled = False
            fieldobj.save()
            if verbose:
                print(f"  field disable - {classobj.keyname}:{fieldname}")            
            return fieldobj

    elif action == "enable":

        if fieldobj:
            fieldobj.is_enabled = True
            fieldobj.save()
            if verbose:
                print(f"  field enable - {classobj.keyname}:{fieldname}")            
            return fieldobj

    elif action == "update":
        # no creation, see below for update
        if not fieldobj:
            return

    elif action == "init": 
        # skip if alreay created
        if fieldobj:
            return fieldobj
        fieldobj=DataSchema()
        fieldobj.classobj = classobj
        fieldobj.keyname = fieldname
        fieldobj.save()
        if verbose:
            print(f"  field init - {classobj.keyname}:{fieldname}")            


    elif action == "create":
        if not fieldobj:
            fieldobj=DataSchema()
            fieldobj.classobj = classobj
            fieldobj.keyname = fieldname
            fieldobj.default = fielddata.get("default", "")

            fieldobj.save()
            if verbose:
                print(f"  field create - {classobj.keyname}:{fieldname}")            
    else: 
        # unknown action
        if verbose:
            print(f"  ERR unknown field action: {action} for {classobj.keyname}:{fieldname}")
        return fieldobj


    # update provided params if provided only !
    if not fieldobj:
        return

    if "displayname" in fielddata:
        fieldobj.displayname = fielddata.get("displayname")

    if "description" in fielddata:
        fieldobj.description = fielddata.get("description")

    if "is_enabled" in fielddata:
        fieldobj.is_enabled = fielddata.get("is_enabled") in TRUE_LIST

    if "order" in fielddata:
        fieldobj.order = int( fielddata.get("order") )
    if "page" in fielddata:
        fieldobj.page = fielddata.get("page")

    if "dataformat" in fielddata:
        fieldobj.dataformat = fielddata.get("dataformat")
    if "dataformat_ext" in fielddata:
        fieldobj.dataformat_ext = fielddata.get("dataformat_ext")
    if "default" in fielddata:
        fieldobj.default = fielddata.get("default", "")
    if "cardinal_min" in fielddata:
        fieldobj.cardinal_min = int( fielddata.get("cardinal_min") )
    if "cardinal_max" in fielddata:
        fieldobj.cardinal_max = int( fielddata.get("cardinal_max") )

    fieldobj.save()
    if verbose:
        print(f"  field update - {classobj.keyname}:{fieldname}")
    return fieldobj



def load_instance(datadict=None, verbose=True):

    if not datadict:
        return

    classname = datadict.get("classname", None)
    if not classname: 
        print(f"ERR - missing classname: {datadict}")
        return

    keyname = datadict.get("keyname", None)
    if not keyname: 
        print(f"ERR - missing keyname: {datadict}")
        return

    classobj = get_class_by_name(classname)
    if not classobj:
        print(f"ERR - unknown classname: {classname}:{keyname}")
        return

    classname = classobj.keyname
    schema = get_schema(classname=classname)
    instance = Instance(classname=classname, iname=keyname,  schema=schema)

    if not instance:
        print(f"ERR - couldn't initiate instance for {classname}:{keyname}")
        return

    action = datadict.get("_action", "create")

    if action == "delete":
        if instance.is_bound():
            instance.delete()
            if verbose:
                print(f"instance delete - {classname}:{keyname}")            
            return instance

    elif action == "disable":
        if instance.is_bound():
            instance.disable()
            if verbose:
                print(f"instance disable - {classname}:{keyname}")            
            return instance

    elif action == "enable":
        if instance.is_bound():
            instance.enable()
            if verbose:
                print(f"instance enable - {classname}:{keyname}")            
            return instance

    elif action == "init":
        if instance.is_bound():
            return instance
        instance.create()
        if verbose:
            print(f"instance init - {classname}:{keyname}")            

    elif action == "create":
        if not instance.is_bound():
            instance.create()
            if verbose:
                print(f"instance create - {classname}:{keyname}")            

    elif action == "update":    
        if not instance.is_bound():
            return

    # update
    instance.merge_import_data(datadict)
    instance.update()
    if verbose:
        print(f"instance update - {classname}:{keyname}")

    return instance


# --------------------------------------------------------
#  EXPORT Class/schema structure
# --------------------------------------------------------

def dataclass_listdict_format(classes=None):

    datalist = []

    dict_attributs =  [
        "keyname", "displayname", "is_enabled", 
        "is_bigset", "count_estimation","handle_method",
        "icon","page","order",
        "p_read","p_create","p_update","p_delete","p_export","p_import","p_admin",
        ] 

    if not classes:
        classes = get_classes()

    for classname in classes:

        classobj = get_class_by_name(classname)
        schema = get_schema(classname=classname)

        m = model_to_dict(classobj, fields=dict_attributs)
        m["classname"] = "_schema"

        for fieldname,fieldstruct in schema.items():
            m[fieldname] = fieldstruct

        datalist.append(m)
        
    return datalist


# --------------------------------------------------------
#  EXPORT Instance
# --------------------------------------------------------

def data_listdict_format(classes=None, keyname=None):

    datalist = []

    if not classes:
        classes = get_classes()

    for classname in classes:
        
        schema = get_schema(classname=classname)

        # Queryset of DB objects
        qs_iobj = []
        if keyname:
            a = get_instance_by_name(classname=classname, iname=keyname)
            if a:
                qs_iobj = [a]
        else:   
            qs_iobj =  get_instances(classname = classname)
        

        for iobj in qs_iobj:
            instance = Instance(classname=classname, iobj=iobj,  schema=schema)
            data = instance.get_dict_for_export()            
            datalist.append(data)

    return datalist


#YAML
class MyYamlDumper(yaml.SafeDumper):
    def write_line_break(self, data=None):
        super().write_line_break(data)
        if len(self.indents) < 2:
            super().write_line_break()

def data_yaml_response(classes=None):
    datalist = data_listdict_format(classes=classes)
    filedata = yaml.dump(datalist, allow_unicode=True, Dumper=MyYamlDumper, sort_keys=False)
    response = HttpResponse(filedata, content_type='text/yaml')  
    response['Content-Disposition'] = 'attachment; filename="data.yaml"'
    return response

# JSON
def data_json_response(classes=None):
    datalist = data_listdict_format(classes=classes)
    filedata = json.dumps(datalist, indent=4, ensure_ascii=False)
    response = HttpResponse(filedata, content_type='text/json')  
    response['Content-Disposition'] = 'attachment; filename="data.json"'
    return response
