import socket


def ip_address_is_valid(address):
    try:
        socket.inet_aton(address)
    except socket.error:
        return False
    else:
        return True

address = "5.9.85.206"
print(ip_address_is_valid(address))