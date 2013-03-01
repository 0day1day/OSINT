from cymru.bogon.dns import DNSClient as bogon


def bogon_check(ip_address):
    client = bogon()
    return client.lookupmany_dict(ip_address, 'IP')

ip_address = ['10.10.10.10']
print bogon_check(ip_address)