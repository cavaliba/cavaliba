# test_app_data 
# (c) cavaliba.com

import yaml

from django.test import TestCase, override_settings
from django.urls import reverse

#from app_data..models import XXXXXXXXx;


#self.assertRedirects(response, '/accounts/login/?next=/catalog/mybooks/')
#self.assertEqual(r.value, 'no')

from app_data.models import DataSchema
from app_data.models import DataClass

from app_data.data import load_data

from app_data.fieldtypes.field_ipv4 import FieldIPV4
from app_data.fieldtypes.field_float import FieldFloat
from app_data.fieldtypes.field_int import FieldInt


class DataLoadTest(TestCase):

    def setUp(self):

        filedata = yaml.safe_load('''
            _schema:class_unittest:
                #_action: create
                _displayname: ClassUnittest
                _is_enabled: yes
                _order: 999
                _page: Test        
                _icon: fa-question
                mystring:
                    displayname: MyString
                    dataformat: string
                    description: description ...            
                    order: 100
                    page: Strings
                myint:
                    displayname: MyInt
                    dataformat: int
                    order: 200
                    description: description ...            
                    page: Numbers
                myfloat:
                    displayname: MyFloat
                    dataformat: float
                    description: description ...
                    order: 210
                    page: Numbers
                myboolean:
                    displayname: MyBoolean
                    dataformat: boolean
                    description: Cocher pour activer !
                    order: 300
                    page: Booleans
                mydate:
                    displayname: MyDate
                    description: format YYYY-MM-DD
                    dataformat: date
                    order: 400
                    page: Other
                myipv4:
                    displayname: MyIPV4
                    dataformat: ipv4
                    description: A.B.C.D or A.B.C.D/mask
                    order: 410
                    page: Other
                my_sirene_group:
                    displayname: MysireneGroup
                    dataformat: sirene_group
                    description: select sirene user group object(s)
                    order: 500
                    page: Objects
                    cardinal_max: 0
                my_sirene_app:      
                    displayname: MySireneData(app)
                    dataformat: sirene_data
                    dataformat_ext: app
                    description: select sirene data instace object(s)
                    order: 510
                    page: Objects
                    cardinal_max: 0

            ''')
        load_data(filedata, verbose=False)


    def test_schema_exist(self):
        classobj = DataClass.objects.get(keyname='class_unittest')
        self.assertIsNotNone(classobj)


    def test_schema_delete(self):
        filedata = yaml.safe_load('''
            _schema:class_unittest:
                _action: delete
            ''')
        load_data(filedata, verbose=False)
        classobj = DataClass.objects.filter(keyname='class_unittest').first()
        self.assertIsNone(classobj)


    def test_schema_disable(self):
        filedata = yaml.safe_load('''
            _schema:class_unittest:
                _action: disable
            ''')
        load_data(filedata, verbose=False)
        classobj = DataClass.objects.filter(keyname='class_unittest').first()
        self.assertEqual(classobj.is_enabled, False)


    def test_schema_enable(self):
        filedata = yaml.safe_load('''
            _schema:class_unittest:
                _action: disable
            _schema:class_unittest:
                _action: enable
            ''')
        load_data(filedata, verbose=False)
        classobj = DataClass.objects.filter(keyname='class_unittest').first()
        self.assertEqual(classobj.is_enabled, True)






class FieldIPV4Test(TestCase):

    def setUp(self):

        pass
        # fieldobj=DataSchema()
        # fieldobj.keyname = "test_field"
        # fieldobj.displayname = "test_field_display"
        # fieldobj.order = 200
        # fieldobj.page = "page1"
        # fieldobj.dataformat = "ipv4"
        # fieldobj.dataformat_ext = ""
        # fieldobj.default = ""
        # fieldobj.cardinal_min = 0
        # fieldobj.cardinal_max = 1


    def test_int_valid(self):

        fieldschema = {'cardinal_min':0, 'cardinal_max':1, 'default_value':''}

        # OK
        f = FieldInt( fieldname='data', fieldschema=fieldschema, alljson={'data':[33]} )
        self.assertEqual( f.is_valid(), True)
        f = FieldInt( fieldname='data', fieldschema=fieldschema, alljson={'data':[-3]} )
        self.assertEqual( f.is_valid(), True)

        # KO
        f = FieldInt( fieldname='data', fieldschema=fieldschema, alljson={'data':["a"]} )
        self.assertEqual( f.is_valid(), False)
        f = FieldInt( fieldname='data', fieldschema=fieldschema, alljson={'data':[33.4]} )
        self.assertEqual( f.is_valid(), False)


    def test_float_valid(self):

        fieldschema = {'cardinal_min':0, 'cardinal_max':1, 'default_value':''}

        # OK
        f = FieldFloat( fieldname='data', fieldschema=fieldschema, alljson={'data':[33.2]} )
        self.assertEqual( f.is_valid(), True)

        # KO
        f = FieldFloat( fieldname='data', fieldschema=fieldschema, alljson={'data':["a"]} )
        self.assertEqual( f.is_valid(), False)


    def test_ipv4_valid(self):

        fieldschema = {'cardinal_min':0, 'cardinal_max':1, 'default_value':''}

        # OK
        f = FieldIPV4( fieldname='myip', fieldschema=fieldschema, alljson={'myip':['10.1.2.3/24']} )
        self.assertEqual( f.is_valid(), True)
        f = FieldIPV4( fieldname='myip', fieldschema=fieldschema, alljson={'myip':['10.1.2.3']} )
        self.assertEqual( f.is_valid(), True)
        f = FieldIPV4( fieldname='myip', fieldschema=fieldschema, alljson={'myip':['0.0.0.0']} )
        self.assertEqual( f.is_valid(), True)
        f = FieldIPV4( fieldname='myip', fieldschema=fieldschema, alljson={'myip':['255.255.255.255']} )
        self.assertEqual( f.is_valid(), True)


        # KO
        f = FieldIPV4( fieldname='myip', fieldschema=fieldschema, alljson={'myip':['10.1.2.256']} )
        self.assertEqual( f.is_valid(), False)
        f = FieldIPV4( fieldname='myip', fieldschema=fieldschema, alljson={'myip':['10.1.2']} )
        self.assertEqual( f.is_valid(), False)
        f = FieldIPV4( fieldname='myip', fieldschema=fieldschema, alljson={'myip':['10.1.2.3.4']} )
        self.assertEqual( f.is_valid(), False)
        f = FieldIPV4( fieldname='myip', fieldschema=fieldschema, alljson={'myip':['10.1.2.3/33']} )
        self.assertEqual( f.is_valid(), False)
        #print("*** ", f.value) 








