"""tcp client."""
import socket

ipaddr = '127.0.0.1'
port = 8060

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((ipaddr, port))

data = """GET / HTTP/1.0\r\n\r\nHello world!"""
client.send(data.encode('utf-8'))

resp = client.recvfrom(2048)
print(resp[0].decode())

client.close()
