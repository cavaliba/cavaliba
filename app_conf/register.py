# app_conf - aaa.py


APP_NAME = "conf"

APP_VERSION = "0.5"

# (keyname, displayname, description, default)
PERMISSIONS = [
    ("p_conf_access", "Access App Conf", "", False),
]

ROLES_BUILTIN = {
    'role_conf_admin': [
        'p_conf_access',
    ]
}

GROUPS_BUILTIN = {
}

PERMISSIONS_CLEANUP = [
]

ROLES_CLEANUP = [
]

