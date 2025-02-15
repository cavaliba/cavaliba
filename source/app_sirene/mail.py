# (c) cavaliba.com - sirene - mail.py

import time
from datetime import datetime, timedelta
import random
import re

from django.utils import timezone

from django.core import mail

from app_home.configuration import get_configuration
from app_home.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL

# ----------------------------------------------------------------------
def sirene_send_mail(subject, text_content, sender, dests, html_content=None, aaa=None):
    ''' returns  True/False ''' 

    mode = get_configuration("sirene", "EMAIL_MODE") 

    # limit subject length
    subject_cut = subject[:80]
    if len(subject_cut) != len(subject):
        subject_cut += ' (...)'


    if mode == "stdout":
        return mail_mode_stdout(subject_cut, text_content, sender, dests, html_content, aaa=aaa)

    if mode == "folder":       
        return mail_mode_folder(subject_cut, text_content, sender, dests, html_content, aaa=aaa)

    if mode == "smtp":
        return mail_mode_smtp(subject_cut, text_content, sender, dests, html_content, aaa=aaa)

    return False


# ----------------------------------------------------------------------------
def mail_check_valid_address(email):


    if not email:
        return False 

    if not type(email) is str:
        return False 

    if not len(email) > 3:
        return False
        
    #regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+') 
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    if re.fullmatch(regex, email):
        return True

    return False


# ----------------------------------------------------------------------
# to STDOUT
# ----------------------------------------------------------------------
def mail_mode_stdout(subject, text_content, sender, dests, html_content=None, aaa=None):

    for dest in dests:

        if mail_check_valid_address(dest):
            print(f"MAIL (STDOUT) - {dest} - {subject}")
        else:
            log(ERROR, aaa=aaa, app="sirene", view="mail", action="mode_stdout", status="KO", data=f"{dest}")
            return False
    
    log(INFO, aaa=aaa, app="sirene", view="mail", action="mode_stdout", status="OK", data=f"{dest} - {subject}")    
    return True

# ----------------------------------------------------------------------
# to Folder
# ----------------------------------------------------------------------

def mail_mode_folder(subject, text_content, sender, dests, html_content=None, aaa=None):


    now = timezone.now()
    now_msec = time.time()
    filename = str(now_msec)
    filename = str ( datetime.today().strftime('%Y-%m-%d-%H%M%S') )
    filename += "-"
    alea = int ( random.random() * 1000000000)
    filename += str ( alea )
    filename += ".json"

    email_folder = get_configuration("sirene", "EMAIL_FOLDER") 

    path = "/files/" + email_folder + "/" + filename 

    count = 0
    with open(path,"a") as f:
        f.write('[')
        first = True
        for dest in dests:
            if not mail_check_valid_address(dest):
                log(ERROR, aaa=aaa, app="sirene", view="mail", action="mode_folder", status="KO", data=f"{dest}")
                continue
            if not first:
                f.write(',\n')
            data = f"'timestamp': '{now}',\n'msec': {now_msec},\n"
            data += f"'from': {sender},\n"
            data += f"'to': '{dest}',\n"
            data += f"'subject': '{subject}'\n'"
            data += f"body': '{text_content}'\n"
            data = "{\n" + data + "}"
            f.write(data)
            count += 1
            first = False
            log(INFO, aaa=aaa, app="sirene", view="mail", action="mode_folder", status="OK", data=f"{dest} - {subject}")

        f.write(']\n')
        f.close()

    
    return True


# ----------------------------------------------------------------
# SMTP
# ----------------------------------------------------------------


def mail_mode_smtp(subject, text_content, sender, dests, html_content=None, aaa=None):

    batch = []
    count = 0
    result = True
    batch_size = int(get_configuration("sirene", "EMAIL_SMTP_BATCH"))


    for dest in dests:

        if not mail_check_valid_address(dest):
            log(ERROR, aaa=aaa, app="sirene", view="mail", action="mode_smtp", status="KO", data=f"{dest}")
            continue

        msg = mail.EmailMultiAlternatives(subject, text_content, sender, [], [dest])
        #msg = EmailMessage(subject, text_content, sender, [], [dest])

        if html_content:
            msg.attach_alternative(html_content, "text/html")

        #print(html_content)

        batch.append(msg)
        count += 1

        # ready to send ?
        if count >= batch_size:
            r2 = smtp_batch(batch, aaa=aaa)
            if not r2:
                result = False
            batch.clear()
            count = 0


    # last partial batch  ?
    if len(batch) > 0:
        r2 = smtp_batch(batch, aaa=aaa)
        if not r2:
            result = False
        batch.clear()        

    if result:
        log(INFO, aaa=aaa, app="sirene", view="mail", action="mode_smtp", status="OK", data=f"batch - {subject}")
    else:
        log(ERROR, aaa=aaa, app="sirene", view="mail", action="mode_smtp", status="KO", data=f"batch - {subject}")

    return result



def smtp_batch(batch, aaa=None):

    try:
        connection = mail.get_connection()
    except Exception as e:
        print("Mail batch connection failed : ", e)
        log(ERROR, aaa=aaa, app="sirene", view="mail", action="smtp_batch", status="KO", data=f"Connect failed")
        return False

    try:
        connection.send_messages(batch)
    except Exception as e:
        print("Mail batch send failed : ", e)
        log(ERROR, aaa=aaa, app="sirene", view="mail", action="smtp_batch", status="KO", data=f"Send failed")
        # error(domain="mail.smtp.send", data=f"smtp send failed", aaa=aaa)
        #print(batch)
        return False

    try:
        connection.close()
    except Exception as e:
        print("Mail batch close connection failed : ", e)
        log(ERROR, aaa=aaa, app="sirene", view="mail", action="smtp_batch", status="KO", data=f"Close failed")
        # error(domain="mail.smtp.close", data=f"smtp close connection failed", aaa=aaa)
        return False

    count = len(batch)
    log(INFO, aaa=aaa, app="sirene", view="mail", action="smtp_batch", status="OK", data=f"{count}")

    return True







