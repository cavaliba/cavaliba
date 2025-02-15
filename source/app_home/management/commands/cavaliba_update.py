# (c) cavaliba.com


# django command / cavaliba_update.py
# Update default configuration, apps, roles, groups
# (add new entries, purge orphans)

import sys
import yaml
import json
import os
from pprint import pprint

from django.core.management.base import BaseCommand, CommandError

from app_home.home import cavaliba_update


class Command(BaseCommand):
    help = 'Cavaliba Update : update configuration, roles, permissions, dashboard'

    def handle(self, *args, **options):

        cavaliba_update()
        self.stdout.write("Done\n")
        

