"""
raw socket ip proto
https://tools.ietf.org/html/rfc791.

    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |Version|  IHL  |Type of Service|          Total Length         |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |         Identification        |Flags|      Fragment Offset    |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |  Time to Live |    Protocol   |         Header Checksum       |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                       Source Address                          |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                    Destination Address                        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |                    Options                    |    Padding    |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

                    Example Internet Datagram Header
"""

import socket
import struct


class ByKeyOrValue(object):
    _set_of_pairs = set()

    @classmethod
    def get(cls, key_or_value, default="Unknown"):
        for pair in cls._set_of_pairs:
            if pair[0] == key_or_value:
                return pair[1]
            elif pair[1] == key_or_value:
                return pair[0]

        return default


class EtherTypes(ByKeyOrValue):
    _set_of_pairs = {
        ("IPv4", 0x0800),
        ("ARP", 0x0806),
        ("RARP", 0x8035),
        ("SNMP", 0x814c),
        ("IPv6", 0x86dd)
    }


class IPVersions(ByKeyOrValue):
    _set_of_pairs = {
        ("IPv4", 4),
        ("IPv6", 6)
    }


class TransportProtocols(ByKeyOrValue):
    _set_of_pairs = {
        ("ICMP", 1),
        ("TCP", 6),
        ("UDP", 17)
    }


def format_field(field, field_type):

    if field_type == "mac":
        # Format a MAC address as XX:XX:XX:XX:XX:XX
        byte_str = ["{:02x}".format(field[i])
                    for i in range(0, len(field))]
        return ":".join(byte_str)
    elif field_type == "ethertype":
        return EtherTypes.get(field)
    elif field_type == "ipver":
        return IPVersions.get(field)
    elif field_type == "transproto":
        return TransportProtocols.get(field)


class IPFlags(object):

    def __init__(self, flag_bits):
        # Flags is an integer taking 3-bit
        # The 1st bit is reserved and is of no use
        # The 2nd bit:
        self.DF = flag_bits & 0b11 >> 1
        # The 3rd bit:
        self.MF = flag_bits & 0b1

    def __str__(self):
        result = []
        if self.DF:
            result.append("DF, ")
        if self.MF:
            result.append("MF, ")

        "".join(result)

        if result:
            return result[:-2]
        else:
            return "--"


def handler_ip_header(ip_header):
    iph = struct.unpack('!BBHHHBBH4s4s', ip_header)

    version_ihl = iph[0]
    version = version_ihl >> 4

    ihl = version_ihl & 0xF

    total_len = iph[2]
    ident = '0x{:04x}'.format(iph[3])
    iph_length = ihl * 4

    flags = IPFlags(iph[4] >> 3)
    frag_off = iph[4] & 0b1111111111111
    ttl = iph[5]
    protocol = iph[6]
    check_sum = iph[7]
    src_ip = socket.inet_ntoa(iph[8])
    dst_ip = socket.inet_ntoa(iph[9])

    print(
        'Version: %s IHL: %s Total Length: %s\n'
        'Identification: %s  Flags: %s Fragment Offset: %s\n'
        'TTL: %s Protocol: %s Header Checksum: %s\n'
        'Source Address: %s\n'
        'Destination Address: %s\n' %
        (version, iph_length, total_len, ident, flags, frag_off,
         ttl, format_field(protocol, 'transproto'), check_sum, src_ip, dst_ip)
    )


def main():
    # the public network interface
    host = socket.gethostbyname(socket.gethostname())

    # create a raw socket and bind it to the public interface
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
    sock.bind((host, 0))
    while True:
        data, addr = sock.recvfrom(65565)
        print('Data len: %s addr: %s' % (len(data), addr))
        handler_ip_header(data[:20])


if __name__ == '__main__':
    main()
