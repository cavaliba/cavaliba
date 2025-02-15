# (c) cavaliba.com - sirene - common.py

import re
from datetime import timedelta

from django.utils import timezone
from app_home.configuration import get_configuration
from app_home.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL

from .models import Category
from .models import PublicPage
from .models import MessageTemplate
from .models import Message
from .models import SIRENE_SEVERITY


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def make_dictlist_from_csv(filedata,  splitfields=[]):

    lines = filedata.splitlines()
    header = []
    rows = []
    line_count = 0

    delimiter = get_configuration("CSV_DELIMITER") 


    # # convert fields csv "a+b+c" to list [a,b,c]
    # for rowdict in rows:
    #     a = []
    #     if 'notify_to' in rowdict:
    #         a = rowdict['notify_to'].split("+")
    #         rowdict['notify_to'] = a
    #     a = []
    #     if 'notify_apps' in rowdict:
    #         a = rowdict['notify_apps'].split("+")
    #         rowdict['notify_apps'] = a


    for line in lines:
        entry = {}                    
        fields = line.split(delimiter)
        if line_count == 0:
            header = fields
            line_count = 1
        else:
            line_count += 1
            for i in range(0,len(header)):
                hi = header[i]
                if hi in splitfields:
                    try:
                        a = fields[i].split("+")
                        entry[hi] = a
                    except:
                        pass
                else:
                    try:
                        entry[hi] = fields[i]
                    except:
                        pass
            rows.append(entry)        

    return rows


def get_bootstrap_colors2(severity):
    # (0, "white"),
    # (1, "green"),
    # (2, "yellow"),
    # (3, "red"),
    # (4, "black"),
    # (5, "blue"),
    # (6, "grey"),

    # white
    if severity == 'na':
        return ('light', 'dark')
    # green        
    if severity == 'ok':
        return ('success', 'text-white')
    # yellow        
    if severity == 'minor':
        return ('warning', 'dark')
    # red        
    if severity == 'major':        
        return ('danger', 'text-white')
    # black    
    if severity == 'critical':        
        return ('dark', 'text-white')
    # blue
    if severity == 'info':        
        return ('info', 'text-dark')
    # other        
    if severity == 'other':        
        return ('secondary', 'text-white')
    
    return ('secondary', 'text-white')


# --------------------------------------------------------------------------
# sort by severity
# --------------------------------------------------------------------------

# SIRENE_SEVERITY = (
#      ("critical", "critical"),     # black
#      ("major", "major"),           # red
#      ("minor", "minor"),           # yellow
#      ("info", "info"),             # blue
#      ("other", "other"),           # grey
#      ("na", "n/a"),                # white
#      ("ok", "ok"),                 # green
# )

def sort_by_severity(pages):

    severity_order = ["critical","major","minor","info","other","na","ok"]

    result = []
    for s in severity_order:
        for p in pages:
            if p.severity == s:
                result.append(p)
    return result

# --------------------------------------------------------------------------
# message template expansion / placeholder
# --------------------------------------------------------------------------

def replace_placeholder(message=None, cleaned_data=None):

    # TODO bugfix (App/Site)
    return

    if not message:
        return 


    if r"$APPS$" in message.body:
        list_apps = [s.s_name for s in cleaned_data["notify_to_app"]]
        txt_apps = "<ul>\n"
        for i in list_apps:
            try:
                app = App.objects.get(name=i)
                disp = f"{app.name} - {app.display}"
            except:
                disp = i
            txt_apps += f"<li>{disp}</li>\n"
        txt_apps += "</ul>\n"            
        message.body  = re.sub(r"\$APPS\$", txt_apps, message.body)


    if r"$SITES$" in message.body:
        list_sites = [s.s_name for s in cleaned_data["notify_to_site"]]
        txt_sites = "<ul>\n"
        for i in list_sites:
            try:
                site = Site.objects.get(name=i)
                disp = f"{site.name} - {site.display}"
            except:
                disp = i
            txt_sites += f"<li>{disp}</li>\n"
        txt_sites += "</ul>\n"            
        message.body  = re.sub(r"\$SITES\$", txt_sites, message.body)

    return



# -----------------------------------------------------------------------
# 
# -----------------------------------------------------------------------


def is_valid_template_name(name):

    tmp = MessageTemplate.objects.filter(name=name).first()
    if tmp:
        return True
    return False


def is_valid_severity(name):

    for item in SIRENE_SEVERITY:
        if name == item[0]:
            return True
    return False



def is_valid_category(name):

    tmp = Category.objects.filter(name=name).first()
    if tmp:
        return True
    return False


def is_valid_publicpage(name):

    tmp = PublicPage.objects.filter(name=name).first()
    if tmp:
        return True
    return False


# --------------------------------------------------------------------------
# for private/anonymous list view
# --------------------------------------------------------------------------

def cleanup_old_messages(aaa=None):
    '''Remove expired messages ; returns number of removed items.'''

    max_duration = int(get_configuration("sirene", "PRIVATE_MAX_MINUTES"))

    pages = Message.objects.filter(is_visible=True).order_by('-created_at')
    # if None
    if len(pages) == 0:
        return 0

    count = 0
    now = timezone.now()

    # check date and update accordingly
    for page in pages:

        # "just" expired : if removed_at exists and crossed
        if page.removed_at:
            if  now > page.removed_at:
                page.is_visible = False
                page.removed_by = "auto"
                page.save()
                log(aaa=aaa, domain="cleanup", data=f"private page: {page.title}")
                count += 1
                continue

        # very old (wrong or missing removed_at value)
        now = timezone.now()
        if now > page.created_at + timedelta(minutes=max_duration):
            page.is_visible = False
            page.removed_at = now
            page.removed_by = "auto"
            page.save()
            #info(aaa=aaa, domain="cleanup", data=f"private page: {page.title}")
            count += 1
            continue

    return count



