# (c) cavaliba.com


# django command / sirene_load.py
# load data from YAML files in the Cavaliba  database



import os

from pprint import pprint

from django.core.management.base import BaseCommand, CommandError


from app_data.data import update_bigset


class Command(BaseCommand):
    help = 'Update class bigset / count_estimation'

    # https://docs.python.org/3/library/argparse.html#name-or-flags
    # def add_arguments(self, parser):
    #     parser.add_argument('filenames', nargs='+', type=str)

    def handle(self, *args, **options):

        update_bigset()
        self.stdout.write("Done\n")


