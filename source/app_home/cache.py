# (c) cavaliba.com - home - cache.py

# -----------------------------------------
# cache
# -----------------------------------------
cache_enum = {}
cache_classname = {}
cache_classid = {}
cache_schema = {}
cache_instance_name = {}
cache_fieldschema_detail = {}

def init():
    global cache_enum
    global cache_classname
    global cache_classid
    global cache_schema
    global cache_instance_name
    global cache_fieldschema_detail

    cache_enum = {}
    cache_classname = {}
    #cache_classname.clear()  
    cache_classid = {}
    cache_schema = {}
    cache_instance_name = {}
    cache_fieldschema_detail = {}

# def flush_cache_per_request():

#     global cache_enum
#     global cache_classname
#     global cache_classid
#     global cache_schema
#     global cache_instance_name

#     cache_enum = {}

#     cache_classname = {}
#     #cache_classname.clear()
    
#     cache_classid = {}
#     cache_schema = {}
#     cache_instance_name = {}

#     print("in flush:", len(cache_schema))
# 	#print("##### FLUSHED PER REQUEST CACHE #####")
