# app_user - aaa.py

import json
import re
import base64
from pprint import pprint

from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.forms.models import model_to_dict
from django.utils.translation import gettext as _
from django.db.models import F

from django.contrib.auth import authenticate

from app_home.configuration import load_configuration_cache
from app_home.configuration import get_configuration

from app_home.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL

from .models import SireneGroup
from .models import SirenePermission
from .models import SireneVisitor


from .ip import get_user_ip
from .ip import is_trusted_ip

from .user import user_get_by_login
from .user import user_get_by_id
from .user import user_create
from .group import group_get_by_name
from .role import role_get_by_name

from app_home.cache import flush_cache_per_request

# cache
global_aaa = None



# def debug_aaa(data):
#     debug_aaa = get_configuration(appname="user", keyname="DEBUG_AAA")
#     if debug_aaa == "yes":
#         print("DEBUG_AAA: ", data)

# ==============================================================================
# update_last_login
# ==============================================================================

def update_last_login(aaa):


    if aaa["userid"]:
        user = user_get_by_id(aaa["userid"])
        if user:
            user.last_login = timezone.now()
            user.save(update_fields=["last_login"])

    elif aaa["is_visitor"]:
        
        username = aaa["username"]
        if not username:
            return
        if len(username) == 0:
            return

        visitor = SireneVisitor.objects.filter(username=username).first()
        if not visitor:
            visitor = SireneVisitor(username=username)

        visitor.last_login = timezone.now()
        visitor.user_ip = aaa.get("user_ip", "")
        visitor.save()
        return



# ==============================================================================
# start_ajax
# ==============================================================================

def start_ajax(request):


    flush_cache_per_request() 


    # reset conf cache (from previous HIT)
    load_configuration_cache()


    # reset current user (from previous HIT)
    global global_aaa 
    global_aaa = None
    

    if  get_configuration(appname="user", keyname="DEBUG_AAA2") == "yes":
        aaa = get_aaa(request)
        request.session["aaa"] = aaa
        pprint(aaa)
    else:
        # session ?
        if 'aaa' in request.session:
            aaa = request.session['aaa']
        else:
            aaa = get_aaa(request)
            request.session["aaa"] = aaa

    global_aaa = aaa

    context = {}
    context["aaa"] = aaa

    return context



# ==============================================================================
# start_view
# - load conf in cache  (refresh for each view)
# - check existing session => get login / age
# - get_aaa => redirect if KO
# - check perm for view  => redirect if KO
# - log
# ==============================================================================

    # r = sirene_start_view(request, domain="category", view="list", 
    #     noauth="app_sirene:index", perm="p_conf_cat_read", noauthz="app_sirene:private")
    # if r:
    #     return redirect(r)
    # aaa = get_aaa(request)



def start_view(request, app="na", view="na", noauth=None, perm=None, noauthz=None, visitor=False):
    ''' returns a context w/ a redirect target if auth or autor i'''


    flush_cache_per_request() 


    # visitor access need explicit visitor=True

    debug_aaa     = get_configuration(appname="user", keyname="DEBUG_AAA")
    debug_aaa2    = get_configuration(appname="user", keyname="DEBUG_AAA2")
    cache_session = get_configuration(appname="user", keyname="CACHE_SESSION")

    if debug_aaa == "yes":
        print("------------------------------------")
        print(f"START VIEW - start for app={app} - view={view}")



    # reset conf cache (from previous HIT)
    load_configuration_cache()
    if debug_aaa == "yes":
        print("START VIEW - load_configuration_cache()")

    # reset current user (from previous HIT)
    global global_aaa 
    global_aaa = None
    
    if debug_aaa == "yes":
        print("START VIEW - global_aaa emptied to None")


    # do not use session cache
    if  cache_session == "no":
        aaa = get_aaa(request)
        if debug_aaa == "yes":
            print("START VIEW - cache_session=no ; get_aaa() called")

    # use session cache
    else:
        # cache_hit
        if 'aaa' in request.session:
            aaa = request.session['aaa']
            if debug_aaa == "yes":
                print("START VIEW - cache_session=yes. cache_hit, aaa in request.session")
        
        # cache_miss
        else:
            aaa = get_aaa(request)
            if debug_aaa == "yes":
                print("START VIEW - cache_session=yes ; cache_miss ;  get_aaa()")
            # only cache if successfully authenticated
            if aaa["is_authenticated"]:
                request.session["aaa"] = aaa
                if debug_aaa == "yes":
                    print("START VIEW - cache miss + authenticated=yes ; set request.session")
            else:
                request.session.flush()
                if debug_aaa == "yes":
                    print("START VIEW - cache_miss + authenticated = no ; flush session")


    global_aaa = aaa

    if  debug_aaa2 == "yes":
        pprint(aaa)
    elif debug_aaa == "yes":
        print("START VIEW  aaa result:")
        print("  auth_mode:", aaa["auth_mode"])
        print("  impersonate:", aaa["impersonate"])
        print("  is_anonymous:", aaa["is_anonymous"])
        print("  is_authenticated:", aaa["is_authenticated"])
        print("  is_admin:", aaa["is_admin"] )
        print("  is_trusted_ip:", aaa["is_trusted_ip"])
        print("  is_visitor:", aaa["is_visitor"])
        print("  user_ip:", aaa["user_ip"])
        print("  user_id:", aaa["userid"])
        print("  username:", aaa["username"])
        pprint(aaa["user"])
        print("  ---------")

    context = {}
    context["aaa"] = aaa
    context["redirect"] = None

    update_last_login(aaa)

    # if noauth provided; restricted access
    if noauth:

        # Django Auth mode
        if aaa["auth_mode"] == "local":
            if not (aaa['is_authenticated'] or (visitor and aaa["is_visitor"])):
                context["redirect"] = f"{settings.LOGIN_URL}?next={request.path}" 
                return context

        # other modes / federated mode
        else:
            if not (aaa['is_authenticated'] or (visitor and aaa["is_visitor"])):
                context["redirect"] = noauth
                return context
            
    
    if perm:
        if perm not in aaa["perms"]:
            log(WARNING, aaa=aaa, app=app, view=view, action="access", data="Not allowed")
            context["redirect"] = noauthz
            return context

    log(DEBUG, aaa=aaa, app=app, view=view, action="start_view", status="OK")

    return context


# ----------------------------------------------------------------------
# get_aaa
# ----------------------------------------------------------------------
#
# auth_mode          : oauth2, basic, local, forced, unittest (hidden)
#
# is_trusted_ip      : user IP belongs to configured trusted list
# is_anonymous       : default - no session, no user info (no auth performed)
# is_visitor         : externally authenticated  but not in SireneUser DB (e.g. external oauth)
# is_authenticated   : authenticated & exist in SireneUser DB (or admin)
#                     - auth basic (HTTP header)
#                     - fed/oauth2
#                     - sirene internal auth forms [TBD]
#                     - session from previous
# is_admin           : built-in admin account
# user               : dict serialized SireneUser
# username           : login
# userid             : pk from DB
# user_ip            : 
# perms:[]           : [keyname, ...]
# groups:[]          : [group keynales, ...]
# groups_indirect:[] : [group keynames, ...]
# impersonate        : True/False
# ----------------------------------------------------------------------

def get_aaa(request):

    global global_aaa 

    debug_aaa = get_configuration(appname="user", keyname="DEBUG_AAA")

    # use global_aaa created from start_view, (...)  if available
    if global_aaa:
        if debug_aaa == "yes":
            print("DEBUG AAA - used global_aaa for get_aaa(). DONE")
        return global_aaa
    
    #load_configuration_from_db()

    aaa={}

    uname = ""
    email = ""

    aaa["is_trusted_ip"] = False
    aaa["is_anonymous"] = True
    aaa["is_authenticated"] = False
    aaa["is_visitor"] = False
    aaa["is_admin"] = False

    aaa['username'] = "unknown"
    aaa["user"] = None
    aaa["userid"] = None
    
    aaa["groups"] = []
    aaa["groups_indirect"] = []
    #aaa["roles"] = []
    aaa["perms"] = []

    aaa['user_ip'] = get_user_ip(request)
    aaa["is_trusted_ip"] = is_trusted_ip(aaa['user_ip'])

    aaa["impersonate"] = False

    # ----------------
    # get uname
    # ----------------

    #auth_mode = get_setting("SIRENE_AUTH_MODE", "basic")
    auth_mode = get_configuration(appname="user", keyname="AUTH_MODE")
    aaa["auth_mode"] = auth_mode

    if debug_aaa == "yes":
        print("DEBUG_AAA - auth_mode: ", auth_mode)

    if auth_mode == "basic":
        header = request.META.get('HTTP_AUTHORIZATION')
        try:
            auth = header.split()
        except Exception as e:
            auth = ""
            uname = ""
        if len(auth) == 2:
            if auth[0].lower() == "basic":
                myenc = auth[1]
                myenc = bytes(myenc, encoding='utf-8')
                uname,pwd = str(base64.b64decode(myenc)).split(':')
                uname=uname[2:]
    
    # OIDC  (OKTA , ...)
    elif auth_mode == "oauth2":
        login_field = get_configuration(appname="user", keyname="AUTH_FEDERATED_LOGIN_FIELD")
        uname =  request.headers.get(login_field)
        email_field = get_configuration(appname="user", keyname="AUTH_FEDERATED_EMAIL_FIELD")
        email =  request.headers.get(email_field)

        if debug_aaa == "yes":
            print("DEBUG_AAA - oauth2 login_field / uname ", login_field, uname)
            print("DEBUG_AAA - oauth2 email_field / email ", email_field, email)

    elif auth_mode == "local":
        if request.user.is_authenticated:
            uname = request.user.username
            aaa["is_anonymous"] = False
            if debug_aaa == "yes":
                print("DEBUG_AAA - auth_mode local - anonymous=False, request.user.username", uname)
        else:
            if debug_aaa == "yes":
                print("DEBUG_AAA - auth_mode local - no request.user.is_authenticated , no username")



    # Django unittest
    elif auth_mode == "unittest":
        # TODO : make other user available (or None)
        uname = "unittest"
        aaa["is_anonymous"] = False

    elif auth_mode == "forced":
        # Force User from env/settings
        force_user = get_configuration(appname="user", keyname="AUTH_MODE_FORCE_USER")
        if debug_aaa == "yes":
            print("DEBUG_AAA - force_user ", force_user)
        if len(force_user) > 0:
            uname = force_user
            aaa["is_anonymous"] = False
            if debug_aaa == "yes":
                print("DEBUG_AAA - force_user ; is_anonymous=False")
        else:
            aaa["is_anonymous"] = True
            if debug_aaa == "yes":
                print("DEBUG_AAA - force_user ; is_anonymous=True. DONE.")
            return aaa

    if debug_aaa == "yes":
        print("DEBUG_AAA - uname=", uname)


    # ----------------
    # anonymous
    # ----------------

    # no uname : anonymous !
    if not uname:
        aaa["is_anonymous"] = True
        if debug_aaa == "yes":
            print("DEBUG_AAA - no uname ; is_anonymous=True. DONE.")
        return aaa
    
    if len(uname) == 0:
        aaa["is_anonymous"] = True
        if debug_aaa == "yes":
            print("DEBUG_AAA - len(uname)=0 ; is_anonymous=True. DONE.")
        return aaa

    aaa["is_anonymous"] = False
    if debug_aaa == "yes":
        print("DEBUG_AAA - is_anonymous=False, uname=", uname)

    # ----------------
    # username 
    # ----------------

    # remove domain from uname ?
    truncate_login = get_configuration(appname="user", keyname="AUTH_LOGIN_REMOVE_DOMAIN")
    if truncate_login == "yes":
        if '@' in uname:
            uname = re.sub("@(.*)$", '', uname)
            if debug_aaa == "yes":
                print("DEBUG_AAA - truncated domain name in login ; uname=", uname)


    # ----------------
    # impersonate ?
    # ----------------
    if uname == "admin":
        impersonate = get_configuration(appname="user", keyname="SYSADMIN_IMPERSONATE")
        if impersonate:
            if debug_aaa == "yes":
                print("DEBUG_AAA - impersonate: ", impersonate)
            if len(impersonate) > 0:
                uname = impersonate
                aaa["impersonate"] = True
                if debug_aaa == "yes":
                    print("DEBUG_AAA - impersonated=True, uname=", uname)

    # authenticated / visitor : register name
    aaa['username'] = uname
    
    if debug_aaa == "yes":
        print("DEBUG_AAA - uname post impersonate: ", uname)

    # -------------------------------
    # check in DB  > is_authenticated
    # -------------------------------
    # default safe values
    aaa["is_visitor"] = True
    aaa["is_authenticated"] = False

    user = user_get_by_login(uname)

    if debug_aaa == "yes":
        print(f"DEBUG_AAA - user_get_by_login(): {user}")

    # JIT Just-in-Time provisioning if allowed  and user not found
    jit = get_configuration(appname="user", keyname="AUTH_PROVISIONING")
    if debug_aaa == "yes":
        print("DEBUG_AAA - jit config: ", jit)

    # user in DB
    if user:
        aaa["is_visitor"] = False
        aaa['is_authenticated'] = True
        if debug_aaa == "yes":
            print("DEBUG_AAA - user found in DB ; visitor=False, authenticated=True")        

        if not user.is_enabled:        
            aaa['is_authenticated'] = False
            if debug_aaa == "yes":
                print("DEBUG_AAA - user disabled ; authenticated=False. DONE.")        
            return aaa

    # user not in DB
    else:
        if debug_aaa == "yes":
            print("DEBUG_AAA - user NOT in DB , assuming visitor for now")

        # if uname == "admin":
        #     aaa["is_visitor"] = False
        #     aaa['is_authenticated'] = True
        #     user = user_create({'login':uname})
        #     if debug_aaa == "yes":
        #         print("DEBUG_AAA - uname is admin")

        if jit == "visitor":
            aaa["is_visitor"] = True
            aaa['is_authenticated'] = False
            # stay visitor, not authenticated (not in DB)
            if debug_aaa == "yes":
                print(f"DEBUG_AAA - jit ({jit}), visitor=True, authenticated=False")

        elif jit == "create" or jit == "sync":
            
            if not email:
                user = user_create({'login':uname})
            else:
                user = user_create({'login':uname, 'email':email})

            if user:
                log(INFO, aaa=aaa, data=f"JIT - ({jit}) get_aaa JIT user created in DB: {uname}")
                # not a visitor anymore, real user in DB
                aaa["is_visitor"] = False
                aaa['is_authenticated'] = True
                if debug_aaa == "yes":
                    print(f"DEBUG_AAA - jit ({jit}) user created. visitor=False. authenticated=True")
            else:
                # failed to create in DB
                log(ERROR, aaa=aaa, data=f"JIT ({jit}) failed to create user in DB: {uname}")
                if debug_aaa == "yes":
                    print(f"DEBUG_AAA - jit ({jit}) user not created. visitor=True. authenticated=False")
                aaa["is_visitor"] = True
                aaa['is_authenticated'] = True
                return aaa


        
        else:
            # unknown user, and no JIT / no auto-create
            aaa["is_visitor"] = False
            aaa['is_authenticated'] = False
            if debug_aaa == "yes":
                print(f"DEBUG_AAA - jit other: ({jit}). DONE")
            return aaa
    
    # ---------------------
    # user_id / user dict
    # ---------------------

    if user:

        aaa['userid'] = user.id
        #aaa['user'] = user   # !!!! => Serialization KO when session/tasks / need conversion to dict
        dict_attributs =  [
            "login", "firstname","lastname", "displayname", "email","mobile", 
            "external_id", "is_enabled", "description",
            "want_notifications", "want_24", "want_email", "want_sms", 
            "secondary_email", "secondary_mobile"
        ] 
        # standard attibuts
        aaa['user'] = model_to_dict(user, fields=dict_attributs)
        if debug_aaa == "yes":
            print("DEBUG_AAA - aaa[user] attributes populated with DB content.")


    # ----------------
    # Authorizations
    # ----------------

    # groups (and role_default)
    groups = get_direct_groups(aaa)
    aaa["groups"] = groups

    groups_indirect = get_indirect_groups(aaa)
    aaa["groups_indirect"] = groups_indirect

    # add perms & roles to global_aaa dict
    tmp = get_permissions_for_aaa(aaa)
    aaa["perms"] = [i.keyname for i in tmp] 

    if debug_aaa == "yes":
        print("DEBUG_AAA - group, groups_indirect, perms computed.")

    # ----------------
    # admin
    # ----------------

    # built-in user admin ?
    if aaa["username"] == "admin":
        aaa["is_admin"] = True
        if debug_aaa == "yes":
            print("DEBUG_AAA - username is admin => is_admin=True")

    # built-in role_admin  ?
    if "role_admin" in groups + groups_indirect:
        aaa["is_admin"] = True
        if debug_aaa == "yes":
            print("DEBUG_AAA - role_admin => is_admin=True")

    if aaa["is_admin"]:
        # give all groups, all perms        
        perms = []
        dbperms = SirenePermission.objects.all()
        for p in dbperms:
            perms.append(p.keyname)
        aaa["perms"] = perms
        allgroups=[]
        dbgroups = SireneGroup.objects.all()
        for g in dbgroups:
            allgroups.append(g.keyname)
        aaa["groups"] = allgroups
        if debug_aaa == "yes":
            print("DEBUG_AAA - all groups, perms for admin")

    if debug_aaa == "yes":
        print("DEBUG_AAA - get_aaa() end, DONE.")

    return aaa


# ------------------------------------
# get all groups for aaa 'user'
# ------------------------------------

def get_direct_groups(aaa):

    reply=[]

    if "username" not in aaa:
        return reply

    user = user_get_by_login(aaa["username"])
    # visitor or changed user ?
    if not  user:
        return reply

    # groups = SireneGroup.objects.filter(is_enabled = True, users__in=[user]).prefetch_related("subgroups").distinct()
    groups = SireneGroup.objects.filter(is_enabled = True, users__in=[user]).distinct()

    # convert to array
    for g in groups:
        reply.append(g.keyname)

    # append "role_default"
    gobj = SireneGroup.objects.filter(is_enabled = True, is_role=True, keyname="role_default").first()
    if gobj:
        reply.append(gobj.keyname)

    return reply





def get_indirect_groups(aaa):

    reply = []

    if "username" not in aaa:
        return reply

    user = user_get_by_login(aaa["username"])
    # visitor ?
    if not user:
        return reply


    dbgroups = SireneGroup.objects.filter(is_enabled = True).prefetch_related("subgroups").prefetch_related("users").distinct()

    #new = 0
    redo = 0

    # first level above aaa["groups""]
    for g0 in aaa["groups"]:
        for g1 in dbgroups:
            if g0 in [x.keyname for x in g1.subgroups.all()]:
                if user not in g1.users.all():
                    if g1.keyname not in reply:
                        reply.append(g1.keyname)
                        redo = 1
        
        # while new parent groups, loop
        while redo > 0:
            redo = 0
            for g1 in reply:
                for g2 in dbgroups:
                    if g1 in [x.keyname for x in g2.subgroups.all()]:
                        if user not in g2.users.all():
                            if g2.keyname not in reply:
                                reply.append(g2.keyname)
                                redo = 1
                
    reply = list(set(reply))
    return reply


def get_permissions_for_aaa(aaa):

    perms = []

    groups = aaa["groups"]  + aaa["groups_indirect"]
    for g in groups:
        gobj = role_get_by_name(g, enabled_only=True)
        if gobj:
            dbperms = SirenePermission.objects.filter(sirenegroup__in=[gobj])
            for p in dbperms:
                #perms.append(p.keyname)
                perms.append(p)

    # role_default permissions come from direct groups

    # add all default=True permissions
    # deprecated => to be removed
    dbperms = SirenePermission.objects.filter(default=True)
    for p in dbperms:
        if len(p.keyname) > 0:
            perms.append(p)

    perms = list(set(perms))
    return perms


# --- by login, return full objects
# TODO: build cache

def get_all_groups_for_login(login=None):

    reply = []
    if not login:
        return reply
    user = user_get_by_login(login)
    if not  user:
        return reply

    alldbgroups = SireneGroup.objects.filter(is_enabled = True)\
        .prefetch_related("subgroups")\
        .prefetch_related("users")\
        .prefetch_related("permissions")\
        .distinct()

    #initgroups = SireneGroup.objects.filter(is_enabled = True, users__in=[user]).distinct()

    #new = 0
    redo = 0

    # initgroups
    initgroups = []
    for g in alldbgroups:
        if user in g.users.all():
            if g not in initgroups:
                initgroups.append(g)

    # append "role_default"
    gobj = SireneGroup.objects.filter(is_enabled = True, is_role=True, keyname="role_default").first()
    initgroups.append(gobj)


    # first level of groups where user isn't 
    for g0 in initgroups:
        for g1 in alldbgroups:
            #if g0.keyname in [x.keyname for x in g1.subgroups.all()]:
            if g0 in g1.subgroups.all():
                if user not in g1.users.all():
                    if g1 not in reply:
                        reply.append(g1)
                        redo = 1
        
        # while new parent groups, loop
        while redo > 0:
            redo = 0
            for g1 in reply:
                for g2 in alldbgroups:
                    #if g1.keyname in [x.keyname for x in g2.subgroups.all()]:
                    if g1 in g2.subgroups.all():    
                        if user not in g2.users.all():
                            if g2 not in reply:
                                reply.append(g2)
                                redo = 1
                
    #reply = list(set(reply))
    return initgroups, reply



