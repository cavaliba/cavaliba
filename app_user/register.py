# app_user - register.py


APP_NAME = "user"

APP_VERSION = "1.1"


# -- orga
#     View User                                       ; role_user_ro
#     Create User                                     ; role_user_rw
#     Admin User                                      ; role_user_admin   delete/export/import

#     View Group GO                                   ; role_group_ro
#     Create Group GO                                 ; role_group_rw
#     Admin Group GO           +map go/go, user       ; role_group_admin  delete/export/import + map

# -- secu
#     GS <=> GO    : add GO to GS, create GS, Perms   ; role_secu_admin
#     Security audit                                  ; role_secu_audit


PERMISSIONS_CLEANUP = [
    # ("p_default", "Default permissions from role_default", "", False),
    "p_default",
]

ROLES_CLEANUP = [
]


# (keyname, displayname, description, default)
PERMISSIONS = [
    

    ("p_user_access", "Access to User App UI", "", False),
    ("p_user_pref", "Edit self preferences", "Edit self preferences", False),
    ("p_user_debug", "Access Env debug", "", False),

    ("p_user_view", "User View", "", False),
    ("p_user_cud", "User Edit", "", False),
    ("p_user_delete", "User Delete", "", False),
    ("p_user_export", "User Export", "", False),
    ("p_user_import", "User Import", "", False),

    ("p_user_email_test", "Send test email", "", False),
    ("p_user_sms_test", "Send test SMS", "", False),

    ("p_group_view", "Group View", "", False),
    ("p_group_cud", "Group Edit", "", False),
    ("p_group_delete", "Group Delete", "", False),
    ("p_group_export", "Group Export", "", False),
    ("p_group_import", "Group Import", "", False),

    ("p_user_map", "map users to groups", "", False),
    ("p_group_map", "map groups to groups", "", False),

    ("p_role_ro", "Roles RO", "", False),
    ("p_role_rw", "Roles RW/Delete/Export/Map/Perms", "", False),
    ("p_role_import", "Role Import", "", False),

    #("p_role_map", "map groups to roles", "", False),

]


ROLES_BUILTIN = {

    # prefs ?
    # visitors ?
    # users

    'role_user_ro': [
        "p_user_access",
        "p_user_pref",
        "p_user_ro",
        "p_user_debug",
    ],
    'role_user_rw': [
        "p_user_access",
        "p_user_pref",
        "p_user_debug",
        "p_user_view",
        "p_user_cud",
        "p_user_email_test",
        "p_user_sms_test",
        "p_user_map",
    ],
    'role_user_admin': [
        "p_user_access",
        "p_user_pref",
        "p_user_debug",
        "p_user_view",
        "p_user_cud",
        "p_user_email_test",
        "p_user_sms_test",
        "p_user_delete",
        "p_user_export",
        "p_user_import",
        "p_user_map",
    ],

    'role_group_ro': [
        "p_group_view",
    ],
    'role_group_rw': [
        "p_group_view",
        "p_group_cud",
        "p_user_map",
        "p_group_map",
    ],
    'role_group_admin': [
        "p_group_view",
        "p_group_cud",
        "p_group_delete",
        "p_group_export",
        "p_group_import",
        "p_user_map",
        "p_group_map",
    ],

    'role_secu_admin': [
        "p_role_ro",
        "p_role_rw",
        "p_role_import",
        #"p_role_map",
    ],
    'role_secu_audit': [
        "p_user_access",
        "p_user_pref",
        "p_user_view",
        "p_user_export",
        "p_group_view",
        "p_group_export",
        "p_role_ro",
    ],

    'role_default': [
        "p_default",
        "p_sirene_anonymous",
        "p_sirene_access",
        "p_sirene_history",
        "p_sirene_detail",
    ],

    'role_sysadmin': [],  # all perms Sirene 

}


GROUPS_BUILTIN = {
}
