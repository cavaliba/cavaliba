# app_home - aaa.py


# global framework version
SIRENE_VERSION = "3.9"

APP_NAME = "home"

APP_VERSION = "1.5"

# (keyname, displayname, description, default)
PERMISSIONS = [
    
    ("p_home_access", "UI access", "", False),
    ("p_home_update", "Update dashboard", "", False),
    ("p_home_import_yaml", "Import YAML content", "", False),
    ("p_home_import", "Import HOME configuration", "", False),
]

ROLES_BUILTIN = {
    'role_home_user': [
        'p_home_access',
    ],

    'role_home_admin': [
        'p_home_access',
        "p_home_update",
        "p_home_import_yaml",
        "p_home_import",
    ]
}


PERMISSIONS_CLEANUP = [
]

ROLES_CLEANUP = [
]


GROUPS_BUILTIN = {
}
