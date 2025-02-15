# (c) cavaliba.com
# unittest - test_data_load

import yaml

from django.test import TestCase, override_settings
from django.urls import reverse


from app_data.models import DataSchema
from app_data.models import DataClass

from app_data.loader import load_broker

import app_home.cache as cache



class DataLoadTest(TestCase):

    def setUp(self):

        datalist = yaml.safe_load('''
- classname: _schema
  keyname: class_unittest
  #_action: create
  displayname: ClassUnittest
  is_enabled: yes
  order: 999
  page: Test        
  icon: fa-question
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
  my_group:
        displayname: MysireneGroup
        dataformat: group
        description: select sirene user group object(s)
        order: 500
        page: Objects
        cardinal_max: 0
  my_app:      
        displayname: MySireneData(app)
        dataformat: schema
        dataformat_ext: app
        description: select data instance object(s)
        order: 510
        page: Objects
        cardinal_max: 0
''')
        aaa = {'perms':'*'}
        r = load_broker(datalist=datalist, aaa=aaa, verbose=False)
        self.assertEqual(r, 1)

        cache.init()

    def test_schema_exist(self):
        classobj = DataClass.objects.get(keyname='class_unittest')
        self.assertIsNotNone(classobj)


    def test_schema_delete(self):

        datalist = yaml.safe_load('''
            - classname: _schema
              keyname: class_unittest
              _action: delete
            ''')
        aaa = {'perms':'*'}
        r = load_broker(datalist=datalist, aaa=aaa, verbose=False)

        classobj = DataClass.objects.filter(keyname='class_unittest').first()
        self.assertIsNone(classobj)


    def test_schema_disable(self):
        datalist = yaml.safe_load('''
            - classname: _schema
              keyname: class_unittest
              _action: disable
            ''')
        aaa = {'perms':'*'}
        load_broker(datalist=datalist, aaa=aaa, verbose=False)
        classobj = DataClass.objects.filter(keyname='class_unittest').first()
        self.assertEqual(classobj.is_enabled, False)


    def test_schema_enable(self):
        datalist = yaml.safe_load('''
            - classname: _schema
              keyname: class_unittest
              _action: enable
            ''')
        aaa = {'perms':'*'}
        load_broker(datalist=datalist, aaa=aaa, verbose=False)
        classobj = DataClass.objects.filter(keyname='class_unittest').first()
        self.assertEqual(classobj.is_enabled, True)










