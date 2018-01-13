import argparse
import sys
import time
from socket import(
    socket,
    error as socket_error,
    AF_INET,
    SOCK_STREAM
)
from SnifferAPI import Sniffer, Logger

# global sniffer object
ble_sniffer = None
udp_socket = None

def setup(device_addr, udp_host, udp_port):
    # create udp dgram socket
    try:
        global udp_socket
        udp_socket = socket(AF_INET, SOCK_STREAM)
        print udp_host, udp_port, type(udp_port)
        udp_socket.connect((udp_host, udp_port))
    except socket_error, msg:
        print 'Failed to create socket. Error Code: %s | Message: %s' % (str(msg[0]), str(msg[1]))
        sys.exit()

    print 'UDP Socket created, Host: %s Port: %s' % (udp_host, udp_port)

    # initialize sniffer over the serial connection
    print "Connecting to sniffer on " + device_addr

    global ble_sniffer
    ble_sniffer = Sniffer.Sniffer(device_addr)
    ble_sniffer.start()

def scan_devices_and_follow():
    global ble_sniffer
    global udp_socket
    #devices = {}
    while True:
        packets = ble_sniffer.getPackets()
        for packet in packets:
            if packet.blePacket is not None:
                try:
                    addr = ':'.join(["%02X" % x for x in packet.blePacket.advAddress])
                    # Display the raw BLE packet payload
                    # Note: 'BlePacket' is nested inside the higher level 'Packet' wrapper class
                    # if addr in devices:
                    #     # print devices[addr], packet.RSSI
                    #     print addr, packet.RSSI
                    # else:
                    #     devices[addr] = len(devices.keys())
                    #     # print devices[addr], packet.RSSI
                    #     print addr, packet.RSSI
                    print addr, packet.RSSI
                    udp_socket.sendall('%s %d' % (addr, packet.RSSI))
                except:
                    pass



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Sniff Bluetooth and send information to another server to sonify"
    )
    parser.add_argument('device_addr', help='address of ble device something like /dev/ttyUSB0')
    parser.add_argument('udp_host', help='host address to send UDP packets to')
    parser.add_argument('udp_port', help='port to send UDP packets over', type=int)
    parser.add_argument(
        '-v', '--verbose', action='store_true', default=False,
        help='verbose mode (show all serial traffic)'
    )

    args = parser.parse_args()

    try:
        setup(args.device_addr, args.udp_host, args.udp_port)
    except OSError:
        # pySerial returns an OSError if an invalid port is supplied
        print "Unable to open serial port '" + args.serialport + "'"
        sys.exit(-1)
    except KeyboardInterrupt:
        sys.exit(-1)

    scan_devices_and_follow()
