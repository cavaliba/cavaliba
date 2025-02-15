# (c) cavaliba.com - IAM - ip.py



from app_home.configuration import get_configuration
from app_home.log import log, DEBUG, INFO, WARNING, ERROR, CRITICAL


# ======================================
# IP Range check
# ======================================

def cidr_fit(cidr_a, cidr_b):

    def split_cidr(cidr):
        part_list = cidr.split("/")
        if len(part_list) == 1:
            # if just an IP address, assume /32
            part_list.append("32")

        # return address and prefix size
        return part_list[0].strip(), int(part_list[1])

    def address_to_bits(address):
        # convert each octet of IP address to binary
        bit_list = [bin(int(part)) for part in address.split(".")]

        # join binary parts together
        # note: part[2:] to slice off the leading "0b" from bin() results
        return "".join([part[2:].zfill(8) for part in bit_list])

    def binary_network_prefix(cidr):
        # return CIDR as bits, to the length of the prefix size only (drop the rest)
        address, prefix_size = split_cidr(cidr)
        return address_to_bits(address)[:prefix_size]

    prefix_a = binary_network_prefix(cidr_a)
    prefix_b = binary_network_prefix(cidr_b)

    return prefix_a.startswith(prefix_b) or prefix_b.startswith(prefix_a)


def is_trusted_ip(ip):

    if not ip:
        return False

    cidr_item = get_configuration(appname="user", keyname="TRUSTED_ANONYMOUS_IPS").split(",")
    for item in cidr_item:
        if len(item) == 0:
            continue
        # item = "127.0.0.1"
        # item = "192.168.0.0/22"
        # item = "0.0.0.0/0"
        try:
            if cidr_fit(item, ip):
                return True
        except:
            # bug in cidr_fit...
            log(ERROR, action="is_trusted_ip", status="FAIL", data=f"invalid cidr range ({ip})")

    return False


def get_user_ip(request):

    x_real_ip       = request.META.get('HTTP_X_REAL_IP')
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    remote_addr     = request.META.get('REMOTE_ADDR')

    if x_real_ip:
        ip = x_real_ip
    elif x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = remote_addr

    return ip
