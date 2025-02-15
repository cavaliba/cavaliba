# test_app_user 
# (c) cavaliba.com

import yaml 

from django.test import TestCase
from django.urls import reverse

from app_home.home import cavaliba_update
from app_data.data import Instance



class APIKeyTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cavaliba_update(verbose=False)

        instance = Instance(classname="_apikey", iname="unittestoff")
        data = {
            "keyvalue":"ktest",
            "ip_filter":"*",
            "is_readonly":False,
            "is_enabled":False,
        }
        instance.merge_import_data(data)
        instance.create()



        instance = Instance(classname="_apikey", iname="unittestro")
        data = {
            "keyvalue":"ktest",
            "ip_filter":"*",
            "is_readonly":True,
            "is_enabled":True,
        }
        instance.merge_import_data(data)
        instance.create()

        instance = Instance(classname="_apikey", iname="unittestrw")
        data = {
            "keyvalue":"ktest",
            "ip_filter":"*",
            "is_readonly":False,
            "is_enabled":True,
        }
        instance.merge_import_data(data)
        instance.create()



    def test_auth_nokey(self):
        # no key 
        response = self.client.get(reverse('app_data:api_index'))
        self.assertEqual(response.status_code, 401)


    def test_auth_key(self):
        # key OK
        response = self.client.get(
            reverse('app_data:api_index'),
            headers = {"X-Cavaliba-Key":"unittestro ktest"},
            )
        self.assertEqual(response.status_code, 200)



    def test_auth_keyoff(self):
        # key OFF
        response = self.client.get(
            reverse('app_data:api_index'),
            headers = {"X-Cavaliba-Key":"unittestoff ktest"},
            )
        self.assertEqual(response.status_code, 401)


    def test_auth_badpwd(self):
        # Bad PWD
        response = self.client.get(
            reverse('app_data:api_index'),
            headers = {"X-Cavaliba-Key":"unittestro badkv"},
            )
        self.assertEqual(response.status_code, 401)



    def test_auth_rorw(self):
        # RO / RW
        response = self.client.post(
            reverse('app_data:api_index'),
            headers = {"X-Cavaliba-Key":"unittestro ktest"},
            )
        self.assertEqual(response.status_code, 401)


        # key RW
        response = self.client.get(
            reverse('app_data:api_index'),
            headers = {"X-Cavaliba-Key":"unittestro ktest"},
            )
        self.assertEqual(response.status_code, 200)


