# (c) cavaliba.com - sirene - sms_view.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext as _

from django.db.models.functions import ExtractWeek, ExtractYear, ExtractDay, ExtractMonth
from django.db.models import Sum, Count, Max, Min

from app_home.configuration import get_configuration
from app_home.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL

from app_user.aaa import start_view

# Celery tasks
from app_sirene.tasks import task_send_sms

from .sms import sms_check_valid_number
from .sms import get_sms_quota
from .models import SMSJournal
from .sms_forms import SMSForm

# -------------------------------------------
# private INDEX, message list
# -------------------------------------------

def sms_send(request):

    context = start_view(request, app="sirene", view="sms_send", 
        noauth="app_sirene:index", perm="p_sirene_sms_send", noauthz="app_sirene:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]

    if get_sms_quota(aaa) < 1:
        messages.add_message(request, messages.ERROR, _("Insufficient SMS Quota"))
        log(WARNING, aaa=aaa, app="sirene", view="sms", action="quota", status="KO", data="insufficient SMS quota") 
        return redirect("app_sirene:private")

    if request.method == "POST":

        form = SMSForm(request.POST)
        if form.is_valid():

            cd = form.cleaned_data
            mobile = cd["mobile"]
            message= cd["message"]

            if not sms_check_valid_number(mobile):
                messages.add_message(request, messages.ERROR, _("Invalid SMS number"))
                log(WARNING, aaa=aaa, app="sirene", view="sms", action="send", status="KO", data="Invalid number") 
            else:
                task_send_sms.delay([mobile], message, aaa=aaa)
                messages.add_message(request, messages.SUCCESS, _("SMS sent"))
                log(INFO, aaa=aaa, app="sirene", view="sms", action="send", status="OK", data="Queued") 
                return redirect("app_sirene:private")
    else:
        form = SMSForm()
        log(DEBUG, aaa=aaa, app="sirene", view="sms", action="form", status="OK", data="Get form") 
    
    context["sms_warning"] = get_configuration("sirene", "SMS_WARNING")
    context["form"] = form
    return render(request, 'app_sirene/sms_send.html', context)


#-----------------------------------------
#  SMS stats
#-----------------------------------------
def sms_journal(request):

    context = start_view(request, app="sirene", view="sms_journal", 
        noauth="app_sirene:index", perm="p_sirene_sms_journal", noauthz="app_sirene:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]

    journal = SMSJournal.objects.all().order_by('-created_at')
    log(DEBUG, aaa=aaa, app="sirene", view="sms", action="journal", status="OK", data="Get form") 

    context["journal"] = journal
    return render(request, 'app_sirene/sms_journal.html', context)



#-----------------------------------------
#  SMS stats
#-----------------------------------------
def sms_stat(request):

    context = start_view(request, app="sirene", view="sms_stat", 
        noauth="app_sirene:index", perm="p_sirene_sms_stat", noauthz="app_sirene:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]


    stat_year = (SMSJournal.objects
        .annotate(year=ExtractYear('created_at'))
        .values('year')
        .annotate(count=Count('id'))
        .annotate(numsender=Count('created_by', distinct=True))
        .annotate(numdest=Count('mobile', distinct=True))
    )

    stat_month = (SMSJournal.objects
        .annotate(year=ExtractYear('created_at'))
        .annotate(month=ExtractMonth('created_at'))
        .values('year','month')
        .annotate(count=Count('id'))
        .annotate(numsender=Count('created_by', distinct=True))
        .annotate(numdest=Count('mobile', distinct=True))
    )


    stat_day = (SMSJournal.objects
        .annotate(year=ExtractYear('created_at'))
        .annotate(month=ExtractMonth('created_at'))
        .annotate(day=ExtractDay('created_at'))
        .values('year', 'month', 'day')
        .annotate(count=Count('id'))
        .annotate(numsender=Count('created_by', distinct=True))
        .annotate(numdest=Count('mobile', distinct=True))
    )

    log(DEBUG, aaa=aaa, app="sirene", view="sms", action="stat", status="OK", data="Get form") 

    context["stat_year"] = stat_year
    context["stat_month"] = stat_month
    context["stat_day"] = stat_day
    return render(request, 'app_sirene/sms_stat.html', context)


