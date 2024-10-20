# app_conf - configuration.py


from functools import lru_cache
from django.shortcuts import render, redirect


from .models import SireneConfiguration
from .configuration_default import CONFIGURATION_DEFAULT



from .configuration_form import AppHomeConfigurationForm
from .configuration_form import AppConfConfigurationForm
from .configuration_form import AppUserConfigurationForm
from .configuration_form import AppLogConfigurationForm
from .configuration_form import AppSireneConfigurationForm
from .configuration_form import AppDataConfigurationForm


#from app_.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL
#log(DEBUG, aaa=aaa, app="log", view="private", action="list", status="OK", data="")


global_configuration = {}


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
    elif appname == "conf":
        form = AppConfConfigurationForm(request.POST)
    elif appname == "user":
        form = AppUserConfigurationForm(request.POST)
    elif appname == "log":
        form = AppLogConfigurationForm(request.POST)
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
    elif appname == "conf":
        form = AppConfConfigurationForm(initial=initial)
    elif appname == "user":
        form = AppUserConfigurationForm(initial=initial)
    elif appname == "log":
        form = AppLogConfigurationForm(initial=initial)
    elif appname == "data":
        form = AppDataConfigurationForm(initial=initial)
    else:
        form = None
    return form



def register_configuration():
    ''' Setup DB - called by command sirene_init and periodic tasks'''

    for appname, appconfig in CONFIGURATION_DEFAULT.items():

        for keyname,value in appconfig.items():

            # NEXT use global_configuration
            dbentry = SireneConfiguration.objects.filter(appname=appname, keyname = keyname).first()

            if not dbentry:
                dbentry = SireneConfiguration()
                dbentry.appname = appname
                dbentry.description = ""
                dbentry.page = ""
                dbentry.order = 100        
                dbentry.keyname = keyname
                dbentry.value = value
                dbentry.save()
    
    # remove unused configurations
    dbentries = SireneConfiguration.objects.all()
    for dbentry in dbentries:
        if dbentry.appname not in CONFIGURATION_DEFAULT:
            dbentry.delete()
        else:
            if dbentry.keyname not in CONFIGURATION_DEFAULT[dbentry.appname]:
                dbentry.delete()

    print("register_configuration done.")



def load_configuration_cache():

    global global_configuration

    global_configuration = {}

    # first, load default
    for appname,appconfig in CONFIGURATION_DEFAULT.items():
        global_configuration[appname] = {}
        for k,v in appconfig.items():
            global_configuration[appname][k] = v

    # then, load from db
    dbconf = SireneConfiguration.objects.all()
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
    except:
        print(f"Unkown configuration {appname} - {keyname}")


    return response



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
            dbentry = SireneConfiguration.objects.filter(appname=appname, keyname = k).first()
            if not dbentry:
                dbentry = SireneConfiguration()
                dbentry.appname = appname
                dbentry.keyname = k

            dbentry.value = v
            dbentry.save()

    # perform a new init to populate cache
    load_configuration_cache()


