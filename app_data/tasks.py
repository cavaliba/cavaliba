# Create your tasks here


from time import sleep
from celery import shared_task

#from .common import get_setting
from app_conf.configuration import get_configuration
from app_conf.configuration import load_configuration_cache

from app_log.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL
#log(INFO, aaa=aaa, app="home", view="private", action="update_dashboard", status="OK", data="")



from .data import update_bigset

# ------------------------------------------------------------
@shared_task
def task_update_bigtest():

    update_bigset()

    return



