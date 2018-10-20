#!/usr/bin/env python3

import urllib3, readline
from sys import argv, exit

def thumb():
	u = "https://i.ytimg.com/vi/{}/{}default.jpg"
	for q in ("maxres", "sd", "hq", "mq", ""):
		r = http.urlopen("GET", u.format(code, q))
		if r.status not in range(200, 300):
			if q: continue
			return f"Error: video https://www.youtube.com/watch?v={code} does not exist!"
		try:
			r = http.urlopen("GET", u.format(code, q))
			with open(code + ".jpg", "wb") as f:
				f.write(r.data)
			return "Done."
		except Exception as e:
			return "Error: " + str(e)

try:
	http = urllib3.PoolManager(10)
	urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
	if argv[1:]:
		if not all(len(x) == 11 for x in argv[1:]):
			exit("Usage: thumbnail [code ...]\nCode is the 11-character part after 'watch?v=' in the URL.")
		err = []
		pos = 1
		for code in argv[1:]:
			msg = thumb()
			if msg[0] == "E":
				err.append(msg)
			else:
				print(f"\rDone {pos}/{len(argv[1:])}", end="")
				pos += 1
		exit("\n" * (len(err) > 0) + "\n".join(err))
	print("Enter the video's 11-character code, the part after 'watch?v='")
	while 1:
		code = input(">> ").strip()
		if len(a) != 11:
			print("Video code must be 11 characters long!")
		else:
			print(thumb())
except KeyboardInterrupt:
	print()
except Exception as e:
	exit("Error: " + str(e))
