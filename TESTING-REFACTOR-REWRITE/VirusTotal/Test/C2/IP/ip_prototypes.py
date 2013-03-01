from netaddr import IPAddress
from netaddr import IPSet
from pybloom import BloomFilter
from multiprocessing import Pool


def multi_process(jobname):
    po = Pool()
    po.apply_async(jobname)
    po.close
    po.join


def bogon_check():
    ipv4_addr_space = IPSet(['0.0.0.0/0'])
    private = IPSet(['10.0.0.0/8', '172.16.0.0/12', '192.0.2.0/24', '192.168.0.0/16', '239.192.0.0/14'])
    reserved = IPSet(['225.0.0.0/8', '226.0.0.0/7', '228.0.0.0/6', '234.0.0.0/7', '236.0.0.0/7',
                      '238.0.0.0/8', '240.0.0.0/4'])
    unavailable = reserved | private
    available = ipv4_addr_space ^ unavailable
    for cidr in available.iter_cidrs():
        for ip in cidr:
            yield ip


def bloomFilter(check_ip_address):
    f = BloomFilter(capacity=10000000, error_rate=0.001)
    [f.add(ip_address) for ip_address in bogon_check()]
    return check_ip_address in f


def main():
    for item in bogon_check():
        print item
    # check_ip_address = '10.10.10.10'
    # print(bloomFilter(check_ip_address))

if __name__ == '__main__':
    multi_process(main())