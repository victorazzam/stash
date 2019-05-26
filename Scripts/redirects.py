#!/usr/bin/env python3
"""
Find out where a URL redirects to by following the HTTP "Location" response header.
"""

import requests
from sys import argv, exit

try:
	if not (argv[1:] + [""])[0].startswith(("http://", "https://")):
		exit("Usage: long <URL>\nExample: long https://bit.ly/AbCdEf")
	u = argv[1]
	while 1:
		r = requests.head(u)
		if "Location" not in r.headers:
			break
		u = r.headers["Location"]
		print(u)
except (KeyboardInterrupt, EOFError):
	print()
except Exception:
	exit("Error, the URL could not be retrieved.")
