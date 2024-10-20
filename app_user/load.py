# app_user - load.py

import re

from app_user.user import user_import

from app_user.user import user_create
from app_user.user import user_update_by_data
from app_user.user import user_delete_by_data
from app_user.user import user_enable_by_data
from app_user.user import user_disable_by_data

from app_user.group import group_import
from app_user.role import role_import



    # login = data.get('login', None)
    # if not login:
    #     return

    # action = data.get("_action", "create_or_update")
    
    # if action == "create":
    #     user = user_create(data)

    # elif action == "update":
    #     user = user_update_by_data(data)

    # elif action == "delete":
    #     user = user_delete_by_data(data)

    # else:
    #     user = user_create(data)

    # return user, action

def load_user2(filedata, force_action=None, verbose=None):

    count = 0
    
    for item,data in filedata.items():
    
        if not item.startswith("_user:"):
            continue

        login = re.sub("^_user:", '', item)

        if login == "":
            continue

        if not data:
            data = {}

        data["login"] = login

        action = data.get("_action", force_action)
        if not action:
            action = "create_or_update"
    

        if action == "create":
            user = user_create(data)

        elif action == "create_or_update":
            user = user_create(data)
            user = user_update_by_data(data)

        elif action == "update":
            user = user_update_by_data(data)

        elif action == "delete":
            user = user_delete_by_data(data)

        elif action == "enable":
            user = user_enable_by_data(data)

        elif action == "disable":
            user = user_disable_by_data(data)

        else:
            # unknown action
            pass

        if user:
            count += 1
            if verbose:
                print(f"load_user: {action} - {login}")


    return count

def load_user(filedata):

    # # multiple entries : _user:
    # if "_user" in filedata:
    #     datalist = filedata["_user"]
    #     for row in datalist:    
    #         # action = row.get("action", "create_or_update")
    #         # login = row.get('login', None)
    #         login, action = user_import(row)
    #         if login:
    #             print(f"  user {action} - {login}")

    count = 0

    # single user entry
    for item,data in filedata.items():
        if item.startswith("_user:"):
            login = re.sub("^_user:", '', item)
            if login == "":
                continue
            if not data:
                data = {}
            #action = data.get("action", "create_or_update")
            data["login"] = login
            r, action = user_import(data)
            if r:
                print(f"  user {action} - {login}")


def load_group(filedata):

    # if "_group" in filedata:
    #     data = filedata["_group"]
    #     group_import_dictlist(data)


    if "_group" in filedata:
        datalist = filedata["_group"]
        for row in datalist:    
            # action = row.get("action", "create_or_update")
            # login = row.get('login', None)
            group, action = group_import(row)
            if group:
                print(f"  group {action} - {group}")


    for item,data in filedata.items():
        if item.startswith("_group:"):
            keyname = re.sub("^_group:", '', item)
            if keyname == "":
                continue
            #action = data.get("action", "create_or_update")
            if not data:
                data = {}
            data["keyname"] = keyname
            r, action = group_import(data)
            if r:
                print(f"  group {action} - {keyname}")


def load_role(filedata):

    # if "_role" in filedata:
    #     data = filedata["_role"]
    #     role_import_dictlist(data)


    if "_role" in filedata:
        datalist = filedata["_role"]
        for row in datalist:    
            role, action = role_import(row)
            if role:
                print(f"  role {action} - {role}")


    for item,data in filedata.items():
        if item.startswith("_role:"):
            keyname = re.sub("^_role:", '', item)
            if keyname == "":
                continue
            if not data:
                data = {}
            data["keyname"] = keyname
            r, action = role_import(data)
            if r:
                print(f"  role {action} - {keyname}")


