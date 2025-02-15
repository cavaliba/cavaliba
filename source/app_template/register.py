# {{ app_name }} - aaa.py

from django.utils.translation import gettext as _


# appname without app_ 
APP_NAME = "XX"

BUILTIN_DATA = '''

# _permission:p_xxxx:
#     _action: init
#     is_builtin: True
#     appname: conf
#     description: ""
#     displayname: "p_xxx"



# _role:role_conf_admin:
#     _action: init
#     displayname: Built-in Conf admin role
#     is_builtin: True
#     permissions: 
#       - p_conf_access


'''

