# app_sirene - register.py


APP_NAME = "sirene"


# - p_sirene_access
# - p_sirene_access_restricted
# - p_sirene_detail
# - p_sirene_history
# - p_sirene_new
# - p_sirene_update
# - p_sirene_archive
# - p_sirene_public_push
# - p_sirene_flushall
# - p_sirene_cat_read
# - p_sirene_cat_cud
# - p_sirene_public_read
# - p_sirene_public_cud
# - p_sirene_template_cud
# - p_sirene_template_read
# - p_sirene_import
# - p_sirene_export
# - p_sirene_sms_send
# - p_sirene_sms_journal
# - p_sirene_sms_stat
# - p_log_access


BUILTIN_DATA = '''

_permission:p_sirene_access:
    is_builtin: True
    appname: sirene
    description: "Built-in SIRENE app access"
    displayname: ""

_permission:p_sirene_access_restricted:
    is_builtin: True
    appname: sirene
    description: "Built-in SIRENE app access restricted messages"
    displayname: ""

_permission:p_sirene_detail:
    is_builtin: True
    appname: sirene
    description: "Built-in SIRENE access details"
    displayname: ""

_permission:p_sirene_history:
    is_builtin: True
    appname: sirene
    description: "Built-in SIRENE access history"
    displayname: ""

_permission:p_sirene_new:
    is_builtin: True
    appname: sirene
    description: "Built-in SIRENE create a new notification"
    displayname: ""

_permission:p_sirene_update:
    is_builtin: True
    appname: sirene
    description: "Built-in SIRENE update a notification"
    displayname: ""

_permission:p_sirene_archive:
    is_builtin: True
    appname: sirene
    description: "Built-in SIRENE archive a message"
    displayname: ""

_permission:p_sirene_public_push:
    is_builtin: True
    appname: sirene
    description: "Built-in SIRENE push a public page"
    displayname: ""

_permission:p_sirene_flushall:
    is_builtin: True
    appname: sirene
    description: "Built-in SIRENE archive all active messages"
    displayname: ""

_permission:p_sirene_cat_read:
    is_builtin: True
    appname: sirene
    description: "Built-in SIRENE RO category"
    displayname: ""

_permission:p_sirene_cat_cud:
    is_builtin: True
    appname: sirene
    description: "Built-in SIRENE RW category"
    displayname: ""

_permission:p_sirene_public_read:
    is_builtin: True
    appname: sirene
    description: "Built-in SIRENE RO public models"
    displayname: ""

_permission:p_sirene_public_cud:
    is_builtin: True
    appname: sirene
    description: "Built-in SIRENE RW public models"
    displayname: ""


_permission:p_sirene_template_read:
    is_builtin: True
    appname: sirene
    description: "Built-in SIRENE RO templates"
    displayname: ""

_permission:p_sirene_template_cud:
    is_builtin: True
    appname: sirene
    description: "Built-in SIRENE RW templates"
    displayname: ""

_permission:p_sirene_import:
    is_builtin: True
    appname: sirene
    description: "Built-in SIRENE Import"
    displayname: ""

_permission:p_sirene_export:
    is_builtin: True
    appname: sirene
    description: "Built-in SIRENE Export"
    displayname: ""

_permission:p_sirene_sms_send:
    is_builtin: True
    appname: sirene
    description: "Built-in SIRENE SMS Send"
    displayname: ""

_permission:p_sirene_sms_journal:
    is_builtin: True
    appname: sirene
    description: "Built-in SIRENE SMS Journal"
    displayname: ""

_permission:p_sirene_sms_stat:
    is_builtin: True
    appname: sirene
    description: "Built-in SIRENE SMS Stat"
    displayname: ""


# roles
# ------


_role:role_sirene_admin:
    is_builtin: True
    displayname: Built-in Sirene admin Role
    permissions: 
       - p_sirene_access
       - p_sirene_access_restricted
       - p_sirene_detail
       - p_sirene_history
       - p_sirene_new
       - p_sirene_update
       - p_sirene_archive
       - p_sirene_public_push
       - p_sirene_flushall
       - p_sirene_cat_read
       - p_sirene_cat_cud
       - p_sirene_public_read
       - p_sirene_public_cud
       - p_sirene_template_cud
       - p_sirene_template_read
       - p_sirene_import
       - p_sirene_export
       - p_sirene_sms_send
       - p_sirene_sms_journal
       - p_sirene_sms_stat
       - p_log_access

_role:role_sirene_manage:
    is_builtin: True
    displayname: Built-in Sirene Manage Role
    permissions: 
       - p_sirene_access
       - p_sirene_access_restricted
       - p_sirene_detail
       - p_sirene_history
       - p_sirene_new
       - p_sirene_update
       - p_sirene_archive
       - p_sirene_public_push
       - p_sirene_flushall
       - p_sirene_cat_read
       - p_sirene_public_read
       - p_sirene_public_cud
       - p_sirene_template_cud
       - p_sirene_template_read
       - p_sirene_sms_send
       - p_sirene_sms_journal
       - p_sirene_sms_stat
       - p_log_access

_role:role_sirene_operator:
    is_builtin: True
    displayname: Built-in Sirene Operator Role
    permissions: 
       - p_sirene_access
       - p_sirene_access_restricted
       - p_sirene_detail
       - p_sirene_history
       - p_sirene_new
       - p_sirene_update
       - p_sirene_archive
       - p_sirene_public_push
       - p_sirene_flushall
       - p_sirene_cat_read
       - p_sirene_public_read
       - p_sirene_template_read
       - p_sirene_sms_send
       - p_sirene_sms_journal
       - p_sirene_sms_stat


_role:role_sirene_user:
    is_builtin: True
    displayname: Built-in Sirene User Role
    permissions: 
       - p_sirene_access
       - p_sirene_detail
       - p_sirene_history       









'''



# ROLES_BUILTIN = {
#     'role_sirene_admin': [
#         "p_sirene_access",
#         "p_sirene_access_restricted",        
#         "p_sirene_detail",
#         "p_sirene_history",
#         'p_sirene_new',
#         "p_sirene_update",
#         "p_sirene_archive",        
#         "p_sirene_public_push",
#         "p_sirene_flushall",
#         "p_sirene_cat_read",
#         "p_sirene_cat_cud",
#         "p_sirene_public_read",
#         "p_sirene_public_cud",
#         "p_sirene_template_cud",
#         "p_sirene_template_read",
#         "p_sirene_import",
#         "p_sirene_export",
#         "p_sirene_conf",

#         "p_sirene_app_read",
#         "p_sirene_site_read",
#         "p_sirene_sitegroup_read",
#         "p_sirene_user_read",
#         "p_sirene_group_read",

#         "p_sirene_sms_send",
#         "p_sirene_sms_journal",
#         "p_sirene_sms_stat",
#         "p_log_access",
#     ],
#     'role_sirene_manage': [
#         "p_sirene_access",
#         "p_sirene_access_restricted",        
#         "p_sirene_detail",
#         "p_sirene_history",
#         'p_sirene_new',
#         "p_sirene_update",
#         "p_sirene_archive",        
#         "p_sirene_public_push",
#         "p_sirene_flushall",
#         "p_sirene_cat_read",
#         "p_sirene_public_read",
#         "p_sirene_public_cud",
#         "p_sirene_template_cud",
#         "p_sirene_template_read",
#         "p_sirene_conf",
#         "p_sirene_app_read",
#         "p_sirene_site_read",
#         "p_sirene_sitegroup_read",
#         "p_sirene_user_read",
#         "p_sirene_group_read",
#         "p_sirene_sms_send",
#         "p_sirene_sms_journal",
#         "p_sirene_sms_stat",
#         "p_log_access",        
#     ],
#     'role_sirene_operator': [
#         "p_sirene_access",
#         "p_sirene_detail",        
#         "p_sirene_history",
#         'p_sirene_new',
#         "p_sirene_update",
#         "p_sirene_archive",
#         "p_sirene_public_push",
#         "p_sirene_flushall",
#         "p_sirene_cat_read",
#         "p_sirene_public_read",
#         "p_sirene_template_read",
#         "p_sirene_conf",
#         "p_sirene_app_read",
#         "p_sirene_site_read",
#         "p_sirene_sitegroup_read",
#         "p_sirene_user_read",
#         "p_sirene_group_read",
#         "p_sirene_sms_send",
#         "p_sirene_sms_journal",
#         "p_sirene_sms_stat",
#         "p_log_access",        
#     ],
#     'role_sirene_user': [
#         "p_sirene_access",
#         "p_sirene_detail",        
#         "p_sirene_history",
#     ],

#     'role_sirene_contact': [
#     ],
# }

# # (keyname, displayname, description, default)
# PERMISSIONS = [

#     ("p_sirene_access", "Access to sirene, view private notifications","", False),
#     ("p_sirene_detail", "View notifications details and updates","", False),
#     ("p_sirene_access_restricted", "View restricted notifications from other users","", False),
#     ("p_sirene_history", "View archived notifications","", False),

#     ("p_sirene_new", "Create a notification","", False),
#     ("p_sirene_update", "Update an existing notification","", False),
#     ("p_sirene_archive", "Archive an active notification","", False),
#     ("p_sirene_flushall", "Remove all active notifications","", False),
#     ("p_sirene_public_push", "","", False),

#     ("p_sirene_cat_read", "View categories","", False),
#     ("p_sirene_cat_cud", "Edit categories","", False),

#     ("p_sirene_public_read", "View public page config","", False),
#     ("p_sirene_public_cud", "Edit public pages","", False),

#     ("p_sirene_template_cud","View templates","",False),
#     ("p_sirene_template_read","Edit templates","",False),

#     ("p_sirene_import", "Use import tool for sirene items","", False),
#     ("p_sirene_export", "Use export tools","", False),

#     ("p_sirene_app_read", "Acces to application management","", False),
#     ("p_sirene_site_read", "Access to site management","", False),
#     ("p_sirene_sitegroup_read", "Access to sitegroup management","", False),
#     ("p_sirene_user_read", "Access to user management","", False),
#     ("p_sirene_group_read", "Access to group management","", False),

#     ("p_sirene_sms_send", "","", False),
#     ("p_sirene_sms_journal", "","", False),
#     ("p_sirene_sms_stat", "","", False),

#     ("p_sirene_conf", "Access to admin menu","", False),

# # ---

#     ("p_sirene_anonymous", "Can access anonymous page (trusted_ip, visitor, ...)","", False),
        
# ]

