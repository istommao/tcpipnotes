"""raw socket demo."""
import sys
import socket
import struct


# def calc_checksum(data):
#     """TCP checksum.

#     https://tools.ietf.org/html/rfc1071
#     """
#     s = 0
#     n = len(data) % 2
#     for i in range(0, len(data) - n, 2):
#         s += ord(data[i]) + (ord(data[i + 1]) << 8)

#     if n:
#         s += ord(data[i + 1])
#     while (s >> 16):
#         s = (s & 0xFFFF) + (s >> 16)

#     s = ~s & 0xffff
#     return s

def calc_checksum(source_string):
    # I'm not too confident that this is right but testing seems to
    # suggest that it gives the same answers as in_cksum in ping.c.
    sum = 0
    l = len(source_string)
    count_to = (l / 2) * 2
    count = 0
    while count < count_to:
        this_val = source_string[count + 1] * 256 + source_string[count]
        sum = sum + this_val
        sum = sum & 0xffffffff  # Necessary?
        count = count + 2
    if count_to < l:
        sum = sum + source_string[l - 1]
        sum = sum & 0xffffffff  # Necessary?
    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    # Swap bytes. Bugger me if I know why.
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


try:
    conn = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
except socket.error as msg:
    print('Socket could not be created. Error %s' % msg)
    sys.exit()

packet = b''

source_ip = '192.168.1.142'
dest_ip = '192.168.1.130'


def generate_ip_header():
    ip_ihl = 5
    ip_ver = 4
    ip_tos = 0
    ip_tot_len = 0
    ip_id = 54321
    ip_frag_off = 0
    ip_ttl = 255
    ip_proto = socket.IPPROTO_TCP
    ip_check = 0

    ip_saddr = socket.inet_aton(source_ip)
    ip_daddr = socket.inet_aton(dest_ip)

    ip_ihl_ver = (ip_ver << 4) + ip_ihl

    ip_header = struct.pack('!BBHHHBBH4s4s', ip_ihl_ver, ip_tos, ip_tot_len,
                            ip_id, ip_frag_off, ip_ttl, ip_proto, ip_check, ip_saddr, ip_daddr)

    return ip_header


def generate_tcp_header(source_port=None, destination_port=None, check_sum=None):
    # tcp header fields
    src_port = 34234   # source port
    dst_port = 24830   # destination port
    seq = 454
    ack_seq = 0
    doff = 5  # 4 bit field, size of tcp header, 5 * 4 = 20 bytes

    # tcp flags
    tcp_fin = 0
    tcp_syn = 1
    tcp_rst = 0
    tcp_psh = 0
    tcp_ack = 0
    tcp_urg = 0
    window_size = socket.htons(5840)  # maximum allowed window size
    check_sum = 0
    urg_ptr = 0

    offset_res = (doff << 4) + 0
    flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + \
        (tcp_psh << 3) + (tcp_ack << 4) + (tcp_urg << 5)

    # the ! in the pack format string means network order

    if check_sum:
        tcp_header = struct.pack(
            '!HHLLBBH', src_port, dst_port, seq, ack_seq,
            offset_res, flags, window_size
        ) + struct.pack('H', check_sum) + struct.pack('!H', urg_ptr)
    else:
        tcp_header = struct.pack(
            '!HHLLBBHHH', src_port, dst_port, seq, ack_seq,
            offset_res, flags, window_size, check_sum, urg_ptr)

    return tcp_header


user_data = b'Hello, how are you'

# pseudo header fields
src_addr = socket.inet_aton(source_ip)
dst_addr = socket.inet_aton(dest_ip)
placeholder = 0

tcp_header = generate_tcp_header()
tcp_length = len(tcp_header) + len(user_data)

psh = struct.pack('!4s4sBBH', src_addr, dst_addr,
                  placeholder, socket.IPPROTO_TCP, tcp_length)

psh = psh + tcp_header + user_data


check_sum = calc_checksum(psh)
# print tcp_checksum

# # make the tcp header again and fill the correct checksum - remember checksum is NOT in network byte order
tcp_header = generate_tcp_header(check_sum)

ip_header = generate_ip_header()
# final full packet - syn packets dont have any data
packet = ip_header + tcp_header + user_data

# Send the packet finally - the port specified has no effect
# put this in a loop if you want to flood the target
result = conn.sendto(packet, (dest_ip, 0))
print(packet, result)
