# (c) cavaliba.com

# django command / cavaliba_load.py
# load data from CSV/JSON/YAML file to DB

import os
import csv 
import re
import json

from pprint import pprint

from django.core.management.base import BaseCommand, CommandError

from app_data.loader import load_file_yaml
from app_data.loader import load_file_json
from app_data.loader import load_file_csv

from app_data.pipeline import apply_pipeline
from app_data.pipeline import get_pipeline

from app_data.loader import load_broker



class Command(BaseCommand):
    help = 'Load a YAML/JSON/CSV file to database'

    # https://docs.python.org/3/library/argparse.html#name-or-flags
    def add_arguments(self, parser):
        parser.add_argument('--pipeline', type=str, help="pipeline to preprocess data")
        parser.add_argument('--force_action', type=str, help="override _action field in files")      
        parser.add_argument('--first', type=int, default=1, help="first line to load. default 1")
        parser.add_argument('--last', type=int, default=1, help="last line to load. Default 0 (last)")
        parser.add_argument('--pass', type=int, default=1, help="default 1 , increase number for relationships between objects")
        parser.add_argument('--dryrun', action='store_true', help='Dry run, no loading. Use verbose to see data' )
        parser.add_argument('--verbose', action='store_true', help='Verbose mode' )
        parser.add_argument('--progress', action='store_true', help='Display progress' )
        # parser.add_argument('--test', action='store_true', help='Test/do nothing' )
        parser.add_argument('filenames', nargs='+', type=str)


    def handle(self, *args, **options):

        verbose = options.get("verbose", True)

        print("="*60)
        first = options.get("first", 1)
        last = options.get("last", 0)
        if last > 0 and last < first:
            print("ERR - invalid first/last values")
            exit(0)
        print(f"first/last:  {first}, {last}")


        # pipeline
        pipeline = options.get("pipeline", None)
        # TODO : chech w/ regexp
        if pipeline:
            print(f"pipeline:    {pipeline}")
            pipeline_data = get_pipeline(pipeline)
            if not pipeline_data:
                print(f"ERR - invalid pipeline {pipeline}")
                exit(0)
            if verbose:
                print(json.dumps(pipeline_data, indent=2, ensure_ascii=False))

        # force_action
        force_action = options.get("force_action", None)
        if force_action:
            if force_action not in ["create", "init","update", "delete", "enable", "disable"]:
                print(f"ERR - invalid force_action {force_action}")
                exit(0)
            print(f"force_action: {force_action}")

        # pass count
        passcount = options.get("pass", 1)
        print(f"pass:        {passcount}")

        # dryrun
        dryrun = options.get("dryrun", None)
        print(f"dryrun:      {dryrun}")

        # progress
        progress = options.get("progress", False)
        print(f"progress:    {progress}")

        # build file list ordered
        ordered = []
        for fileentry in options['filenames']:
            if os.path.isfile(fileentry):
                ordered.append(fileentry)
            elif os.path.isdir(fileentry):
                for item in os.scandir(fileentry):
                    if item.is_file(follow_symlinks=False):
                        if item.path not in ordered:
                            ordered.append(item.path)
                ordered.sort()
            else:
                print(f"SKIP - Unknown filename: {fileentry}")
                

        for passcurrent in range(1,passcount+1):

            print("="*60)
            print(f"pass : {passcurrent} / {passcount}")
            print("="*60)


            for filename in ordered:

                print()
                print(f"File: {filename} ...")
                datalist = []

                if filename.endswith('.csv'):
                    datalist = load_file_csv(filename,pipeline=pipeline,first=first,last=last)

                elif filename.endswith('.yml') or filename.endswith('.yaml'):
                    datalist = load_file_yaml(filename,pipeline=pipeline,verbose=verbose)

                elif filename.endswith('.json'):
                    datalist = load_file_json(filename,pipeline=pipeline,verbose=verbose)

                else:
                    print(f"SKIP - Unknown filtetype ({filename})")
                    continue

                if not datalist:
                    print(f"SKIP - no data in ({filename})")
                    continue
                    
                if len(datalist) == 0:
                    print(f"SKIP - empty data in ({filename})")
                    continue

                print("Found: ", len(datalist), "objects")

                if verbose:
                    print(json.dumps(datalist, indent=2, ensure_ascii=False))
                
                # apply pipeline
                print(f"Pipeline: {pipeline}")
                if pipeline:
                    datalist = apply_pipeline(pipeline=pipeline, datalist=datalist)

                if verbose:
                    print(json.dumps(datalist, indent=2, ensure_ascii=False))

                # load to DB
                if not dryrun:
                    print("Loading to DB...")
                    aaa = {'perms':'*'}
                    r = load_broker(datalist, aaa=aaa, force_action=force_action, verbose=verbose, progress=progress)
                    #if verbose:
                    print(f"Loaded: {r} objects")
                else:
                    print("Dryrun : no DB action")

        # END
        self.stdout.write("Done\n")
