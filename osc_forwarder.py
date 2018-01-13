import argparse
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

def setup(tcp_port, osc_port):
    global tcp_socket, osc_target
    # create OSC server address to send OSC data to
    try:
        osc_target = liblo.Address(osc_port)
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
        tcp_socket.listen(1)

    except error , msg:
        print 'Bind failed. Error Code: %s | Message: %s' % (str(msg[0]), str(msg[1]))
        sys.exit()

    print 'TCP Socket created, Port: %s' % (tcp_port)

def serve_and_forward_packets():
    global tcp_socket, osc_target
    device_mapping = {}
    conn, addr = tcp_socket.accept()
    # accept connections
    while True:
        # recieve a packet
        data = conn.recv(1024)
        addr, rssi = data.split()

        # for each new device seen, assign a random frequency value
        if addr not in device_mapping:
            device_mapping[addr] = random.random()

        liblo.send(osc_target, "/ble", device_mapping[addr], rssi, "test")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Sniff Bluetooth and send information to another server to sonify"
    )
    parser.add_argument('tcp_port', help='port to receive TCP packets over', type=int)
    parser.add_argument('osc_port', help='port to send OSC data over', default='10000', type=int)
    parser.add_argument(
        '-v', '--verbose', action='store_true', default=False,
        help='verbose mode (show all serial traffic)'
    )

    args = parser.parse_args()

    try:
        setup(args.tcp_port, args.osc_port)
    except OSError:
        # pySerial returns an OSError if an invalid port is supplied
        print "Unable to open serial port '" + args.serialport + "'"
        sys.exit(-1)
    except KeyboardInterrupt:
        sys.exit(-1)

    serve_and_forward_packets()
