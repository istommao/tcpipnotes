"""
https://tools.ietf.org/html/rfc793

0                   1                   2                   3
0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Source Port          |       Destination Port        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                        Sequence Number                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Acknowledgment Number                      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Data |           |U|A|P|R|S|F|                               |
| Offset| Reserved  |R|C|S|S|Y|I|            Window             |
|       |           |G|K|H|T|N|N|                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|           Checksum            |         Urgent Pointer        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Options                    |    Padding    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                             data                              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

"""

import socket
import struct


def handler_tcp_header(packet, iph_length):
    """Handler tcp header."""
    tcp_header = packet[iph_length:iph_length + 20]

    tcph = struct.unpack('!HHLLBBHHH', tcp_header)

    src_port = tcph[0]
    dst_port = tcph[1]
    seq = tcph[2]
    ack = tcph[3]
    doff_reserved = tcph[4]
    tcph_length = doff_reserved >> 4

    print('Source Port: %s Dest Port: %s Seq: %s Ack: %s TCP header length: %s' %
          (src_port, dst_port, seq, ack, tcph_length))

    header_size = iph_length + tcph_length * 4
    data_size = len(packet) - header_size

    # get data from the packet
    data = packet[data_size:]
    print('Data', data)


def main():
    # create a raw socket and bind it to the public interface
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

    host = socket.gethostbyname(socket.gethostname())
    port = 0
    sock.bind((host, port))
    while True:
        data, addr = sock.recvfrom(65565)

        print('Data len: %s Addr: %s' % (len(data), addr))
        handler_tcp_header(data, 20)


if __name__ == '__main__':
    main()
