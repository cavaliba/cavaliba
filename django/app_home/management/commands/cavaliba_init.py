# (c) Cavaliba 2020-2024


# django command / cavaliba_init.py
# Create initial config,user, groups, roles


import yaml
import json
import os
from pprint import pprint

from django.core.management.base import BaseCommand, CommandError

from app_home.home import cavaliba_init





class Command(BaseCommand):
    help = 'Cavaliba Init : load initial config, admin users and data model'

    # https://docs.python.org/3/library/argparse.html#name-or-flags
    # def add_arguments(self, parser):
    #     parser.add_argument('filenames', nargs='+', type=str)

    def handle(self, *args, **options):

        cavaliba_init()


