# app_home - configuration.py

# from django.shortcuts import render, redirect

from .models import CavalibaConfiguration
from .configuration_default import CONFIGURATION_DEFAULT

from .configuration_form import AppHomeConfigurationForm
from .configuration_form import AppUserConfigurationForm
from .configuration_form import AppSireneConfigurationForm
from .configuration_form import AppDataConfigurationForm


global_configuration = {}



# --------------------------------------------
# access
# --------------------------------------------


def load_configuration_cache():

    global global_configuration

    global_configuration = {}

    # first, load default
    for appname,appconfig in CONFIGURATION_DEFAULT.items():
        global_configuration[appname] = {}
        for k,v in appconfig.items():
            global_configuration[appname][k] = v

    # then, load from db
    dbconf = CavalibaConfiguration.objects.all()
    for item in dbconf:
        if item.appname not in global_configuration:
            global_configuration[item.appname] = {}
        global_configuration[item.appname][item.keyname] = item.value

    # NEXT: store in faster redis cache


def get_configuration(appname="home", keyname=None):

    global global_configuration

    if not global_configuration:
        load_configuration_cache()

    response = None

    try:
        response = global_configuration[appname][keyname]
    except Exception as e:
        print(f"Unkown configuration {appname} - {keyname} {e}")


    return response




# --------------------------------------------
# Form
# --------------------------------------------

def get_post_form(request, appname=None):

    global global_configuration
    if not global_configuration:
        load_configuration_cache()

    if not appname:
        return
        
    if appname not in global_configuration:
        return

    if appname == "sirene":
        form = AppSireneConfigurationForm(request.POST)
    elif appname == "home":
        form = AppHomeConfigurationForm(request.POST)
    elif appname == "user":
        form = AppUserConfigurationForm(request.POST)
    elif appname == "data":
        form = AppDataConfigurationForm(request.POST)
    else:
        form = None

    return form



def get_initial_form(appname=None):

    global global_configuration
    if not global_configuration:
        load_configuration_cache()

    if not appname:
        return

    if appname not in global_configuration:
        return

    initial = {}
    for k,v in global_configuration[appname].items():
        #print(appname, k,v)
        initial[k]=v

    if appname == "sirene":
        form = AppSireneConfigurationForm(initial=initial)
    elif appname == "home":
        form = AppHomeConfigurationForm(initial=initial)
    elif appname == "user":
        form = AppUserConfigurationForm(initial=initial)
    elif appname == "data":
        form = AppDataConfigurationForm(initial=initial)
    else:
        form = None
    return form



def save_form(form, appname=None):

    global global_configuration
    if not global_configuration:
        load_configuration_cache()

    if not appname:
        return

    if appname not in global_configuration:
        return

    if appname not in CONFIGURATION_DEFAULT:
        return


    appconfig = CONFIGURATION_DEFAULT[appname]


    for k,v in form.cleaned_data.items():

        if k in appconfig:
            dbentry = CavalibaConfiguration.objects.filter(appname=appname, keyname=k).first()
            if not dbentry:
                dbentry = CavalibaConfiguration()
                dbentry.appname = appname
                dbentry.keyname = k

            dbentry.value = v
            dbentry.save()

    # perform a new init to populate cache
    load_configuration_cache()


# -------------------------------------------------------------------
# commands
# -------------------------------------------------------------------



def init_configuration(verbose=True):
    ''' init configuration - add new default conf entries '''

    r = add_configuration(verbose=verbose)
    if verbose:
        print(f"configuration: entries created ({r})")




def update_configuration(verbose=True):
    ''' update configuration - add new default conf entries '''

    r1 = purge_configuration(verbose=verbose)
    if verbose:
        print(f"configuration: orphans purged ({r1})")

    r2 = add_configuration(verbose=verbose)
    if verbose:
        print(f"configuration: new entries created ({r2})")






# no direct call
def add_configuration(verbose=True):
    # add new/missing configuration entries with default values

    count = 0

    for appname, appconfig in CONFIGURATION_DEFAULT.items():

        for keyname,value in appconfig.items():

            # NEXT use global_configuration
            dbentry = CavalibaConfiguration.objects.filter(appname=appname, keyname = keyname).first()

            if not dbentry:
                dbentry = CavalibaConfiguration()
                dbentry.appname = appname
                dbentry.description = ""
                dbentry.page = ""
                dbentry.order = 100        
                dbentry.keyname = keyname
                dbentry.value = value
                dbentry.save()

                count += 1

    return count

# no direct call
def purge_configuration(verbose=True):
    ''' remove orphans conf entries '''
    
    count = 0

    dbentries = CavalibaConfiguration.objects.all()
    for dbentry in dbentries:

        # app not existing
        if dbentry.appname not in CONFIGURATION_DEFAULT:
            dbentry.delete()
            count += 1

        # entry for app not existing
        else:
            if dbentry.keyname not in CONFIGURATION_DEFAULT[dbentry.appname]:
                dbentry.delete()
                count += 1

    return count


def import_configuration():
    pass

def export_configuration():
    pass


