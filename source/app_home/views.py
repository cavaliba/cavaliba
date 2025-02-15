# (c) cavaliba.com - home - views.py

import re

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.utils.translation import gettext as _
from django.db.models import Q


from app_user.aaa import start_view

from .configuration import get_configuration

from .log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL
from .log import purge
from .models import CavalibaLog

from .configuration import get_initial_form
from .configuration import get_post_form
from .configuration import save_form

from .home import get_app_by_name
from .home import get_applist
from .home import get_cavaliba_apps
from .home import cavaliba_update

from app_data.data import update_bigset


# -----------------------------------------
# status page
#-----------------------------------------
def status(request):
    return HttpResponse("OK")


# -----------------------------------------
# private - private_page
#-----------------------------------------

def private(request):

    context = start_view(request, app="home", view="private", 
            noauth="app_sirene:index", perm="p_home_access", noauthz="app_sirene:index")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]

    if request.method == "POST":

        if 'p_home_update' in aaa["perms"]:
            cavaliba_update()
            update_bigset()
            messages.add_message(request, messages.SUCCESS, _("Dashboard updated"))
            log(INFO, aaa=aaa, app="home", view="private", action="cavaliba_update", status="OK", data="")

        else:
            messages.add_message(request, messages.ERROR, _("Not allowed"))
            log(ERROR, aaa=aaa, app="home", view="dashboard", action="update", status="KO", data="not allowed")
            return render(request, 'app__sirene:index')    

    apps = get_applist(aaa)
    for x in apps:
        if x.keyname=='home':
            apps.remove(x)
            break


    # page/order for UI
    # [  [page1, [item1, item22,  ...] , [ page2, [...] ] ,  ... ]
    paginated = []
    pagelist = []
    index = {}     # page => [class1, class2]
    default_name = get_configuration("home", "GLOBAL_APPNAME")

    for element in apps:
        order = element.order
        section = element.dashboard_section
        if not section:
            section = default_name
        if len(section) == 0:
            section = default_name
        if section not in index:
            index[section] = []
            pagelist.append(section)
        index[section].append(element)
        default_name = section
    for p in pagelist:
        paginated.append([p, index[p]])


    log(DEBUG, aaa=aaa, app="home", view="dash", action="view", status="OK")


    #context['apps'] = apps
    context['paginated'] = paginated
    return render(request, 'app_home/private.html', context)


# -----------------------------------------
# configuration
#-----------------------------------------

def configuration(request, appname=None):

    #context = start_view(request, app="home", view="private", noauth="app_sirene:index", perm="p", noauthz="app_sirene:index")
    context = start_view(request, app="home", view="configuration", noauth="app_home:index", 
                            perm="p_conf_admin", noauthz="app_sirene:index")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]

    if appname:
        appobj = get_app_by_name(appname)
        if not appobj:
            return redirect("app_home:index")


    if request.method == "POST":

        form = get_post_form(request, appname=appname)

        if form.is_valid():
            save_form(form, appname=appname)
            messages.add_message(request, messages.SUCCESS, _("Configuration updated"))
            log(INFO, aaa=aaa, app="home", view="configuration", action="update", status="OK", data=f"app {appname}")
            return redirect("app_home:configuration", appname)
        else:
            messages.add_message(request, messages.ERROR, _("Invalid configuration"))
    
    else:
        form = get_initial_form(appname)

    if appname:
        context["appname"] = appobj.keyname

    context["apps"] = get_cavaliba_apps()
    context["form"] = form
    return render(request, 'app_home/configuration.html', context)


# -----------------------------------------
# log
#-----------------------------------------

def logview(request, level="debug"):

    context = start_view(request, app="home", view="log", noauth="app_sirene:index", perm="p_log_view", noauthz="app_home:index")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]


    # purge ?
    if request.method == "POST":
        if request.POST.get('purge'):
            if 'p_log_manage' in aaa["perms"]:
                count = purge(aaa=aaa, keep_days=0)
                messages.add_message(request, messages.SUCCESS, _("All Log purged: ") + str(count) )
                log(WARNING, aaa=aaa, app="home", view="log", action="purge", status="OK", data=f"{count} removed")
                return redirect("app_home:log")


    # bigset or not
    count = CavalibaLog.objects.count()
    bigset = True
    context["bigset"] = bigset
    context["count"] = count



    # Filter POST (form)
    # -------------------
    #query = request.GET.get("q", "")
    query = ""
    if request.method == "POST":
        if request.POST.get('query'):
            query = request.POST.get('query')
    if request.method == "GET":
        if request.GET.get('query'):
            query = request.GET.get('query')
    if query:
        m = re.compile(r'[a-zA-Z0-9()_/.-]*$')
        if not m.match(query):
            query = ""
    context["query"] = query


    # partial query + paginate if bigset
    try:
        size = int(request.GET.get("size", 100))
        page = int(request.GET.get("page",1))
    except:
        return redirect("app_home:log")

    if page < 1 or size > 10000 or size < 1:
        return redirect("app_home:log")


    offset = (page-1) * size
    limit = offset + size

    if len(query) > 0:

        if level not in ["debug","info","warning","error","critical"]:
            level = "debug"

        if level == "info":
            level_display = _('INFO')
            logs = CavalibaLog.objects.all().order_by("-id").filter(level__in=['INFO','WARNING','ERROR','CRITICAL']).filter(
                    Q(app__icontains=query) |
                    Q(username__icontains=query) |
                    Q(view__icontains=query) |
                    Q(action__icontains=query) |
                    Q(data__icontains=query) |
                    Q(status__icontains=query) |
                    Q(user_ip__icontains=query)\
                    )[offset:limit]

        elif level == "warning":
            level_display = _('WARNING')
            logs = CavalibaLog.objects.all().order_by("-id").filter(level__in=['WARNING','ERROR','CRITICAL']).filter(
                    Q(app__icontains=query) |
                    Q(username__icontains=query) |
                    Q(view__icontains=query) |
                    Q(action__icontains=query) |
                    Q(data__icontains=query) |
                    Q(status__icontains=query) |
                    Q(user_ip__icontains=query)\
                    )[offset:limit]                
            

        elif level == "error":
            level_display = _('ERROR')
            logs = CavalibaLog.objects.all().order_by("-id").filter(level__in=['ERROR','CRITICAL']).filter(
                    Q(app__icontains=query) |
                    Q(username__icontains=query) |
                    Q(view__icontains=query) |
                    Q(action__icontains=query) |
                    Q(data__icontains=query) |
                    Q(status__icontains=query) |
                    Q(user_ip__icontains=query)\
                    )[offset:limit]                
            

        elif level == "critical":
            level_display = _('CRITICAL')
            logs = CavalibaLog.objects.all().order_by("-id").filter(level='CRITICAL').filter(
                    Q(app__icontains=query) |
                    Q(username__icontains=query) |
                    Q(view__icontains=query) |
                    Q(action__icontains=query) |
                    Q(data__icontains=query) |
                    Q(status__icontains=query) |
                    Q(user_ip__icontains=query)\
                    )[offset:limit]                        

        else:
            level_display = _('DEBUG')
            logs = CavalibaLog.objects.all().order_by("-id").filter(
                    Q(app__icontains=query) |
                    Q(username__icontains=query) |
                    Q(view__icontains=query) |
                    Q(action__icontains=query) |
                    Q(data__icontains=query) |
                    Q(status__icontains=query) |
                    Q(user_ip__icontains=query)\
                    )[offset:limit]
    else:

        if level not in ["debug","info","warning","error","critical"]:
            level = "debug"

        if level == "info":
            level_display = _('INFO')
            logs = CavalibaLog.objects.all().order_by("-id").filter(level__in=['INFO','WARNING','ERROR','CRITICAL'])[offset:limit]
            
        elif level == "warning":
            level_display = _('WARNING')
            logs = CavalibaLog.objects.all().order_by("-id").filter(level__in=['WARNING','ERROR','CRITICAL'])[offset:limit]

        elif level == "error":
            level_display = _('ERROR')
            logs = CavalibaLog.objects.all().order_by("-id").filter(level__in=['ERROR','CRITICAL'])[offset:limit]

        elif level == "critical":
            level_display = _('CRITICAL')
            logs = CavalibaLog.objects.all().order_by("-id").filter(level='CRITICAL')[offset:limit]

        else:
            level_display = _('DEBUG')
            logs = CavalibaLog.objects.all().order_by("-id")[offset:limit]
                
    
    # PREV | FIRST || CURRENT or ... || LAST | NEXT
    context["size"] = size
    context["page"] = page
    page_last = int (count / size) + 1
    
    if page > 1:
        context["page_prev"] = page - 1
    else:
        context["page_prev"] = page
    
    if page == 1:
        context["page_first"] = True
    else:
        context["page_first"] = False

    if page > 1 and page < page_last:
        context["page_current"] = True
    else:
        context["page_current"] = False

    context["page_last"] = page_last
    if page < page_last:
        context["page_last_active"] = False
    else:
        context["page_last_active"] = True

    if page < page_last:
        context["page_next"] = page + 1
    else:
        context["page_next"] = page

    context["level"] = level_display
    context["logs"] = logs
    return render(request, 'app_home/log.html', context)

