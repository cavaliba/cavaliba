# (c) Cavaliba 2020-2024 - Sirene


# django command / cavaliba_load.py
# load data from CSV/JSON/YAML file to DB



import os
import csv 
import re
import json

from pprint import pprint

from django.core.management.base import BaseCommand, CommandError

from app_home.home import load_file_yaml_to_data
from app_home.home import load_file_json_to_data
from app_home.home import load_file_csv_to_data

from app_home.home import load_dict
from app_home.home import apply_pipeline
from app_home.home import get_pipeline



class Command(BaseCommand):
    help = 'Load a YAML/JSON/CSV file to database'

    # https://docs.python.org/3/library/argparse.html#name-or-flags
    def add_arguments(self, parser):
        parser.add_argument('--pipeline', type=str, help="pipeline to preprocess data")
        parser.add_argument('--classname', type=str, help="for CSV file only (_user, _group, ...)")
        parser.add_argument('--force_action', type=str, help="override _action field in files")
        parser.add_argument('--csv_delimiter', type=str)
        #parser.add_argument('--no_csv_header', action='store_true', help="No columns name in file, use pipeline instead")
        
        parser.add_argument('--pass', type=int, default=1, help="default 1 , increase number for relationships between objects")
        parser.add_argument('--dryrun', action='store_true', help='Dry run, no loading. Use verbose to see data' )
        parser.add_argument('--verbose', action='store_true', help='Verbose mode' )
        parser.add_argument('filenames', nargs='+', type=str)


    def handle(self, *args, **options):

        # verbose = False 
        # if options["verbose"]:
        #     verbose = True
        verbose = options.get("verbose", True)

        print("==================")

        # pipeline
        pipeline = options.get("pipeline", None)
        # TODO : chech w/ regexp
        if pipeline:
            print(f"pipeline:  {pipeline}")
            pipeline_data = get_pipeline(pipeline)
            if not pipeline_data:
                print(f"ERR - invalid pipeline {pipeline}")
                exit(0)
            if verbose:
                print(json.dumps(pipeline_data, indent=2, ensure_ascii=False))



        # classname
        classname = options.get("classname", None)
        # TODO : chech w/ regexp
        if classname:
            print(f"classname: {classname}")

        # csv_delimiter
        csv_delimiter = options.get("csv_delimiter", None)
        # TODO : chech w/ regexp & len
        if csv_delimiter:
            print(f"csv_delimiter: {csv_delimiter}")

        # force_action
        force_action = options.get("force_action", None)
        if force_action:
            if force_action not in ["create", "init","update", "delete", "enable", "disable"]:
                print(f"ERR - invalid force_action {force_action}")
                exit(0)
            print(f"force_action: {force_action}")


        # pass 
        passcount = options.get("pass", 1)

        # dryrun
        dryrun = options.get("dryrun", None)
        print(f"dryrun:    {dryrun}")


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

            print("==================")
            print(f"pass : {passcurrent} / {passcount}")


            for filename in ordered:

                print()
                print(f"File: {filename} ...")
                data = {}

                if filename.endswith('.csv'):

                    data = load_file_csv_to_data(filename, \
                        pipeline=pipeline,\
                        #force_action=force_action,\
                        classname=classname,\
                        csv_delimiter=csv_delimiter,\
                        verbose=verbose)

                elif filename.endswith('.yml') or filename.endswith('.yaml'):

                    data = load_file_yaml_to_data(filename,\
                        pipeline=pipeline,\
                        verbose=verbose)

                elif filename.endswith('.json'):

                    data = load_file_json_to_data(filename,\
                        pipeline=pipeline,\
                        verbose=verbose)

                else:
                    print(f"SKIP - Unknown filtetype ({filename})")
                    continue

                if not data:
                    continue
                    
                if len(data) == 0:
                    continue

                print(f"Read: ", len(data), "objects")

                if verbose:
                    print(json.dumps(data, indent=2, ensure_ascii=False))
                

                # pipeline
                print("Pipeline")
                if pipeline:
                    print(f"... applying pipeline {pipeline}")
                    data = apply_pipeline(pipeline=pipeline, data=data, verbose=verbose)

                if verbose:
                    print(json.dumps(data, indent=2, ensure_ascii=False))

                # load to DB with force_action option
                if not dryrun:
                    print("Loading to DB ...")
                    r = load_dict(data, pipeline=pipeline, force_action=force_action, verbose=verbose)
                else:
                    print("dryrun : no DB action.")
