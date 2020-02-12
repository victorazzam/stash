#!/usr/bin/env python3

with open("stupid_cupid.txt") as f:
    a = [x.replace(" ", "").strip("- \n") for x in f if x.strip()]
    print("".join(x[int(y)-1] for x, y in zip(a[4:], a[0].split(","))))
