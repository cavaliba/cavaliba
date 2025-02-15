# (c) cavaliba.com

# django command / load_model.py
# load data from YAML files in the Cavaliba database

import yaml
import json
import os

from django.core.management.base import BaseCommand, CommandError

from app_home.configuration import get_configuration
from app_home.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL
from app_home.log import purge


class Command(BaseCommand):

    help = 'Purge log table - use optional keep_days to preserve logs ; 0 removes all'

    def add_arguments(self, parser):

        parser.add_argument('keep_days', nargs='?', type=int)

        # Named (optional) arguments
        parser.add_argument(
            '--verbose', 
            action='store_true',
            help='Verbose mode',
        )


    def handle(self, *args, **options):

        keep_days = options.get("keep_days",None)

        if keep_days is None:
            keep_days = int(get_configuration("home", "LOG_KEEP_DAYS"))


        count = purge(keep_days=keep_days)

        if keep_days == 0:
            print(f"deleted all: {count} entries")
        else:
            print(f"deleted older than {keep_days} days : {count} entries")

        log(INFO, app="log", view="manage_command", action="purge", status="OK", data=f"{count} entries removed")

        self.stdout.write("Done\n")

        