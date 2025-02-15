# (c) cavaliba.com
# app_home - load.py

from app_home.cavaliba import TRUE_LIST
from .configuration import get_configuration


from app_home.models import DashboardApp

from app_user.permission import permission_get_by_name


# ---------------------------------------------------------------------
# Load HOME data struct
# ---------------------------------------------------------------------

def load_home(datadict=None, verbose=None):

    if not datadict:
        return

    keyname = datadict.get("keyname", None)
    if not keyname: 
        return

    action = datadict.get("_action", "create")

    r = None

    dbentry = DashboardApp.objects.filter(keyname=keyname).first()

    if action == "delete":
        if dbentry:
            dbentry.delete()


    elif action == "enable":
        if dbentry:
            dbentry.is_enabled = True
            dbentry.save()

    elif action == "disable":
        if dbentry:
            dbentry.is_enabled = False
            dbentry.save()

    elif action == "update":
        if dbentry:
            dbentry.keyname = keyname
            dbentry.displayname = datadict.get('displayname', keyname)
            dbentry.description = datadict.get('description', '')
            dbentry.url = datadict.get('url', '/')
            dbentry.icon = datadict.get('icon', 'fa-question')
            #dbentry.page = datadict.get('page', '')
            dbentry.sidebar_section = datadict.get('sidebar_section', '')
            dbentry.dashboard_section = datadict.get('dashboard_section', '')
            dbentry.order = datadict.get('order', 999)
            dbentry.is_enabled = datadict.get('is_enabled', True) in TRUE_LIST
            dbentry.save()

            # permissions
            if "permission" in datadict:
                p = datadict['permission']
                pobj = permission_get_by_name(p)
                if pobj:
                    dbentry.permission = pobj
                    dbentry.save()

    elif action == "create" or (action == "init" and not dbentry):

        if not dbentry:
            dbentry = DashboardApp()

        dbentry.keyname = keyname
        dbentry.displayname = datadict.get('displayname',keyname)
        dbentry.description = datadict.get('description','')
        dbentry.url = datadict.get('url', '/')
        dbentry.icon = datadict.get('icon', 'fa-question')
        #dbentry.page = datadict.get('page', '')
        dbentry.sidebar_section = datadict.get('sidebar_section', '')
        dbentry.dashboard_section = datadict.get('dashboard_section', '')
        dbentry.order = datadict.get('order', 999)
        dbentry.is_enabled = datadict.get('is_enabled', True) in TRUE_LIST
        dbentry.save() 

        # permissions
        if "permission" in datadict:
            p = datadict['permission']
            pobj = permission_get_by_name(p)
            if pobj:
                dbentry.permission = pobj
                dbentry.save() 

    # TODO: update only provided fields and sub-elements (permissions)
    elif action == "append":
        pass

    if dbentry:
        if verbose:
            print(f"dashboard: {action} - {keyname}")

    return dbentry

