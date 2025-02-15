# (c) cavaliba.com - sirene - register.py


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

- classname: _permission
  keyname: p_sirene_access
  is_builtin: True
  appname: sirene
  description: "Built-in SIRENE app access"
  displayname: ""

- classname: _permission
  keyname: p_sirene_access_restricted
  is_builtin: True
  appname: sirene
  description: "Built-in SIRENE app access restricted messages"
  displayname: ""

- classname: _permission
  keyname: p_sirene_detail
  is_builtin: True
  appname: sirene
  description: "Built-in SIRENE access details"
  displayname: ""

- classname: _permission
  keyname: p_sirene_history
  is_builtin: True
  appname: sirene
  description: "Built-in SIRENE access history"
  displayname: ""

- classname: _permission
  keyname: p_sirene_new
  is_builtin: True
  appname: sirene
  description: "Built-in SIRENE create a new notification"
  displayname: ""

- classname: _permission
  keyname: p_sirene_update
  is_builtin: True
  appname: sirene
  description: "Built-in SIRENE update a notification"
  displayname: ""

- classname: _permission
  keyname: p_sirene_archive
  is_builtin: True
  appname: sirene
  description: "Built-in SIRENE archive a message"
  displayname: ""

- classname: _permission
  keyname: p_sirene_public_push
  is_builtin: True
  appname: sirene
  description: "Built-in SIRENE push a public page"
  displayname: ""

- classname: _permission
  keyname: p_sirene_flushall
  is_builtin: True
  appname: sirene
  description: "Built-in SIRENE archive all active messages"
  displayname: ""

- classname: _permission
  keyname: p_sirene_cat_read
  is_builtin: True
  appname: sirene
  description: "Built-in SIRENE RO category"
  displayname: ""

- classname: _permission
  keyname: p_sirene_cat_cud
  is_builtin: True
  appname: sirene
  description: "Built-in SIRENE RW category"
  displayname: ""

- classname: _permission
  keyname: p_sirene_public_read
  is_builtin: True
  appname: sirene
  description: "Built-in SIRENE RO public models"
  displayname: ""

- classname: _permission
  keyname: p_sirene_public_cud
  is_builtin: True
  appname: sirene
  description: "Built-in SIRENE RW public models"
  displayname: ""


- classname: _permission
  keyname: p_sirene_template_read
  is_builtin: True
  appname: sirene
  description: "Built-in SIRENE RO templates"
  displayname: ""

- classname: _permission
  keyname: p_sirene_template_cud
  is_builtin: True
  appname: sirene
  description: "Built-in SIRENE RW templates"
  displayname: ""

- classname: _permission
  keyname: p_sirene_import
  is_builtin: True
  appname: sirene
  description: "Built-in SIRENE Import"
  displayname: ""

- classname: _permission
  keyname: p_sirene_export
  is_builtin: True
  appname: sirene
  description: "Built-in SIRENE Export"
  displayname: ""

- classname: _permission
  keyname: p_sirene_sms_send
  is_builtin: True
  appname: sirene
  description: "Built-in SIRENE SMS Send"
  displayname: ""

- classname: _permission
  keyname: p_sirene_sms_journal
  is_builtin: True
  appname: sirene
  description: "Built-in SIRENE SMS Journal"
  displayname: ""

- classname: _permission
  keyname: p_sirene_sms_stat
  is_builtin: True
  appname: sirene
  description: "Built-in SIRENE SMS Stat"
  displayname: ""


# roles
# ------

- classname: _role
  keyname: role_sirene_admin
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

- classname: _role
  keyname: role_sirene_manage
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

- classname: _role
  keyname: role_sirene_operator
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


- classname: _role
  keyname: role_sirene_user
  is_builtin: True
  displayname: Built-in Sirene User Role
  permissions: 
    - p_sirene_access
    - p_sirene_detail
    - p_sirene_history       



# Sirene
# ------

- classname: _schema
  keyname: app
  displayname: Applications
  is_enabled: yes
  icon: fa-window-maximize
  order: 50
  page: MeteoSI
  description:
        #_action: create
        displayname: Description
        order: 100
        dataformat: string
        dataformat_ext: ""
        cardinal_min: 0
        cardinal_max: 1
        default : ""
  sirene_group:
        displayname: Sirene User Groups to notify
        order: 120
        dataformat: group
        cardinal_max: 0



- classname: _schema
  keyname: site
  #_action: create
  displayname: Etablissements
  is_enabled: yes
  order: 60
  page: MeteoSI        
  icon: fa-hospital-o
  description:
        _action: create
        displayname: Cliniques, Sieges, CSP
        order: 100
        dataformat: string
        dataformat_ext: ""
        cardinal_min: 0
        cardinal_max: 1
        default : ""
  sirene_group:
        displayname: Sirene User Groups to notify
        page: Sirene
        order: 500
        dataformat: group
        cardinal_max: 0
  sirene_app:      
        displayname: Sirene App subscriptions
        page: Sirene
        order: 510           
        dataformat: schema
        dataformat_ext: app
        cardinal_max: 0



- classname: _schema
  keyname: sitegroup
  displayname: Groups of Sites
  is_enabled: yes
  icon: fa-university
  order: 70
  page: MeteoSI        
  description:
        #_action: create
        displayname: Description
        order: 100
        dataformat: string
        dataformat_ext: ""
        cardinal_min: 0
        cardinal_max: 1
        default : ""
  members:
        displayname: Sites (members)
        page: Org
        order: 120           
        dataformat: schema
        dataformat_ext: site
        cardinal_max: 0
  subgroups:
        displayname: Subgroups
        page: Org
        order: 130
        dataformat: schema
        dataformat_ext: sitegroup
        cardinal_max: 0
  sirene_group:
        displayname: Sirene User Groups to notify
        page: Sirene
        order: 500
        dataformat: group
        cardinal_max: 0

- classname: _schema
  keyname: customer
  displayname: Clients
  is_enabled: yes
  icon: fa-credit-card
  order: 290
  page: Data
  description:
        #_action: create
        displayname: Description
        order: 100
        dataformat: string
        dataformat_ext: ""
        cardinal_min: 0
        cardinal_max: 1
        default : ""
  sirene_group:
        displayname: Sirene User Groups to notify
        order: 150
        dataformat: group
        cardinal_max: 0
        
'''

