# (c) cavaliba.com - home - context_processor.py


from django.conf import settings

from app_user.aaa import get_aaa
from app_home.configuration import get_configuration
from app_home.home import get_sidebar

from app_home.cavaliba import CAVALIBA_VERSION


def get_info(request):

    context = {}

    aaa=get_aaa(request)
    #context['aaa'] = aaa

    for k,v in aaa.items():
        if not k.startswith("p_"):
            continue
        context[k] = v

    context["CAVALIBA_VERSION"] = CAVALIBA_VERSION

    # SIDEBAR
    sidebar_entries = get_sidebar(aaa)          
    # page/order for UI
    # [  [page1, [item1, item22,  ...] , [ page2, [...] ] ,  ... ]
    paginated = []
    pagelist = []
    index = {}     # page => [class1, class2]
    default_name = get_configuration("home", "GLOBAL_APPNAME")

    for element in sidebar_entries:
        if element.keyname == 'home':
            continue
        order = element.order
        section = element.sidebar_section
        if not section:
            continue
        if len(section) == 0:
            continue
        if section not in index:
            index[section] = []
            pagelist.append(section)
        index[section].append(element)
        default_name = section
    for p in pagelist:
        paginated.append([p, index[p]])

    context["sidebar"] = paginated


    # notif app
    context['SIRENE_APPNAME'] = get_configuration("sirene", "SIRENE_APPNAME")

    # global
    context["GLOBAL_APPNAME"] = get_configuration("home", "GLOBAL_APPNAME")

    # navbar logo or Home icon
    context["LOGO_SIZE"] = int(get_configuration("home", "LOGO_SIZE"))


    return context
