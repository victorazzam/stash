#!/usr/bin/env python3

import os

def tabs(app):
    for w in range(1, 21):
        for t in range(1, 101):
            out = os.popen(cmd.format(app, t, w)).read().strip()
            if "Can't get tab" in out:
                break
            if "Can't get window" in out or "execution error:" in out:
                return
            if out != "chrome://newtab/":
                print(out.strip())

try:
    cmd = "osascript -e 'tell application \"{}\" to get URL of tab {} of window {}' 2>&1"
    ps = os.popen("ps -ax").read()
    for app in ("Google Chrome", "Chromium"):
        if f"{app}.app" not in ps:
            print(f"{app} is not running.")
        else:
            tabs(app)
except (KeyboardInterrupt, EOFError):
    print()
