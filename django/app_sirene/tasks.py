# Create your tasks here


from time import sleep
from celery import shared_task

#from .common import get_setting
from app_home.configuration import get_configuration
from app_home.configuration import load_configuration_cache

from app_home.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL

from .mail import sirene_send_mail
from .sms import sirene_send_sms

# ------------------------------------------------------------
@shared_task
def task_send_sms(dests, data, aaa=None):
    ''' returns number of sms sent successfully'''

    # TODO : don't use cached configuration ()
    load_configuration_cache()

    if len(data) ==0:
        return 0

    count = 0

    for num in dests:
        result = sirene_send_sms(num, data, aaa=aaa)
        if result:
            count += 1

    # debug(domain="sms.task.sent", data=f"TASK - {count} SMS sent", aaa=aaa)

    return count



# ------------------------------------------------------------
@shared_task
def task_send_mail(subject, text_content,  dests, html_content=None, aaa=None):


    # TODO : don't use cached configuration ()
    load_configuration_cache()


    # add entry to log

    dest_count = len(dests)

    sender = get_configuration("sirene", "EMAIL_FROM")

    result = sirene_send_mail(subject, text_content, sender, dests, html_content=html_content, aaa=aaa)

    # if result:
    #     debug(domain="mail.task.sent", data=f"{dest_count} MAILs sent ; subject {subject} ; sender {sender}", aaa=aaa)
    # else:
    #     warning(domain="mail.task.failed", data=f"Failed to send emails", aaa=aaa)

    return result

# ------------------------------------------------------------


# @shared_task
# def add(x, y):
#     return x + y


# @shared_task
# def mul(x, y):
#     return x * y


# @shared_task
# def xsum(numbers):
#     return sum(numbers)

# @shared_task()
# def task_mysleep(data):
#     sleep(20)  # Simulate expensive operation(s) that freeze Django


# ------

#from demoapp.models import Widget

# @shared_task
# def count_widgets():
#     return Widget.objects.count()


# @shared_task
# def rename_widget(widget_id, name):
#     w = Widget.objects.get(id=widget_id)
#     w.name = name
#     w.save()
