#!/usr/bin/env python3

import requests

try:
    u = "https://7aimehagbl.neverlanctf.com"
    while 1:
        r = requests.get(u, allow_redirects=False)
        u = r.headers["Location"] 
        if "flag{" in r.text:
            flag = r.text.split("flag{")[1].split("}")[0]
            exit("flag{" + flag + "}")
except (KeyboardInterrupt, EOFError):
    print()
