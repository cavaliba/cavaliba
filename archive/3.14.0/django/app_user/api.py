# app_user - api.py

import json
import re
import base64
from pprint import pprint

from django.conf import settings
from django.utils import timezone
# from django.contrib import messages
# from django.forms.models import model_to_dict
from django.utils.translation import gettext as _
from django.db.models import F

# from django.contrib.auth import authenticate

from app_home.configuration import load_configuration_cache
from app_home.configuration import get_configuration
from app_home.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL

# from .models import SirenePermission

from .ip import get_user_ip
from .ip import is_trusted_ip

from app_home.models import CavalibaAPIStat
from app_data.data import Instance 

from app_home.cache import flush_cache_per_request



# ==============================================================================
# api helper
# ==============================================================================

def api_update_error(keyname=None):
    
    if not keyname:
        return
    
    CavalibaAPIStat.objects.get_or_create(keyname=keyname)
    CavalibaAPIStat.objects.filter(keyname=keyname)\
        .update(error_count=F("error_count") + 1, last_error = timezone.now())


def api_update_success(keyname=None):

    if not keyname:
        return
    
    CavalibaAPIStat.objects.get_or_create(keyname=keyname)
    CavalibaAPIStat.objects.filter(keyname=keyname)\
        .update(success_count=F("success_count") + 1, last_success = timezone.now())
    

def check_ip_filter(ip, filter):
    # TODO : ip in ACL filter ? 
    # filter format [!]range range range"  or "*"" or "0.0.0.0/0"
    return True


# ==============================================================================
# start_api
# ==============================================================================

def start_api(request):

    # check API key 
    # check time range, IP range, enabled, ...
    # build API permissions/ACL structure

    reply = {}
    reply["is_allowed"] = False
    reply["keyname"] = None
    reply["is_readonly"] = True
    reply["error"] = "no action performed"
    reply["user_ip"] = None
    reply["acl_filter"] = None
    reply["permissions"] = []


    flush_cache_per_request() 

    #header = request.META.get('HTTP_AUTHORIZATION')
    cavaliba_auth = request.headers.get('X-Cavaliba-Key','')
    if not cavaliba_auth:
        reply["error"] = "api - no key in header"
        return reply

    (keyname, keyvalue) = cavaliba_auth.split( )

    #print("start_api: ", keyname, keyvalue)

    # keyname 
    m = re.compile(r'[a-zA-Z0-9()_/.-]*$')

    if not keyname:
        reply["error"] = "api - no keyname in header"
        return reply
    if not m.match(keyname):
        reply["error"] = "api - invalid chars in keyname"
        return reply

    reply["keyname"] = keyname


    instance = Instance(classname="_apikey", iname=keyname)
    if not instance:
        reply["error"] = f"api - non-existent key {keyname} in DB"
        return

    # is_enabled
    if not instance.is_enabled:
        reply["error"] = f"api - key {keyname} disabled"
        api_update_error(keyname)
        return reply

    # keyvalue
    instance.fields["is_readonly"].get_first_value()

    if keyvalue != instance.fields["keyvalue"].get_first_value():
        reply["error"] = f"api - invalid keyvalue for key {keyname}"
        api_update_error(keyname)
        return reply

    # is_readonly
    reply["is_readonly"] = instance.fields["is_readonly"].get_first_value()

    # check not after
    # TODO

    # check timerange 
    # TODO
    
    # check ip source
    user_ip = get_user_ip(request)
    reply["user_ip"] = user_ip
    ip_filter = instance.fields["ip_filter"].get_first_value()

    if not ip_filter:
        reply["error"] = f"api - no ip_filter for key {keyname}"
        api_update_error(keyname)
        return reply

    r = check_ip_filter(user_ip, ip_filter)
    if not r:
        reply["error"] = f"api - source IP not allowed for key {keyname}"
        api_update_error(keyname)
        return reply

    # get ACL/objects
    try:
        reply["acl_filter"] = instance.fields["acl_filter"].get_first_value()
    except:
        reply["acl_filter"] = ""

    # get permissions
    try:
        reply["permissions"] = instance.fields["permissions"].get_first_value().splitlines()
    except:
        reply["permissions"] = ""
    
    api_update_success(keyname)
    
    reply["is_allowed"] = True
    reply["error"] = ""
    return reply




