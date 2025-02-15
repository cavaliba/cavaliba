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
# - p_user_read
# - p_user_create
# - p_user_update
# - p_user_delete
# - p_user_import
# - p_user_export
# - p_group_read
# - p_group_create
# - p_group_update
# - p_group_delete
# - p_group_import
# - p_group_export
# - p_role_read
# - p_role_create
# - p_role_update
# - p_role_delete
# - p_role_import
# - p_role_export
# - p_permission_ro
# - p_permission_rw
# - p_permission_import
# - p_permission_export



BUILTIN_DATA = '''

- classname: _permission
  keyname: p_user_admin
  is_builtin: True
  appname: user
  description: "Built-in USER admin"
  displayname: ""

- classname: _permission
  keyname: p_user_access
  is_builtin: True
  appname: user
  description: "Built-in USER access"
  displayname: ""

- classname: _permission
  keyname: p_iam_access
  is_builtin: True
  appname: user
  description: "Built-in IAM access"
  displayname: "p_iam_access"

# -- user

- classname: _permission
  keyname: p_user_pref
  is_builtin: True
  appname: user
  description: "Built-in USER.preferences permission"
  displayname: ""

- classname: _permission
  keyname: p_user_email_test
  is_builtin: True
  appname: user
  description: "Built-in USER.test_email permission"
  displayname: ""

- classname: _permission
  keyname: p_user_sms_test
  is_builtin: True
  appname: user
  description: "Built-in USER.test_sms permission"
  displayname: ""

- classname: _permission
  keyname: p_user_debug
  is_builtin: True
  appname: user
  description: "Built-in USER.debug permission"
  displayname: ""

- classname: _permission
  keyname: p_user_read
  is_builtin: True
  appname: user
  description: "Built-in USER read permission"
  displayname: "p_user_read"

- classname: _permission
  keyname: p_user_create
  is_builtin: True
  appname: user
  description: "Built-in USER create permission"
  displayname: "p_user_create"

- classname: _permission
  keyname: p_user_update
  is_builtin: True
  appname: user
  description: "Built-in USER update permission"
  displayname: "p_user_update"

- classname: _permission
  keyname: p_user_delete
  is_builtin: True
  appname: user
  description: "Built-in USER delete permission"
  displayname: "p_user_delete"
    
- classname: _permission
  keyname: p_user_import
  is_builtin: True
  appname: user
  description: "Built-in USER import permission"
  displayname: ""

- classname: _permission
  keyname: p_user_export
  is_builtin: True
  appname: user
  description: "Built-in USER export permission"
  displayname: ""

  # -- group

- classname: _permission
  keyname: p_group_read
  is_builtin: True
  appname: user
  description: "Built-in GROUP read permission"
  displayname: "p_group_read"

- classname: _permission
  keyname: p_group_create
  is_builtin: True
  appname: user
  description: "Built-in GROUP create permission"
  displayname: "p_group_create"

- classname: _permission
  keyname: p_group_update
  is_builtin: True
  appname: user
  description: "Built-in GROUP update permission"
  displayname: "p_group_update"

- classname: _permission
  keyname: p_group_delete
  is_builtin: True
  appname: user
  description: "Built-in GROUP delete permission"
  displayname: "p_group_delete"
  
- classname: _permission
  keyname: p_group_import
  is_builtin: True
  appname: user
  description: "Built-in GROUP import permission"
  displayname: ""

- classname: _permission
  keyname: p_group_export
  is_builtin: True
  appname: user
  description: "Built-in GROUP export permission"
  displayname: ""

# -- role

- classname: _permission
  keyname: p_role_read
  is_builtin: True
  appname: user
  description: "Built-in IAM role read permission"
  displayname: p_role_read

- classname: _permission
  keyname: p_role_create
  is_builtin: True
  appname: user
  description: "Built-in IAM role create permission"
  displayname: p_role_create

- classname: _permission
  keyname: p_role_update
  is_builtin: True
  appname: user
  description: "Built-in IAM role update permission"
  displayname: p_role_update

- classname: _permission
  keyname: p_role_delete
  is_builtin: True
  appname: user
  description: "Built-in IAM role delete permission"
  displayname: p_role_delete
    

- classname: _permission
  keyname: p_role_import
  is_builtin: True
  appname: user
  description: "Built-in USER.role_import permission"
  displayname: ""

- classname: _permission
  keyname: p_role_export
  is_builtin: True
  appname: user
  description: "Built-in USER.role_export permission"
  displayname: ""


- classname: _permission
  keyname: p_permission_ro
  is_builtin: True
  appname: user
  description: "Built-in USER.permission_read permission"
  displayname: ""

- classname: _permission
  keyname: p_permission_rw
  is_builtin: True
  appname: user
  description: "Built-in USER.permission_write permission"
  displayname: ""


- classname: _permission
  keyname: p_permission_import
  is_builtin: True
  appname: user
  description: "Built-in USER.permission_import permission"
  displayname: ""

- classname: _permission
  keyname: p_permission_export
  is_builtin: True
  appname: user
  description: "Built-in USER.permission_export permission"
  displayname: ""

  
# ------------
# Roles
# ------------

- classname: _role
  keyname: role_user_admin
  is_builtin: True
  displayname: Built-in USER ADMIN Role
  permissions: 
    - p_user_access
    - p_user_admin
    - p_user_pref
    - p_user_email_test
    - user_sms_test
    - p_user_debug
    - p_user_read
    - p_user_create
    - p_user_update
    - p_user_delete
    - p_user_import
    - p_user_export
    - p_group_read
    - p_group_create
    - p_group_update
    - p_group_delete
    - p_group_import
    - p_group_export
    - p_role_read
    - p_role_create
    - p_role_update
    - p_role_delete
    - p_role_import
    - p_role_export
    - p_permission_ro
    - p_permission_rw
    - p_permission_import
    - p_permission_export


- classname: _role
  keyname: role_user_rw
  is_builtin: True
  displayname: Built-in USER RW Role
  permissions: 
    - p_user_access
    - p_user_pref
    - p_user_email_test
    - user_sms_test
    - p_user_debug
    - p_user_read
    - p_user_create
    - p_user_update
    - p_user_delete
    - p_user_import
    - p_user_export
    - p_group_read
    - p_group_create
    - p_group_update
    - p_group_delete
    - p_group_import
    - p_group_export
    - p_role_read


- classname: _role
  keyname: role_user_ro
  is_builtin: True
  displayname: Built-in USER RO Role
  permissions: 
    - p_user_access
    - p_user_pref
    - p_user_debug
    - p_user_read
    - p_group_read


- classname: _role
  keyname: role_group_ro
  is_builtin: True
  displayname: Built-in USER Group RO Role
  permissions: 
    - p_user_access
    - p_user_read
    - p_group_read

- classname: _role
  keyname: role_group_rw
  is_builtin: True
  displayname: Built-in USER Group RW Role
  permissions: 
    - p_user_access
    - p_user_read
    - p_group_read
    - p_group_create
    - p_group_update
    - p_group_delete
    - p_group_import
    - p_group_export


- classname: _role
  keyname: role_role_ro
  is_builtin: True
  displayname: Built-in USER RO Role
  permissions: 
    - p_user_access
    - p_user_read
    - p_group_read
    - p_permission_ro
    - p_role_read

- classname: _role
  keyname: role_role_rw
  is_builtin: True
  displayname: Built-in USER RW Role
  permissions: 
    - p_user_access
    - p_user_read
    - p_group_read
    - p_role_read
    - p_role_create
    - p_role_update
    - p_role_delete
    - p_role_import
    - p_role_export
    - p_permission_ro
    - p_permission_rw
    - p_permission_import
    - p_permission_export


- classname: _role
  keyname: role_security_audit
  is_builtin: True
  displayname: Built-in USER Security RO Role
  permissions: 
    - p_user_access
    - p_user_pref
    - p_user_email_test
    - user_sms_test
    - p_user_debug
    - p_user_read
    - p_user_export
    - p_group_read
    - p_group_export
    - p_role_read
    - p_role_export
    - p_permission_ro
    - p_permission_export


- classname: _role
  keyname: role_security_admin
  is_builtin: True
  displayname: Built-in USER Security RW Role
  permissions: 
    - p_user_access
    - p_user_admin
    - p_user_pref
    - p_user_email_test
    - user_sms_test
    - p_user_debug
    - p_user_read
    - p_user_create
    - p_user_update
    - p_user_delete
    - p_user_import
    - p_user_export
    - p_group_read
    - p_group_create
    - p_group_update
    - p_group_delete
    - p_group_import
    - p_group_export
    - p_role_read
    - p_role_create
    - p_role_update
    - p_role_delete
    - p_role_import
    - p_role_export
    - p_permission_ro
    - p_permission_rw
    - p_permission_import
    - p_permission_export


# ------------
# API Keys
# ------------
- classname: _schema
  keyname: _apikey
  #_action: init
  displayname: API Keys
  is_enabled: yes
  icon: fa-key
  order: 820
  page: Internal
  keyvalue:
        displayname: Secret
        order: 50
        dataformat: string
  description:
        displayname: Description
        order: 60
        dataformat: string
        dataformat_ext: ""
        cardinal_min: 0
        cardinal_max: 1
        default : "API Key"
  is_readonly:
        displayname: Read-Only
        dataformat: boolean
        order: 70
        description: Cocher pour activer !
        default: true
  permissions:
        order: 80
        displayname: Permissions
        dataformat: text
  not_after:
        displayname: Not After
        description: format YYYY-MM-DD
        dataformat: date
  time_filter:
        displayname: Time Filter
        dataformat: text
  ip_filter:
        displayname: IP Filter
        dataformat: text
        default : "*"
  acl_filter:
        displayname: ACL Filter
        cardinal_max: 0
        dataformat: text
  last_success:
        displayname: Last Success
        description: format YYYY-MM-DD
        dataformat: date
  last_error:
        displayname: Last Error
        description: format YYYY-MM-DD
        dataformat: date
  success_count:
        displayname: Success Count
        dataformat: int
  error_count:
        displayname: Error Count
        dataformat: int

'''

