import socket
from SyslogProtocol import SyslogProtocol

def syslog_tcp_open(host='127.0.0.1', port=514):
    """Open TCP Socket to Syslog Server"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock


def syslog_tcp(sock, message, priority=0, facility=0):
    """Send TCP Event via Syslog Protocol"""
    # Uncomment to DEBUG syslog messages
    print(message)
    data = SyslogProtocol.encode(facility, priority, message)
    sock.send(data + '\n')


def syslog_tcp_close(sock):
    """Close the TCP Socket once message has completed being sent"""
    sock.close()
