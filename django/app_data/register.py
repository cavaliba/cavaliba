# app_data - aaa.py

from django.utils.translation import gettext as _


# appname without app_
APP_NAME = "data"


# # (keyname, displayname, description, default)
# PERMISSIONS = [


#      ("p_data_access", "Access UI", "", False),
#      ("p_data_class_ro", "Access RO on classes", "", False),
#      ("p_data_class_rw", "Access RWD on classes", "", False),
#      ("p_data_schema_ro", "Schema RO", "", False),
#      ("p_data_schema_rw", "Schema RWD", "", False),
#      ("p_data_instance_ro", "Global RO on instances", "", False),
#      ("p_data_instance_rw", "Global RWD on instances", "", False),
#      ("p_data_import", "Use file or YAML import tool", "", False),
#      ("p_data_admin", "Other sensitive actions on data app", "", False),

# ]

# # only gives permissions ; role_data_CLASSNAME_XX pour each class
# ROLES_BUILTIN = {
#     'role_data_ro': [
#         "p_data_access",
#         "p_data_class_ro",
#         "p_data_schema_ro",
#         "p_data_instance_ro",

#     ],
#     # class: create/update/delete/onoff
#     'role_data_rw': [
#         "p_data_access", 
#         "p_data_class_rw",
#         "p_data_schema_rw",
#         "p_data_instance_rw",
#     ],
#     # class: import/export
#     'role_data_admin': [
#         "p_data_access", 
#         "p_data_class_rw",
#         "p_data_schema_rw",
#         "p_data_instance_rw",
#         "p_data_import",
#         "p_data_admin",
#     ],
# }



BUILTIN_DATA = '''


_permission:p_data_admin:
    is_builtin: True
    appname: data
    description: "Built-in DATA Admin"
    displayname: "p_data_admin"


_permission:p_data_access:
    is_builtin: True
    appname: data
    description: "Built-in DATA Access"
    displayname: "p_data_access"

_permission:p_schema_ro:
    is_builtin: True
    appname: data
    description: "Built-in DATA RO Schema"
    displayname: "p_schema_ro"

_permission:p_schema_rw:
    is_builtin: True
    appname: data
    description: "Built-in DATA RW Schema"
    displayname: "p_schema_rw"

_permission:p_instance_ro:
    is_builtin: True
    appname: data
    description: "Built-in DATA RO Instance"
    displayname: "p_instance_rw"

_permission:p_instance_rw:
    is_builtin: True
    appname: data
    description: "Built-in DATA RW Instance"
    displayname: "p_instance_rw"


_permission:p_data_import:
    is_builtin: True
    appname: data
    description: "Built-in DATA Import"
    displayname: "p_data_import"


# ----

_role:role_data_admin:
    displayname: Built-in DATA Admin Role
    is_builtin: true
    permissions:
      - p_data_access
      - p_schema_rw
      - p_schema_ro
      - p_instance_rw
      - p_instance_ro
      - p_data_import
      - p_data_admin

_role:role_data_ro:
    displayname: Built-in DATA RO Role
    is_builtin: true
    permissions:
      - p_data_access
      - p_schema_ro
      - p_instance_ro

_role:role_data_rw:
    displayname: Built-in DATA RW Role
    is_builtin: true
    permissions:
      - p_data_access
      - p_schema_rw
      - p_schema_ro
      - p_instance_rw
      - p_instance_ro


# schemas
# -------


_schema:app:

    _displayname: Applications
    _is_enabled: yes
    _icon: fa-window-maximize
    _order: 50
    _page: MeteoSI
    _role_show: role_data_admin
    _role_access: role_data_admin
    _role_read: role_data_admin
    _role_create: role_data_admin
    _role_update: role_data_admin
    _role_delete: role_data_admin
    _role_onoff: role_data_admin
    _role_import: role_data_admin
    _role_export: role_data_admin
    description:
        #_action: create_or_update          
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
        dataformat: sirene_group
        cardinal_max: 0



_schema:site:
    #_action: create_or_update
    _displayname: Etablissements
    _is_enabled: yes
    _order: 60
    _page: MeteoSI        
    _icon: fa-hospital-o
    _role_show: role_data_admin
    _role_access: role_data_admin
    _role_read: role_data_admin
    _role_create: role_data_admin
    _role_update: role_data_admin
    _role_delete: role_data_admin
    _role_onoff: role_data_admin
    _role_import: role_data_admin
    _role_export: role_data_admin
    description:
        _action: create_or_update          
        displayname: Cliniques, Sieges, CSP
        order: 100
        dataformat: string
        dataformat_ext: ""
        cardinal_min: 0
        cardinal_max: 1
        default : ""
    address:
        displayname: Address
        page: Address
        order: 110
        dataformat: string                    
    city:
        displayname: City
        page: Address
        order: 111
        dataformat: string
    zip:
        displayname: Zipcode
        page: Address
        order: 113
        dataformat: string
    sirene_group:
        displayname: Sirene User Groups to notify
        page: Sirene
        order: 500
        dataformat: sirene_group
        cardinal_max: 0
    sirene_app:      
        displayname: Sirene App subscriptions
        page: Sirene
        order: 510           
        dataformat: sirene_data
        dataformat_ext: app
        cardinal_max: 0



_schema:sitegroup:

    _displayname: Groups of Sites
    _is_enabled: yes
    _icon: fa-university
    _order: 70
    _page: MeteoSI        
    _role_show: role_data_admin
    _role_access: role_data_admin
    _role_read: role_data_admin
    _role_create: role_data_admin
    _role_update: role_data_admin
    _role_delete: role_data_admin
    _role_onoff: role_data_admin
    _role_import: role_data_admin
    _role_export: role_data_admin
    description:
        #_action: create_or_update          
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
        dataformat: sirene_data
        dataformat_ext: site
        cardinal_max: 0
    subgroups:
        displayname: Subgroups
        page: Org
        order: 130
        dataformat: sirene_data
        dataformat_ext: sitegroup
        cardinal_max: 0
    sirene_group:
        displayname: Sirene User Groups to notify
        page: Sirene
        order: 500
        dataformat: sirene_group
        cardinal_max: 0

_schema:customer:

    _displayname: Clients
    _is_enabled: yes
    _icon: fa-credit-card
    _order: 290
    _page: Data
    _role_show: role_data_admin
    _role_access: role_data_admin
    _role_read: role_data_admin
    _role_create: role_data_admin
    _role_update: role_data_admin
    _role_delete: role_data_admin
    _role_onoff: role_data_admin
    _role_import: role_data_admin
    _role_export: role_data_admin
    description:
        #_action: create_or_update          
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
        dataformat: sirene_group
        cardinal_max: 0
        

_schema:data_enumerate:
    #_action: init
    _displayname: Data Enumerates
    _is_enabled: yes
    _icon: fa-table
    _order: 810
    _page: Internal
    _role_show: role_data_admin
    _role_access: role_data_admin
    _role_read: role_data_admin
    _role_create: role_data_admin
    _role_update: role_data_admin
    _role_delete: role_data_admin
    _role_onoff: role_data_admin
    _role_import: role_data_admin
    _role_export: role_data_admin
    description:
        displayname: Description
        order: 100
        dataformat: string
        dataformat_ext: ""
        cardinal_min: 0
        cardinal_max: 1
        default : ""
    content:
        displayname: Content
        cardinal_min: 0
        cardinal_max: 1
        page: input
        order: 120
        dataformat: text
        dataformat_ext: yaml 




_schema:data_pipeline:
    _displayname: Data Pipeline
    _is_enabled: yes
    _icon: fa-gears
    _order: 500
    _page: Internal
    _role_show: role_data_admin
    _role_access: role_data_admin
    _role_read: role_data_admin
    _role_create: role_data_admin
    _role_update: role_data_admin
    _role_delete: role_data_admin
    _role_onoff: role_data_admin
    _role_import: role_data_admin
    _role_export: role_data_admin
    description:
        displayname: Description
        order: 100
        dataformat: string
        dataformat_ext: ""
        cardinal_min: 0
        cardinal_max: 1
        default : ""
    content:
        displayname: Content
        cardinal_min: 0
        cardinal_max: 1
        page: Content
        order: 100
        dataformat: text
        dataformat_ext: yaml


_schema:data_view:
    _displayname: Data Views
    _is_enabled: yes
    _icon: fa-table
    _order: 810
    _page: Internal
    _role_show: role_data_admin
    _role_access: role_data_admin
    _role_read: role_data_admin
    _role_create: role_data_admin
    _role_update: role_data_admin
    _role_delete: role_data_admin
    _role_onoff: role_data_admin
    _role_import: role_data_admin
    _role_export: role_data_admin
    description:
        displayname: Description
        order: 100
        dataformat: string
        dataformat_ext: ""
        cardinal_min: 0
        cardinal_max: 1
        default : ""
    classname:
        displayname: Schema
        cardinal_min: 0
        cardinal_max: 1
        order: 110
        dataformat: string
    content:
        displayname: Content
        cardinal_min: 0
        cardinal_max: 1
        order: 120
        dataformat: text
        dataformat_ext: yaml


'''
