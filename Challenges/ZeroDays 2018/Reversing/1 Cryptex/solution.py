#!/usr/bin/python

# Function from challenge
a = lambda x: (((ord(x) << 2) | (ord(x) >> 5)) ^ 123) & 255

# All possible values
b = [a(chr(g)) for g in range(255)]

# Values from challenge
v = [113, 220, 168, 206, 164, 220, 180, 236, 250, 73, 196, 228, 220, 244]

print "".join(chr(b.index(i)) for i in v)

# Bit-wise Logic
# Flag: ZD2018{Bit-wise Logic}