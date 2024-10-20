# {{ app_name }} - aaa.py

from django.utils.translation import gettext as _


# appname without app_ 
APP_NAME = "XX"

APP_VERSION = "0.1"

# (keyname, displayname, description, default)
PERMISSIONS = [
#    ("p_XXXXXX_main", "XXX: view main page", "UI access to main page", False),
     ("p_xx_access", "Access UI", "", False),

     ("p_xx_read" ,  "Read-Only", "", False),
     ("p_xx_write" , "Create/Update", "", False),
     ("p_xx_admin" , "Delete/Import/Export", "", False),
]

ROLES_BUILTIN = {
    'role_xx_view': [
        'p_xx_access',
        'p_xx_read',
    ],
    'role_xx_manage': [
        'p_xx_access',
        'p_xx_read',
        'p_xx_write',
        'p_xx_admin',
    ],
}

PERMISSIONS_CLEANUP = [
]

ROLES_CLEANUP = [
]


GROUPS_BUILTIN = {
}
