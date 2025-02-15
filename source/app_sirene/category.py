# (c) cavaliba.com - sirene - category.py



from app_home.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL
from .models import Category


# -------------------------------------------------------
# category
# -------------------------------------------------------

def category_get_by_name(name):
    return Category.objects.filter(name=name).first()




