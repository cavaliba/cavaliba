# (c) cavaliba.com - home - cavaliba.py


# global framework version
CAVALIBA_VERSION = "3.15.0"

# Global True list string equivs
TRUE_LIST = ('on', 'On', 'ON', True, 'yes', 'Yes', 'YES', 'True', 'true', 'TRUE', 1, "1")


GLOBAL_BUILTIN_DATA = '''

# ---------------
# permissions
# ---------------

# admin
# all permissions by default

- classname: _user
  keyname: admin
  displayname: Built-in Global Admin user


# conf

- classname: _permission
  keyname: p_conf_access
  appname: conf
  description: "Built-in conf access permission"
  displayname: "p_conf_access"
  is_builtin: True

- classname: _permission
  keyname: p_conf_admin
  appname: conf
  description: "Built-in conf admin permission"
  displayname: "p_conf_admin"
  is_builtin: True

# log    

- classname: _permission
  keyname: p_log_access
  is_builtin: True
  appname: log
  description: "Built-in LOG app Access"
  displayname: "p_log_access"

- classname: _permission
  keyname: p_log_view
  is_builtin: True
  appname: log
  description: "Built-in LOG view"
  displayname: "p_log_view"

- classname: _permission
  keyname: p_log_manage
  is_builtin: True
  appname: log
  description: "Built-in LOG manage"
  displayname: "p_log_manage"

# ------------
# roles
# ------------

# admin

- classname: _role
  keyname: role_admin
  displayname: Built-in Global Admin role
  is_builtin: true
  users:
    - admin
    # all permissions by default (code)

# default

- classname: _role
  keyname: role_default
  is_builtin: True
  displayname: Built-in Default role for new users/anonymous/visitors
  permissions:
    - p_sirene_access
    - p_sirene_history
    - p_sirene_detail

    
# Log

- classname: _role
  keyname: role_log_view
  displayname: Built-in LOG view Role
  is_builtin: true
  permissions:
    - p_log_access
    - p_log_view

- classname: _role
  keyname: role_log_manage
  displayname: Built-in LOG manage Role
  is_builtin: true
  permissions:
    - p_log_access
    - p_log_view
    - p_log_manage
'''

