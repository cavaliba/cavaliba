# (c) Cavaliba 2020-2024


# django command / cavaliba_update.py
# Update default configuration, apps, roles, groups
# (add new entries, purge orphans)


import yaml
import json
import os
from pprint import pprint

from django.core.management.base import BaseCommand, CommandError

from app_home.home import cavaliba_update


class Command(BaseCommand):
    help = 'Cavaliba Update : update configuration, roles, permissions, dashboard'

    # https://docs.python.org/3/library/argparse.html#name-or-flags
    # def add_arguments(self, parser):
    #     parser.add_argument('filenames', nargs='+', type=str)

    def handle(self, *args, **options):

        cavaliba_update()


