#!/usr/bin/python
#
# Attempt to fix broken PNG files
# Author: Victor Azzam

from os import path
from sys import argv
from struct import pack

if not argv[1:]:
	exit("Usage: python fixpng.py /path/to/pngfile")

if not path.isfile(argv[1]):
	exit("File does not exist!")

crc_table = [0] * 256

for n in xrange(256):
	c = n
	for k in xrange(8):
		if c & 1:
			c = 0xEDB88320L ^ (c >> 1)
		else:
			c >>= 1
	crc_table[n] = c

def update_crc(c, buf):
	for byte in buf:
		c = crc_table[int((c ^ ord(byte)) & 0xFF)] ^ (c >> 8)
	return c

def get_crc(buf):
	return update_crc(0xFFFFFFFFL, buf) ^ 0xFFFFFFFFL

Hex = lambda x: x.encode("hex")
UnHex = lambda x: x.replace(" ", "").decode("hex")

FILE = argv[1]
new_image = ""
HEAD = UnHex("89 50 4E 47 0D 0A 1A 0A 00 00") # 8-byte header + 2 empty bytes
IEND = UnHex("00 00 00 00 49 45 4E 44 AE 42 60 82") # 12-byte final chunk
print

with open(FILE) as f:
	image = f.read()

if image[:10] != HEAD:
#	print "'" + image[:10] + "'"
	print "Invalid PNG header, fixing"

new_image += HEAD[:-2]

if image[12:16] != "IHDR":
#	print "'" + image[12:16] + "'"
	exit("Invalid IHDR chunk, exiting\n")

# Offset of IHDR and all IDAT chunks
CHNK = [8] + [x-4 for x in range(len(image)) if image.startswith("IDAT", x)]

# Check if IHDR chunk and all IDAT chunks are correctly assembled
for i in sorted(set(CHNK)):
	length = int(image[i:i+4].encode("hex"), 16)
	name = image[i+4:i+8]
	if name == "IHDR":
		length = int(image[i+2:i+4].encode("hex"), 16)
	data = image[i+8:i+8+length]
#	Debugging, get offset and redundancy check number
#	print hex(i), i, length, image[i:i+4]
#	print [hex(ord(x)) for x in image[i+8+length:i+8+length+4]]
	crc = int(image[i+8+length:i+8+length+4].encode("hex"), 16)
	csum = get_crc(name + data)
	if crc != csum:
		print "Invalid CRC at offset " + hex(i + 8 + length)
		print "Changing {} to {}\n".format(hex(crc).strip("L"), hex(csum).strip("L"))
	new_image += pack(">I", length) + name + data + pack(">I", csum)

if image[-12:] != IEND:
	print "Invalid IEND chunk, fixing"

new_image += IEND

with open("fixed-" + FILE, "w") as f:
	f.write(new_image)

print "All done! Saved as {}\n".format("fixed-" + FILE)

'''

REFERENCES
==========
https://en.wikipedia.org/wiki/Portable_Network_Graphics#File_format
http://www.libpng.org/pub/png/spec/1.2/PNG-Structure.html
https://stackoverflow.com/q/42748223
https://stackoverflow.com/q/19890545
https://www.w3.org/TR/PNG/#11IHDR

'''