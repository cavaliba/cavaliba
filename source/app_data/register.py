# (c) cavaliba.com - data - aaa.py

APP_NAME = "data"

BUILTIN_DATA = '''

# ---------------------
# permissions Builtin
# ---------------------

# dashboard access to DATA app
# ----------------------------
- classname: _permission
  keyname: p_data_access
  is_builtin: True
  appname: data
  description: "Built-in DATA dashboard access"
  displayname: "p_data_access"

  
- classname: _permission
  keyname: p_permission_edit
  is_builtin: True
  appname: data
  description: "Built-in PERMISSION edit"
  displayname: p_permission_edit

  
# schema / class definitions
# --------------------------

- classname: _permission
  keyname: p_schema_read
  is_builtin: True
  appname: data
  description: "Built-in SCHEMA read"
  displayname: "p_schema_read"

- classname: _permission
  keyname: p_schema_create
  is_builtin: True
  appname: data
  description: "Built-in SCHEMA create"
  displayname: "p_schema_create"

- classname: _permission
  keyname: p_schema_update
  is_builtin: True
  appname: data
  description: "Built-in SCHEMA update"
  displayname: "p_schema_update"

- classname: _permission
  keyname: p_schema_delete
  is_builtin: True
  appname: data
  description: "Built-in SCHEMA delete"
  displayname: "p_schema_delete"


- classname: _permission
  keyname: p_schema_import
  is_builtin: True
  appname: data
  description: "Built-in SCHEMA import"
  displayname: "p_schema_import"

- classname: _permission
  keyname: p_schema_export
  is_builtin: True
  appname: data
  description: "Built-in SCHEMA export"
  displayname: p_schema_export

  
# all data classes + not blockable
# ---------------------------------
# special / non-blocking downwards

- classname: _permission
  keyname: p_data_admin
  is_builtin: True
  appname: data
  description: "Built-in DATA all permissions non-blocking"
  displayname: "p_data_admin"

# all data classes if not blocked at class level
# ----------------------------------------------

- classname: _permission
  keyname: p_data_read
  is_builtin: True
  appname: data
  description: "Built-in DATA read all"
  displayname: "p_data_read"

- classname: _permission
  keyname: p_data_create
  is_builtin: True
  appname: data
  description: "Built-in DATA create all"
  displayname: "p_data_create"

- classname: _permission
  keyname: p_data_update
  is_builtin: True
  appname: data
  description: "Built-in DATA update all"
  displayname: "p_data_update"

- classname: _permission
  keyname: p_data_delete
  is_builtin: True
  appname: data
  description: "Built-in DATA delete all"
  displayname: "p_data_delete"

- classname: _permission
  keyname: p_data_import
  is_builtin: True
  appname: data
  description: "Built-in DATA import all"
  displayname: "p_data_import"

- classname: _permission
  keyname: p_data_export
  is_builtin: True
  appname: data
  description: "Built-in DATA export all"
  displayname: p_data_export

  

# --------------------
# Roles Builtin
# --------------------

- classname: _role
  keyname: role_schema_admin
  displayname: Built-in SCHEMA admin role
  is_builtin: true
  permissions:
      - p_data_access
      - p_schema_read
      - p_schema_create
      - p_schema_delete
      - p_schema_update
      - p_schema_export
      - p_schema_import

- classname: _role
  keyname: role_data_admin
  displayname: Built-in DATA admin role
  is_builtin: true
  permissions:
      - p_schema_read
      - p_data_access
      - p_data_admin
      - p_permission_edit

- classname: _role
  keyname: role_data_read
  displayname: Built-in DATA read role
  is_builtin: true
  permissions:
      - p_data_access
      - p_data_read

- classname: _role
  keyname: role_data_create
  displayname: Built-in DATA create role
  is_builtin: true
  permissions:
      - p_data_access
      - p_data_read
      - p_data_create

- classname: _role
  keyname: role_data_update
  displayname: Built-in DATA update role
  is_builtin: true
  permissions:
      - p_data_access
      - p_data_read
      - p_data_update

- classname: _role
  keyname: role_data_delete
  displayname: Built-in DATA delete role
  is_builtin: true
  permissions:
      - p_data_access
      - p_data_read
      - p_data_delete

      
# -------------------
# schema: enumerate
# -------------------

- classname: _schema
  keyname: _enumerate
  #_action: init
  displayname: Data Enumerates
  is_enabled: yes
  icon: fa-table
  order: 810
  page: Internal
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


# -------------------
# schema: pipeline
# -------------------

- classname: _schema
  keyname: _pipeline
  displayname: Data Pipelines
  is_enabled: yes
  icon: fa-gears
  order: 500
  page: Internal
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

    

# -------------------
# schema: dataview
# -------------------


- classname: _schema
  keyname: _dataview
  displayname: Data Views
  is_enabled: yes
  icon: fa-table
  order: 810
  page: Internal
  description:
    displayname: Description
    order: 100
    dataformat: string
    dataformat_ext: ""
    cardinal_min: 0
    cardinal_max: 1
    default : ""
  target_class:
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


# default Dataview for _dataview
# ------------------------------
- classname: _dataview
  keyname: _dataview_default
  target_class: _dataview
  displayname: Data View default
  is_enabled: true
  description: Default dataview for DataView
  content: |
    columns:
      - keyname
      - displayname
      - target_class
      - last_update

'''
