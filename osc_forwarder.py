import sys
import liblo
from socket import(
    error,
    socket,
    AF_INET,
    SOCK_STREAM
)

global tcp_socket
global osc_target

def setup(tcp_host, tcp_port, osc_port):
    global tcp_socket, osc_host
    # create OSC server address to send OSC data to
    try:
        osc_host = liblo.Address(osc_port)
    except liblo.AddressError, msg:
        print 'Failed to create osc address. Error Code: %s | Message: %s' % (str(msg[0]), str(msg[1]))
        sys.exit()

    # create tcp dgram socket
    try:
        tcp_socket = socket(AF_INET, SOCK_STREAM)
    except socket_error, msg:
        print 'Failed to create socket. Error Code: %s | Message: %s' % (str(msg[0]), str(msg[1]))
        sys.exit()

    # Bind socket to local host and port
    try:
        tcp_socket.bind(("", tcp_port))
        tcp_socket.listen()
        conn, addr = tcp_socket.accept()
    except error , msg:
        print 'Bind failed. Error Code: %s | Message: %s' % (str(msg[0]), str(msg[1]))
        sys.exit()

    print 'TCP Socket created, Host: %s Port: %s' % (tcp_host, tcp_port)

def serve_and_forward_packets():
    global tcp_socket, osc_target

    # accept connections
    tcp_socket.listen(1)
    while True:
        # recieve a packet
        d = conn.recv(1024)
        data = d[0]
        addr = d[1]

        print 'recieved message:'
        print data.strip()

    liblo.send(osc_target, "/foo/message1", 123, 456.789, "test")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Sniff Bluetooth and send information to another server to sonify"
    )
    parser.add_argument('device_addr', help='address of ble device something like /dev/ttyUSB0')
    parser.add_argument('tcp_port', help='port to receive TCP packets over')
    # parser.add_argument('osc_host', help='host address to send OSC  data to', default='localhost')
    parser.add_argument('osc_port', help='port to send OSC data over', default='10000')
    parser.add_argument(
        '-v', '--verbose', action='store_true', default=False,
        help='verbose mode (show all serial traffic)'
    )

    args = parser.parse_args()

    try:
        setup(args.tcp_host, args.tcp_port, args.osc_port)
    except OSError:
        # pySerial returns an OSError if an invalid port is supplied
        print "Unable to open serial port '" + args.serialport + "'"
        sys.exit(-1)
    except KeyboardInterrupt:
        sys.exit(-1)

    serve_and_forward_packets()
