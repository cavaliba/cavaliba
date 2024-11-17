# app_user - permission.py

import re


from app_home.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL
from .models import SirenePermission



def permission_get_by_id(pid):
    return SirenePermission.objects.filter(pk=pid).first()


def permission_get_by_name(keyname):
    return SirenePermission.objects.filter(keyname=keyname).first()


def permission_get_by_data(data):
    
    keyname = data.get('keyname', None)
    if not keyname:
        return
    return  permission_get_by_name(keyname)




def permission_set(keyname=None, appname=None, displayname=None, description=None, default=False):
    
    ''' create/update a single permission in Database '''

    if not keyname:
        return

    p = permission_get_by_name(keyname)
    if not p:
        p = SirenePermission()
        p.keyname = keyname

    if appname:
        p.appname = appname

    if displayname:
        p.displayname = displayname

    if description:        
        p.description = description

    p.default = default
    p.save()

    return p



def permission_init(data):

    keyname = data.get('keyname', None)
    if not keyname:
        return

    # skip if exists
    entry = permission_get_by_name(keyname)
    if entry:
        return

    entry = SirenePermission()
    entry = permission_update(entry, data)

    return entry



def permission_create(data):

    keyname = data.get('keyname', None)
    if not keyname:
        return

    # create or update
    entry = permission_get_by_name(keyname)
    if not entry:
        entry = SirenePermission()

    entry = permission_update(entry, data)

    return entry


def permission_update(iobj, data):
    ''' update Object with data dict info'''

    attributs =  [
        "keyname", "appname", "displayname", "description","is_builtin", "default",
    ] 

    if not iobj:
        return

    if not data:
        return

    for attrib in attributs:
        if attrib in data:
            try:
                setattr(iobj, attrib, data[attrib])
            except:
                pass

    #iobj.last_update = timezone.now()
    iobj.save()
    return iobj


def permission_update_by_data(data):

    iobj = permission_get_by_data(data)
    if iobj:
        return permission_update(iobj, data)



def permission_delete(iobj):

    if not iobj:
        return False

    if iobj.is_builtin:
        return False
    
    try:
        iobj.delete()
        return True
    except Exception as e:
        print("permission_delete failed : ",e)
        return False


def permission_delete_by_id(pid):

    iobj = permission_get_by_id(pid)
    r = permission_delete(iobj)
    return iobj



def permission_delete_by_data(data):

    iobj = permission_get_by_data(data)
    if iobj:
        return permission_delete_by_id(iobj.id)


# # Called by commands / external to sync permissions for this app
# def permission_register(appname, permissions):

#     #total, created, deleted, invalid  = permission_set_all_for_app(appname=appname, permlist=permissions)

#     total = 0
#     created = 0
#     deleted = 0
#     invalid = 0
 
#     if not permissions:
#         return

#     perm_list = []

#     # add permissions
#     for permtuple in permissions:

#         try:
#             (keyname, displayname, description, default) = permtuple
#         except:
#             invalid += 1
#             continue

#         perm_list.append(keyname)

#         p = permission_set(keyname=keyname, appname=appname, displayname=displayname, description=description, default=default)
#         if p:
#             created += 1


#     # Remove unused permissions from DB
#     perms = SirenePermission.objects.filter(appname=appname).all()
#     for perm in perms:
#         if perm.keyname not in perm_list:
#             perm.delete()
#             deleted += 1

#     total = SirenePermission.objects.filter(appname=appname).count()

#     #print (f"Register permissions for {appname} - total={total} created={created} deleted={deleted} invalid={invalid}")

#     return total, created, deleted, invalid

# -------------------------------------------------------
# IMPORTS
# -------------------------------------------------------
def load_permissions(filedata, force_action=None, verbose=None):

    count = 0

    # _role:rolename: {}
    for item,data in filedata.items():
        if not item.startswith("_permission:"):
            continue

        keyname = re.sub("^_permission:", '', item)
        if keyname == "":
            continue
        if not data:
            data = {}
        data["keyname"] = keyname

        action = force_action
        if not action:
            action = data.get("_action", "create")

        if action == "init":
            perm = permission_init(data)

        elif action == "create":
            perm = permission_create(data)
            perm = permission_update_by_data(data)

        elif action == "update":
            perm = permission_update_by_data(data)

        elif action == "delete":
            perm = permission_delete_by_data(data)

        # elif action == "enable":
        #     perm = permission_enable_by_data(data)

        # elif action == "disable":
        #     perm = permission_disable_by_data(data)
        else:
            pass

        if perm:
            count += 1
            if verbose:
                print(f"permission: {action} - {keyname}")

    return count


# def permission_import(data):

#     TRUE_LIST = ('on', 'On', 'ON', True, 'yes', 'Yes', 'YES', 'True', 'true', 'TRUE', 1, "1")

#     keyname = data.get('keyname', None)
#     if not keyname:
#         return

#     appname = data.get('appname', "")
#     displayname = data.get('displayname', "")
#     description = data.get('description', "")
#     default = data.get("default", False) in TRUE_LIST
#     is_builtin = data.get("is_builtin", False) in TRUE_LIST

#     # create, delete
#     action = data.get("action", "create")

#     if action == "create":
#         perm = permission_create(data)

#     elif action == "init":
#         perm = permission_init(data)
 
#     elif action == "delete":
#         perm = permission_delete_by_data(data)

#     elif action == "update":
#         perm = permission_update_by_data(data)

#     else:
#         perm = None

#     return perm, action

