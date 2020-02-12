#!/usr/bin/env python3

with open("download.svg") as f:
    s = "".join("01"[i[0] == "3"] for i in f.read().split('fill:#')[1:])
    print(bytes.fromhex(hex(int(s + "0", 2))[2:]).decode())
