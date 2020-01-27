#!/usr/bin/env python3

import os
from sys import argv, exit

dns = "/usr/local/share/dns/saved"

def run(a, b):
    cmd = f"networksetup -{a}etdnsservers Wi-Fi {b}"
    return os.popen(cmd).read().strip()

if not argv[1:]:
    out = run("g", "")
elif "-h" in argv:
    exit("Usage: dns [clear|save|saved|restore|0.0.0.0 ...]")
elif argv[1] == "clear":
    out = run("s", "empty")
elif argv[1] == "save":
    if not os.path.isdir(dns[:-6]):
        os.makedirs(dns[:-6])
    a = " ".join(run("g", "").split())
    if "DNS" in a:
        exit("There is nothing to save!")
    try:
        with open(dns, "w") as f:
            f.write(a)
    except IOError:
        exit(f"Could not open DNS file: {dns}")
    exit(0)
elif argv[1] == "saved":
    try:
        with open(dns) as f:
            a = f.read()
    except IOError:
        exit(f"Could not open DNS file: {dns}")
    if not a:
        exit("There are no entries saved!")
    print(a)
    exit(0)
elif argv[1] == "restore":
    try:
        with open(dns) as f:
            a = f.read()
        if not a:
            exit("There is nothing to restore!")
        out = run("s", a)
    except IOError:
        exit(f"Could not open DNS file: {dns}")
else:
    out = run("s", " ".join(argv[1:]))

print(out, end="\n" * (len(out) > 0))
