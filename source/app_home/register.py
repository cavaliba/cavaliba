# (c) cavaliba.com - home - aaa.py

APP_NAME = "home"

# - p_home_access
# - p_home_update
# - p_home_import_yaml


BUILTIN_DATA = '''

# permission home
# ---------------

- classname: _permission
  keyname: p_home_access
  is_builtin: True
  appname: home
  description: "Built-in HOME app Access"
  displayname: "p_home_access"

- classname: _permission
  keyname: p_home_update
  is_builtin: True
  appname: home
  description: "Built-in HOME update dashboard"
  displayname: "p_home_update"

- classname: _permission
  keyname: p_home_import
  is_builtin: True
  appname: home
  description: "Built-in HOME import"
  displayname: p_home_import



# roles home
# ----------

- classname: _role
  keyname: role_home_admin
  displayname: Built-in HOME Admin Role
  is_builtin: true
  permissions:
    - p_home_access
    - p_home_update
    - p_home_import

- classname: _role
  keyname: role_home_access
  displayname: Built-in HOME User Role
  is_builtin: true
  permissions:
    - p_home_access


# Dashboard entries
# -----------------

# -- Services 

- classname: _home
  keyname: home
  #_action: ...
  displayname: Home Dashboard
  description: Main App
  icon: fa-home
  url: /home/private/
  #dashboard_section: 
  #sidebar_section:
  order: 10
  permission: p_home_access

# ---
- classname: _home
  keyname: sirene
  displayname: Sirene
  description: Sirene
  icon: fa-sun-o
  url: /sirene/private/
  dashboard_section: Services
  sidebar_section: Services
  order: 20
  permission: p_sirene_access


- classname: _home
  keyname: sms
  displayname: SMS Sarbacane
  description: Send SMS
  icon: fa-paper-plane
  url: /sirene/private/sms/send/
  dashboard_section: Services
  sidebar_section: Services
  order: 30
  permission: p_sirene_access


# ---- IAM

- classname: _home
  keyname: user
  displayname: Users
  description: Users
  icon: fa-user-plus
  url: /user/private/users/
  order: 100
  dashboard_section: IAM
  sidebar_section: IAM
  permission: p_user_read

- classname: _home
  keyname: group
  displayname: Groups
  description: Groups
  icon: fa-users
  url: /user/private/groups/
  order: 110
  dashboard_section: IAM
  sidebar_section: IAM
  permission: p_group_read

- classname: _home
  keyname: role
  displayname: Roles
  description: Roles
  icon: fa-user-secret
  url: /user/private/roles/
  order: 120
  dashboard_section: IAM
  sidebar_section: IAM
  permission: p_role_read

# --- Data Management

- classname: _home
  keyname: data_app
  displayname: Applications
  description: Applications
  icon: fa-firefox
  url: /data/private/c/app/list/
  dashboard_section: Data Management
  sidebar_section: Data Management
  order: 200
  permission: p_data_read

- classname: _home
  keyname: data_site
  displayname: Sites
  description: Sites
  icon: fa-hospital-o
  url: /data/private/c/site/list/
  dashboard_section: Data Management
  sidebar_section: Data Management
  order: 210
  permission: p_data_read

- classname: _home
  keyname: data_sitegroup
  displayname: Groups of Sites
  description: Groups of Sites
  icon: fa-university
  url: /data/private/c/sitegroup/list/
  dashboard_section: Data Management
  sidebar_section: Data Management
  order: 220
  permission: p_data_read

- classname: _home
  keyname: data
  displayname: "[+] Data Management"
  description: Data Management (all)
  icon: fa-database
  url: /data/private/
  dashboard_section: Data Management
  sidebar_section: Data Management
  order: 299
  permission: p_data_access


    
# --- Admin

- classname: _home
  keyname: conf
  displayname: Configuration
  description: Configuration Management
  icon: fa-wrench
  url: /home/private/conf/
  order: 300
  dashboard_section: Admin
  sidebar_section: Admin
  permission: p_conf_access

# Logs

- classname: _home
  keyname: log
  displayname: Logs
  description: Audit trail
  icon: fa-list
  url: /home/private/log/
  dashboard_section: Admin
  sidebar_section: Admin
  order: 310
  permission: p_log_access

- classname: _home
  keyname: sms_stat
  displayname: SMS Stats
  description: SMS Stats
  icon: fa-list
  url: /sirene/private/sms/stat/
  dashboard_section: Admin
  sidebar_section: Admin
  order: 320
  permission: p_sirene_sms_stat

- classname: _home
  keyname: sms_journal
  displayname: SMS Journal
  description: SMS Journal
  icon: fa-list
  url: /sirene/private/sms/journal/
  dashboard_section: Admin
  sidebar_section: Admin
  order: 330
  permission: p_sirene_sms_journal

- classname: _home
  keyname: import
  displayname: Import
  description: Import tool
  icon: fa-plus
  url: /data/private/import/
  dashboard_section: Admin
  sidebar_section: Admin
  order: 340
  permission: p_data_import

- classname: _home
  keyname: export
  displayname: Export
  description: Export tool
  icon: fa-minus
  url: /data/private/export/
  dashboard_section: Admin
  sidebar_section: Admin
  order: 350
  permission: p_data_export



# Doc
- classname: _home
  keyname: cavaliba
  displayname: Doc Cavaliba (Ext)
  description: Doc Cavaliba
  icon: fa-book
  url: https://cavaliba.com/docs/
  dashboard_section: Other
  sidebar_section: Other
  order: 500
  permission: p_home_access


'''
