#!/usr/bin/env python3

import gmpy2

try:
    n, e, c = 2533, 569, "2193 1745 2164 970 1466 2495 1438 1412 1745 1745 2302 1163 2181 1613 1438 884 2495 2302 2164 2181 884 2302 1703 1924 2302 1801 1412 2495 53 1337 2217"
    p, q = 17, 149 # factordb.com
    d = gmpy2.invert(e, (p-1) * (q-1))
    m = b""
    for i in c.split():
        m += bytes.fromhex(hex(pow(int(i), d, n))[2:])
except Exception:
    print(m.decode())
