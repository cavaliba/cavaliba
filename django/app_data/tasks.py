# Create your tasks here


from time import sleep
from celery import shared_task

#from .common import get_setting
from app_home.configuration import get_configuration
from app_home.configuration import load_configuration_cache

from app_home.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL



from .data import update_bigset

# ------------------------------------------------------------
@shared_task
def task_update_bigtest():

    update_bigset()

    return



