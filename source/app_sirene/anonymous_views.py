# (c) cavaliba.com - sirene - views_trusted_ip.py


from django.shortcuts import render, redirect


from app_home.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL

from .models import Message

from .common import get_bootstrap_colors2
from .common import cleanup_old_messages

from app_user.aaa import start_view
from app_user.aaa import get_aaa
    
#-----------------------------------------
# {% url 'anonymous_index' %}
#-----------------------------------------

def list(request):

    context = start_view(request, app="sirene", view="anonymous_list")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]

    if not (aaa["is_trusted_ip"] or aaa["is_authenticated"] or aaa["is_visitor"]):
        return redirect("app_sirene:index")

    count = cleanup_old_messages()
    if count>0:
        log(INFO, aaa=aaa, app="sirene", view="anonymous_list", action="cleanup", data=f"{count} removed")


    pages = []
        
    # shared private pages
    globalpages = Message.objects.filter(is_visible=True, has_privatepage=True).order_by('-created_at')
    for page in globalpages:
        (bgcolor, fgcolor)= get_bootstrap_colors2(page.severity)
        page.bgcolor=bgcolor
        page.fgcolor=fgcolor
        #page.dest="TOUS"
        pages.append(page)


    log(DEBUG, aaa=aaa, app="sirene", view="anonymous_list", action="get", status="OK", data=f"")

    context["privatepages"] = pages
    return render(request, 'app_sirene/anonymous_index.html', context)



def detail(request, pageid):
    ''' display private message details for anonymous users'''

    context = start_view(request, app="sirene", view="anonymous_detail")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]

    aaa = get_aaa(request)
    if not (aaa['is_trusted_ip'] or aaa['is_authenticated']  or aaa["is_visitor"]):
        log(DEBUG, aaa=aaa, app="sirene", view="anonymous_detail", action="get", status="KO", data=f"access denied")
        return redirect("app_sirene:index")

    
    page = Message.objects.filter(pk=pageid).first()
    if not page:
        log(DEBUG, aaa=aaa, app="sirene", view="anonymous_detail", action="get", status="KO", data=f"no page")
        return redirect("app_sirene:anonymous")

    # if private, allowed for all 
    if not page.has_privatepage:
        log(DEBUG, aaa=aaa, app="sirene", view="anonymous_detail", action="get", status="KO", data=f"not allowed")
        return redirect("app_sirene:anonymous")


    (bgcolor, fgcolor)= get_bootstrap_colors2(page.severity)
    page.bgcolor=bgcolor
    page.fgcolor=fgcolor


    log(DEBUG, aaa=aaa, app="sirene", view="anonymous_detail", action="get", status="OK", data=f"")

    context["page"] = page
    
    return render(request, 'app_sirene/anonymous_detail.html', context)

