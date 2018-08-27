#!/usr/bin/python

# First unzip dragons.zip

import os, hashlib

os.chdir("dragons")

a = [x for x in os.listdir(".") if x.startswith("dragon")]
c = []

for i in a:
	with open(i) as f:
		c += [x for x in f][-2:]

print hashlib.md5("".join(c)).hexdigest()

# ZD2018{5fdccf8d016ca3e9f3ad18bc9056cb2c}