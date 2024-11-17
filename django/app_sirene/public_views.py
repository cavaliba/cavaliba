# views_public.py

from datetime import datetime, timedelta
import base64

from django.utils import timezone
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages


#from .log import debug, info, warning, error

from .models import PublicPage
from .models import PublicPageJournal

from .common import get_bootstrap_colors2
from .common import sort_by_severity


from app_home.configuration import get_configuration
from app_home.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL
from app_user.aaa import start_view
from app_user.aaa import get_aaa




def cleanup_public_page():

    max_duration = int(get_configuration("sirene", "PUBLIC_MAX_MINUTES"))

    default_seen = False
    default_is_first = False
    now = timezone.now()


    #journal = PublicPageJournal.objects.filter(is_visible=True).order_by('-created_at')
    journal = PublicPageJournal.objects.filter(is_visible=True)

    count = 0

    for page in journal:

        # expire
        if now > page.created_at + timedelta(minutes=max_duration):
            page.remove()
            count += 1
            # debug(domain="publicpage", data=f"removed/cleanup: {page.title}")

        if page.is_default:
            default_seen = True

        if default_seen:
            page.remove()
            count += 1
            # debug(domain="publicpage", data=f"removed/cleanup: {page.title}")

    # if count > 0:
    #     info(domain="publicpage", data=f"removed/cleanup count: {count}")

    return count



#-----------------------------------------
# /  (index, public page)
#-----------------------------------------
def index(request):

    context = start_view(request, app="sirene", view="public") 
    if context["redirect"]:
        return redirect(context["redirect"])
    # aaa = context["aaa"]


    # r = sirene_start_view(request, domain="public", view="index")
    # #aaa = get_aaa(request)


    max_display = int(get_configuration("sirene", "PUBLIC_MAX_ITEMS"))
    sort_order = get_configuration("sirene", "PUBLIC_SORT_ORDER")


    # debug(domain="public", data=f"access")


    # skip public page, if 
    # - trusted ip / or authenticated
    # - configuration requires skip
    # - no toggle in GET URL
    skip_public = get_configuration("sirene", "PUBLIC_SKIP_TO_TRUSTED")
    keep_public = request.GET.get('public', 'no')

    if keep_public != "yes":
        if skip_public == "yes":
            aaa = get_aaa(request)
            if (aaa['trusted_ip'] or aaa['is_authenticated']):
                return redirect("app_sirene:anonymous")

    # cleanup expired pages
    count = cleanup_public_page()


    # get & sort pages according to sort_order configuration
    if sort_order == "severity":
        goods = PublicPageJournal.objects.filter(is_visible=True)
        pages = sort_by_severity(goods)
    elif sort_order == "creation":
        pages = PublicPageJournal.objects.filter(is_visible=True).order_by('-created_at')
    else:
        # unknown order
        pages = PublicPageJournal.objects.filter(is_visible=True)


    # no pages ? get first default
    if not pages:
        pages = PublicPage.objects.filter(is_default=True, is_enabled=True)[0:1]

    # colors
    for page in pages:
        (bgcolor, fgcolor)= get_bootstrap_colors2(page.severity)
        page.bgcolor = bgcolor
        page.fgcolor = fgcolor

    # user_ip = get_user_ip(request)
    # trusted_ip = is_trusted_ip(user_ip)
    
    context["pages"] = pages[:max_display]
    # context["trusted_ip"] = trusted_ip
    # if trusted_ip:
    #     context["button_anonymous"] = "Anonyme"
    return render(request, 'app_sirene/index.html', context)

