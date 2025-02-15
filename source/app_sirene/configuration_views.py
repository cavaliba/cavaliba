# (c) cavaliba.com - sirene - configuration_views.py


from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext as _

from app_home.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL
from app_user.aaa import start_view
from .export import full_yaml_response

# Celery tasks
from app_sirene.tasks import task_send_mail
from app_sirene.tasks import task_send_sms


from .models import Message
from .models import PublicPageJournal

#-----------------------------------------
def flushall(request):
    ''' POST with CSRF  > remove all is_visble messages'''

    context = start_view(request, app="sirene", view="config_flushall", 
        noauth="app_sirene:index", perm="p_sirene_flushall", noauthz="app_sirene:index")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]


    if request.method != 'POST':
        messages.add_message(request, messages.ERROR, _("Not allowed"))
        log(ERROR, aaa=aaa, app="sirene", view="flushall", action="check", status="KO", data="method not supported")
        return redirect("app_sirene:index")

    pages = Message.objects.filter(is_visible=True)

    count=0
    for page in pages:
        now = timezone.now()
        page.is_visible = False
        page.removed_at = now
        page.removed_by = aaa['username']
        page.save()
        count+=1

    #PublicPageJournal.reset(aaa=aaa)

    journal = PublicPageJournal.objects.filter(is_visible=True)
    count2 = 0
    for page in journal:
        now = timezone.now()
        page.is_visible = False
        page.save()
        count2 += 1

    total = count + count2
    log(INFO, aaa=aaa, app="sirene", view="flushall", action="post", status="OK", data=f"flushall {count} entries")
    messages.add_message(request, messages.SUCCESS, _("OK"))
    return redirect("app_sirene:private")




#-----------------------------------------
# 
#-----------------------------------------

def conf_export(request):

    context = start_view(request, app="sirene", view="conf_export", 
        noauth="app_sirene:index", perm="p_sirene_export", noauthz="app_sirene:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    #aaa = context["aaa"]

    # rawdata = conf_export_to_yaml()
    # rawdata = yaml.dump(rawdata, allow_unicode=True)
    response = full_yaml_response()
    return response

    #print(rawdata)
    # context["rawdata"] = rawdata
    # return render(request, 'app_sirene/conf_export.html', context)

# ---------------


def doc(request):

    context = start_view(request, app="sirene", view="doc", 
        noauth="app_sirene:index")
    if context["redirect"]:
        return redirect(context["redirect"])
    #aaa = context["aaa"]

    # r = sirene_start_view(request, domain="configuration", view="doc", noauth="app_sirene:index")
    # if r:
    #     return redirect(r)
    # aaa = get_aaa(request)


    return render(request, 'app_sirene/doc.html', context)
    
