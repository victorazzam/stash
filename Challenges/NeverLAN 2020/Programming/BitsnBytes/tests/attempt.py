#!/usr/bin/env python3

import time, requests

d = lambda x: bytes.fromhex(hex(int(x, 2))[2:]).decode()

def p(x):
    for y, i in enumerate(x):
        if y % 25 == 0:
            print()
        print(i, end=" ", flush=True)
    print()

while 1:
    r = requests.get("https://challenges.neverlanctf.com:1150/svg.php")
    s = "".join("01"[i[0] == "3"] for i in r.text.split('fill:#')[1:])
    # v = (r.headers["Date"], d(s+"0"), d(s+"1"), d(s[-7:]+"0"), d(s[-7:]+"1"))
    # print("\n".join(v) + "\n")
    p(s)

    time.sleep(60)
