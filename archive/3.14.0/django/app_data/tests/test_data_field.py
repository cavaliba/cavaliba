# (c) cavaliba.com
# unittest - test_data_field


import yaml

from django.test import TestCase, override_settings
from django.urls import reverse



from app_data.models import DataSchema
from app_data.models import DataClass

from app_data.loader import load_broker

from app_data.fieldtypes.field_ipv4 import FieldIPV4
from app_data.fieldtypes.field_float import FieldFloat
from app_data.fieldtypes.field_int import FieldInt




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
        








