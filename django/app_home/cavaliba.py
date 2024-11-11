# cavaliba.com
# cavaliba.py


# global framework version
CAVALIBA_VERSION = "3.10"


GLOBAL_BUILTIN_DATA = '''

# user
# ----

# all permissions by default
_user:admin:
    displayname: Built-in Global Admin user


# permissions
# -----------

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


'''

