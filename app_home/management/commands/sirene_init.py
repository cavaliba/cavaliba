# (c) Cavaliba 2020-2024 - Sirene


# django command / sirene_load.py
# load data from YAML files in the sirene database


import yaml
import json
import os

from pprint import pprint

from django.core.management.base import BaseCommand, CommandError


from app_home.home import update_dashboard 



class Command(BaseCommand):
    help = 'Init Sirene - configuration, roles, permissions, dashboard'

    # https://docs.python.org/3/library/argparse.html#name-or-flags
    # def add_arguments(self, parser):
    #     parser.add_argument('filenames', nargs='+', type=str)

    def handle(self, *args, **options):

        update_dashboard()


