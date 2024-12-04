# sirene - sms.py

import os
import time
from datetime import datetime, timedelta
import random
import base64
import re
import requests

from django.conf import settings
from django.utils import timezone


from app_home.configuration import get_configuration

from app_home.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL

from .models import SMSJournal



def sms_encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()

def sms_decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)


# ----------------------------------------------------------------------
# Add journal entry

def add_journal(mobile=None, sms=None, aaa=None):



    quota = get_sms_quota(aaa)

    entry = SMSJournal()

    try:
        entry.created_by = aaa["username"]
    except:
        entry.created_by = "n/a"

    entry.mobile = mobile
    entry.quota = quota
    
    # TODO encrypt content
    key = os.environ.get('CAVALIBA_CIPHER_KEY')
    if key:
        entry.content = sms_encode(key,sms)
    else:
        entry.content = "no encryption key, no content."

    entry.save()


def get_sms_quota(aaa=None):

    if 'username' not in aaa:
        return 9999999

    period = timezone.now()-timedelta(days=1)
    sent = SMSJournal.objects.filter(created_by = aaa["username"], created_at__gte=period).count()

    quota = int(get_configuration("sirene", "SMS_QUOTA_PER_DAY"))
    
    sms_left =  max(quota - sent, 0)

    return sms_left

# ----------------------------------------------------------------------
def sirene_send_sms(num, sms, aaa=None):
    ''' returns  True/False ''' 

    if not sms_check_valid_number(num):
        #error(domain="sms.send", data=f"Invalid SMS number {num}", aaa=aaa)
        return False

    mode = get_configuration("sirene","SMS_MODE") 

    # limit to 159 chars max
    sms_cut = sms[:153]
    if len(sms_cut) != len(sms):
        sms_cut += ' (...)'

    if mode == "stdout":
        return sms_mode_stdout(num, sms_cut, aaa=aaa)

    if mode == "folder":       
        return sms_mode_folder(num, sms_cut, aaa=aaa)

    if mode == "clicsecure":       
        return sms_mode_clicsecure(num, sms_cut, aaa=aaa)

    # TODO
    # octopush ?
    # aws
    # azure


    return False


# ----------------------------------------------------------------------------
def sms_check_valid_number(num):

    # TODO : adapt for international SMS numbers
    #if not re.match(r'^^\+?1?\d{9,15}$', sms):

    if not re.match(r'^^\d{10}$', num):
        #print("SMS: incorrect SMS number: ", num)
        return False

    return True


# ----------------------------------------------------------------------
def sms_mode_stdout(num, sms, aaa=None):


    print(f"SMS (STDOUT) - {num} - {sms}")

    add_journal(mobile=num, sms=sms, aaa=aaa)

    # info(domain="sms.ok", data=f"SMS sent to stdout for {num}", aaa=aaa)
    return True


# ----------------------------------------------------------------------
def sms_mode_folder(num, sms, aaa=None):

    # to folder 

    now_msec = time.time()
    filename = str(now_msec)
    filename = str ( datetime.today().strftime('%Y-%m-%d-%H%M%S') )
    filename += "-"
    alea = int ( random.random() * 1000000000)
    filename += str ( alea )
    filename += ".json"

    sms_folder = get_configuration("sirene", "SMS_FOLDER") 
    path = "/files/" + sms_folder + "/" + filename 

    now = timezone.now()
    data=f"'timestamp': '{now}',\n'msec': {now_msec},\n'sms': '{num}',\n'message': '{sms}'\n"    
    data = "{\n" + data + " }\n"
    f = open(path, "a")
    f.write(data)
    f.close()

    add_journal(mobile=num, sms=sms, aaa=aaa)

    print(f"SMS (FOLDER) - {filename} - {num} - {sms}")
    # info(domain="sms.ok", data=f"SMS sent to folder for {num} - {sms}", aaa=aaa)

    #add_journal(mobile=num, sms=sms, aaa=aaa)

    return True

# ----------------------------------------------------------------------
def sms_mode_clicsecure(num, sms, aaa=None):

    # https://www.clic-secure.com/http.php?email=&pass=&numero=&message=
    #login = settings.CAVALIBA_SMS_LOGIN
    #password = settings.CAVALIBA_SMS_PASSWORD
    #url = settings.CAVALIBA_SMS_URL
    login = os.environ.get("CAVALIBA_SMS_LOGIN","cavaliba")
    password = os.environ.get("CAVALIBA_SMS_PASSWORD","changeme")
    url = os.environ.get("CAVALIBA_SMS_URL","https://localhost/")

    
    query = "{}email={}&pass={}&numero={}&message={}".format(
        url,
        login,
        password,
        num,
        sms,
        )
    r = requests.get(query)

    if  r.text == '80' or r.text == '81':
        add_journal(mobile=num, sms=sms, aaa=aaa)
        # info(domain="sms.ok", data=f"SMS sent with clicsecure for {num} - {r.status_code}/{r.text} - {sms}", aaa=aaa)
    else:
        #error(domain="sms.ko", data=f"SMS Failed with clicsecure for {num} - {r.status_code}/{r.text} - {sms}", aaa=aaa)
        pass    
    return True




