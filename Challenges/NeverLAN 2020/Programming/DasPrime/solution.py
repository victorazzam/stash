#!/usr/bin/env python3

prime = lambda n: all(n % x for x in range(2, int(n ** 0.5 + 1)))
p, c = 3, 2

while c < 10497:
    p += 2
    if prime(p):
        c += 1

print(p)
