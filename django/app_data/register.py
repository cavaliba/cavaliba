# app_data - aaa.py

from django.utils.translation import gettext as _


# appname without app_
APP_NAME = "data"




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
    _role_show: role_data_ro
    _role_access: role_data_ro
    _role_read: role_data_ro
    _role_create: role_data_rw
    _role_update: role_data_rw
    _role_delete: role_data_rw
    _role_onoff: role_data_rw
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
    _role_show: role_data_ro
    _role_access: role_data_ro
    _role_read: role_data_ro
    _role_create: role_data_rw
    _role_update: role_data_rw
    _role_delete: role_data_rw
    _role_onoff: role_data_rw
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

        
data_view:default_dataview:
  classname: data_view
  displayname: Default View
  is_enabled: true
  description: Default dataview for DataView itself
  content: |
    columns:
      - keyname
      - displayname
      - classname
      - last_update


'''
