# cavaliba.com
# app_log


# appname without app_  from  app_log
APP_NAME = "log"

# - p_log_access
# - p_log_view
# - p_log_manage


BUILTIN_DATA = '''


# permissions
# -----------


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

# # (keyname, displayname, description, default)
# PERMISSIONS = [
#      ("p_log_access", "Access UI", "", False),
# #    ("p_XXXXXX_main", "XXX: view main page", "UI access to main page", False),
#      ("p_log_view" , "View logs", "UI access to logs", False),
#      ("p_log_manage" , "Purge logs", "UI access to purge logs", False),
# ]

# ROLES_BUILTIN = {
#     'role_log_view': [
#         "p_log_access",
#         'p_log_view',
#     ],
#     'role_log_manage': [
#         "p_log_access",
#         'p_log_manage',
#     ],
# }

# GROUPS_BUILTIN = {
# }
