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
    # ---------------------
    # 123-SMS / clic-secure
    # ---------------------
    # https://www.clic-secure.com/http.php?email=&pass=&numero=&message=
    login = settings.SIRENE_SMS_LOGIN
    password = settings.SIRENE_SMS_PASSWORD
    url = settings.SIRENE_SMS_URL
    
    #query = "https://www.clic-secure.com/http.php?{}email={}&pass={}&numero={}&message={}".format(
    
    query = "{}email={}&pass={}&numero={}&message={}".format(
        url,
        login,
        password,
        num,
        sms,
        )
    #print("SMS:QUERY:",query)
    r = requests.get(query)
    # print("SMS:RESPONSE:", r.status_code, r.text, type(r.text))
    #print(f"SMS (CLICSECURE) - {num} - {sms}")

    if  r.text == '80' or r.text == '81':
        add_journal(mobile=num, sms=sms, aaa=aaa)
        # info(domain="sms.ok", data=f"SMS sent with clicsecure for {num} - {r.status_code}/{r.text} - {sms}", aaa=aaa)
    else:
        #error(domain="sms.ko", data=f"SMS Failed with clicsecure for {num} - {r.status_code}/{r.text} - {sms}", aaa=aaa)
        pass    
    return True

    # a 80 : Le message a été envoyé
    # a 81 : Le message est enregistré pour un envoi en différé
    # r 82 : Le login et/ou mot de passe n’est pas valide
    # r 83 : vous devez créditer le compte
    # r 84 : le numéro de gsm n’est pas valide
    # r 85 : le format d’envoi en différé n’est pas valide
    # r 86 : le groupe de contacts est vide
    # r 87 : la valeur email est vide
    # r 88 : la valeur pass est vide
    # r 89 : la valeur numero est vide
    # r 90 : la valeur message est vide
    # r 91 : le message a déjà été envoyé à ce numéro dans les 24
    # dernières heures
    # (L’erreur 91 peut être désactivée dans la rubrique « Modifier les
    # options »)
    # a 92 le test d’envoi «à blanc» est positif
    # r 93 pour effectuer l’envoi de SMS vers les DOM TOM, vous
    # devez activer l’option (14) dans l’espace client
    # a 94 votre envoi en différé est supprimé
    # r 95 votre envoi en différé n’a pas pu être supprimé
    # r 96 votre adresse IP n’est pas valide
    # r 97 le SENDER ID n’est pas valide
    # r 98 la date de début n’est pas valide
    # r 99 la date de fin n’est pas valide
    # r 100 la date de fin est supérieure à la date de début
    # r 101 le numéro de mobile est bloqué et/ou blacklisté
    # r 102 le changement de Sender-ID vous oblige à rajouter «stop
    # SMS au 36001» à la fin de votre message

    #print("send_sms() ; from:",num," ; content:",sms[0:5],"(...)")


