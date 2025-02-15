# (c) cavaliba.com
# CLI cavaliba_export

# Export Data structure to CSV/JSON/YAML


import os
import csv 
import re
import json
import yaml

from app_user.models import SireneUser
from app_user.models import SireneGroup
from app_user.models import SirenePermission

from app_data.models import DataClass

from app_user.user import user_listdict_format
from app_user.group import group_listdict_format
from app_user.role import role_listdict_format
from app_user.permission import permission_listdict_format

from app_sirene.export import sirene_export_dict

from app_data.data import data_listdict_format
from app_data.data import dataclass_listdict_format

from app_home.export import home_export_dict

from django.core.management.base import BaseCommand, CommandError


SCHEMA_LIST = ["user","group","role","permission", "home",
               "sirene", "sirene_category", "sirene_template", "sirene_public",
               "apikey", "dataview","enumerate","pipeline",
               "dataclass"
               ]

# YAML
class MyYamlDumper(yaml.SafeDumper):
    def write_line_break(self, data=None):
        super().write_line_break(data)
        if len(self.indents) < 2:
            super().write_line_break()



class Command(BaseCommand):
    help = 'Export DATA to YAML/JSON/CSV from database'

    # https://docs.python.org/3/library/argparse.html#name-or-flags
    def add_arguments(self, parser):
        parser.add_argument('--list', action='store_true', help="List available schemas")
        parser.add_argument('--schema', type=str, help="use --list to see available values")
        parser.add_argument('--format', type=str, default="yaml", help="yaml(default), json")
        parser.add_argument('--key', type=str, help="export specific keyname")
        parser.add_argument('--verbose', action='store_true', help='Verbose mode' )


    def handle(self, *args, **options):

        verbose = options.get("verbose", True)

        schema = options.get("schema", None)
        format = options.get("format", "yaml")
        if format not in ["yaml", "json"]:
            print(f"Unknown format: {format}")
            exit(0)

        key = options.get("key", None)

        # --list
        wantlist = options.get("list", None)
        if wantlist:
            print("Built-In schemas:")
            for i in SCHEMA_LIST:
                print('-',i)
            print()
            
            print("Custom schemas:")
            classes = DataClass.objects.all()
            for i in classes:
                if i.keyname in SCHEMA_LIST:
                    continue
                if i.keyname.startswith('_'):
                    if i.keyname[1:] in SCHEMA_LIST:
                        continue
                print('-', i)

            exit(0)

        filedata= []
        datalist = []

        # user
        if schema == "user":
            if key:
                users = SireneUser.objects.filter(login=key)
            else:
                users = SireneUser.objects.order_by('login').all()
            datalist = user_listdict_format(users)

        # group
        elif schema == "group":
            groups = SireneGroup.objects\
                .filter(is_role=False)\
                .prefetch_related("users")\
                .prefetch_related("subgroups")\
                .order_by('keyname')
            datalist = group_listdict_format(groups)

        # role
        elif schema == "role":
            roles = SireneGroup.objects\
                .filter(is_role=True)\
                .prefetch_related("permissions")\
                .prefetch_related("users")\
                .prefetch_related("subgroups")\
                .order_by('keyname')
            datalist = role_listdict_format(roles)

        # permission
        elif schema == "permission":
            permissions = SirenePermission.objects.all()
            datalist = permission_listdict_format(permissions)

        # sirene
        elif schema == "sirene":
            datalist = sirene_export_dict()

        elif schema == "sirene_public":
            datalist = sirene_export_dict(category=False, template=False, public=True)

        elif schema == "sirene_template":
            datalist = sirene_export_dict(category=False, template=True, public=False)

        elif schema == "sirene_category":
            datalist = sirene_export_dict(category=True, template=False, public=False)

        # home
        elif schema == "home":
            datalist = home_export_dict(keyname=key)
            

        # _builtin(s)
        elif schema in ["apikey", "enumerate", "dataview", "pipeline"]:
            classes = ["_" + schema]
            if key:
                datalist = data_listdict_format(classes=classes, keyname=key)
            else:
                datalist = data_listdict_format(classes=classes)            
            datalist = data_listdict_format(classes)

        elif schema == "dataclass":
            if key:
                datalist = dataclass_listdict_format(classes=[key])
            else:
                datalist = dataclass_listdict_format()

        # schema
        else:
            classes = [schema]
            if key:
                datalist = data_listdict_format(classes=classes, keyname=key)
            else:
                datalist = data_listdict_format(classes=classes)

        # ----

        if format == "yaml":
            filedata = yaml.dump(datalist, allow_unicode=True, Dumper=MyYamlDumper, sort_keys=False)

        elif format == "json":
            filedata = json.dumps(datalist, indent=4, ensure_ascii = False)

        elif format == "csv":
            pass

        else:
            exit(0)
            

        print(filedata)
