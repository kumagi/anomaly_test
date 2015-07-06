# -*- coding: utf-8 -*-
import socket
import msgpack
from contextlib import closing

host = '127.0.0.1'
port = 9191
backlog = 10
bufsize = 4096

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

with closing(sock):
    sock.bind((host, port))
    sock.listen(backlog)
    while True:
        conn, address = sock.accept()
        buff = ""
        while True:
            msg = conn.recv(bufsize)
            if len(msg) == 0:
                break
            buff += msg

        print(msgpack.loads(buff))

