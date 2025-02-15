from django.test import TestCase

from app_sirene.models import MyLog
from app_sirene.models import SireneUser
from app_sirene.models import SireneUserGroup
from app_sirene.models import MessageTemplate
from app_sirene.models import Message
from app_sirene.models import Site
from app_sirene.models import SiteGroup
from app_sirene.models import App


class ModelTest(TestCase):

    fixtures = ["test_data.json"]


    # @classmethod
    # def setUpTestData(cls):
    #     super().setUpClass()
    #     # Set up non-modified objects used by all test methods
    #     Site.objects.create(name='site1', description='description_site1')
    #     SiteGroup.objects.create(name='sitegroup1', description='description_sitegroup1')
    #     App.objects.create(name='app1', description='description_app1')
    #     SireneUser.objects.create(login='user1', description='description_user1')
    #     SireneUserGroup.objects.create(name='group1', description='description_group1')
        

    def test_model_site(self):
        #site = Site.objects.get(name="site")
        #Site.objects.create(name='site1', description='description_site_1')
        #site = Site(name="site2", description="description_site_2")
        #site.save()
        site = Site.objects.get(name="site01")
        #print(site.id)
        #self.assertIsNotNone(site.id)
        self.assertEquals(site.name,"site01")
        # field_label = site._meta.get_field('name').verbose_name
        # self.assertEquals(field_label, 'name')

    def test_model_sitegroup(self):
        item = SiteGroup.objects.get(name="sitegroup01")
        self.assertEquals(item.name,"sitegroup01")

    def test_model_sitegroup_addsite(self):
        sitegroup  = SiteGroup.objects.get(name="sitegroup01")
        site = Site.objects.get(name="site05")
        sitegroup.sites.add(site)
        sitegroup.save()
        a = sitegroup.sites.count()
        self.assertEquals(a,3)


    def test_model_app(self):
        item = App.objects.get(name="app01")
        self.assertEquals(item.name,"app01")

    def test_model_app_addsite(self):
        app  = App.objects.get(name="app01")
        site = Site.objects.get(name="site01")
        app.site = site
        app.save()
        self.assertEquals(app.site.name,"site01")

    def test_model_user(self):
        item = SireneUser.objects.get(login="user01")
        self.assertEquals(item.login,"user01")

    def test_model_usergroup(self):
        item = SireneUserGroup.objects.get(name="group01")
        self.assertEquals(item.name,"group01")

    def test_model_usergroup_adduser(self):
        group = SireneUserGroup.objects.get(name="group01")
        user = SireneUser.objects.get(login="user0101")
        group.users.add(user)
        group.save()
        a = group.users.count()
        self.assertEquals(a,6)

