# tests app_sirene

from django.test import TestCase, override_settings
from django.urls import reverse


from app_home.home import cavaliba_update
from app_home.configuration import get_configuration
from app_home.models import CavalibaConfiguration

from app_user.aaa import get_aaa
from app_user.aaa import global_aaa

from app_user.models import SireneUser, SireneGroup
from app_user.group import group_get_by_name
from app_user.role import role_get_by_name

from app_sirene.models import Category
from app_sirene.models import PublicPage
from app_sirene.models import PublicPageJournal
from app_sirene.models import MessageTemplate
from app_sirene.models import Message
from app_sirene.models import MessageUpdate
from app_sirene.models import SMSJournal




#self.assertRedirects(response, '/accounts/login/?next=/catalog/mybooks/')
#self.assertEqual(r.value, 'no')

class AppSireneAnonymousTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cavaliba_update(verbose=False)

        # force mode
        conf = CavalibaConfiguration.objects.get(appname="user", keyname="AUTH_MODE")
        conf.value = "basic"
        conf.save()

        conf = CavalibaConfiguration.objects.get(appname="user", keyname="DEBUG_AAA")
        conf.value = "no"
        conf.save()


    def test_init(self):
        self.assertEqual(True, True)


    def test_public(self):
        response = self.client.get(reverse('app_sirene:index'))
        self.assertEqual(response.status_code, 200)


    def test_anonymous(self):
        response = self.client.get(reverse('app_sirene:anonymous'))
        # user = admin
        self.assertEqual(response.status_code, 302)


    def test_trusted_ip(self):
        conf = CavalibaConfiguration.objects.get(appname="user",keyname="TRUSTED_ANONYMOUS_IPS")
        conf.value="0.0.0.0/0"
        conf.save()

        response = self.client.get(reverse('app_sirene:anonymous'))
        self.assertEqual(response.status_code, 200)

        #print(global_aaa)

        response = self.client.get(reverse('app_sirene:private'))
        self.assertEqual(response.status_code, 302)



class AppSireneSysadminTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        # load default conf in DB
        # load APPS, ROLES, PERMS in DB
        cavaliba_update(verbose=False)

        conf = CavalibaConfiguration.objects.get(appname="user", keyname="AUTH_MODE")
        conf.value = "forced"
        conf.save()


        conf = CavalibaConfiguration.objects.get(appname="user", keyname="AUTH_MODE_FORCE_USER")
        conf.value = "admin"
        conf.save()

        conf = CavalibaConfiguration.objects.get(appname="user", keyname="DEBUG_AAA")
        conf.value = "no"
        conf.save()

    # def setUp(self):
        
    #     # load default conf in DB
    #     # load APPS, ROLES, PERMS in DB
    #     cavaliba_update()

    def test_init(self):
        self.assertEqual(True, True)

    def test_appname(self):
        r = get_configuration("home", "GLOBAL_APPNAME")
        self.assertEqual(r, 'Cavaliba')

        r = get_configuration(keyname="GLOBAL_APPNAME")
        self.assertEqual(r, 'Cavaliba')



    def test_conf_no_skip_public(self):
        r = CavalibaConfiguration.objects.get(appname="sirene", keyname="PUBLIC_SKIP_TO_TRUSTED")
        self.assertEqual(r.value, 'no')


    def test_public(self):
        response = self.client.get(reverse('app_sirene:index'))
        self.assertEqual(response.status_code, 200)

    def test_anonymous(self):
        response = self.client.get(reverse('app_sirene:anonymous'))
        # user = admin
        self.assertEqual(response.status_code, 200)


    def test_trusted_ip(self):
        conf = CavalibaConfiguration.objects.get(appname="user",keyname="TRUSTED_ANONYMOUS_IPS")
        conf.value="0.0.0.0/0"
        conf.save()

        response = self.client.get(reverse('app_sirene:anonymous'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('app_sirene:private'))
        self.assertEqual(response.status_code, 200)





class AppSireneUserTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        # load default conf in DB
        # load APPS, ROLES, PERMS in DB
        cavaliba_update(verbose=False)

        user = SireneUser.objects.create(login="unittest", firstname="unittestname")
        user.save()


        role = role_get_by_name("role_sirene_user")
        role.users.add(user)
        role.save()

        # force mode
        conf = CavalibaConfiguration.objects.get(appname="user", keyname="AUTH_MODE")
        conf.value = "unittest"
        conf.save()


        conf = CavalibaConfiguration.objects.get(appname="user", keyname="DEBUG_AAA")
        conf.value = "no"
        conf.save()


    # def test_auth(self):
    #     self.assertEqual(True, True)


    def test_user_public(self):
        response = self.client.get(reverse('app_sirene:index'))
        self.assertEqual(response.status_code, 200)


    def test_user_anonymous(self):
        response = self.client.get(reverse('app_sirene:anonymous'))
        self.assertEqual(response.status_code, 200)


    def test_user_private(self):
        response = self.client.get(reverse('app_sirene:private'))
        self.assertEqual(response.status_code, 200)

    def test_user_history(self):
        response = self.client.get(reverse('app_sirene:history'))
        self.assertEqual(response.status_code, 200)


# Denied

    def test_user_message_editor(self):
        response = self.client.get(reverse('app_sirene:message_editor'))
        self.assertEqual(response.status_code, 302)


# -- flush all GET/POST
    def test_user_flushall_get(self):
        response = self.client.post(reverse('app_sirene:flushall'), follow=True)
        a = ('/sirene/', 302)
        #print(response.redirect_chain)
        self.assertTrue( a in response.redirect_chain)
        

# --------------------------------------------------
# Sirene Operator
# --------------------------------------------------
class AppSireneOperatorTest(TestCase):


    @classmethod
    def setUpTestData(cls):

        # load default conf in DB
        # load APPS, ROLES, PERMS in DB
        cavaliba_update(verbose=False)


        user = SireneUser.objects.create(login="unittest", firstname="unittestname")
        user.save()

        role = role_get_by_name("role_sirene_operator")
        role.users.add(user)
        role.save()

        # force mode
        conf = CavalibaConfiguration.objects.get(appname="user", keyname="AUTH_MODE")
        conf.value = "unittest"
        conf.save()

        conf = CavalibaConfiguration.objects.get(appname="user", keyname="DEBUG_AAA")
        conf.value = "no"
        conf.save()



    def test_operator_public(self):
        response = self.client.get(reverse('app_sirene:index'))
        self.assertEqual(response.status_code, 200)


    def test_operator_anonymous(self):
        response = self.client.get(reverse('app_sirene:anonymous'))
        self.assertEqual(response.status_code, 200)


    def test_operator_private(self):
        response = self.client.get(reverse('app_sirene:private'))
        self.assertEqual(response.status_code, 200)

    def test_operator_history(self):
        response = self.client.get(reverse('app_sirene:history'))
        self.assertEqual(response.status_code, 200)


    def test_operator_message_editor(self):
        response = self.client.get(reverse('app_sirene:message_editor'))
        self.assertEqual(response.status_code, 200)


    def test_operator_smsjournal(self):
        response = self.client.get(reverse('app_sirene:sms_journal'))
        self.assertEqual(response.status_code, 200)

# -- TEMPLATE
    def test_operator_template_selector(self):
        response = self.client.get(reverse('app_sirene:template_selector'))
        self.assertEqual(response.status_code, 200)


    def test_operator_template_list(self):
        response = self.client.get(reverse('app_sirene:template_list'))
        self.assertEqual(response.status_code, 200)

    # can read (200) form, but not submit
    def test_operator_template_edit(self):
        response = self.client.get(reverse('app_sirene:template_edit'))
        self.assertEqual(response.status_code, 200)


# -- flush all GET/POST
    def test_operator_flushall_get(self):
        response = self.client.get(reverse('app_sirene:flushall'), follow=True)
        #self.assertEqual(response.status_code, 302)
        a = ('/sirene/', 302)
        #print(response.redirect_chain)
        self.assertTrue( a in response.redirect_chain)

    def test_operator_flushall_post(self):
        response = self.client.post(reverse('app_sirene:flushall'), follow=True)
        a = ('/sirene/private/', 302)
        #print(response.redirect_chain)
        self.assertTrue( a in response.redirect_chain)


# -- CATEGORY

    def test_auth_allperm_category_list(self):
        response = self.client.get(reverse('app_sirene:category_list'))
        self.assertEqual(response.status_code, 200)

    def test_auth_allperm_category_edit(self):
        response = self.client.get(reverse('app_sirene:category_edit'))
        self.assertEqual(response.status_code, 200)



