# app_data - models.py

import datetime
from datetime import datetime
from datetime import timedelta


from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


from app_user.models import SireneGroup


    # name             = models.SlugField('Name (slug,unique)', max_length=50, blank=False, unique=True)
    # title            = models.CharField('Title', max_length=250, blank=True)
    # body             = models.TextField('Text', max_length=2500, blank=True)
    # severity         = models.CharField('Severity', choices=SIRENE_SEVERITY, max_length=20, default="na")
    # is_default       = models.BooleanField('Default Public Page', default=False)
    # is_enabled       = models.BooleanField('Enabled', default=True)
    # is_visible = models.BooleanField('Is visible', default=True, db_index=True)
    # created_at = models.DateTimeField("Created at", auto_now_add=False, db_index=True)   # , default=datetime.now
    # created_by = models.CharField('Created by', max_length=200, blank=True)
    # removed_at = models.DateTimeField("Removed at", auto_now_add=False, blank=True, null=True)
    # removed_by = models.CharField('Removed by', max_length=200, blank=True, default='auto')
    # notify_to        = models.ManyToManyField(Scope, blank=True)
    # severity         = models.CharField('Sévérité', choices=SIRENE_SEVERITY, max_length=20, default="na")
    # site          = models.ForeignKey("Site", null=True, blank=True, on_delete=models.SET_NULL)


    #appname = models.SlugField('Sirene App', max_length=128, null=False, blank=False, default="home")


# ----------------------------------------------------------------------------------
# DataClass
# ----------------------------------------------------------------------------------


class DataClass(models.Model):

    keyname = models.SlugField(max_length=128, null=False, blank=False, unique=True)
    displayname = models.CharField(max_length=500,  null=True, blank=True)
    is_enabled = models.BooleanField(default=True)
    
    is_bigset = models.BooleanField(default=False)
    count_estimation = models.IntegerField(default=0)

    icon  = models.CharField('Icon', max_length=128, blank=True, default="")
    page = models.CharField(max_length=255,  null=True, blank=True)
    order = models.IntegerField(default=100)

    role_show   = models.ForeignKey(SireneGroup, related_name="+", on_delete=models.SET_DEFAULT, null=True, blank=True, default=None)
    role_access = models.ForeignKey(SireneGroup, related_name="+", on_delete=models.SET_DEFAULT, null=True, blank=True, default=None)
    role_read   = models.ForeignKey(SireneGroup, related_name="+", on_delete=models.SET_DEFAULT, null=True, blank=True, default=None)

    role_create = models.ForeignKey(SireneGroup, related_name="+", on_delete=models.SET_DEFAULT, null=True, blank=True, default=None)
    role_update = models.ForeignKey(SireneGroup, related_name="+", on_delete=models.SET_DEFAULT, null=True, blank=True, default=None)
    role_delete = models.ForeignKey(SireneGroup, related_name="+", on_delete=models.SET_DEFAULT, null=True, blank=True, default=None)
    role_onoff  = models.ForeignKey(SireneGroup, related_name="+", on_delete=models.SET_DEFAULT, null=True, blank=True, default=None)

    role_import = models.ForeignKey(SireneGroup, related_name="+", on_delete=models.SET_DEFAULT, null=True, blank=True, default=None)
    role_export = models.ForeignKey(SireneGroup, related_name="+", on_delete=models.SET_DEFAULT, null=True, blank=True, default=None)

    class Meta:
        #db_table = "{{ app_name}}_category"
        ordering = ['keyname']
        verbose_name = "Sirene Data Class"
        verbose_name_plural = "Sirene Data Classes"

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
    ("sirene_data","sirene_data"),
    ("sirene_static", "sirene_static"),
    ("sirene_group","sirene_group"),
    ("sirene_user","sirene_user"),
    ("datetime", "datetime"),
    ("json", "json"),
    ("text", "text"),
    ("enumerate", "enumerate"),

    # bin / encrypt ?
    # file
    # sirene_data
    # sirene_link?
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


    class Meta:
        #db_table = "{{ app_name}}_category"
        unique_together = ["classobj", "keyname"]
        ordering = ['classobj','keyname','order']
        verbose_name = "Sirene Data Schema"
        verbose_name_plural = "Sirene Data Schema"

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
    keyname = models.SlugField(max_length=128, null=False, blank=False)
    displayname = models.CharField(max_length=500,  null=True, blank=True)
    is_enabled = models.BooleanField(default=True)
    data_json = models.TextField(max_length=5000,  null=True, blank=True)
    last_update = models.DateTimeField(_("Last update"), auto_now_add=False, blank=True, null=True)


    class Meta:
        #db_table = "{{ app_name}}_category"
        indexes = [
            models.Index(fields=["classobj"]),
            models.Index(fields=["keyname"]),
            models.Index(fields=["is_enabled"]),
            ]
        unique_together = ["classobj", "keyname"]
        ordering = ['classobj','keyname']
        verbose_name = "Sirene Data Instance"
        verbose_name_plural = "Sirene Data Instances"

    def __str__(self):
        if self.displayname:
            return f"{self.displayname}"
        else:
            return f"{self.keyname}"



