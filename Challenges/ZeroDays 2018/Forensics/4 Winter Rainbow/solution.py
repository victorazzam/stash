#!/usr/bin/python

from PIL import Image

img = Image.open("rainbow.png")
pix = img.load()
pixels = [[pix[x,y] for x in range(img.size[0])] for y in range(img.size[1])]
a = []
for i in pixels[0]:
	if i[:3] not in a:
		a.append(i[:3])

print "".join(chr(x) for y in a for x in y)

# ZD2018{T4ste_Th3 R41nB0w F33l The fun }