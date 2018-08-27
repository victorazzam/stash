#!/usr/bin/python
#
# Author: Victor Azzam

with open("masked.png") as f:
	a = f.read()

# First "row" of bytes
m = list(map(ord, a[:16]))

# Actual PNG header + IHDR chunk length and name
p = [int(x, 16) for x in "89 50 4E 47 0D 0A 1A 0A 00 00 00 0D 49 48 44 52".split()]

# XOR: CONQUESTCONQUEST
print "XOR: " + "".join(chr(x ^ y) for x, y in zip(m,p))

# Positions in the ASCII table
key = [x ^ y for x, y in zip(m,p)][:8]

# Repeated XOR using the key
with open("output.png", "w") as f:
	f.write("".join(chr(ord(x) ^ key[y % 8]) for y, x in enumerate(a)))

print "Written to file: output.png"