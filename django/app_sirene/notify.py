# notify.py

import re
import requests
from datetime import datetime, timedelta

from django.conf import settings
from django.utils import timezone
#from jinja2 import Environment, FileSystemLoader


from app_home.configuration import get_configuration
from app_log.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL

from app_user.models import SireneGroup
from app_user.group import group_expand_to_users
from app_user.group import group_get_by_name
from app_user.group import group_get_subgroups

from app_user.user import user_get_mobile
from app_user.user import user_get_email

from app_data.data import Instance
from app_data.data import get_instances_raw_json
from app_data.data import get_instance_by_name

# Celery tasks
from app_sirene.tasks import task_send_mail
from app_sirene.tasks import task_send_sms

from .sms import get_sms_quota




# -------------------------------------------------------------------------
# Compute and Queue Notifications for the given message 
# -------------------------------------------------------------------------

def is_24():
    ''' return True if current time outside business hours  Mo-Fr 08h00-18h00'''
    dt = timezone.now()
    wd = dt.weekday()  # Week =0-4 WEnd=5/6
    ho = dt.hour

    if wd > 4:
        return True

    if ho < 8:
        return True

    if ho > 17:
        return True

    return False


# def get_user_email(user):
#     if user.secondary_email:
#         if len(user.secondary_email) > 0:
#             return user.secondary_email
#     return user.email


# def get_user_mobile(user):
#     if user.secondary_mobile:
#         if len(user.secondary_mobile) > 0:
#             return user.secondary_mobile
#     return user.mobile


# -----------------------------------
# Core Notification compute function
# -----------------------------------

def sirene_expand_notify(message):

    allgroups = []
    app_watchlist = []

    # APP
    # message.notify_app : DataInstance iobj(s) = app1, app2, app3
    #   .sirene_group = "g1", "g2", "g3"
    for app_obj in message.notify_app.all():
        instance = Instance(iobj=app_obj)
        # keep list for site using this app
        app_watchlist.append(instance)
        xlist = instance.get_attribute("sirene_group")
        for g in xlist:
            if g:
                if g not in allgroups:
                    allgroups.append(g)


    # add all site using these apps
    if len(app_watchlist) > 0:
        # some apps to propagate
        allsites = get_instances_raw_json(classname='site', is_enabled=True, fieldname='sirene_app')
        for sitekeyname, siteapps in allsites.items():
            for app in app_watchlist:
                if app.keyname in siteapps:
                    # app in use for this site ; site must be notified
                    site_obj = get_instance_by_name(iname=sitekeyname, classname='site')
                    instance = Instance(iobj=site_obj)
                    xlist = instance.get_attribute("sirene_group")
                    for g in xlist:
                        if g:
                            if type(g) is SireneGroup:
                                if not g in allgroups:
                                    allgroups.append(g)


    # SITE
    # message.notify_site : DataInstance iobj(s) = site1, site2, ...
    #   .sirene_group = "g1", "g2", "g3"
    #   .sirene_app = "app1", "app2", ...   => 

    for site_obj in message.notify_site.all():
        instance = Instance(iobj=site_obj)
        xlist = instance.get_attribute("sirene_group")
        for g in xlist:
            if g:
                if type(g) is SireneGroup:
                    if not g in allgroups:
                        allgroups.append(g)



    # CUSTOMER
    # message.notify_app : DataInstance iobj(s) = app1, app2, app3
    #   .sirene_group = "g1", "g2", "g3"
    for cust_obj in message.notify_customer.all():
        instance = Instance(iobj=cust_obj)
        xlist = instance.get_attribute("sirene_group")
        for g in xlist:
            if g:
                if type(g) is SireneGroup:
                    if not g in allgroups:
                        allgroups.append(g)



    # SITEGROUP
    # message.notify_sitegroup
    #   .sirene_group
    #   .members => "sitegroup1", "sitegroup2"   == TEXT(DataInstance.sitegroup)
    for sitegroup_obj in message.notify_sitegroup.all():

        instance = Instance(iobj=sitegroup_obj)
        xlist = instance.get_recursive_content(
            fieldname="sirene_group", 
            fieldmember="members", 
            fieldrecurse="subgroups",
            done=[])

        for g in xlist:
            if g:
                if type(g) is SireneGroup:
                    if not g in allgroups:
                        allgroups.append(g)


    # Sirene Group
    # message.notify_group
    #     .users       SireneUser
    #     .subgroups   SireneGroup
    for group_obj in message.notify_group.all():
        if not group_obj in allgroups:
            allgroups.append(group_obj)
            xlist = group_get_subgroups(group_obj)
            for g in xlist:
                if g:
                    if type(g) is SireneGroup:
                        if not g in allgroups:
                            allgroups.append(g)


    # Compute users involved in allgroups
    allusers = group_expand_to_users([], allgroups)
    message.users.clear()
    for u in allusers:
        message.users.add(u)

    # build text attributes
    message.notify_text = ' '.join([g.keyname for g in allgroups])
    message.users_text = ' '.join([u.login for u in allusers])




def sirene_notify(message=None, aaa=None):
    ''' send notifications for message - Email and SMS '''

    error = 0

    # set instead of array [] for unique values
    email_list = set()
    sms_list = set()


    for user in message.users.all():

        if not user.is_enabled:
            continue
        if not user.want_notifications:
            continue
        if not user.want_24:
            if is_24():
                continue

        email = user_get_email(user)
        if email:
            email_list.add(email)
        mobile = user_get_mobile(user)
        if mobile:
            sms_list.add(mobile)


    email_dests = list(email_list)
    email_count = len(email_dests)

    sms_dests = list(sms_list)
    sms_count = len(sms_dests)


    # send emails 
    if message.has_email and len(email_dests) > 0:
        prefix = get_configuration("sirene", "EMAIL_PREFIX") 
        subject = prefix + message.title
        text_content = message.body
        #html_content = None
        html_content = message.body
        task_send_mail.delay(subject, text_content, email_dests, html_content=html_content, aaa=aaa)
        # debug(domain="notify", data=f"MAILS queued: {email_count}", aaa=aaa)
    else:
        email_count = 0


    if message.has_sms and sms_count>0:
        #sms_left = int(get_configuration("sms", "SMS_QUOTA_PER_DAY")) - get_sms_quota(aaa)
        sms_left = get_sms_quota(aaa)
        if sms_left - sms_count < 0:
            error = 1
            # warning(domain="notify", data=f"SMS - NOK - Failed - quota left {sms_left} / {sms_count} needed", aaa=aaa)
        else:
            prefix = get_configuration("sirene", "SMS_PREFIX")
            text_content = prefix + message.title
            task_send_sms.delay(sms_dests, text_content, aaa=aaa)
            # debug(domain="notify", data=f"SMS queued: {sms_count}", aaa=aaa)
    else:
        sms_count = 0


    return (email_count, sms_count, error)



def sirene_notify_update(update=None, aaa=None):
    ''' send notifications update for MessageUpdate - Email and SMS  '''

    error = 0

    # set instead of array [] for unique values
    email_list = set()
    sms_list = set()

    message = update.message

    for user in message.users.all():

        if not user.is_enabled:
            continue
        if not user.want_notifications:
            continue
        if not user.want_24:
            if is_24():
                continue

        email = user_get_email(user)
        if email:
            email_list.add(email)
        mobile = user_get_mobile(user)
        if mobile:
            sms_list.add(mobile)


    email_dests = list(email_list)
    email_count = len(email_dests)

    sms_dests = list(sms_list)
    sms_count = len(sms_dests)


    # send emails 
    if update.has_email and email_count > 0:
        prefix = get_configuration("sirene", "EMAIL_UPDATE_PREFIX") 
        subject = prefix + message.title
        text_content = update.content
        html_content = update.content
        task_send_mail.delay(subject, text_content, email_dests, html_content=html_content, aaa=aaa)
        # debug(domain="notify.update", data=f"Queued {email_count} update MAILs", aaa=aaa)
    else:
        email_count = 0

    # send sms
    if update.has_sms and sms_count > 0:
        #sms_left = int(get_configuration("sms", "SMS_QUOTA_PER_DAY")) - get_sms_quota(aaa)
        sms_left = get_sms_quota(aaa)
        if sms_left - sms_count < 0:
            error = 1
            # warning(domain="notify.update", data=f"SMS - Failed - quota left {sms_left} / {sms_count} needed", aaa=aaa)
        else:
            prefix = get_configuration("sirene", "SMS_UPDATE_PREFIX")
            text_content = prefix + message.title
            task_send_sms.delay(sms_dests, text_content, aaa=aaa)
            # debug(domain="notify.update", data=f"SMS queued: {sms_count}", aaa=aaa)
    else:
        sms_count = 0


    return (email_count, sms_count, error)

