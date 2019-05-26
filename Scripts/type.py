#!/usr/bin/env python3
"""
Type out the contents of a file by simulating the necessary keyboard presses.
"""

import os, time
from sys import argv, exit, stdout

def timer(s=5):
	print("\033[?25l", end="")
	for i in range(s)[::-1]:
		print(f"Typing in {i+1}", end="\r")
		stdout.flush()
		time.sleep(1)
	print("\033[?25h")

try:
	with open(argv[1]) as f:
		import pyautogui
#		pyautogui.FAILSAFE = True # Move mouse to top left corner of screen to stop typing.
		pyautogui.FAILSAFE = False
		s = [x[8:] for x in argv[2:] if x.startswith("--speed=") and len(x) > 8]
		s = s[-1] if s else "medium"
		d = [x[8:] for x in argv[2:] if x.startswith("--delay=") and len(x) > 8 and x[8:].isdigit()]
		d = d[-1] if d else 5
		speed = {"slow":0.1, "medium":0.05, "fast":0.01}.get(s, 0.05)
		print("Click on the text field where the keypresses should be sent to.")
		timer(int(d))
		pyautogui.typewrite(f.read(), speed)
		print("Done!")
except IndexError:
	print(f"Usage: {argv[0]} <file> [--speed=slow|medium|fast] [--delay=<seconds>]")
	print(f"Example: {argv[0]} example.txt --speed=slow --delay=3")
	exit("Default typing speed is medium. Default delay before typing is 5 seconds.")
except ImportError:
	print("Please make sure you have \033[1;93mpip install\033[med the following dependencies:")
	exit("pyautogui\npyobjc (macOS only)\npyobjc-core (macOS only)")
except IOError:
	print("File does not exist.")
except (KeyboardInterrupt, EOFError, Exception):
	print("\033[?25h")
