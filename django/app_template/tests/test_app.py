# test_{{ app_name }} 
# (c) cavaliba.com

from django.test import TestCase, override_settings
from django.urls import reverse

#from {{ app_name }}..models import XXXXXXXXx;


#self.assertRedirects(response, '/accounts/login/?next=/catalog/mybooks/')
#self.assertEqual(r.value, 'no')



class BasicTest(TestCase):

    def setUp(self):

        pass
        # init_configuration_to_db()
        # aaa_init_permissions()


    def test_test(self):
        self.assertEqual('a', 'a')


    # def test_anonymous_public(self):
    #     response = self.client.get(reverse('{{ app_name }}:index'))
    #     self.assertEqual(response.status_code, 200)




class FixtureTest(TestCase):

    pass
    # fixtures = ["test_data.json"]

    # def setUp(self):

    #     init_configuration_to_db()
    #     aaa_init_permissions()


    #     role = AAARole.objects.create(name="unittest")
    #     role.save()
    #     for perm in AAAPermission.objects.all():
    #         role.permissions.add(perm)
    #     role.save()

    #     user = SireneUser.objects.create(login="unittest", name="unittestname")
    #     user.roles.add(role)
    #     user.save()

    #     scope_clean()



    # def test_model_user(self):
    #     user = SireneUser.objects.get(login="unittest")
    #     self.assertEqual(user.name, 'unittestname')


    # def test_model_site(self):
    #     site = Site.objects.get(name="site01")
    #     #self.assertIsNotNone(site.id)
    #     self.assertEquals(site.name,"site01")


    # def test_get_scope_members(self):

    #     users = scope_get_members([], "user:unittest")
    #     self.assertEquals(len(users),1)

    #     users = scope_get_members([], "site:site01")
    #     self.assertEquals(len(users),0)




# class NoAuthAccessTestCase(TestCase):

#     def setUp(self):
#         init_configuration_to_db()
#         aaa_init_permissions()


#     def test_noauth_public(self):
#         response = self.client.get(reverse('index'))
#         self.assertEqual(response.status_code, 200)

#     def test_noauth_anonymous(self):
#         response = self.client.get(reverse('anonymous'))
#         self.assertEqual(response.status_code, 302)



# class AnonymousAccessTestCase(TestCase):

#     def setUp(self):
#         init_configuration_to_db()
#         aaa_init_permissions()
#         conf = Configuration.objects.get(key="TRUSTED_ANONYMOUS_IPS")
#         conf.value="0.0.0.0/0"
#         conf.save()


#     def test_anonymous_public(self):
#         response = self.client.get(reverse('anonymous'))
#         self.assertEqual(response.status_code, 200)


#     def test_anonymous(self):
#         response = self.client.get(reverse('anonymous'))
#         self.assertEqual(response.status_code, 200)


#     def test_anonymous_private(self):
#         response = self.client.get(reverse('private'))
#         self.assertEqual(response.status_code, 302)


# ----------------------------------------------------------
# Authenticated access with ALL perms
# ----------------------------------------------------------

# @override_settings(SIRENE_AUTH_MODE="unittest")
# class AuthAccessAllPermTestCase(TestCase):

#     def setUp(self):

#         init_configuration_to_db()
#         aaa_init_permissions()

#         role = AAARole.objects.create(name="unittest")
#         role.save()
#         for perm in AAAPermission.objects.all():
#             role.permissions.add(perm)
#         role.save()

#         user = SireneUser.objects.create(login="unittest", name="unittestname")
#         user.roles.add(role)
#         user.save()

#         Site.objects.create(name="site01", description="site01")


#     def test_auth_allperm_public(self):
#         response = self.client.get(reverse('index'))
#         self.assertEqual(response.status_code, 200)


#     def test_auth_allperm_anonymous(self):
#         response = self.client.get(reverse('anonymous'))
#         self.assertEqual(response.status_code, 200)


#     def test_auth_allperm_private(self):
#         response = self.client.get(reverse('private'))
#         self.assertEqual(response.status_code, 200)

#     def test_auth_allperm_selector(self):
#         response = self.client.get(reverse('selector'))
#         self.assertEqual(response.status_code, 200)

#     def test_auth_allperm_history(self):
#         response = self.client.get(reverse('history'))
#         self.assertEqual(response.status_code, 200)

 

# ----------------------------------------------------------
# Authenticated access with NO perms
# ----------------------------------------------------------

# @override_settings(SIRENE_AUTH_MODE="unittest")
# class AuthAccessNoPermTestCase(TestCase):

#     def setUp(self):

#         init_configuration_to_db()
#         aaa_init_permissions()

#         role = AAARole.objects.create(name="unittest")
#         role.save()
#         # for perm in AAAPermission.objects.all():
#         #     role.permissions.add(perm)
#         # role.save()

#         user = SireneUser.objects.create(login="unittest", name="unittestname")
#         user.roles.add(role)
#         user.save()

#         Site.objects.create(name="site01", description="site01")


#     def test_auth_noperm_public(self):
#         response = self.client.get(reverse('index'))
#         #self.assertRedirects(response, '/accounts/login/?next=/catalog/mybooks/')
#         self.assertEqual(response.status_code, 200)


#     def test_auth_noperm_anonymous(self):
#         response = self.client.get(reverse('anonymous'))
#         #self.assertRedirects(response, '/accounts/login/?next=/catalog/mybooks/')
#         self.assertEqual(response.status_code, 200)


    # def test_auth_noperm_private(self):
    #     response = self.client.get(reverse('private'))
    #     self.assertEqual(response.status_code, 302)



