# (c) cavaliba.com - data - handle.py

import uuid
import hashlib


# supported methods
# ----------------

# keyname
# uuid
# md5
# external



def update_handle(method="keyname", keyname=None, current_handle=None):

    if method == "keyname":
        return keyname
    
    elif method == "external":
        return current_handle
    
    elif method == "uuid":
        return str(uuid.uuid4())
    
    elif method == "md5":
        m = hashlib.md5()
        m.update(keyname.encode('UTF-8'))
        return m.hexdigest()

    return keyname



