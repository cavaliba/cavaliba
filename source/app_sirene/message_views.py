# (c) cavaliba.com - sirene - views_private.py


from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext as _


from app_home.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL

from app_user.aaa import start_view
from app_user.user import user_get_by_login

from .models import MessageTemplate
from .models import Message
from .models import MessageUpdate
from .models import PublicPageJournal

from .common import get_bootstrap_colors2
from .common import cleanup_old_messages
from .common import replace_placeholder

from .notify import sirene_expand_notify
from .notify import sirene_notify
from .notify import sirene_notify_update

from .message_form import MessageForm
from .message_form import MessageUpdateForm




# -------------------------------------------
# private INDEX, message list
# -------------------------------------------

def list(request):

    context = start_view(request, app="sirene", view="message_list", 
        noauth="app_sirene:index", perm="p_sirene_access", noauthz="app_sirene:index",
        # explicitly allow visitor
        visitor = True  
        )
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]

    

    count = cleanup_old_messages(aaa=aaa)
    if count>0:
        log(INFO, aaa=aaa, app="sirene", view="message", action="cleanup", status="OK", data=f"{count} removed")


    pages = []
        
    # shared private pages
    globalpages = Message.objects.filter(is_visible=True, has_privatepage=True).order_by('-created_at')
    for page in globalpages:
        (bgcolor, fgcolor)= get_bootstrap_colors2(page.severity)
        page.bgcolor=bgcolor
        page.fgcolor=fgcolor
        #page.dest="TOUS"
        page.is_mypage = False
        pages.append(page)

    # limited user pages
    #user = aaa["user"]
    user = user_get_by_login(aaa["username"])
    if "p_sirene_access_restricted" in aaa["perms"]:
        mypages = Message.objects.filter(is_visible=True, has_privatepage=False).order_by('-created_at')
    else:
        mypages = Message.objects.filter(is_visible=True, has_privatepage=False, users__in=[user]).order_by('-created_at')
    
    for page in mypages:
        (bgcolor, fgcolor)= get_bootstrap_colors2(page.severity)
        page.bgcolor = bgcolor
        page.fgcolor = fgcolor
        
        page.is_mypage = True
        pages.append(page)
    


    log(DEBUG, aaa=aaa, app="sirene", view="message", action="list", status="OK", data=f"")

    context["privatepages"] = pages
    context["mypages"] = mypages

    return render(request, 'app_sirene/message_list.html', context)



# ---------------
def history(request):

    context = start_view(request, app="sirene", view="history", 
        noauth="app_sirene:index", perm="p_sirene_history", noauthz="app_sirene:private",
        visitor=True)
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]


    pages=[]

    # private pages for all
    globalpages = Message.objects.filter(is_visible=False, has_privatepage=True).order_by('-created_at')
    for page in globalpages:
        (bgcolor, fgcolor)= get_bootstrap_colors2(page.severity)
        page.bgcolor=bgcolor
        page.fgcolor=fgcolor
        pages.append(page)

    # limited user pages
    user = user_get_by_login(aaa["username"])
    # if perm to see all restricted message, select all
    if "p_sirene_access_restricted" in aaa["perms"]:
        mypages = Message.objects.filter(is_visible=False, has_privatepage=False).order_by('-created_at')
    # else, filter by user
    else:
        mypages = Message.objects.filter(is_visible=False, has_privatepage=False, users__in=[user]).order_by('-created_at')
    
    for page in mypages:
        (bgcolor, fgcolor)= get_bootstrap_colors2(page.severity)
        page.bgcolor = bgcolor
        page.fgcolor = fgcolor
        pages.append(page)

    log(DEBUG, aaa=aaa, app="sirene", view="message", action="history", status="OK", data=f"")

    context["page_obj"] = pages
    return render(request, 'app_sirene/history.html', context)




def aaa_message_allowed(message=None, aaa=None):
    '''
    Check if private message can be accessed by user. 
    For detail/remove/history/... views
    '''

    # if has_private, allowed for all 
    if message.has_privatepage:
        return True

    if 'p_sirene_access_restricted' in aaa["perms"]:
        return True

    #user = aaa["user"]
    user = user_get_by_login(aaa['username'])

    if user in message.users.all():
        return True

    return False

# ---------------
def detail(request, pageid):
    ''' GET id - display details + admin tools'''

    context = start_view(request, app="sirene", view="detail", 
        noauth="app_sirene:index", perm="p_sirene_detail", noauthz="app_sirene:private",
        visitor=True)
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]


    try: 
        page = Message.objects.get(pk=pageid)
    except:
        messages.add_message(request, messages.ERROR, _("Not found"))
        log(ERROR, aaa=aaa, app="sirene", view="message", action="detail", status="KO", data=f"id {page.id} not found")
        return redirect("app_sirene:private")


    if not aaa_message_allowed(message=page, aaa=aaa):
        messages.add_message(request, messages.ERROR, _("Not allowed"))
        log(ERROR, aaa=aaa, app="sirene", view="message", action="detail", status="KO", data=f"id {page.id} not allowed")
        return redirect("app_sirene:private")


    (bgcolor, fgcolor)= get_bootstrap_colors2(page.severity)
    page.bgcolor=bgcolor
    page.fgcolor=fgcolor

    # print(page.id, page.updates)
    # for i in page.updates.all():
    #     print(i, i.created_by, i.content)

    log(DEBUG, aaa=aaa, app="sirene", view="message", action="detail", status="OK", data=f"{page.title}")


    context["page"] = page
    context["title"] = f"{page.title}"

    return render(request, 'app_sirene/message_detail.html', context)


# ---------------
def remove(request):
    ''' POST with pageid > close message in Message'''

    context = start_view(request, app="sirene", view="remove", 
        noauth="app_sirene:index", perm="p_sirene_archive", noauthz="app_sirene:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]


    if request.method != 'POST':
        messages.add_message(request, messages.ERROR, _("Invalid call"))
        log(ERROR, aaa=aaa, app="sirene", view="message", action="remove", status="KO", data=f"Method not supported")
        return redirect("app_sirene:private")

    try:
        pageid=int(request.POST['pageid'])
    except Exception as e:
        messages.add_message(request, messages.ERROR, _("Not found"))
        log(ERROR, aaa=aaa, app="sirene", view="message", action="remove", status="KO", data=f"Not found (no id)")
        return redirect("app_sirene:private")
    
    try: 
        page = Message.objects.get(pk=pageid)
    except Exception as e:
        messages.add_message(request, messages.ERROR, _("Not found"))
        log(ERROR, aaa=aaa, app="sirene", view="message", action="remove", status="KO", data=f"Not found (invalid id)")
        return redirect("app_sirene:private")


    if not aaa_message_allowed(message=page, aaa=aaa):
        messages.add_message(request, messages.ERROR, _("Not allowed"))
        log(ERROR, aaa=aaa, app="sirene", view="message", action="remove", status="KO", data=f"Not allowed for {page.title}")        
        return redirect("app_sirene:private")

    page.remove(aaa=aaa)
    log(INFO, aaa=aaa, app="sirene", view="message", action="remove", status="OK", data=f"{page.title} removed")
    messages.add_message(request, messages.SUCCESS, _("Message removed"))

    return redirect("app_sirene:private")


# ---------------
def update(request, mid=None):
    ''' Edit MessageUpdate - GET/POST'''

    context = start_view(request, app="sirene", view="update", 
        noauth="app_sirene:index", perm="p_sirene_update", noauthz="app_sirene:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]

    try: 
        message = Message.objects.get(pk=mid)
    except:
        messages.add_message(request, messages.ERROR, _("Not found"))
        log(ERROR, aaa=aaa, app="sirene", view="update", action="edit", status="KO", data=f"ID not found")
        return redirect("app_sirene:private")

    if request.method == "POST":

        form = MessageUpdateForm(request.POST)

        if form.is_valid():
            
            mu = MessageUpdate()
            cd = form.cleaned_data
            mu.message = message
            mu.content = cd["content"]
            mu.created_by = aaa['username']
            mu.has_email = cd['has_email']
            mu.has_sms = cd['has_sms']
            mu.save()

            # message updated_at/by update
            message.updated_by = aaa['username']
            message.updated_at = mu.created_at
            message.save() 

            # send notifications update
            (email_count, sms_count, error) = sirene_notify_update(update=mu, aaa=aaa)
            
            if error == 1:
                messages.add_message(request, messages.ERROR, _("Partial / Error - check SMS quota"))
                log(WARNING, aaa=aaa, app="sirene", view="update", action="send", status="KO", data=f"Partial / SMS Quota reached")
            else:
                messages.add_message(request, messages.SUCCESS, f"OK {email_count} emails / {sms_count} SMS")
                log(INFO, aaa=aaa, app="sirene", view="update", action="send", status="OK", data=f"Update sent")

            return redirect("app_sirene:private")

        else:
            messages.add_message(request, messages.ERROR, _("Invalid form"))
            log(INFO, aaa=aaa, app="sirene", view="update", action="edit", status="KO", data=f"Invalid form")
    else:
        form = MessageUpdateForm()
        log(DEBUG, aaa=aaa, app="sirene", view="update", action="edit", status="OK", data=f"")

    context["form"] = form
    context["message"] = message
    return render(request, 'app_sirene/message_update.html', context)


# ---------------------------
# EDITOR V2
# ---------------------------

def editor2(request, template_id=None):
    """ 
    template_id given from URL editor/##/ 
    """

    context = start_view(request, app="sirene", view="editor2", 
        noauth="app_sirene:index", perm="p_sirene_new", noauthz="app_sirene:private")
    if context["redirect"]:
        return redirect(context["redirect"])
    aaa = context["aaa"]

    template = None
    if template_id:
        try:
            template = MessageTemplate.objects.get(pk=template_id)
        except:
            messages.add_message(request, messages.ERROR, _("Invalid request"))
            log(ERROR, aaa=aaa, app="sirene", view="message", action="edit", status="KO", data=f"invalid id {template_id}")
            return redirect("app_sirene:private")


    form = {}

    # if POST, a form is already being edited
    if request.method == "POST":

        form = MessageForm(request.POST)

        if form.is_valid():

            newmessage = Message()
            cd = form.cleaned_data

            newmessage.title    = cd['title']
            newmessage.severity = cd['severity']
            newmessage.body     = cd['body']

            #replace_placeholder()
            replace_placeholder(newmessage, cd)


            newmessage.has_privatepage = cd['has_privatepage']        
            newmessage.has_email       = cd['has_email']
            newmessage.has_sms         = cd['has_sms']
            newmessage.created_by      = aaa['username']

            newmessage.save()


            # set category text value
            category = cd['category']
            try:
                newmessage.category = category.name
            except:
                newmessage.category = "?"

            if template:
                newmessage.template = template.name


            publicpage = cd['publicpage']
            if publicpage:
                journal = PublicPageJournal.add(publicpage=publicpage, aaa=aaa)
                if journal:
                    newmessage.publicpage = journal
                    # info(aaa=aaa, domain="editor.public", data=f"publicpage {journal.name} published")
                    newmessage.save()
                    newmessage.has_publicpage = True
                    newmessage.publicpage_text = publicpage.body
                else:
                    newmessage.has_publicpage = False
            else:
                newmessage.has_publicpage = False

            # notify_xxxxx
            #newmessage.notify_app.clear()
            for item in cd["notify_app"]:
                newmessage.notify_app.add(item)

            #newmessage.notify_site.clear()
            for item in cd["notify_site"]:
                newmessage.notify_site.add(item)

            #newmessage.notify_sitegroup.clear()
            for item in cd["notify_sitegroup"]:
                newmessage.notify_sitegroup.add(item)

            #newmessage.notify_customer.clear()
            for item in cd["notify_customer"]:
                newmessage.notify_customer.add(item)

            #newmessage.notify_group.clear()
            for item in cd["notify_group"]:
                newmessage.notify_group.add(item)

            sirene_expand_notify(newmessage)
            newmessage.save()

            (email_count, sms_count, error) = sirene_notify(newmessage, aaa=aaa)
            newmessage.email_count = email_count
            newmessage.sms_count = sms_count
            newmessage.save()


            if error == 1:
                messages.add_message(request, messages.ERROR, _("Partial / Error - check SMS quota"))
                log(WARNING, aaa=aaa, app="sirene", view="message", action="send", status="KO", data=f"Partial / SMS Quota reached")
            else:
                messages.add_message(request, messages.SUCCESS, f"OK {email_count} emails / {sms_count} SMS")
                log(INFO, aaa=aaa, app="sirene", view="message", action="send", status="OK", data=f"OK {email_count} emails / {sms_count} SMS")


            return redirect("app_sirene:private")

        else:
            messages.add_message(request, messages.ERROR, _("Invalid form"))
            log(INFO, aaa=aaa, app="sirene", view="message", action="edit", status="KO", data="Invalid form")

    # GET
    else:

        # blank or template ?
        if template_id:

            template = MessageTemplate.objects.get(pk=template_id)
            initial = {}

            #initial["name"]             = template.name
            initial["title"]            = template.title
            initial["category"]         = template.category
            initial["severity"]         = template.severity
            initial["description"]      = template.description
            initial["body"]             = template.body
            initial["publicpage"]       = template.publicpage
            initial["has_publicpage"]   = template.has_publicpage
            initial["has_privatepage"]  = template.has_privatepage
            initial["has_email"]        = template.has_email
            initial["has_sms"]          = template.has_sms

            # notify_xxxx split
            initial["notify_group"]     = [g for g in template.notify_group.all()]
            initial["notify_site"]      = [i for i in template.notify_site.all()]
            initial["notify_app"]       = [i for i in template.notify_app.all()]
            initial["notify_sitegroup"] = [i for i in template.notify_sitegroup.all()]
            initial["notify_customer"]  = [i for i in template.notify_customer.all()]

            form = MessageForm(initial=initial)
            log(DEBUG, aaa=aaa, app="sirene", view="message", action="edit", status="OK", data=f"template {template.title}")

        else:
            # if not "p_sirene_new" in aaa["perms"]:
            #     messages.add_message(request, messages.ERROR, _("Not allowed"))
            #     log(WARNING, aaa=aaa, app="sirene", view="message", action="editor", status="KO", data=f"not allowed")
            #     return redirect("app_sirene:template_list")

            form = MessageForm()
            log(DEBUG, aaa=aaa, app="sirene", view="message", action="edit", status="OK", data="")


    context['form'] = form
    
    return render(request, 'app_sirene/message_edit.html', context)
    


