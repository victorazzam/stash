#!/usr/bin/env python3

import requests
from sys import *

try:
	help = "Usage: long <URL>\nExample: long https://bit.ly/AbCdEf"
	if not (argv[1:] + [""])[0].startswith(("http://", "https://")):
		exit(help)
	u = argv[1]
	while 1:
		r = requests.head(u)
		if "Location" not in r.headers:
			break
		u = r.headers["Location"]
		print(u)
except KeyboardInterrupt:
	exit()
except Exception:
	exit("Error: the URL could not be retrieved")