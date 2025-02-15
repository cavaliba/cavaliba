# cavaliba.com



# -----------------------------------------
# cache
# -----------------------------------------

# DataSchema
cache_schema = {}

# DataClass Enumerate
cache_enum = {}

# DB class objects : classname => DB object
cache_classname = {}
cache_classid = {}

# DB  instance by name
cache_instance_name = {}



def flush_cache_per_request():

    global cache_enum
    global cache_classname
    global cache_classid
    global cache_schema
    global cache_instance_name

    cache_enum = {}

    cache_classname = {}
    #cache_classname.clear()
    
    cache_classid = {}
    cache_schema = {}
    cache_instance_name = {}


	#print("##### FLUSHED PER REQUEST CACHE #####")
