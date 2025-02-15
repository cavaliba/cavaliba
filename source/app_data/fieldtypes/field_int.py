

from .field import Field

# -------------
# INT
# -------------
class FieldInt(Field):


    def get_datapoint_ui_detail(self):
        datapoint = super().get_datapoint_ui_detail()
        a = [str(i) for i in self.value]
        datapoint["value"] = ', '.join(a)
        return datapoint


    def merge_edit_data(self, data):
        self.value = []
        for i in data:
            if len(i) > 0:
                try:
                    self.value.append(int(i))
                except:
                    pass

    def merge_new_data(self, data):
        self.value = []
        for i in data:
            if len(i) > 0:
                try:
                    self.value.append(int(i))
                except:
                    pass


    # def is_valid(self):
    #     r = super().is_valid()
    #     # TODO
    #     return r


    def is_valid(self):
        r = super().is_valid()
        for v in self.value:
            if type(v) is str:
                if len(v) ==0:
                    continue
            try:
                int(str(v))
            except:
                return False
        return r