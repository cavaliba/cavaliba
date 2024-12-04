# cavaliba.com



# -----------------------------------------
# cache
# -----------------------------------------

# DataClass Enumerate
cache_enum = {}




def flush_cache_per_request():

	global cache_enum
	cache_enum = {}

	#print("##### FLUSHED PER REQUEST CACHE #####")
