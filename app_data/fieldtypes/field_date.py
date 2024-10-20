import datetime

from .field import Field

# -------------
# DATE
# -------------
class FieldDate(Field):

    def print(self):
        a = self.value
        print(f"    {self.fieldname} = {self.value}")


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
                
    def is_valid(self):
        r = super().is_valid()
        for v in self.value:
            if type(v) is str:
                if len(v) ==0:
                    continue            
            try:
                # YYYY-MM-DD
                datetime.date.fromisoformat(v)
            except:
                return False
        return r



