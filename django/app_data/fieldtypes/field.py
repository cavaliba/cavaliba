# cavaliba - sirene - field.py





# --------------------------------------------------------
#  FIELDS
# --------------------------------------------------------

def split_composite(data):
    # Transform a data struct in flat list = [A,b,c,d,]
    # struct can be any "a,b,c" or [a , [b,c,], d, ...]

    reply = []
    
    if type(data) is str:
        result = [x.strip() for x in data.split(',')]
        reply += result
    
    elif type(data) is list:
        for g in data:
            reply += split_composite(g)
    
    elif type(data) is dict:
        pass

    else:
        result = [data]
        reply += result

    return reply


class Field:

    # self.fieldname 
    # self.fieldschema = {...}
    # self.value = []
    # self.errors

    def __init__(self, fieldname=None, fieldschema=None, alljson=None):
        
        self.fieldname = fieldname
        self.fieldschema = fieldschema

        myjson=None
        if alljson:
            if fieldname in alljson:
                myjson = alljson[fieldname]
        if not myjson:
            if fieldschema:
                if 'default_value' in fieldschema:
                    myjson = fieldschema["default_value"]

        # default if no unpacking needed
        if not type(myjson) is list:
            myjson = []
    
        self.value = myjson
        self.errors = []


    def print(self):
        try:
            value_str = '|'.join(self.value)
            print(f"    {self.fieldname} = {self.value}")
        except:
            pass


    def get_attribute(self):
        # RAW return of JSON self.value = ["a", "b", ..."]
        return self.value


    def get_cardinal3(self):

        cardinal = len(self.value)
        cardinal_min = self.fieldschema["cardinal_min"]
        cardinal_max = self.fieldschema["cardinal_max"]
        
        return cardinal, cardinal_min, cardinal_max


    def get_datapoint_ui_detail(self):

        datapoint = {}
        datapoint["fieldname"] = self.fieldname
        datapoint["displayname"] = self.fieldschema["displayname"]
        datapoint["description"] = self.fieldschema["description"]
        datapoint["dataformat"] = self.fieldschema["dataformat"]
        datapoint["dataformat_ext"] = self.fieldschema["dataformat_ext"]
        datapoint["is_multi"] = self.fieldschema["is_multi"]
        datapoint["bigset"] = False
        datapoint["value"] = ''

        if len(self.value) == 1:
            datapoint["value"] = self.value[0]
        elif len(self.value) > 1:
            datapoint["value"] = ', '.join(self.value)

        return datapoint


    def get_datapoint_ui_edit(self):

        # default / parent behavior
        # surcharged in subclass

        datapoint = {}
        datapoint["fieldname"] = self.fieldname
        datapoint["displayname"] = self.fieldschema["displayname"]
        datapoint["description"] = self.fieldschema["description"]
        datapoint["dataformat"] = self.fieldschema["dataformat"]
        datapoint["dataformat_ext"] = self.fieldschema["dataformat_ext"]
        datapoint["is_multi"] = self.fieldschema["is_multi"]
        datapoint["value"] = self.value

        return datapoint


    def get_datapoint_for_export(self):

        # if not type(self.value) is list:
        #     return self.value    
        # else:
        if not self.fieldschema["is_multi"]:
            try:
                return self.value[0]
            except:
                # empty
                return ''
        return self.value



    def merge_edit_data(self, data):
        # default behavior
        if not data:
            self.value = []
            return
            
        if len(data) == 0:
            self.value = []
            return
        
        if not type(data) is list:
            self.value = [data]
            return

        self.value = data


    def merge_new_data(self, data):
        # default behavior

        if not data:
            self.value = []
            return

        if len(data) == 0:
            self.value = []
            return

        if not type(data) is list:
            self.value = [data]
        else:
            self.value = data


    def merge_import_data(self, data):
        # default behavior
        self.value = split_composite(data)
        #print("*** ", self.fieldname, data)
        # if not type(data) is list:
        #     self.value = [data]
        # else:
        #     self.value = data


    def get_json(self):
        return self.value


    def is_valid(self):

        # check cardinality
        cardinal = len(self.value)
        cardinal_min = self.fieldschema["cardinal_min"]
        cardinal_max = self.fieldschema["cardinal_max"]
        if cardinal < cardinal_min:
            return False
        if cardinal_max > 0 and cardinal > cardinal_max:
            return False

        return True
