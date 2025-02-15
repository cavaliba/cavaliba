

from .field import Field


def check_valid_ipv4(source_ip):
    # 10.1.2.3
    # 10.0.0.0/24
    # 10.1.2.3/24 

    mask = None
    if '/' in source_ip:
        (ip, mask)=source_ip.split("/")
    else:
        ip = source_ip

    try:
        digits = ip.split('.')
    except:
        #print("ip split failed")
        return False

    # mask
    if mask:
        try:
            a = int(mask)
        except:
            #print("mask not int")
            return False
        if a <0 or a>32:
            #print("mask invalid")
            return False

    # digits
    if len(digits) != 4:
        #print("ip not 4 items")
        return False

    for i in digits:
        try:
            i2 = int(i)
        except:
            return False
        if i2 <0 or i2 > 255:
            return False


    return True

# -------------
# IPV4
# -------------
class FieldIPV4(Field):


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
            r2 = check_valid_ipv4(v)
            if not r2:
                r = False
                break

        return r

