# (c) Cavaliba 2023 - Sirene


# django command / load_model.py
# load data from YAML files in the sirene database

import yaml
import json
import random 

from django.core.management.base import BaseCommand, CommandError


CAT=10
PUBLIC=20
PREDEFINED=50
APP=100
SITE=200
USER=300
USERGROUP=50
SITEGROUP=40

CAT=3
PUBLIC=3
PREDEFINED=5
APP=3
SITE=3
USER=3
USERGROUP=3
SITEGROUP=3


def get_login():
    i = random.randint(0,USER-1)
    return f"login{i}"

def get_login_list(n):
    r = []
    count = 0
    while len(r) < n:
        u2=get_login()
        if not u2 in r:
            r.append(u2)    
        else:
            count += 1
        if count > 20:
            return r
    return r


def get_category():
    i = random.randint(0,CAT-1)
    return f"category{i}"

def get_public():
    i = random.randint(0,PUBLIC-1)
    return f"public{i}"


def get_role():
    values = ["user","contact","localadmin","globaladmin","ops"]
    return random.choice(values)

def get_severity():
    values = ["na","ok", "info","minor","major","critical","other"]
    return random.choice(values)


def get_app():
    i = random.randint(0,APP-1)
    return f"app{i}"

def get_app_list_name(n):
    r = []
    for j in range(n):
        u2=get_app()
        r.append({"name":u2})
    return r

def get_site():
    i = random.randint(0,SITE-1)
    return f"site{i}"

def get_site_list(n):
    r = []
    count = 0
    while len(r) < n:
        u2=get_site()
        if not u2 in r:
            r.append(u2)    
        else:
            count += 1
        if count > 20:
            return r
    return r


def get_sitegroup():
    i = random.randint(0,SITEGROUP-1)
    return f"sitegroup{i}"

def get_sitegroup_list(n):
    r = []
    count = 0
    while len(r) < n:
        u2=get_sitegroup()
        if not u2 in r:
            r.append(u2)    
        else:
            count += 1
        if count > 20:
            return r
    return r
    

class Command(BaseCommand):
    help = 'Generate a fake Data Set'

    def add_arguments(self, parser):

        #parser.add_argument('filenames', nargs='+', type=str)
        # Named (optional) arguments
        parser.add_argument(
            '--verbose', 
            action='store_true',
            help='Verbose mode',
        )
        # if options['delete']:
        #     poll.delete()

    def handle(self, *args, **options):

        verbose = False 
        if options["verbose"]:
            verbose = True

        data = {}



        users=[]
        for i in range(0,USER):
            user={}
            user["login"] = f"login{i}"
            user["mail"] = f"user{i}@test.mail"
            user["mobile"] = random.randint(1111111111,9999999999)
            user["name"] = f"User Name {i}"
            user["description"] = f"Description for user {i}"
            user["is_enabled"] = True
            user["site"] = get_site()
            user["role"] = get_role()
            users.append(user)

        # user_groups
        usergroups=[]
        for i in range(0,USERGROUP):
            ug={}
            ug["name"] = f"usergroup{i}"
            ug["description"] = f"Description for UserGroup {i}"
            ug["is_enabled"] = True
            ug["users"]=get_login_list(3)
            usergroups.append(ug)

        # sitegroups
        sitegroups=[]
        for i in range(0,SITEGROUP):
            sg={}
            sg["description"] = f"Description for sitegroup{i}"
            sg["name"] = f"sitegroup{i}"
            sg["sites"] = get_site_list(4)
            # notify_to:
            sitegroups.append(sg)          

        # sites
        sites=[]
        for i in range(0,SITE):
            site={}
            site["description"] = f"Description for site{i}"
            site["name"] = f"site{i}"
            # apps: []
            site["apps"] = get_app_list_name(5)
            # notify_to: []
            # notify_apps: []
            # sitegroups: []
            # users: []
            sites.append(site)          

        # apps
        apps=[]
        for i in range(0,APP):
            app={}
            app["description"] = f"Description for appname{i}"
            app["name"] = f"app{i}"
            app["site"] = get_site()
            # notify_to
            app["is_enabled"] = True
            apps.append(app)


        # categories
        categories=[]
        for i in range(0,CAT):
            cat={}
            cat["longname"] = f"Long name for category{i}"
            cat["name"] = f"category{i}"
            cat["is_enabled"] = True
            categories.append(cat)


        publicpages=[]
        for i in range(0,PUBLIC):
            pub={}
            pub["name"] = f"public{i}"
            pub["title"] = f"Title Public {i}"
            pub["description"] = f"Description for public page {i}"
            pub["message"] = f"Public{i} Lorem ipsum, lorem ipsum\nLorem2 ipsum2, Lorem2 ipsum2.\nSirene."
            pub["severity"] = get_severity()
            publicpages.append(pub)

        # predefind_messages
            # - name: msg_test
            #   title: Sirene - TEST TEST TEST - message de test
            #   category: test
            #   severity: info
            #   publicpage: test
            #   message: |
            #     TEST TEST TEST
            #     Ceci est un message de test.
            #   privatepage: true
            #   email: true
            #   sms: true
            #   description: Message de test.
            #   notify_to: 
            #     - group:group01
            #     - g:group02
        predefined=[]
        for i in range(0,PREDEFINED):
            pre={}
            pre["name"] = f"predefined{i}"
            pre["title"] = f"Title Predefined {i}"
            pre["category"] =  get_category()
            pre["severity"] = get_severity()
            pre["message"] = f"Predefined {i} Lorem ipsum, lorem ipsum\nLorem2 ipsum2, Lorem2 ipsum2.\nSirene."
            pre["description"] = f"Description for predefined {i}"
            pre["publicpage"] = get_public()
            pre["privatepage"] = True
            pre["email"] = True
            pre["sms"] = True
            # notify_to

            predefined.append(pre)





        # ALL
        data["apps"] = apps
        data["sites"] = sites
        data["users"] = users
        data["user_groups"] = usergroups
        data["site_groups"] = sitegroups
        data["categories"] = categories
        data["public_pages"] = publicpages
        data["predefined_messages"] = predefined
        #print(json.dumps(data, indent=2))

        print(yaml.dump(data))







