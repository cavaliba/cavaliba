# cavaliba.com
# app_user - register.py


APP_NAME = "user"


# Permissions
# - p_user_access
# - p_user_admin
# - p_user_pref
# - p_user_email_test
# - user_sms_test
# - p_user_debug
# - p_user_ro
# - p_user_rw
# - p_user_import
# - p_user_export
# - p_group_ro
# - p_group_rw
# - p_group_import
# - p_group_export
# - p_role_ro
# - p_role_rw
# - p_role_import
# - p_role_export
# - p_permission_ro
# - p_permission_rw
# - p_permission_import
# - p_permission_export



BUILTIN_DATA = '''

_permission:p_user_admin:
    is_builtin: True
    appname: user
    description: "Built-in USER admin"
    displayname: ""

_permission:p_user_access:
    is_builtin: True
    appname: user
    description: "Built-in USER access"
    displayname: ""


_permission:p_user_pref:
    is_builtin: True
    appname: user
    description: "Built-in USER preferences"
    displayname: ""

_permission:p_user_email_test:
    is_builtin: True
    appname: user
    description: "Built-in USER test emails"
    displayname: ""

_permission:p_user_sms_test:
    is_builtin: True
    appname: user
    description: "Built-in USER test sms"
    displayname: ""

_permission:p_user_debug:
    is_builtin: True
    appname: user
    description: "Built-in USER debug"
    displayname: ""



_permission:p_user_ro:
    is_builtin: True
    appname: user
    description: "Built-in USER user read"
    displayname: ""

_permission:p_user_rw:
    is_builtin: True
    appname: user
    description: "Built-in USER user write"
    displayname: ""


_permission:p_user_import:
    is_builtin: True
    appname: user
    description: "Built-in USER user import"
    displayname: ""

_permission:p_user_export:
    is_builtin: True
    appname: user
    description: "Built-in USER user export"
    displayname: ""




_permission:p_group_ro:
    is_builtin: True
    appname: user
    description: "Built-in USER group read"
    displayname: ""

_permission:p_group_rw:
    is_builtin: True
    appname: user
    description: "Built-in USER group write"
    displayname: ""


_permission:p_group_import:
    is_builtin: True
    appname: user
    description: "Built-in USER group import"
    displayname: ""

_permission:p_group_export:
    is_builtin: True
    appname: user
    description: "Built-in USER group export"
    displayname: ""



_permission:p_role_ro:
    is_builtin: True
    appname: user
    description: "Built-in USER role read"
    displayname: ""

_permission:p_role_rw:
    is_builtin: True
    appname: user
    description: "Built-in USER role write"
    displayname: ""


_permission:p_role_import:
    is_builtin: True
    appname: user
    description: "Built-in USER role import"
    displayname: ""

_permission:p_role_export:
    is_builtin: True
    appname: user
    description: "Built-in USER role export"
    displayname: ""


_permission:p_permission_ro:
    is_builtin: True
    appname: user
    description: "Built-in USER permission read"
    displayname: ""

_permission:p_permission_rw:
    is_builtin: True
    appname: user
    description: "Built-in USER permission write"
    displayname: ""


_permission:p_permission_import:
    is_builtin: True
    appname: user
    description: "Built-in USER permission import"
    displayname: ""

_permission:p_permission_export:
    is_builtin: True
    appname: user
    description: "Built-in USER permission export"
    displayname: ""

# ------------

_role:role_user_admin:
    is_builtin: True
    displayname: Built-in USER ADMIN Role
    permissions: 
      - p_user_access
      - p_user_admin
      - p_user_pref
      - p_user_email_test
      - user_sms_test
      - p_user_debug
      - p_user_ro
      - p_user_rw
      - p_user_import
      - p_user_export
      - p_group_ro
      - p_group_rw
      - p_group_import
      - p_group_export
      - p_role_ro
      - p_role_rw
      - p_role_import
      - p_role_export
      - p_permission_ro
      - p_permission_rw
      - p_permission_import
      - p_permission_export


_role:role_user_rw:
    is_builtin: True
    displayname: Built-in USER RW Role
    permissions: 
      - p_user_access
      - p_user_pref
      - p_user_email_test
      - user_sms_test
      - p_user_debug
      - p_user_ro
      - p_user_rw
      - p_user_import
      - p_user_export
      - p_group_ro
      - p_group_rw
      - p_group_import
      - p_group_export
      - p_role_ro


_role:role_user_ro:
    is_builtin: True
    displayname: Built-in USER RO Role
    permissions: 
      - p_user_access
      - p_user_pref
      - p_user_debug
      - p_user_ro
      - p_group_ro


_role:role_group_ro:
    is_builtin: True
    displayname: Built-in USER Group RO Role
    permissions: 
      - p_user_access
      - p_user_ro
      - p_group_ro

_role:role_group_rw:
    is_builtin: True
    displayname: Built-in USER Group RW Role
    permissions: 
      - p_user_access
      - p_user_ro
      - p_group_ro
      - p_group_rw
      - p_group_import
      - p_group_export


_role:role_role_ro:
    is_builtin: True
    displayname: Built-in USER Role RO Role
    permissions: 
      - p_user_access
      - p_user_ro
      - p_group_ro
      - p_permission_ro
      - p_role_ro

_role:role_role_rw:
    is_builtin: True
    displayname: Built-in USER Role RW Role
    permissions: 
      - p_user_access
      - p_user_ro
      - p_group_ro
      - p_role_ro
      - p_role_rw
      - p_role_import
      - p_role_export
      - p_permission_ro
      - p_permission_rw
      - p_permission_import
      - p_permission_export


_role:role_security_audit:
    is_builtin: True
    displayname: Built-in USER Security RO Role
    permissions: 
      - p_user_access
      - p_user_pref
      - p_user_email_test
      - user_sms_test
      - p_user_debug
      - p_user_ro
      - p_user_export
      - p_group_ro
      - p_group_export
      - p_role_ro
      - p_role_export
      - p_permission_ro
      - p_permission_export


_role:role_security_admin:
    is_builtin: True
    displayname: Built-in USER Security RW Role
    permissions: 
      - p_user_access
      - p_user_admin
      - p_user_pref
      - p_user_email_test
      - user_sms_test
      - p_user_debug
      - p_user_ro
      - p_user_rw
      - p_user_import
      - p_user_export
      - p_group_ro
      - p_group_rw
      - p_group_import
      - p_group_export
      - p_role_ro
      - p_role_rw
      - p_role_import
      - p_role_export
      - p_permission_ro
      - p_permission_rw
      - p_permission_import
      - p_permission_export




'''


# (keyname, displayname, description, default)
# PERMISSIONS = [
    

#     ("p_user_access", "Access to User App UI", "", False),
#     ("p_user_pref", "Edit self preferences", "Edit self preferences", False),
#     ("p_user_debug", "Access Env debug", "", False),

#     ("p_user_view", "User View", "", False),
#     ("p_user_cud", "User Edit", "", False),
#     ("p_user_delete", "User Delete", "", False),
#     ("p_user_export", "User Export", "", False),
#     ("p_user_import", "User Import", "", False),

#     ("p_user_email_test", "Send test email", "", False),
#     ("p_user_sms_test", "Send test SMS", "", False),

#     ("p_group_view", "Group View", "", False),
#     ("p_group_cud", "Group Edit", "", False),
#     ("p_group_delete", "Group Delete", "", False),
#     ("p_group_export", "Group Export", "", False),
#     ("p_group_import", "Group Import", "", False),

#     ("p_user_map", "map users to groups", "", False),
#     ("p_group_map", "map groups to groups", "", False),

#     ("p_role_ro", "Roles RO", "", False),
#     ("p_role_rw", "Roles RW/Delete/Export/Map/Perms", "", False),
#     ("p_role_import", "Role Import", "", False),

#     ("p_permission_import", "Role Import Permissions", "", False),
#     #("p_role_map", "map groups to roles", "", False),

# ]


# ROLES_BUILTIN = {

#     # prefs ?
#     # visitors ?
#     # users

#     'role_user_ro': [
#         "p_user_access",
#         "p_user_pref",
#         "p_user_ro",
#         "p_user_debug",
#     ],
#     'role_user_rw': [
#         "p_user_access",
#         "p_user_pref",
#         "p_user_debug",
#         "p_user_view",
#         "p_user_cud",
#         "p_user_email_test",
#         "p_user_sms_test",
#         "p_user_map",
#     ],
#     'role_user_admin': [
#         "p_user_access",
#         "p_user_pref",
#         "p_user_debug",
#         "p_user_view",
#         "p_user_cud",
#         "p_user_email_test",
#         "p_user_sms_test",
#         "p_user_delete",
#         "p_user_export",
#         "p_user_import",
#         "p_user_map",
#     ],

#     'role_group_ro': [
#         "p_group_view",
#     ],
#     'role_group_rw': [
#         "p_group_view",
#         "p_group_cud",
#         "p_user_map",
#         "p_group_map",
#     ],
#     'role_group_admin': [
#         "p_group_view",
#         "p_group_cud",
#         "p_group_delete",
#         "p_group_export",
#         "p_group_import",
#         "p_user_map",
#         "p_group_map",
#     ],

#     'role_secu_admin': [
#         "p_role_ro",
#         "p_role_rw",
#         "p_role_import",
#         #"p_role_map",
#         "p_permission_import",
#     ],
#     'role_secu_audit': [
#         "p_user_access",
#         "p_user_pref",
#         "p_user_view",
#         "p_user_export",
#         "p_group_view",
#         "p_group_export",
#         "p_role_ro",
#     ],

#     'role_default': [
#         "p_default",
#         "p_sirene_anonymous",
#         "p_sirene_access",
#         "p_sirene_history",
#         "p_sirene_detail",
#     ],

#     'role_admin': [],  # all perms Sirene 

# }

