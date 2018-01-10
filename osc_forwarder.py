import sys
import liblo
from socket import(
    error,
    socket,
    AF_INET,
    SOCK_DGRAM
)

UDP_HOST = 'localhost'
UDP_PORT = 11111

# create OSC server address to send OSC data to
try:
    target = liblo.Address(10000)
except liblo.AddressError, msg:
    print 'Failed to create osc address. Error Code: %s | Message: %s' % str(msg[0]), str(msg[1])
    sys.exit()

# create udp dgram socket
try:
    s = socket(AF_INET, SOCK_DGRAM)
except error, msg:
    print 'Failed to create socket. Error Code: %s | Message: %s' % str(msg[0]), str(msg[1])
    sys.exit()

# Bind socket to local host and port
try:
    s.bind((UDP_HOST, UDP_PORT))
except error , msg:
    print 'Bind failed. Error Code: %s | Message: %s' % str(msg[0]), str(msg[1])
    sys.exit()

print 'UDP Socket bind complete'

while True:
    # recieve a packet
    d = s.recvfrom(1024)
    data = d[0]
    addr = d[1]

    print 'recieved message:'
    print data.strip()

liblo.send(target, "/foo/message1", 123, 456.789, "test")
