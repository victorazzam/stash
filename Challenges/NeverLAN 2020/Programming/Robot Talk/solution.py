#!/usr/bin/env python3

import socket, base64

try:
    s = socket.socket()
    s.connect(("challenges.neverlanctf.com", 1120))
    s.settimeout(3)
    s.send(b"GET /\n")
    while 1:
        data = b"".join(s.recv(2048) for i in "  ")
        if b"flag" in data:
            print(data.decode().split()[2])
            raise EOFError
        enc = data.split(b"ypt: ")[-1]
        txt = base64.b64decode(enc)
        s.send(txt)
except (KeyboardInterrupt, EOFError, socket.error):
    s.close()
