

from .field import Field

TRUE_LIST = ('on', 'On', 'ON', True, 'yes', 'Yes', 'YES', 'True', 'true', 'TRUE', 1, "1")


# -------------
# BOOLEAN
# -------------
class FieldBoolean(Field):

    def print(self):
        value_str = ', '.join([str(i) for i in self.value])
        print(f"    {self.fieldname} = {self.value}")


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
        # TODO
        return r