#!/usr/bin/env python3

import json
import socket
import threading

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

_rooms = { "default": []}

class ClientThread(threading.Thread):
    def __init__(self, addr, conn):
        threading.Thread.__init__(self)
        self.conn = conn
        _rooms["default"].append(self)
        self.addr = addr
        print("New connection added: ", addr)

    def __del__(self):
        print("Removing connection", self.addr)
        _rooms["default"].remove(self)

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
            if data[-1] == "\n":
                messages.append(json.loads(message))
                message = b""
            if not data:
                break

            for msg_obj in messages:
                for client in _rooms["default"]:
                    msg_str = bytes(json.dumps(msg_obj), encoding='utf8')
                    try:
                        client.conn.sendall(msg_str + b'\n')
                    except:
                        pass
            messages = []
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
