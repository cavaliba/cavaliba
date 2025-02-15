# (c) cavaliba.com - sirene - tasks.py

from time import sleep
from celery import shared_task

from app_home.configuration import get_configuration
from app_home.configuration import load_configuration_cache
import app_home.cache as cache

from app_home.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL

from .mail import sirene_send_mail
from .sms import sirene_send_sms

# ------------------------------------------------------------
@shared_task
def task_send_sms(dests, data, aaa=None):
    ''' returns number of sms sent successfully'''

    # reload - don't use cached configuration &  data
    load_configuration_cache()
    cache.init()

    if len(data) ==0:
        return 0

    count = 0

    for num in dests:
        result = sirene_send_sms(num, data, aaa=aaa)
        if result:
            count += 1

    return count



# ------------------------------------------------------------
@shared_task
def task_send_mail(subject, text_content,  dests, html_content=None, aaa=None):

    # reload - don't use cached configuration &  data
    load_configuration_cache()
    cache.init()

    # add entry to log

    #dest_count = len(dests)

    sender = get_configuration("sirene", "EMAIL_FROM")
    result = sirene_send_mail(subject, text_content, sender, dests, html_content=html_content, aaa=aaa)


    return result


