#!/usr/bin/env python3

import urllib3, readline
from sys import argv, exit

def thumb(codes):
	u = "https://i.ytimg.com/vi/{}/{}default.jpg"
	for y, c in enumerate(codes):
		for q in ("maxres", "sd", "hq", "mq", ""):
			r = http.urlopen("GET", u.format(c, q))
			if r.status in range(200, 300):
				break
			if not q:
				return "Video https://www.youtube.com/watch?v=" + c + " does not exist!"
		try:
			r = http.urlopen("GET", u.format(c, q))
			with open(c + ".jpg", "wb") as f:
				f.write(r.data)
			return "Done {}/{}".format(y+1, len(codes))
		except Exception as e:
			return "Error: " + str(e)

try:
	http = urllib3.PoolManager(10)
	urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
	if argv[1:]:
		if not all(len(x) == 11 for x in argv[1:]):
			exit("Usage: thumbnail [code ...]\nCode is the 11-character part after 'watch?v=' in the URL.")
		exit(thumb(argv[1:]))
	print("Enter the video's 11-character code, the part after 'watch?v='")
	while 1:
		a = input(">> ").strip()
		if len(a) != 11:
			print("Video code must be 11 characters long!")
		else:
			print(thumb([a]))
except KeyboardInterrupt:
	print()
except Exception as e:
	exit("Error: " + str(e))