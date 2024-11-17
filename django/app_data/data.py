# app_data - data.py


import csv
import json
import yaml
import re

from pprint import pprint

from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.utils.translation import gettext as _
from django.utils import timezone


from app_home.configuration import get_configuration
from app_home.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL

from app_user.group import group_all_filtered
from app_user.group import group_create
from app_user.group import group_get_by_name
from app_user.role import role_get_by_name


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

from .models import DataClass
from .models import DataSchema
from .models import DataInstance
# from .models import DataStatic
# from .models import DataStaticValue


TRUE_LIST = ('on', 'On', 'ON', True, 'yes', 'Yes', 'YES', 'True', 'true', 'TRUE', 1, "1")

# -------------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------------

def get_classes():

    dataclass = DataClass.objects.order_by("order").all()
    return dataclass


def get_class_by_name(keyname):

    dataclass = DataClass.objects.filter(keyname=keyname).first()
    return dataclass


def get_class_by_id(id):

    dataclass = DataClass.objects.filter(pk=id).first()
    return dataclass


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
    iobj = DataInstance.objects.filter(classobj=classobj, keyname=iname).select_related('classobj').first()
    return iobj


def get_field_by_name(classobj, fieldname):

    fieldobj = DataSchema.objects.filter(classobj=classobj, keyname=fieldname).first()
    return fieldobj





def get_schema(cid=None, iid=None, obj=None, classname=None, iname=None):
    ''' dict  + __ordered filled with ordered schema as []'''

    # { 
    #  "__classname":string
    #  "__ordered":[]
    # 'keyname':{
    #         'displayname':''
    #         'description':''
    #         'dataformat':''
    #         'dataformat_ext':''
    #         'order':
    #         'cardinal_min':
    #         'cardinal_max':
    #         'is_multi': True/False
    #         'default_value':
    #  }, 
    #  ...
    # }
    

    reply_dict = {}
    reply_array = []

    classobj = get_class_obj(cid=cid, iid=iid, obj=obj, classname=classname, iname=iname)
    if not classobj:
        return {}

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

        reply_dict[entry.keyname] = m
        arrayentry = (entry.keyname, m )
        reply_array.append(arrayentry)


    reply_dict["__ordered"] = reply_array
    reply_dict["__classname"] = classobj.keyname

    return reply_dict

# -------------------------------------------------------------------------
# Task : biset/count update
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



# --------------------------------------------------------
# INSTANCE
# --------------------------------------------------------
class Instance:

    def __init__(self, iobj=None, iid=None, iname=None, classname=None, schema=None):

        self.iobj = None

        self.classname = None
        self.schema = None

        self.keyname = None

        self.is_enabled = None     # True / False
        self.displayname = None
        self.last_update = None

        self.json = None
        self.fields = {}    # key = field keyname

        self.errors = []

        if schema:
            self.schema = schema

        if classname:
            self.classname = classname

        # is iobj an DataInstance ?
        if iobj:
            if not type(iobj) is DataInstance:
                return


        if not iobj:
            if iid:
                iobj = get_instance_by_id(iid)
            elif iname and classname:
                iobj = get_instance_by_name(iname=iname, classname=classname)

        # existing object in DB
        if iobj:
            self.iobj = iobj
            self.keyname = iobj.keyname
            self.is_enabled = iobj.is_enabled
            self.displayname = iobj.displayname
            self.last_update = iobj.last_update
            if not self.classname:
                self.classname = iobj.classobj.keyname
            if not self.schema:
                self.schema = get_schema(obj=iobj)
        else:
            # new Instance : iobj is None
            self.keyname = iname
            self.is_enabled = True
            self.displayname = None
            self.classname = classname
            if not self.schema:
                self.schema = get_schema(classname=classname)
            
        # TODO : JSON error check !!!
        if iobj:
            self.json = json.loads(iobj.data_json)      

        # create fields
        for fieldname, fieldschema in self.schema.items():
            
            if fieldname.startswith('__'):
                continue        
            
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

            # elif fieldschema["dataformat"] == "sirene_static":
            #     self.fields[fieldname] = FieldSireneStatic(fieldname, fieldschema, self.json)

            elif fieldschema["dataformat"] == "user":
                self.fields[fieldname] = FieldUser(fieldname, fieldschema, self.json)

            elif fieldschema["dataformat"] == "text":
                self.fields[fieldname] = FieldText(fieldname, fieldschema, self.json)

            elif fieldschema["dataformat"] == "enumerate":
                self.fields[fieldname] = FieldEnumerate(fieldname, fieldschema, self.json)

            else:
                self.fields[fieldname] = FieldString(fieldname, fieldschema, self.json)



    def __str__(self):
        return f"{self.classname}:{self.keyname}"

    def is_bound(self):
        ''' if object from DB in self.iobj '''
        if self.iobj:
            return True
        return False

    def print(self):
        print(f"{self.classname}:{self.keyname}")
        print(f"    is_enabled:  {self.is_enabled}")
        print(f"    displayname: {self.displayname}")
        print(f"    iobj:        {self.iobj}")
        print(f"    is_bound:    {self.is_bound()}")
        print(f"    is_valid:    {self.is_valid()}")
        print( "    schema:")
        pprint(self.schema)
        for k,v in self.fields.items():
            v.print()

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


    def get_attribute(self, fieldname):
        '''  
        Returns : list []
        Get attribute value(s) from instance. 
        Convert to obj if DataClass  or SireneGroup
        '''

        if not fieldname in self.schema:
            return

        if not fieldname in self.fields:
            return


        datapoint = self.fields[fieldname].get_attribute()
        return datapoint


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
                if not z in done:
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
                            if not z in done:
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
                            if not z in done:
                                reply.append(z)
                    #reply += xlist5


        reply = list(set(reply))
        return reply



    def get_dict_for_ui_detail(self):
        ''' dict suited for list template '''

        # ui = { 
        #   keyname:"xxxx"
        #   displayname:"xxx"
        #   is_enabled:True/False"
        #   "PAGES": {  
        #     "(page)1": { "(order)100": { "attribname":{DATAPOINT}, "attribname":{}, ... }, "(order)101": {... }, ... }, 
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
        instance_ui["displayname"] = self.displayname
        instance_ui["is_enabled"] = self.is_enabled

        instance_ui["PAGES"] = {}

        if "__ordered" in self.schema:
            for element in self.schema["__ordered"]:
                (fieldname,fieldschema) = element

                order = fieldschema["order"]
                page = fieldschema.get("page")
                if not page:
                    page = self.keyname

                if page not in instance_ui["PAGES"]:
                    instance_ui["PAGES"][page] = {}
                if order not in instance_ui["PAGES"][page]:
                    instance_ui["PAGES"][page][order]= []

                datapoint = self.fields[fieldname].get_datapoint_ui_detail()
                instance_ui["PAGES"][page][order].append(datapoint)

        return instance_ui


    # used for edit in form : new or edit
    def get_dict_for_ui(self):
        
        # ui = { 
        #   keyname:"xxxx"
        #   displayname:"xxx"
        #   is_enabled:True/False"
        #    "PAGES": {  
        #     "(page)1": { "(order)100": { "attribname":{DATAPOINT}, "attribname":{}, ... }, "(order)101": {... }, ... }, 
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
        #     TODO: multi, values stuct w/ allowed/checked
        # }
        # value : format depend on dataformat for the field


        # TODO - merge errors


        instance_ui = {}

        # SPECIAL fields
        instance_ui["keyname"] = self.keyname
        instance_ui["displayname"] = self.displayname
        instance_ui["is_enabled"] = self.is_enabled

        instance_ui["PAGES"] = {}
        if "__ordered" in self.schema:
            for element in self.schema["__ordered"]:
                (fieldname,fieldschema) = element

                order = fieldschema["order"]
                page = fieldschema.get("page")
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
        #instance_export["keyname"] = self.keyname
        instance_export["displayname"] = self.displayname
        instance_export["is_enabled"] = self.is_enabled

        #keyname = f"{self.classname}:{self.keyname}"


        if "__ordered" in self.schema:
            for element in self.schema["__ordered"]:
                (fieldname,fieldschema) = element

                datapoint = self.fields[fieldname].get_datapoint_for_export()
                cardinal, cardinal_min, cardinal_max = self.fields[fieldname].get_cardinal3()
                if not (cardinal_min == 0 and cardinal == 0):
                    instance_export[fieldname] = datapoint

        return instance_export


    def merge_edit_post_request(self, request):
        
        # instance name: no change, not editable

        # displayname
        self.displayname = request.POST.get("displayname", "")
        # TODO : cleanup / error check

        # is_enabled
        if "is_enabled" in request.POST:
            self.is_enabled = request.POST["is_enabled"] in TRUE_LIST
        else:
            self.is_enabled = False

        for fieldname, fieldschema in self.schema.items():

            # __ordered, __classname : not real fields
            if fieldname.startswith("__"):
                continue

            # special case : Boolean are not in POST request if False
            postdata = request.POST.getlist(fieldname,default=[])
            self.fields[fieldname].merge_edit_data(postdata)




    def merge_new_post_request(self, request):

        # instance name: no change, not editable
        self.keyname = request.POST.get("keyname", "")
        # TODO : cleanup / error check

        # displayname
        self.displayname = request.POST.get("displayname", "")
        # TODO : cleanup / error check

        # is_enabled
        if "is_enabled" in request.POST:
            self.is_enabled = request.POST["is_enabled"] in TRUE_LIST
        else:
            self.is_enabled = False


        for fieldname, fieldschema in self.schema.items():

            # __ordered, __classname : not real fields
            if fieldname.startswith("__"):
                continue

            # special case : Boolean are not in POST request if False
            postdata = request.POST.getlist(fieldname, default=[])
            self.fields[fieldname].merge_new_data(postdata)


    def merge_import_data(self, data):

        # instance name: mandatory and already loaded as in {keyname : data}
        # self.keyname = data.get("keyname", "")
        # TODO : cleanup / error check

        # displayname
        if 'displayname' in data:
            self.displayname = data["displayname"]

        # is_enabled
        if "is_enabled" in data:
            self.is_enabled = data["is_enabled"] in TRUE_LIST
        #else:
        #    self.is_enabled = False


        for fieldname, fieldschema in self.schema.items():

            # __ordered, __classname : not real fields
            if fieldname.startswith("__"):
                continue

            # special case : Boolean are not in POST request if False
            if fieldname in data:
                    fielddata = data[fieldname] 
                    self.fields[fieldname].merge_import_data(fielddata)



    def is_valid(self):

        reply = True

        if not self.keyname:
            self.errors.append(_("missing keyname"))
            return False

        if len(self.keyname) == 0:
            self.errors.append(_("keyname empty"))
            return False

        # TODO keyname: slug format
        # TODO displayname : safe string for display
        # TODO classname

        # is_enabled
        if type(self.is_enabled) is not bool:
            return False


        for fieldname, fieldschema in self.schema.items():
            
            # __ordered, __classname : not real fields
            if fieldname.startswith("__"):
                continue

            r = self.fields[fieldname].is_valid()
            if not r:
                reply = False
                #err = fieldname
                err = fieldschema["displayname"]
                self.errors.append(str(err))
                # TODO  use field.errors info

        return reply



    def update(self):

        if not self.iobj:
            return False

        self.iobj.keyname = self.keyname
        self.iobj.displayname = self.displayname
        self.iobj.is_enabled = self.is_enabled


        data = {}

        for fieldname, fieldschema in self.schema.items():
        
            if fieldname.startswith("__"):
                # __ordered, __classname : not real fields
                continue

            field_datalist = self.fields[fieldname].get_json()
            # don't store empty fields in DB
            if len(field_datalist) > 0:
                data[fieldname] = field_datalist

        try:
            self.iobj.data_json = json.dumps(data, indent=4)
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
            print("! already exists in struct")
            return False

        # valid class ?
        classobj = get_class_by_name(self.classname)
        if not classobj:
            print("! no classobj")
            return False
        if not classobj.is_enabled:
            print("! classobj disabled")
            return False

        # instance already in DB ?
        iobj = get_instance_by_name(iname=self.keyname,  classname=self.classname)
        if iobj:
            print("! classobj already exists in DB")
            return False

        # create new instance
        self.iobj = DataInstance()
        self.iobj.classobj = classobj
        self.iobj.keyname = self.keyname
        self.iobj.displayname = self.displayname
        self.iobj.is_enabled = self.is_enabled

        data = {}

        for fieldname, fieldschema in self.schema.items():

            if fieldname.startswith("__"):
                # __ordered, __classname : not real fields
                continue

            data[fieldname] = self.fields[fieldname].get_json()


        try:
            self.iobj.data_json = json.dumps(data, indent=4)
        except:
            print("Invalid JSON in create()")
            return False

        self.save()
        return True


    # only place where save() to DB for instances
    def save(self):

        if not self.iobj:
            print("!! no iobj in save()")
            return False

        self.iobj.last_update = timezone.now()

        try:

            self.iobj.save()
            #print("!! saved")
        except Exception as e:
            print(f"save() to DB failed: {e}")
            return False

# -------------------------------------------------------
# IMPORTS
# -------------------------------------------------------

def make_dictlist_from_csv(filedata,  splitfields=[]):

    lines = filedata.splitlines()
    header = []
    rows = []
    line_count = 0

    # global (no appname)
    delimiter = get_configuration(keyname="CSV_DELIMITER") 

    for line in lines:
        entry = {}                    
        fields = line.split(delimiter)
        if line_count == 0:
            header = fields
            line_count = 1
        else:
            line_count += 1
            for i in range(0,len(header)):
                hi = header[i]
                if hi in splitfields:
                    try:
                        a = fields[i].split("+")
                        entry[hi] = a
                    except:
                        pass
                else:
                    try:
                        entry[hi] = fields[i]
                    except:
                        pass
            rows.append(entry)        

    return rows




def data_import_csv(file):
    
    filedata = file.read().decode("utf-8")  
    rows = make_dictlist_from_csv(filedata, splitfields=["roles"])

    err = load_data(rows)
    return err


def data_import_json(file):

    filedata = json.load(file) 
    #print(json.dumps(filedata, indent=4))
    # data = filedata.get("users", '')
    err = load_data(filedata)
    return err


def data_import_yaml(file):

    filedata = yaml.load(file, Loader=yaml.SafeLoader)
    #print(json.dumps(filedata, indent=4))
    #data = filedata.get("users", '')
    err = load_data(filedata)
    return err


# --------------------------------------------------------
# LOADER / IMPORT
# Global LOADER : class, schema, instance, static
# --------------------------------------------------------

def load_data(filedata, force_action=None, verbose=True):

    count = 0

    line_total = 0
    line_ok = 0

    # _schema:classname: {} 
    for item, classdata in filedata.items():
        if item.startswith("_schema:"):
            classname = re.sub("^_schema:", '', item)
           
            if classname == "":
                continue
            
            classobj = load_class(classname, classdata, force_action=force_action, verbose=verbose)
            if not classobj:
                continue
            
            count += 1

            # fields
            for fieldname, fielddata in classdata.items():
                # ignore class meta data in ["_action", "_displayname", "_is_enabled", "_icon", "_page", "_order"]
                if fieldname.startswith("_"):
                    continue
                fieldobj = load_schema(classobj, fieldname, fielddata, force_action=force_action, verbose=verbose)


    # instances:  classname:instancename: {}
    for item, instdata in filedata.items():

        if item.startswith("_"):
            continue
        if not ":" in item:
            continue

        try:
            (classname, keyname) = item.split(":")
        except:
            continue


        classobj = get_class_by_name(classname)
        if not classobj:
            if verbose:
                print(f"  !!skip - unknown class: {classname}")
            continue

        # for each item ...
        schema = get_schema(classname=classname)
        r, action = load_instance(classobj=classobj, keyname=keyname, instdata=instdata, schema=schema, 
            force_action=force_action, verbose=verbose)
        if r:
            count += 1
            if verbose:
                print(f"instance: {action} - {classname} => {keyname}")

    return count



# loads class definition (fields not loaded here)
def load_class(classname, classdata, force_action=None, verbose=True):

    if not type(classname) is str:
        return

    if not type(classdata) is dict:
        return

    if not len(classname)>0: 
        return

    action = force_action
    if not action:
        action = classdata.get("_action", "create")

    classobj = get_class_by_name(classname)

    if action == "delete":
        if classobj:
            classobj.delete()
            if verbose:
                print(f"class : {action} - {classname}")            
            return

    elif action == "disable":
        if classobj:
            classobj.is_enabled = False
            classobj.save()
            if verbose:
                print(f"class : {action} - {classname}")            
            return

    elif action == "enable":
        if classobj:
            classobj.is_enabled = True
            classobj.save()
            if verbose:
                print(f"class : {action} - {classname}")            
            return

    elif action == "update":
        # no creation, see below
        pass

    elif action == "init": 
        # skip if alreay created
        if classobj:
            # return None to skip creating fields
            return None
        classobj=DataClass(keyname=classname)
        classobj.save()

    elif action == "create":
        if not classobj:    
            classobj=DataClass(keyname=classname)
            classobj.save()
    else:
        # unknown action
        if verbose:
            print(f"  !!! unknown action {action} for class {classname}")
        return

    # update for all remaining actions
    # --------------------------------
    if not classobj:
        return

    if "_displayname" in classdata:
        classobj.displayname = classdata.get("_displayname","")

    if "_icon" in classdata:
        classobj.icon = classdata.get("_icon")

    if "_order" in classdata:
        classobj.order = classdata.get("_order",100)

    if "_page" in classdata:
        classobj.page = classdata.get("_page")

    if "_is_enabled" in classdata:
        classobj.is_enabled = classdata.get("_is_enabled") in TRUE_LIST


    # update roles
    # ------------
    #"show", "access", "read", "create","update","delete","onoff","import","export"
    rolename = classdata.get("_role_show")
    role = role_get_by_name(rolename, enabled_only=False)
    if role:
        classobj.role_show = role
    rolename = classdata.get("_role_access")
    role = role_get_by_name(rolename, enabled_only=False)
    if role:
        classobj.role_access = role
    rolename = classdata.get("_role_read")
    role = role_get_by_name(rolename, enabled_only=False)
    if role:
        classobj.role_read = role
    rolename = classdata.get("_role_create")
    role = role_get_by_name(rolename, enabled_only=False)
    if role:
        classobj.role_create = role
    rolename = classdata.get("_role_update")
    role = role_get_by_name(rolename, enabled_only=False)
    if role:
        classobj.role_update = role
    rolename = classdata.get("_role_delete")
    role = role_get_by_name(rolename, enabled_only=False)
    if role:
        classobj.role_delete = role
    rolename = classdata.get("_role_onoff")
    role = role_get_by_name(rolename, enabled_only=False)
    if role:
        classobj.role_onoff = role
    rolename = classdata.get("_role_import")
    role = role_get_by_name(rolename, enabled_only=False)
    if role:
        classobj.role_import = role
    rolename = classdata.get("_role_export")
    role = role_get_by_name(rolename, enabled_only=False)
    if role:
        classobj.role_export = role


    classobj.save()
    if verbose:
        print(f"class : {action} - {classname}")
    return classobj


# load Schema entry in DB
def load_schema(classobj, fieldname, fielddata, force_action=None, verbose=True):

    if not classobj:
        return

    if not type(fieldname) is str:
        return

    if not type(fielddata) is dict:
        return

    if not len(fieldname)>0: 
        return

    action = force_action
    if not action:
        action = fielddata.get("_action", "create")

    fieldobj = get_field_by_name(classobj, fieldname)


    if action == "delete":
        if fieldobj:
            fieldobj.delete()
            if verbose:
                print(f"schema : {action} - {classobj.keyname}:{fieldname}")            
            return fieldobj

    elif action == "disable":
        if fieldobj:
            fieldobj.is_enabled = False
            fieldobj.save()
            if verbose:
                print(f"schema : {action} - {classobj.keyname}:{fieldname}")            
            return fieldobj

    elif action == "enable":

        if fieldobj:
            fieldobj.is_enabled = True
            fieldobj.save()
            if verbose:
                print(f"schema : {action} - {classobj.keyname}:{fieldname}")            
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


    elif action == "create":
        if not fieldobj:
            fieldobj=DataSchema()
            fieldobj.classobj = classobj
            fieldobj.keyname = fieldname
            fieldobj.save()

        # fieldobj.classobj = classobj
        # fieldobj.keyname = fieldname
        # fieldobj.displayname = fielddata.get("displayname", "")
        # fieldobj.description = fielddata.get("description", "")
        # #fieldobj.is_enabled = fielddata.get("is_enabled", True) in TRUE_LIST
        # fieldobj.order = fielddata.get("order", 100)
        # fieldobj.page = fielddata.get("page", "")
        # fieldobj.dataformat = fielddata.get("dataformat", "string")
        # fieldobj.dataformat_ext = fielddata.get("dataformat_ext", "")
        # fieldobj.default = fielddata.get("default", "")

        # fieldobj.cardinal_min = int( fielddata.get("cardinal_min",0) )
        # fieldobj.cardinal_max = int( fielddata.get("cardinal_max",1) )
        # fieldobj.save()

    else: 
        # unknown action
        if verbose:
            print(f"    !!! unknown field action {action} for {classobj.keyname}:{fieldname}")
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
        print(f"schema : {action} - {classobj.keyname}:{fieldname}")
    return fieldobj



def load_instance(classobj=None, keyname=None, instdata=None, schema=None, force_action=None, verbose=True):

    r = False

    if not classobj:
        return r
    if not keyname:
        return r
    if not instdata:
        return r
    if not schema:
        schema = get_schema(classname=classname)

    if len(keyname) == 0:
        return r

    classname = classobj.keyname

    instance = Instance(classname=classname, iname=keyname,  schema=schema)

    if not instance:
        if verbose:
            print(f"  !!ERR - couldn't access instance for {classname}/{keyname}")
        return r


    action = force_action
    if not action:
        action = instdata.get("_action", "create")

    if action == "delete":
        if instance.is_bound():
            r = instance.delete()
            if verbose:
                print(f"instance : {action} - {classname}:{keyname}")            
            return r, action

    elif action == "disable":
        if instance.is_bound():
            r = instance.disable()
            if verbose:
                print(f"instance : {action} - {classname}:{keyname}")            
            return r, action

    elif action == "enable":
        if instance.is_bound():
            r = instance.enable()
            if verbose:
                print(f"instance : {action} - {classname}:{keyname}")            
            return r, action

    elif action == "init":
        if instance.is_bound():
            r = False
            return r, action
        r = instance.create()
        if verbose:
            print(f"instance : {action} - {classname}:{keyname}")            

    elif action == "create":
        if not instance.is_bound():
            r = instance.create()
            if verbose:
                print(f"instance : {action} - {classname}:{keyname}")            

    elif action == "update":    
        if not instance.is_bound():
            r = False
            return r, action

    # update
    instance.merge_import_data(instdata)
    r = instance.update()
    if verbose:
        print(f"instance : {action} - {classname}:{keyname}")

    return r, action


# --------------------------------------------------------
#  EXPORT
# --------------------------------------------------------
#YAML
class MyYamlDumper(yaml.SafeDumper):
    def write_line_break(self, data=None):
        super().write_line_break(data)
        if len(self.indents) < 2:
            super().write_line_break()


def export_data(classes=None):

    reply = {}

    if not classes:
        classes = get_classes()


    for classname in classes:
        # Queryset of DB objects
        qs_iobj =  get_instances(classname = classname)
        schema = get_schema(classname=classname)

        for iobj in qs_iobj:
            #instance = Instance(classname=classname, iname=iobj.keyname,  schema=schema)
            instance = Instance(classname=classname, iobj=iobj,  schema=schema)
            data = instance.get_dict_for_export()
            keyname_full = f"{classname}:{iobj.keyname}"
            reply[keyname_full] = data
        
    # filedata = yaml.dump(reply, allow_unicode=True, Dumper=MyYamlDumper, sort_keys=False)
    # print(json.dumps(reply, indent=2, ensure_ascii=False))

    return reply


def data_yaml_response(classes=None):

    data = export_data(classes)
    filedata = yaml.dump(data, allow_unicode=True, Dumper=MyYamlDumper, sort_keys=False)
    response = HttpResponse(filedata, content_type='text/yaml')  
    response['Content-Disposition'] = 'attachment; filename="cavaliba_data.yaml"'
    return response


def data_json_response(classes=None):

    data = export_data(classes)
    filedata = json.dumps(data, indent=4)
    response = HttpResponse(filedata, content_type='text/json')  
    response['Content-Disposition'] = 'attachment; filename="cavaliba_data.json"'
    return response    