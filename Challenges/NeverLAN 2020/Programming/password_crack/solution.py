#!/usr/bin/env python3

from hashlib import md5

users = "purvesta N30 ZestyFE viking s7a73farm bashNinja".lower().split()
colors = "red green blue yellow orange purple violet cyan indigo grey black white silver gold magenta brown".split()
h = "267530778aa6585019c98985eeda255f"

for user in users:
    for color in colors:
        for year in range(1000, 2020):
            r = f"{color}-{year}-{user}"
            if md5(r.encode()).hexdigest() == h:
                print(r)
                exit(0)
