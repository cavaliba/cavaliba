# app_home - home.py

from app_conf.configuration import register_configuration

from app_user.permission import permission_register
from app_user.permission import permission_cleanup
from app_user.group import group_register_builtin
from app_user.role import role_register_builtin


import app_home.register as app_home
import app_conf.register as app_conf
import app_data.register as app_data
import app_log.register as app_log
import app_user.register as app_user
import app_sirene.register as app_sirene

from .models import DashboardApp



def get_app_by_name(appname):
    app = DashboardApp.objects.filter(keyname=appname).first()
    return app


def get_applist(aaa=None):
    '''   filter: enabled + perm = True'''
    
    apps = DashboardApp.objects.all().prefetch_related("permission").order_by("order")

    reply = []

    for app in apps:

        if app.state != "enabled":
            continue
            
        try:
            perm = app.permission.keyname
        except:
            continue

        if perm:
            if perm in aaa["perms"]:
                reply.append(app)
            
    return reply





def update_dashboard():
    

    # Update SireneConfiguration DB for all Apps
    #print("Register SireneConfiguration for all apps")
    register_configuration()
    #print()



    # register HOME

    #print("HOME: ", app_home.APP_NAME, app_home.APP_VERSION)
    permission_register(app_home.APP_NAME,app_home.PERMISSIONS)
    permission_cleanup(app_home.APP_NAME,app_home.PERMISSIONS_CLEANUP)    
    role_register_builtin(app_home.APP_NAME,app_home.ROLES_BUILTIN)
    group_register_builtin(app_home.APP_NAME,app_home.GROUPS_BUILTIN)
    obj = DashboardApp.objects.filter(keyname="home").first()
    if obj:
        obj.version = app_home.APP_VERSION
        obj.save()
    #print()

    # register CONF

    #print("CONF: ", app_conf.APP_NAME, app_conf.APP_VERSION)
    permission_register(app_conf.APP_NAME,app_conf.PERMISSIONS)
    permission_cleanup(app_conf.APP_NAME,app_conf.PERMISSIONS_CLEANUP)    
    role_register_builtin(app_conf.APP_NAME,app_conf.ROLES_BUILTIN)
    group_register_builtin(app_conf.APP_NAME,app_conf.GROUPS_BUILTIN)
    obj = DashboardApp.objects.filter(keyname="conf").first()
    if obj:
        obj.version = app_conf.APP_VERSION
        obj.save()
    #print()


    # register DATA

    #print("DATA: ", app_data.APP_NAME, app_data.APP_VERSION)
    permission_register(app_data.APP_NAME,app_data.PERMISSIONS)
    permission_cleanup(app_data.APP_NAME,app_data.PERMISSIONS_CLEANUP)    
    role_register_builtin(app_data.APP_NAME,app_data.ROLES_BUILTIN)
    group_register_builtin(app_data.APP_NAME,app_data.GROUPS_BUILTIN)
    obj = DashboardApp.objects.filter(keyname="data").first()
    if obj:
        obj.version = app_data.APP_VERSION
        obj.save()
    #print()


    # register LOG

    #print("LOG:  ", app_log.APP_NAME, app_log.APP_VERSION)
    permission_register(app_log.APP_NAME,app_log.PERMISSIONS)
    permission_cleanup(app_log.APP_NAME,app_log.PERMISSIONS_CLEANUP)
    role_register_builtin(app_log.APP_NAME,app_log.ROLES_BUILTIN)
    group_register_builtin(app_log.APP_NAME,app_log.GROUPS_BUILTIN)
    obj = DashboardApp.objects.filter(keyname="log").first()
    if obj:
        obj.version = app_log.APP_VERSION
        obj.save()
    #print()


    # register USER

    #print("USER: ", app_user.APP_NAME, app_user.APP_VERSION)
    permission_register(app_user.APP_NAME,app_user.PERMISSIONS)
    permission_cleanup(app_user.APP_NAME,app_user.PERMISSIONS_CLEANUP)
    role_register_builtin(app_user.APP_NAME,app_user.ROLES_BUILTIN)
    group_register_builtin(app_user.APP_NAME,app_user.GROUPS_BUILTIN)
    obj = DashboardApp.objects.filter(keyname="user").first()
    if obj:
        obj.version = app_user.APP_VERSION
        obj.save()
    #print()

    # register SIRENE MSI

    #print("SIRENE: ", app_sirene.APP_NAME, app_sirene.APP_VERSION)
    permission_register(app_sirene.APP_NAME,app_sirene.PERMISSIONS)
    permission_cleanup(app_sirene.APP_NAME,app_sirene.PERMISSIONS_CLEANUP)
    role_register_builtin(app_sirene.APP_NAME,app_sirene.ROLES_BUILTIN)
    group_register_builtin(app_sirene.APP_NAME,app_sirene.GROUPS_BUILTIN)
    obj = DashboardApp.objects.filter(keyname="sirene").first()
    if obj:
        obj.version = app_sirene.APP_VERSION
        obj.save()
    #print()


    # For each app, call 
