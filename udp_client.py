import sys
from socket import(
    socket,
    error as socket_error,
    AF_INET,
    SOCK_DGRAM
)

UDP_HOST = 'localhost'
UDP_PORT = 11111

# create udp dgram socket
try:
    s = socket(AF_INET, SOCK_DGRAM)
except socket_error, msg:
    print 'Failed to create socket. Error Code: %s | Message: %s' % str(msg[0]), str(msg[1])
    sys.exit()

print 'UDP Socket created. Send messages with stdin.'

while True:
    msg = sys.stdin.readline()

    try :
        s.sendto(msg, (UDP_HOST, UDP_PORT))

    except socket_error, msg:
        print 'Failed to send message. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
