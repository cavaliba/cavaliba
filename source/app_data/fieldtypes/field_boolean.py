
from app_home.cavaliba import TRUE_LIST
from .field import Field

# -------------
# BOOLEAN
# -------------
class FieldBoolean(Field):

    def get_first_value(self):
        try:
            return self.value[0] in TRUE_LIST
        except:
            return False
        
    
    def __merge_data(self, data):
        self.value=[]
        if type(data) is list:
            for i in data:
                r = i in TRUE_LIST
                self.value.append(r)
        else:
            r = data in TRUE_LIST
            self.value.append(r)


    def merge_edit_data(self, data):
        self.__merge_data(data)
        
    def merge_new_data(self, data):
        self.__merge_data(data)

    def merge_import_data(self, data):
        self.__merge_data(data)


    def is_valid(self):
        r = super().is_valid()
        for b in self.value:
            if not isinstance(b, (bool)):
                return False
        return r
