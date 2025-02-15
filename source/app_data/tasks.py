# (c) cavaliba.com - data - tasks.py



from celery import shared_task
from .data import update_bigset

# ------------------------------------------------------------
@shared_task
def task_update_bigtest():

    update_bigset()

    return



