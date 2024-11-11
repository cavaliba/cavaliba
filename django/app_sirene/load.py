# Loader
# function for Loading JSON into model

import sys
import yaml
import json
import re

from app_sirene.models import MessageTemplate
from app_sirene.models import Category
from app_sirene.models import PublicPage

from app_data.data import get_instance_by_name
from app_user.group import group_get_by_name




# ----------------------------------------------------------------------------
# helper
# ----------------------------------------------------------------------------


def split_composite(data):
    # Transform a data struct in flat list = [A,b,c,d,]
    # struct can be any "a,b,c" or [a , [b,c,], d, ...]

    reply = []
    
    if type(data) is str:
        result = [x for x in data.replace(';',' ').replace(',',' ').split()]
        reply += result
    
    elif type(data) is list:
        for g in data:
            reply += split_composite(g)
    
    elif type(data) is dict:
        pass

    else:
        result = [data]
        reply += result

    return reply


# ----------------------------------------------------------------------------
# Load a SIRENE DATA bloc of configuration
# ----------------------------------------------------------------------------
def load_sirene(data, force_action=None, verbose=False):
    
    count = 0

    if not data:
        return 

    if len(data) == 0:
        return

    for item, instdata in data.items():

        # if not ":" in item:
        #     continue

        if item.startswith("_sirene:"):
            keyname = re.sub("^_sirene:", '', item)
            if keyname == "":
                continue
            instdata["name"] = keyname
            load_template(instdata, force_action=force_action, verbose=verbose)
            count += 1

        if item.startswith("_sirene_public:"):
            keyname = re.sub("^_sirene_public:", '', item)
            if keyname == "":
                continue
            instdata["name"] = keyname
            load_public(instdata, force_action=force_action, verbose=verbose)
            count += 1


        if item.startswith("_sirene_category:"):
            keyname = re.sub("^_sirene_category:", '', item)
            if keyname == "":
                continue
            instdata["name"] = keyname
            load_category(instdata, force_action=force_action, verbose=verbose)
            count += 1
        
    return count
        
# ----------------------------------------------------------------------------
# Category
# ----------------------------------------------------------------------------


def load_category(data, force_action=None, verbose=False): 
    ''' Load a json structure describing a Category into the database '''

    try:
        name = data['name']
    except:
        print(f"  !!err - missing category name")
        return

    # get existing entry or None
    entry = Category.objects.filter(name=name).first()

    # if delete == true, remove & done!
    must_delete  = data.get('delete', False)
    if must_delete:
        if entry:
            entry.delete()
            print(f"  deleted catageory {name}")
        return


    is_new = False
    if not entry:
        entry = Category()
        is_new = True

       
    # create / update
    entry.name        = name
    entry.longname    = data.get('longname', '')
    entry.description = data.get('description', 'n/a')
    entry.is_enabled  = data.get('is_enabled', True)
    entry.save() 

    if verbose:
        if is_new:
            print(f"  created catageory {name}")
        else:
            print(f"  updated catageory {name}")

    return



# ----------------------------------------------------------------------------
# PublicPages
# ----------------------------------------------------------------------------



def load_public(data, force_action=None, verbose=False):
    ''' Load a json structure  into database '''

    try:
        name = data['name']
    except:
        print(f"  !!err - missing public page name")
        return       

    entry =  PublicPage.objects.filter(name=name).first()

    # if delete == true, remove & done!
    must_delete  = data.get('delete', False)
    if must_delete:
        if entry:
            entry.delete()
            print(f"  deleted public page {name}")
        return

    is_new = False
    if not entry:
        entry = PublicPage()
        is_new = True

    entry.name        = name 
    entry.title       = data.get('title', name)
    entry.severity    = data.get('severity', 'na')
    entry.is_default  = data.get('is_default', False)
    entry.is_enabled  = data.get('is_enabled', True)

    if 'message' in data:
        entry.body  = data.get('message')
    else:
        print(f"  !!err - missing public page data")
        return

    entry.save()

    if verbose:
        if is_new:
            print(f"  created public page {name}")
        else:
            print(f"  updated public page {name}")


    return

# ----------------------------------------------------------------------------
# Template
# ----------------------------------------------------------------------------


def load_template(data, load_pass=0, force_action=None, verbose=False):
    ''' Load a json structure  into database '''

    try:
        name = data['name']
    except:
        print(f"  !!err - missing template name")
        return


    entry =  MessageTemplate.objects.filter(name=name).first()

    # if delete == true, remove & done!
    must_delete  = data.get('delete', False)
    if must_delete:
        if entry:
            entry.delete()
            print(f"  deleted template {name}")
        return 1

    is_new = False
    if not entry:
        entry = MessageTemplate()
        is_new = True


    # create ; use default from model if none provided
    entry.name  = name 

    if 'title' in data:
        entry.title       = data.get('title')

    if 'severity' in data:
        entry.severity       = data.get('severity')

    if 'description' in data:
        entry.description = data.get('description')
    

    # if 'is_default' in data:
    #     entry.is_default  = data.get('is_default')
    
    if 'is_enabled' in data:
        entry.is_enabled  = data.get('is_enabled')

    # accept both syntax
    if 'body' in data:
        entry.body  = data.get('body')
    if 'message' in data:
        entry.body  = data.get('message')


    if 'has_publicpage' in data:
        entry.has_publicpage  = data.get('has_publicpage')

    if 'has_privatepage' in data:
        entry.has_privatepage  = data.get('has_privatepage')

    if 'has_email' in data:
         entry.has_email = data.get('has_email')

    if 'has_sms' in data:
        entry.has_sms  = data.get('has_sms')

    entry.save()

    if verbose:
        if is_new:
            print(f"  created template {name}")
        else:
            print(f"  updated template {name}")



    # public page 
    if 'publicpage' in data:
        public_name = data['publicpage']
        try:
            item = PublicPage.objects.get(name=public_name)
            entry.publicpage = item
            entry.has_publicpage  = True
            if verbose:
                print(f"    + added public page {item.name} to template {entry.name}")
        except Exception as e :
            print(f"    !!err invalid public page {public_name} for template {entry.name}")


    # category
    if "category" in data:
        category_name = data['category']
        try:
            item = Category.objects.get(name=category_name)
            entry.category = item
            if verbose:
                print(f"    + added category {item.name} to template {entry.name}")            
        except Exception as e :
            print(f"    !!err invalid category {category_name} for template {entry.name}")
    
    if "notify_site" in data:
        instance_list = split_composite(data['notify_site'])
        for iname in instance_list:
            # TODO - use Configuration for classname
            iobj = get_instance_by_name(classname="site", iname=iname)
            if iobj:
                entry.notify_site.add(iobj)
                if verbose:
                    print(f"    + added notify_site {iname} to template {entry.name}")
            else:
                print(f"    !!err invalid notify_site {iname} for template {entry.name}")

    if "notify_app" in data:
        instance_list = split_composite(data['notify_app'])
        for iname in instance_list:
            # TODO - use Configuration for classname
            iobj = get_instance_by_name(classname="app", iname=iname)
            if iobj:
                entry.notify_app.add(iobj)
                if verbose:
                    print(f"    + added notify_app {iname} to template {entry.name}")
            else:
                print(f"    !!err invalid notify_app {iname} for template {entry.name}")

    if "notify_sitegroup" in data:
        instance_list = split_composite(data['notify_sitegroup'])
        for iname in instance_list:
            # TODO - use Configuration for classname
            iobj = get_instance_by_name(classname="sitegroup", iname=iname)
            if iobj:
                entry.notify_sitegroup.add(iobj)
                if verbose:
                    print(f"    + added notify_sitegroup {iname} to template {entry.name}")
            else:
                print(f"    !!err invalid notify_sitegroup {iname} for template {entry.name}")

    if "notify_customer" in data:
        instance_list = split_composite(data['notify_customer'])
        for iname in instance_list:
            # TODO - use Configuration for classname
            iobj = get_instance_by_name(classname="customer", iname=iname)
            if iobj:
                entry.notify_customer.add(iobj)
                if verbose:
                    print(f"    + added notify_customer {iname} to template {entry.name}")
            else:
                print(f"    !!err invalid notify_customer {iname} for template {entry.name}")


    if "notify_group" in data:
        instance_list = split_composite(data['notify_group'])
        for iname in instance_list:
            iobj = group_get_by_name(iname)
            if iobj:
                entry.notify_group.add(iobj)
                if verbose:        
                    print(f"    + added notify_group {iname} to template {entry.name}")
            else:
                print(f"    !!err invalid notify_group {iname} for template {entry.name}")


    entry.save() 

    return



