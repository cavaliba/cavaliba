# (c) cavaliba.com
# app_data/field_external.py

from .field import Field

# -------------
# EXTERNAL
# -------------
class FieldExternal(Field):


    def __init__(self, fieldname, fieldschema, alljson):

        super().__init__(fieldname, fieldschema, alljson)

        self.parent_fieldname = None
        self.remote_fieldname = None
        self.is_computed = True
        self.value = []

        try:
            tmp = fieldschema["dataformat_ext"].split(' ')
            self.parent_fieldname = tmp[0]
            self.remote_fieldname = tmp[1]
        except:
            pass


    def get_parent_fieldname(self):
        return self.parent_fieldname  


    def get_remote_fieldname(self):
        return self.remote_fieldname


    def is_valid(self):
        r = super().is_valid()
        # TODO
        return r

