# (c) cavaliba.com - home - log.py

from datetime import timedelta
from django.utils import timezone
from django.utils.translation import gettext as _

from app_home.configuration import get_configuration
from .models import CavalibaLog


DEBUG = "DEBUG"
INFO = "INFO"
WARNING = "WARNING"
ERROR = "ERROR"
CRITICAL = "CRITICAL"


def log(level, app="", view="", action="", status="", data="", aaa=None, user_ip=""):

    if level=="DEBUG":
        log_debug = get_configuration(appname="home", keyname="LOG_DEBUG")
        if log_debug != "yes":
            return

    log = CavalibaLog()
    
    log.created_at = timezone.now()
    log.level = level
    
    log.app = app
    log.view = view
    log.action = action
    log.status = status  
    log.data = data

    if aaa:
        log.username = aaa.get("username", "?")
        log.user_ip = aaa.get("user_ip", "")
    else:
        log.username = _("anonymous")
        log.user_ip = user_ip


    # exclude some IPs
    log_excluded_ip = get_configuration(appname="home", keyname="LOG_EXCLUDED_IP").split(' ')
    if '*' in log_excluded_ip:
        return
    if len(log_excluded_ip) > 0:
        if log.user_ip in log_excluded_ip:
            return



    try:
        log.save()
        return log
    except Exception as e:
        print(e)
        return None


# ----------------

def purge(aaa=None, keep_days=None):

    if keep_days is None:
        keep_days = int(get_configuration(appname="home", keyname="LOG_KEEP_DAYS"))

    if keep_days == 0:
        count = CavalibaLog.objects.all().delete()[0]
    else:
        count = CavalibaLog.objects.filter(created__lte=timezone.now()-timedelta(days=keep_days)).delete()[0]

    return count




