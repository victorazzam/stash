#!/usr/bin/python

# Function from challenge
a = lambda x: ((x << 2 | x >> 5) ^ 123) & 255

# All possible values
b = list(map(a, range(256)))

# Values from challenge
c = [113, 220, 168, 206, 164, 220, 180, 236, 250, 73, 196, 228, 220, 244]

print("".join(map(chr, map(b.index, c))))

# Bit-wise Logic
# Flag: ZD2018{Bit-wise Logic}
