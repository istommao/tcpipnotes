import socket
import struct
import binascii

rawsocket = socket.socket(
    socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))

data, addr = rawsocket.recvfrom(2048)

# ethernet header
eth_header = data[0:14]

# 6字节目的mac地址，6字节源mac地址，2字节协议类型
eth_hdr = struct.unpack('!6s6s2s', eth_header)

binascii.hexlify(eth_hdr[0])
binascii.hexlify(eth_hdr[1])
binascii.hexlify(eth_hdr[2])

ipheader = data[14:34]

# 标示转换网络字节序，前12字节为版本、头部长度、服务类型、总长度、标志
# 等其他选项， 后面的两个四字节依次为源IP地址和目的IP地址
ip_hdr = ('!12s4s4s', ipheader)

print('Source IP Address: ' + socket.inet_ntoa(ip_hdr[1]))
print('Destination IP Address: ' + socket.inet_ntoa(ip_hdr[2]))

tcpheader = data[34:54]
tcp_hdr = struct.unpack("!HH16s", tcpheader)

print(tcp_hdr)
