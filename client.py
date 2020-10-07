
import json
import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

conn = socket.create_connection((HOST, PORT))

conn.send(b"{\"a\":1}\n")
conn.close()
while True:
    data = conn.recv(5)
