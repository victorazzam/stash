#!/usr/bin/env python3
"""
Copy files in a nested directory tree into a single directory.
"""

import os, shutil, random
from sys import argv, exit

try:
	if len(argv) != 2:
		exit("Usage: unpack <directory>")
	save = "unpacked_" + str(random.randint(1000, 10000))
	os.makedirs(save)
	for i in os.walk(argv[1]):
		files = [i[0] + "/" + x for x in i[2]]
		for f in files:
			shutil.copyfile(f, save + "/" + f.split("/")[-1])
	print("Files saved to " + save)
except (KeyboardInterrupt, EOFError):
	print()
