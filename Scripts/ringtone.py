#!/usr/bin/env python3

import os, re, sys

def trim(name, cut):
    r = re.match(r"\d\d:\d\d:\d\d-\d\d:\d\d:\d\d", cut)
    if not r:
        sys.exit("Incorrect use of trimming.")
    frm, to = r.group().split("-")
    if not int("".join(frm.split(":"))) < int("".join(to.split(":"))):
        sys.exit("Incorrect use of trimming.")
    a, b = frm.split(":"), to.split(":")
    if any(x not in range(60) for x in map(int, a[1:] + b[1:])):
        sys.exit("Incorrect use of trimming.")
    if any(x not in range(24) for x in map(int, a[:1] + b[:1])):
        sys.exit("Incorrect use of trimming.")
    do(f"ffmpeg -i {name}.mp3 -ss {frm} -to {to} -c copy -y {name}_trimmed.mp3")
    return name + "_trimmed"

def mp3(name, ext):
    try:
        exts = {
            "flac": f"-ab 320k -map_metadata 0 -id3v2_version 3",
            "wav": f"-vn -ar 44100 -ac 2 -ab 320k"
        }
        do(f"ffmpeg -i {name}.{ext} " + exts[ext.lower()] + f" {name}.mp3")
    except KeyError:
        sys.exit("Format not supported.")

def do(cmd):
    print(f"\033[97;41;7m{cmd}\033[m")
    p = os.popen(cmd + " 2>&1").read().lower()
    if "conversion failed!" in p or "error " in p:
        print("\033[31;47;7mError!\033[m")

def main(name, ext, cut):
    if ext != "mp3":
        mp3(name, ext)
    if cut:
        name = trim(name, cut)
    do(f"ffmpeg -i {name}.mp3 -vn -c copy -map_metadata -1 -y {name}__.mp3")
    do(f"ffmpeg -i {name}__.mp3 -ac 1 -ab 320k -f mp4 -c aac -t 30 -y {name}.m4r")
    do(f"rm {name}__.mp3 " + (name + ".mp3") * (ext != "mp3"))

try:
    if not sys.argv[1:]:
        sys.exit("Usage: ringtone <file> [from-to]\nExample: ringtone song.mp3 00:00:48-00:01:18")
    if not os.path.isfile(sys.argv[1]):
        sys.exit("File does not exist.")
    main(*sys.argv[1].rsplit(".", 1) + [sys.argv[2] if sys.argv[2:] else False])
except KeyboardInterrupt:
    print()
