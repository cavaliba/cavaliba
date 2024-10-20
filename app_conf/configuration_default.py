# app_conf / default


CONFIGURATION_DEFAULT = {

	# "app_conf": {},
	"home": {
		"GLOBAL_APPNAME": "Sirene",
	    "CSV_DELIMITER": '|',
	    "LOGO_SIZE": 0,
	    "BETA_PREVIEW": 'no',

	},
	"user": {

	    "TRUSTED_ANONYMOUS_IPS": "",
	    # oauth2, basic, sirene, forced
	    "AUTH_MODE": "forced",
	    "AUTH_MODE_FORCE_USER": "sysadmin",
	    "AUTH_FEDERATED_LOGIN_FIELD": "X-User",
	    "AUTH_FEDERATED_EMAIL_FIELD": "X-Email",
	    "AUTH_LOGIN_REMOVE_DOMAIN": "yes",
	    # manual, create, update, sync, visitor
	    "AUTH_PROVISIONING": "manual",
	    "DEBUG_AAA": "no",
	    "DEBUG_AAA2": "no",
	    "CACHE_SESSION": "no",
	    "SYSADMIN_IMPERSONATE": "",
	},
	"data": {
		"DATA_BIGSET_SIZE": 500,
		"EXPORT_INTERACTIVE_MAX_SIZE": 5000,
	},
	"log": {
	    "LOG_DEBUG": "yes", 
	    "LOG_KEEP_DAYS": 31, 
	},
	"conf": {
		
	},
	"sirene": {
	    "PUBLIC_MAX_ITEMS": 6,
	    "PUBLIC_MAX_MINUTES": 1440,
	    "PUBLIC_SORT_ORDER": "creation",
	    "PRIVATE_MAX_MINUTES": 1440,
	    "PUBLIC_SKIP_TO_TRUSTED": 'no',
	    "EMAIL_MODE": "stdout",
	    "EMAIL_FROM": "noreply@cavaliba.com",
	    "EMAIL_SMTP_BATCH": 100,	    
	    "EMAIL_PREFIX" : "[Sirene] ",
	    "EMAIL_UPDATE_PREFIX" : "[Sirene Update] ",
	    "EMAIL_TEST_SUBJECT": "Sirene - TEST TEST TEST - Please ignore.",
	    "EMAIL_TEST_CONTENT": "Test.Ignore.",
	    "SMS_PREFIX": "[Sirene] ",
	    "SMS_UPDATE_PREFIX": "[Sirene Update] ",
	    "SMS_TEST": "Sirene - TEST TEST TEST - Please ignore.",
	    "SMS_QUOTA_PER_DAY": 100,
	    # stdout, folder, clicsecure
	    "SMS_MODE": "stdout",
	    "APP_CLASS": "app",
	    "SITE_CLASS": "site",
	    "SITEGROUP_CLASS": "sitegroup",
	    "CUSTOMER_CLASS": "customer",
	    },
}
