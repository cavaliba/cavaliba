# (c) cavaliba.com - home - configuration_default.py


CONFIGURATION_DEFAULT = {


	"home": {
		"GLOBAL_APPNAME": "Cavaliba",
	    "CSV_DELIMITER": '|',
	    "LOGO_SIZE": 0,
	    "LOG_DEBUG": "yes", 
	    "LOG_KEEP_DAYS": 31, 
        "LOG_EXCLUDED_IP": "",
	    "BETA_PREVIEW": 'no',
	},
	"user": {
	    "TRUSTED_ANONYMOUS_IPS": "",
	    # oauth2, basic, local, forced
	    "AUTH_MODE": "local",
	    "AUTH_MODE_FORCE_USER": "admin",
	    "AUTH_FEDERATED_LOGIN_FIELD": "X-User",
	    "AUTH_FEDERATED_EMAIL_FIELD": "X-Email",
	    "AUTH_LOGIN_REMOVE_DOMAIN": "yes",
	    # manual, create, update, sync, visitor
	    "AUTH_PROVISIONING": "manual",
	    "DEBUG_AAA": "no",
	    "DEBUG_AAA2": "no",
	    "CACHE_SESSION": "yes",
	    "SYSADMIN_IMPERSONATE": "",
	},
	"data": {
        "DATA_DEFAULT_SIZE": 200,
        "DATA_MAX_SIZE": 500,
		"DATA_BIGSET_SIZE": 500,
		"EXPORT_INTERACTIVE_MAX_SIZE": 5000,
	},
	"sirene": {
        "SIRENE_APPNAME": "Sirene",
	    "PUBLIC_MAX_ITEMS": 6,
	    "PUBLIC_MAX_MINUTES": 1440,
	    "PUBLIC_SORT_ORDER": "creation",
	    "PRIVATE_MAX_MINUTES": 1440,
	    "PUBLIC_SKIP_TO_TRUSTED": 'no',
	    "EMAIL_FOLDER": "/mail/",
	    "EMAIL_MODE": "stdout",
	    "EMAIL_FROM": "noreply@findadomain.com",
	    "EMAIL_SMTP_BATCH": 100,	    
	    "EMAIL_PREFIX" : "[Cavaliba] ",
	    "EMAIL_UPDATE_PREFIX" : "[Cavaliba Update] ",
	    "EMAIL_TEST_SUBJECT": "Cavaliba - TEST TEST TEST - Please ignore.",
	    "EMAIL_TEST_CONTENT": "Test.Ignore.",
	    "SMS_FOLDER": "/sms/",
	    "SMS_PREFIX": "[Cavaliba] ",
	    "SMS_UPDATE_PREFIX": "[Cavaliba Update] ",
	    "SMS_TEST": "Cavaliba - TEST TEST TEST - Please ignore.",
	    "SMS_QUOTA_PER_DAY": 100,
	    "SMS_MODE": "stdout",
        "SMS_WARNING": "IMPORTANT: All SMS activity is recorded for security purposes.",
	    "APP_CLASS": "app",
	    "SITE_CLASS": "site",
	    "SITEGROUP_CLASS": "sitegroup",
	    "CUSTOMER_CLASS": "customer",
	    },
}
