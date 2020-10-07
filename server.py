#!/usr/bin/env python3

import json
import socket
import threading

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


class ClientThread(threading.Thread):
    def __init__(self, addr, conn):
        threading.Thread.__init__(self)
        self.conn = conn
        print("New connection added: ", addr)

    def run(self):
        # self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        messages = []
        message = b""
        while True:
            data = self.conn.recv(1024)
            chunks = data.split(b"\n")
            for chunk in chunks[:-1]:
                message += chunk
                messages.append(json.loads(message))
                message = b""
            message += chunks[-1]
            print(messages)
            if not data:
                break
            conn.sendall(b"hi\n")
        conn.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    print("server started")

    while True:
        s.listen()
        conn, addr = s.accept()
        newthread = ClientThread(addr, conn)
        newthread.start()
