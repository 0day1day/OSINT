import socket
import time
from SyslogProtocol import SyslogProtocol

def syslog_tcp_open(host='127.0.0.1', port=514):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock


def syslog_tcp(sock, message, priority=0, facility=0):
    print "syslog_tcp " + message
    data = SyslogProtocol.encode(facility, priority, message)
    sock.send(data + '\n')


def syslog_tcp_close(sock):
    sock.close()


def main():
    message = "cef"
    sock = syslog_tcp_open('127.0.0.1', port=514)
    syslog_tcp(sock, "%s" % message, priority=0, facility=7)
    time.sleep(0.01)
    syslog_tcp_close(sock)