# app_data - aaa.py

from django.utils.translation import gettext as _


# appname without app_
APP_NAME = "data"

APP_VERSION = "2.0" 

# (keyname, displayname, description, default)
PERMISSIONS = [
#    ("p_XXXXXX_main", "XXX: view main page", "UI access to main page", False),
     # ("p_data_view" , "View Data", "UI access to Data", False),
     # ("p_data_manage" , "Manage Data", "UI access to Data CRUD", False),
     ("p_data_access", "Access UI", "", False),
     ("p_data_class_ro", "Access RO on classes", "", False),
     ("p_data_class_rw", "Access RWD on classes", "", False),
     ("p_data_schema_ro", "Schema RO", "", False),
     ("p_data_schema_rw", "Schema RWD", "", False),
     ("p_data_instance_ro", "Global RO on instances", "", False),
     ("p_data_instance_rw", "Global RWD on instances", "", False),
     ("p_data_import", "Use file or YAML import tool", "", False),
     ("p_data_admin", "Other sensitive actions on data app", "", False),

]

# only gives permissions ; role_data_CLASSNAME_XX pour each class
ROLES_BUILTIN = {
    'role_data_ro': [
        "p_data_access",
        "p_data_class_ro",
        "p_data_schema_ro",
        "p_data_instance_ro",

    ],
    # class: create/update/delete/onoff
    'role_data_rw': [
        "p_data_access", 
        "p_data_class_rw",
        "p_data_schema_rw",
        "p_data_instance_rw",
    ],
    # class: import/export
    'role_data_admin': [
        "p_data_access", 
        "p_data_class_rw",
        "p_data_schema_rw",
        "p_data_instance_rw",
        "p_data_import",
        "p_data_admin",
    ],
}

PERMISSIONS_CLEANUP = [
]

ROLES_CLEANUP = [
]


GROUPS_BUILTIN = {
}

