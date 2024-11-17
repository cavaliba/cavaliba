# cavaliba.com
# cavaliba.py


# global framework version
CAVALIBA_VERSION = "3.11-beta"


GLOBAL_BUILTIN_DATA = '''

# user
# ----

# all permissions by default
_user:admin:
    displayname: Built-in Global Admin user


# permission conf
# ---------------

_permission:p_conf_access:
    appname: conf
    description: "Built-in conf access permission"
    displayname: "p_conf_access"
    is_builtin: True

_permission:p_conf_admin:
    appname: conf
    description: "Built-in conf admin permission"
    displayname: "p_conf_admin"
    is_builtin: True



# permission log    
# --------------
_permission:p_log_access:
    is_builtin: True
    appname: log
    description: "Built-in LOG app Access"
    displayname: "p_log_access"

_permission:p_log_view:
    is_builtin: True
    appname: log
    description: "Built-in LOG view"
    displayname: "p_log_view"


_permission:p_log_manage:
    is_builtin: True
    appname: log
    description: "Built-in LOG manage"
    displayname: "p_log_manage"


# roles
# -----

_role:role_admin:
    displayname: Built-in Global Admin role
    is_builtin: true
    users:
      - admin
    # all permissions by default (code)


_role:role_default:
    is_builtin: True
    displayname: Built-in Default role for new users/anonymous/visitors
    permissions:
       - p_default
       - p_sirene_access
       - p_sirene_history
       - p_sirene_detail

# roles Log
# ---------

_role:role_log_view:
    displayname: Built-in LOG view Role
    is_builtin: true
    permissions:
      - p_log_access
      - p_log_view


_role:role_log_manage:
    displayname: Built-in LOG manage Role
    is_builtin: true
    permissions:
      - p_log_access
      - p_log_view
      - p_log_manage
'''

