#!/usr/bin/env python3

import base64

with open("encrypted_db") as f:
    a = f.read()
    b = bytes.fromhex(a.replace(" ", "").replace("\n", ""))
    c = base64.b64decode(b)
    print("flag{" + c.split(b"flag{")[1].split(b"}")[0].decode() + "}")
