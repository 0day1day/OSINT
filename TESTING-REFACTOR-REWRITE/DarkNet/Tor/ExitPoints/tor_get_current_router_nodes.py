__date__ = "Dec 15, 2012"
__author__ = "AlienOne"
__copyright__ = "GPL"
__credits__ = ["Justin Jessup"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "AlienOne"
__email__ = "Justin@alienonesecurity.com"
__status__ = "Production"


import requests
import daemon
import time
from syslog.syslog_tcp import *


def cull_urlData(url_element, file_name):
    """Cull URL Data"""
    request_urlGet = requests.get(url_element)
    if request_urlGet.status_code == 200:
        data = request_urlGet.text
        with open(file_name, 'wt') as f:
            f.write(data)


def tor_routerNodes():
    """Cull Tor Router Nodes"""
    SEARCH_BASE = "http://128.31.0.34:9031/tor/status/all"
    file_name = "tor_router_nodes.txt"
    cull_urlData(SEARCH_BASE, file_name)
    open_file = open(file_name, 'rt')
    sock = syslog_tcp_open('127.0.0.1', port=1026)
    for i, line in enumerate(open_file):
        if line.startswith('r'):
            urlDataList = [str(i), line.split()[1:]]
            urlDataDict = dict(zip(urlDataList[0:5], urlDataList[1:]))
            for values in urlDataDict.values():
                try:
                    element = values[5].strip('\n')
                    cef_router_node = 'CEF:0|Tor Router Node|Tor Router|1.0|Router Node|Tor Router Node|1| src=%s' % \
                                      element
                    syslog_tcp(sock, "%s" % cef_router_node, priority=0, facility=7)
                except ValueError:
                    return ValueError
    syslog_tcp_close(sock)


def tor_exitNodes():
    """Cull Tor Exit Nodes"""
    url_list = ["http://exitlist.torproject.org/exit-addresses", "http://exitlist.torproject.org/exit-addresses.new"]
    sock = syslog_tcp_open('127.0.0.1', port=1026)
    for url_element in url_list:
        file_name = "tor_exit_nodes.txt"
        cull_urlData(url_element, file_name)
        open_file = open(file_name, 'rt')
        for i, line in enumerate(open_file):
            if line.startswith('ExitAddress'):
                urlDataList = [str(i), line.split()[1:]]
                urlDataDict = dict(zip(urlDataList[0:5], urlDataList[1:]))
                for values in urlDataDict.values():
                    try:
                        element = values[0].strip('\n')
                        cef_exit_node = 'CEF:0|Tor Exit Node|Tor Exit|1.0|Exit Node|Tor Exit Node|1| src=%s' % \
                                        element
                        syslog_tcp(sock, "%s" % cef_exit_node, priority=0, facility=7)
                    except IndexError:
                        return None
    syslog_tcp_close(sock)


def main():
    """Cull Tor Indicators Every 24 Hours"""
    tor_routerNodes()
    tor_exitNodes()
    time.sleep(86400)

if __name__ == '__main__':
    with daemon.DaemonContext():
        main()