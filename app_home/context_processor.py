
import datetime
from django.conf import settings

from app_user.aaa import get_aaa

# from .aaa import get_aaa

# from .configuration import SIRENE_VERSION
# from .configuration import SIRENE_VERSION_DATE

from app_conf.configuration import get_configuration

from app_home.home import get_applist
from app_home.register import SIRENE_VERSION


def get_info(request):

    #print("*** context processor get_info()")

    context = {}


    aaa=get_aaa(request)
    #context['aaa'] = aaa


    for k,v in aaa.items():
        if not k.startswith("p_"):
            continue
        context[k] = v

    # global SIRENE_VERSION
    context["SIRENE_VERSION"] = SIRENE_VERSION

    apps = get_applist(aaa)
    for x in apps:
        if x.keyname == 'home':
            apps.remove(x)
            break   
    context["navbar_apps"] = apps
        

    # notif app
    #context['sirene_appname'] = get_configuration("sirene", "APPNAME")

    # global
    context["GLOBAL_APPNAME"] = get_configuration("home", "GLOBAL_APPNAME")

    # navbar logo or Home icon
    context["LOGO_SIZE"] = int(get_configuration("home", "LOGO_SIZE"))


    return context
