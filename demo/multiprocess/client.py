"""multiprocess client."""
import socket

ipaddr = '127.0.0.1'
port = 6000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((ipaddr, port))

client.send('Hello'.encode('utf-8'))

resp = client.recvfrom(1024)
print(resp[0].decode())

client.close()
