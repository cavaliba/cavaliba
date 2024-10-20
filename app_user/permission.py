# app_user - perm.py

from app_log.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL
#log(DEBUG, aaa=aaa, app="log", view="private", action="list", status="OK", data="")



from .models import SirenePermission



def permission_get_by_id(pid):
    return SirenePermission.objects.filter(pk=pid).first()


def permission_get_by_name(keyname):
    return SirenePermission.objects.filter(keyname=keyname).first()



def permission_set(keyname=None, appname=None, displayname=None, description=None, default=False):
    
    ''' create/update a single permission in Database '''

    if not keyname:
        return

    p = permission_get_by_name(keyname)
    if not p:
        p = SirenePermission()
        p.keyname = keyname

    if appname:
        p.appname = appname

    if displayname:
        p.displayname = displayname

    if description:        
        p.description = description

    p.default = default
    p.save()
    return p


def permission_cleanup(appname, keyname):
    return SirenePermission.objects.filter(appname=appname, keyname=keyname).delete()



# Called by commands / external to sync permissions for this app
def permission_register(appname, permissions):

    #total, created, deleted, invalid  = permission_set_all_for_app(appname=appname, permlist=permissions)

    total = 0
    created = 0
    deleted = 0
    invalid = 0
 
    if not permissions:
        return

    perm_list = []

    # add permissions
    for permtuple in permissions:

        try:
            (keyname, displayname, description, default) = permtuple
        except:
            invalid += 1
            continue

        perm_list.append(keyname)

        p = permission_set(keyname=keyname, appname=appname, displayname=displayname, description=description, default=default)
        if p:
            created += 1


    # Remove unused permissions from DB
    perms = SirenePermission.objects.filter(appname=appname).all()
    for perm in perms:
        if perm.keyname not in perm_list:
            perm.delete()
            deleted += 1

    total = SirenePermission.objects.filter(appname=appname).count()

    #print (f"Register permissions for {appname} - total={total} created={created} deleted={deleted} invalid={invalid}")

    return total, created, deleted, invalid

