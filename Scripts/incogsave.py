#!/usr/bin/env python3

import os

try:
    if "Chrome.app" not in os.popen("ps -ax").read():
        exit("Google Chrome is not running.")
    cmd = "osascript -e 'tell application \"Google Chrome\" to get URL of tab {} of window {}' 2>&1"
    for w in range(1, 21):
        for t in range(1, 101):
            out = os.popen(cmd.format(t, w)).read().strip()
            if "Can’t get tab" in out:
                break
            if "Can’t get window" in out:
                exit()
            if out != "chrome://newtab/":
                print(out.strip())
except (KeyboardInterrupt, EOFError):
    print()
