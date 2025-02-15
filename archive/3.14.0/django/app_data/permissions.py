# (c) cavaliba.com
# app_data / permissions.py


def is_user_in_group(aaa=None, gname=None):

    if gname in aaa["groups"] + aaa["groups_indirect"]:
        return True
    return False


# -- read

def has_read_permission_on_class(aaa=None, classobj=None):
    # classobj is a DB object

    if not aaa:
        return False
    
    if not classobj:
        return False

    if '*' in aaa['perms']:
        return True
    
    # global p_data_admin
    if "p_data_admin" in aaa["perms"]:
        return True

    # p_admin on classobj
    if classobj.p_admin:
        if classobj.p_admin in aaa["perms"]:
            return True

    # p_read  
    if classobj.p_read:
        if classobj.p_read in aaa["perms"]:
            return True
        else:
            return False
    
    # default    
    if "p_data_read" in aaa["perms"]:
        return True

    return False


def has_read_permission_on_instance(aaa=None, iobj=None):
    # iobj is a DB object

    if not aaa:
        return False
    
    if not iobj:
        return False

    if '*' in aaa['perms']:
        return True

    if "p_data_admin" in aaa["perms"]:
        return True

    # class permission ?
    if not has_read_permission_on_class(aaa, classobj=iobj.classobj):
        return False
    
    # p_admin on classobj ? (allow direct & stop inheritance)
    if iobj.classobj.p_admin:
        if iobj.classobj.p_admin in aaa["perms"]:
            return True
            
    # instance permission
    if iobj.p_read:
        if iobj.p_read in aaa["perms"]:
            return True
        else:
            return False

    # default    
    if "p_data_read" in aaa["perms"]:
        return True

    return False

# -- delete

def has_delete_permission_on_class(aaa=None, classobj=None):
    # classobj is a DB object

    if not aaa:
        return False
    
    if not classobj:
        return False

    if '*' in aaa['perms']:
        return True

    # global p_data_admin: allow all on data
    if "p_data_admin" in aaa["perms"]:
        return True

    # p_admin on classobj : allow all on this class
    if classobj.p_admin:
        if classobj.p_admin in aaa["perms"]:
            return True

    #  allow on this class if defined
    if classobj.p_delete:
        if classobj.p_delete in aaa["perms"]:
            return True
        else:
            return False
    
    # default: if allow  on all class / all instances ; overridable
    if "p_data_delete" in aaa["perms"]:
        return True

    return False


def has_delete_permission_on_instance(aaa=None, iobj=None):
    # iobj is a DB object

    if not aaa:
        return False
    
    if not iobj:
        return False

    if '*' in aaa['perms']:
        return True

    if "p_data_admin" in aaa["perms"]:
        return True

    # class permission needed
    if not has_delete_permission_on_class(aaa, classobj=iobj.classobj):
        return False
    
    # p_admin on classobj: allow all on this class; no override 
    if iobj.classobj.p_admin:
        if iobj.classobj.p_admin in aaa["perms"]:
            return True
            
    # instance permission
    if iobj.p_delete:
        if iobj.p_delete in aaa["perms"]:
            return True
        else:
            return False

    # default: class level overridable
    if "p_data_delete" in aaa["perms"]:
        return True

    return False



# -- edit / update

def has_edit_permission_on_class(aaa=None, classobj=None):
    # classobj is a DB object

    if not aaa:
        return False
    
    if not classobj:
        return False

    if '*' in aaa['perms']:
        return True

    # global p_data_admin: allow all on data / no override
    if "p_data_admin" in aaa["perms"]:
        return True

    # p_admin on classobj : allow all on this class / no override
    if classobj.p_admin:
        if classobj.p_admin in aaa["perms"]:
            return True

    #  allow  on this class if defined
    if classobj.p_update:
        if classobj.p_update in aaa["perms"]:
            return True
        else:
            return False
    
    # default: allow update on all class / all instances ; overridable
    if "p_data_update" in aaa["perms"]:
        return True

    return False


def has_edit_permission_on_instance(aaa=None, iobj=None):
    # iobj is a DB object

    if not aaa:
        return False
    
    if not iobj:
        return False

    if '*' in aaa['perms']:
        return True

    if "p_data_admin" in aaa["perms"]:
        return True

    # class permission needed
    if not has_edit_permission_on_class(aaa, classobj=iobj.classobj):
        return False
    
    # p_admin on classobj: allow all on this class; no override 
    if iobj.classobj.p_admin:
        if iobj.classobj.p_admin in aaa["perms"]:
            return True
            
    # instance permission if defined
    if iobj.p_update:
        if iobj.p_update in aaa["perms"]:
            return True
        else:
            return False

    # default: class level overridable
    if "p_data_update" in aaa["perms"]:
        return True

    return False


# -- create new instance

def has_create_permission_on_class(aaa=None, classobj=None):
    # classobj is a DB object

    if not aaa:
        return False
    
    if not classobj:
        return False

    if '*' in aaa['perms']:
        return True

    # global p_data_admin: allow all on DATA / no override
    if "p_data_admin" in aaa["perms"]:
        return True

    # classlevel p_admin if defined : allow all on this class / no override
    if classobj.p_admin:
        if classobj.p_admin in aaa["perms"]:
            return True

    # allow  on this class if defined
    if classobj.p_create:
        if classobj.p_create in aaa["perms"]:
            return True
        else:
            return False
    
    # default: if allow  on all class / all instances ; overridable
    if "p_data_create" in aaa["perms"]:
        return True

    return False