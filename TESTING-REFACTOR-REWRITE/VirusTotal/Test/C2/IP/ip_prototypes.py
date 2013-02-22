from netaddr import IPAddress
from netaddr import IPRange


def exclude_rfc5735_space(address):
    """Exclude RFC 5735 Addresses"""
    ip = IPAddress(address)
    r1 = IPRange('0.0.0.0', '0.255.255.255')
    r2 = IPRange('127.0.0.0', '127.255.255.255')
    if ip not in r1 and ip not in r2:
        print True
        return True
    else:
        return False


def exclude_rfc1918_space(address):
    """Exclude RFC 1918 Addresses"""
    result = True
    ip = IPAddress(address)
    for item in dir(ip):
        if item.startswith('is') and 'unicast' not in item:
            result &= not getattr(ip, item)()
    print True
    return result


def ip_address_valid(address):
    if exclude_rfc5735_space(address) and exclude_rfc1918_space(address):
        yield address


def grab_ip(requestUrl_Text):
    ip_search = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
    for ip_address in ip_search.findall(requestUrl_Text):
        if ip_address_valid(ip_address):
            yield ip_address