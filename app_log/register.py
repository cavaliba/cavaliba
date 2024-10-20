# app_log - aaa.py


# appname without app_  from  app_log
APP_NAME = "log"

APP_VERSION = "0.4"

# (keyname, displayname, description, default)
PERMISSIONS = [
     ("p_log_access", "Access UI", "", False),
#    ("p_XXXXXX_main", "XXX: view main page", "UI access to main page", False),
     ("p_log_view" , "View logs", "UI access to logs", False),
     ("p_log_manage" , "Purge logs", "UI access to purge logs", False),
]

ROLES_BUILTIN = {
    'role_log_view': [
        "p_log_access",
        'p_log_view',
    ],
    'role_log_manage': [
        "p_log_access",
        'p_log_manage',
    ],
}

PERMISSIONS_CLEANUP = [
]

ROLES_CLEANUP = [
]



GROUPS_BUILTIN = {
}
