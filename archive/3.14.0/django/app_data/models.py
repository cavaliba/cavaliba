# app_data - models.py

# import datetime
# from datetime import datetime
# from datetime import timedelta

from django.db import models
# from django.utils import timezone
from django.utils.translation import gettext_lazy as _


from app_user.models import SireneGroup
#from app_user.models import SirenePermission

# ----------------------------------------------------------------------------------
# DataClass
# ----------------------------------------------------------------------------------
HANDLE_CHOICE = (
    ("keyname", "keyname"),
    ("external", "external"),
    ("uuid", "uuid"),
    ("md5", "md5"),
    # ("slugify", "slugify"),
    # ("count", "count"),
)

class DataClass(models.Model):

    keyname = models.SlugField(max_length=128, null=False, blank=False, unique=True)
    displayname = models.CharField(max_length=500,  null=True, blank=True)
    is_enabled = models.BooleanField(default=True)
    
    is_bigset = models.BooleanField(default=False)
    count_estimation = models.IntegerField(default=0)
    handle_method = models.CharField(choices=HANDLE_CHOICE, max_length=32, default="keyname")

    icon  = models.CharField('Icon', max_length=128, blank=True, default="")
    page = models.CharField(max_length=255,  null=True, blank=True)
    order = models.IntegerField(default=100)

    # CRUD permissions per class ; override global built-in ; apply to instances in that class
    p_create = models.CharField(max_length=256,  null=True, blank=True)
    p_read = models.CharField(max_length=256,  null=True, blank=True)
    p_update = models.CharField(max_length=256,  null=True, blank=True)
    p_delete = models.CharField(max_length=256,  null=True, blank=True)
    p_export = models.CharField(max_length=256,  null=True, blank=True)
    p_import = models.CharField(max_length=256,  null=True, blank=True)
    # no override  / all perms
    p_admin = models.CharField(max_length=256,  null=True, blank=True)

    class Meta:
        #db_table = "{{ app_name}}_category"
        ordering = ['keyname']
        verbose_name = "Cavaliba Data Class"
        verbose_name_plural = "Cavaliba Data Classes"

    def __str__(self):
        return f"{self.keyname}"



# ----------------------------------------------------------------------------------
# DataSchema
# ----------------------------------------------------------------------------------

# DataSchema
# - classobj FK => DataClass:keyname   "Site"
# - keyname: attribut Slug              "location", "address", "population", "notify_to", ...
# - displayname
# - format:  int, str, JSON, base64, date, static_list, user, group, DataClass, DataLink
# - format_ext:  (static_list keyname, DataClass keyname, DataLink keyname)
# - order (+page)
# - cardinal_min
# - cardinal_max
# [-widget, ...]



FIELD_FORMAT_CHOICE = (
    ("string", "string"),
    ("int", "int"),
    ("float", "float"),
    ("boolean", "boolean"),
    ("ipv4", "ipv4"),
    ("date", "date"),
    ("schema","schema"),
    ("group","group"),
    ("user","user"),
    ("datetime", "datetime"),
    ("json", "json"),
    ("text", "text"),
    ("enumerate", "enumerate"),
    ("external", "external"),

    # permission
    # html, yaml, json
    # bin / encrypt ?
    # password
    # file
    # link

)


class DataSchema(models.Model):

    classobj = models.ForeignKey("DataClass", on_delete=models.CASCADE)
    keyname = models.SlugField(max_length=128, null=False, blank=False)
    displayname = models.CharField(max_length=500,  null=True, blank=True)
    description = models.CharField(_("Description"), max_length=500, blank=True)
    is_enabled = models.BooleanField(default=True)

    dataformat = models.CharField(choices=FIELD_FORMAT_CHOICE, max_length=32, default="string")
    dataformat_ext = models.CharField(max_length=500,  null=True, blank=True)
    default_value = models.CharField(max_length=500,  null=True, blank=True, default="")

    page = models.CharField(max_length=255,  null=True, blank=True)
    order = models.IntegerField(default=100)

    cardinal_min = models.IntegerField(default=0)
    cardinal_max = models.IntegerField(default=1)

    # NEXT - CRUD permissions at field level
    ###p_create = models.CharField(max_length=256,  null=True, blank=True)
    #p_read = models.CharField(max_length=256,  null=True, blank=True)
    #p_update = models.CharField(max_length=256,  null=True, blank=True)
    ###p_delete = models.CharField(max_length=256,  null=True, blank=True)

    class Meta:
        #db_table = "{{ app_name}}_category"
        unique_together = ["classobj", "keyname"]
        ordering = ['classobj','keyname','order']
        verbose_name = "Cavaliba Data Schema"
        verbose_name_plural = "Cavaliba Data Schema"

    def __str__(self):
        return f"{self.classobj}:{self.keyname}({self.dataformat}/{self.dataformat_ext})"


# ----------------------------------------------------------------------------------
# DataInstance
# ----------------------------------------------------------------------------------
# DataInstance
# - classobj FK => DataClass:keyname   "Site"
# - keyname: slug                       "Site_X324C"
# - displayname                         "Site X2342C in Milan"
# - is_enabled
# - data: JSON => all attributs from Schema   
#     "Location:Paris",
#     "Address:XXXX",
#     "notify_to: ["group1","group2",...]
#     "X_hosts_app: [app1, app2, app3]",


class DataInstance(models.Model):

    classobj = models.ForeignKey("DataClass", on_delete=models.CASCADE)
    keyname = models.CharField(max_length=256, null=False, blank=False)
    handle = models.SlugField(max_length=128, null=True, blank=True)

    displayname = models.CharField(max_length=500,  null=True, blank=True)
    is_enabled = models.BooleanField(default=True)

    data_json = models.TextField(max_length=5000,  null=True, blank=True)
    # NEXT
    #remote_json = models.TextField(max_length=5000,  null=True, blank=True)
    #reverse_json = models.TextField(max_length=5000,  null=True, blank=True)
    
    # CRUD permissions per instance - override per-clas / built-in global
    #p_create = models.CharField(max_length=256,  null=True, blank=True)
    p_read = models.CharField(max_length=256,  null=True, blank=True)
    p_update = models.CharField(max_length=256,  null=True, blank=True)
    p_delete = models.CharField(max_length=256,  null=True, blank=True)

    last_update = models.DateTimeField(_("Last update"), auto_now_add=False, blank=True, null=True)

   
    
    class Meta:
        #db_table = "{{ app_name}}_category"
        indexes = [
            models.Index(fields=["classobj"]),
            models.Index(fields=["keyname"]),
            models.Index(fields=["is_enabled"]),
            ]
        unique_together = ["classobj", "keyname"]
        #unique_together = ["classobj", "handle"]
        ordering = ['classobj','keyname']
        verbose_name = "Cavaliba Data Instance"
        verbose_name_plural = "Cavaliba Data Instances"

    def __str__(self):
        if self.displayname:
            return f"{self.displayname}"
        else:
            return f"{self.keyname}"




