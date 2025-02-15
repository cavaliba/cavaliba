

from .field import Field
# -------------
# STRING
# -------------
class FieldString(Field):


    def merge_edit_data(self, data):
        self.value = []
        for i in data:
            if len(i) > 0:
                self.value.append(i)

    def merge_new_data(self, data):
        self.value = []
        for i in data:
            if len(i) > 0:
                self.value.append(i)

    def merge_import_data(self, data):
        # no split composite !
        self.value = []
        if type(data) is str:
            self.value = [data]
        elif type(data) is list:
            for i in data:
                self.value.append(i)

    def is_valid(self):
        r = super().is_valid()
        # TODO
        return r

