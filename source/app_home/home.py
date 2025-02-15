# (c) cavaliba.com - home - home.py

import yaml

from .cavaliba import GLOBAL_BUILTIN_DATA

#from .configuration import get_configuration
from .configuration import init_configuration
from .configuration import update_configuration

from .configuration_default import CONFIGURATION_DEFAULT

from .models import DashboardApp

import app_home.register as app_home
import app_data.register as app_data
import app_user.register as app_user
import app_sirene.register as app_sirene

from app_data.loader import load_broker

# --------------------------------------------
# Cavaliba Apps
# --------------------------------------------

def get_cavaliba_apps():

    reply = []

    appnames = [ i for i in CONFIGURATION_DEFAULT ]
    for appname in appnames:
        appobj = DashboardApp.objects.filter(keyname=appname).first()
        if appobj:
            reply.append(appobj)

    return reply



def get_app_by_name(appname):
    app = DashboardApp.objects.filter(keyname=appname).first()
    return app



def get_applist(aaa=None):
    '''  UI Home / Private ; filter: enabled + perm = True'''
    
    apps = DashboardApp.objects.all().prefetch_related("permission").order_by("order")

    reply = []

    for app in apps:

        if not app.is_enabled:
            continue
            
        app.is_allowed = False
        try:
            if app.permission.keyname in aaa["perms"]:
                app.is_allowed = True
        except Exception as e:
            print(e)
            pass

        reply.append(app)
            
    return reply


def get_sidebar(aaa=None):
    '''  CTX Processor : sidebar entries ; filter: enabled + perm = True'''
    
    entries = DashboardApp.objects.all().prefetch_related("permission").order_by("order")

    reply = []

    for entry in entries:

        if not entry.is_enabled:
            continue
            
        entry.is_allowed = False
        try:
            if entry.permission.keyname in aaa["perms"]:
                entry.is_allowed = True
        except Exception as e:
            print(e)
            pass

        reply.append(entry)

    return reply


# --------------------------------------------
# init / update
# --------------------------------------------

def cavaliba_init(verbose=False):
    ''' init cavaliba to factory default '''

    init_configuration(verbose=verbose)
    load_builtin(force_action="init", verbose=verbose)


def cavaliba_update(verbose=False):

    update_configuration(verbose=verbose)
    load_builtin(force_action="init", verbose=verbose)


def load_builtin(force_action="init", verbose=True):

    builtins = [
        GLOBAL_BUILTIN_DATA,
        app_user.BUILTIN_DATA,
        app_home.BUILTIN_DATA,
        app_data.BUILTIN_DATA,
        app_sirene.BUILTIN_DATA,
    ]

    # aggregate
    raw = '\n'.join(builtins)
    content = yaml.safe_load(raw)

    # split
    content_permission = []
    content_role = []
    content_group = []
    content_user = []
    content_schema = []
    content_home = []
    content_other = []


    for datadict in content:

        #datadict["_action"] = force_action

        if datadict["classname"] == "_permission":
            content_permission.append(datadict)

        if datadict["classname"] == "_role":
            content_role.append(datadict)

        if datadict["classname"] == "_group":
            content_group.append(datadict)

        if datadict["classname"] == "_user":
            content_user.append(datadict)

        if datadict["classname"] == "_schema":
            content_schema.append(datadict)

        if datadict["classname"] == "_home":
            content_home.append(datadict)
            
        else:
            content_other.append(datadict)


    # # load
    aaa = {'perms':'*'}
    load_broker(datalist=content_permission, aaa=aaa, force_action=force_action, verbose=verbose)
    load_broker(datalist=content_role, aaa=aaa, force_action=force_action, verbose=verbose)
    load_broker(datalist=content_group, aaa=aaa, force_action=force_action, verbose=verbose)
    load_broker(datalist=content_user, aaa=aaa, force_action=force_action, verbose=verbose)
    load_broker(datalist=content_schema, aaa=aaa, force_action=force_action, verbose=verbose)
    load_broker(datalist=content_home, aaa=aaa, force_action=force_action, verbose=verbose)
    load_broker(datalist=content_other, aaa=aaa, force_action=force_action, verbose=verbose)




