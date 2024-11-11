# app_home - aaa.py

APP_NAME = "home"


# - p_home_access
# - p_home_update
# - p_home_import_yaml


BUILTIN_DATA = '''

# permissions
# -----------


_permission:p_home_access:
    is_builtin: True
    appname: home
    description: "Built-in HOME app Access"
    displayname: "p_home_access"

_permission:p_home_update:
    is_builtin: True
    appname: home
    description: "Built-in HOME update dashboard"
    displayname: "p_home_update"


_permission:p_home_import_yaml:
    is_builtin: True
    appname: home
    description: "Built-in HOME import YAML"
    displayname: "p_home_import_yaml"

# roles
# -----

_role:role_home_admin:
    displayname: Built-in HOME Admin Role
    is_builtin: true
    permissions:
      - p_home_access
      - p_home_update
      - p_home_import_yaml

_role:role_home_user:
    displayname: Built-in HOME User Role
    is_builtin: true
    permissions:
      - p_home_access


# Home Dashboard
# --------------



_home:home:
    #_action: ...
    displayname: Home Dashboard
    description: Main App
    icon: fa-home
    url: /home/private/
    page: Applications
    order: 10
    permission: p_home_access

# ---
_home:sirene:
    displayname: Sirene
    description: Sirene
    icon: fa-sun-o
    url: /sirene/private/
    page: Applications
    order: 20
    permission: p_sirene_access


_home:sms:
    displayname: SMS Sarbacane
    description: Send SMS
    icon: fa-paper-plane
    url: /sirene/private/sms/send/
    page: Applications
    order: 30
    permission: p_sirene_access


# ----

_home:data_app:
    displayname: Applications
    description: Applications
    icon: fa-firefox
    url: /data/private/c/app/list/
    page: Data Schema
    order: 100
    permission: p_data_access


_home:data_site:
    displayname: Sites
    description: Sites
    icon: fa-hospital-o
    url: /data/private/c/site/list/
    #page: 
    order: 110
    permission: p_data_access

_home:data_sitegroup:
    displayname: Groups of Sites
    description: Groups of Sites
    icon: fa-university
    url: /data/private/c/sitegroup/list/
    #page: 
    order: 120
    permission: p_data_access

# --- 

_home:user:
    displayname: Users
    description: Users
    icon: fa-user-plus
    url: /user/private/users/
    order: 130
    permission: p_user_access

_home:group:
    displayname: Groups
    description: Groups
    icon: fa-users
    url: /user/private/groups/
    order: 140
    permission: p_group_ro


# Admin

_home:data:
    displayname: Data Management
    description: Data Management
    icon: fa-database
    url: /data/private/
    page: Admin
    order: 200
    permission: p_data_access

_home:role:
    displayname: Roles
    description: Roles
    icon: fa-user-secret
    url: /user/private/roles/
    order: 202
    permission: p_role_ro

_home:sirene_template:
    displayname: Sirene Templates
    description: Sirene Templates
    icon: fa-bullhorn
    url: /sirene/private/template/
    order: 204
    permission: p_sirene_template_read


_home:sirene_public:
    displayname: Sirene Public
    description: Sirene Public Pages
    icon: fa-globe
    url: /sirene/private/publicpage/
    order: 206
    permission: p_sirene_public_read


_home:sirene_category:
    displayname: Sirene Categories
    description: Sirene Categories
    icon: fa-tag
    url: /sirene/private/category/
    order: 220
    permission: p_sirene_cat_read


_home:conf:
    displayname: Configuration
    description: Configuration Management
    icon: fa-wrench
    url: /home/private/conf/
    order: 240
    permission: p_conf_access

# Logs

_home:log:
    displayname: Logs
    description: Audit trail
    icon: fa-list
    url: /log/private/
    page: Logs
    order: 300
    permission: p_log_access

_home:sms_stat:
    displayname: SMS Stats
    description: SMS Stats
    icon: fa-list
    url: /sirene/private/sms/stat/
    page: Logs
    order: 310
    permission: p_sirene_sms_stat

_home:sms_journal:
    displayname: SMS Journal
    description: SMS Journal
    icon: fa-list
    url: /sirene/private/sms/journal/
    page: Logs
    order: 320
    permission: p_sirene_sms_journal



# Doc
_home:cavaliba:
    displayname: Doc Cavaliba (Ext)
    description: Doc Cavaliba
    icon: fa-book
    url: https://cavaliba.com/docs/
    page: Doc
    order: 500
    permission: p_data_access


'''
