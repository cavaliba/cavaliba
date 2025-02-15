# (c) cavaliba.com
# test_data_permission


import yaml

from django.test import TestCase, override_settings
from django.urls import reverse


from app_data.models import DataSchema
from app_data.models import DataClass

from app_data.loader import load_broker

import app_home.cache as cache


class DataTestPermission(TestCase):

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
            ''')
        aaa = {'perms':'*'}
        load_broker(datalist=datalist, aaa=aaa, verbose=False)

        cache.init()



    def test_schema_exist(self):
        classobj = DataClass.objects.get(keyname='class_unittest')
        self.assertIsNotNone(classobj)



    def test_perm_global_p_schema_delete(self):

        classobj = DataClass.objects.get(keyname='class_unittest')
        self.assertIsNotNone(classobj)

        aaa = {'perms':'p_schema_delete'}
        aaa = {'perms':'*'}
        datalist = yaml.safe_load('''       
            - classname: _schema
              keyname: class_unittest
              displayname: ClassUnittest
              _action: delete
            ''')

        r = load_broker(datalist=datalist, aaa=aaa, verbose=False)
        classobj = DataClass.objects.filter(keyname='class_unittest').first()
        self.assertIsNone(classobj)

