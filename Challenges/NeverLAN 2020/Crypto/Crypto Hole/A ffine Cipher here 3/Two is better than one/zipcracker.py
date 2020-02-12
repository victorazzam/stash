#!/usr/bin/env python3

import sys, zlib, zipfile, itertools

pw = ["".join(x) for x in itertools.permutations("I6K BD3 SDF TNR 78D".split())]

for pos, line in enumerate(pw):
    try:
        print(f"\rTrying [{pos}] {line:40}", end="", flush=True)
        zip_file = zipfile.ZipFile(sys.argv[1])
        zip_file.extractall(pwd=f"V{line}Q".encode())
        zip_file.close()
    except KeyboardInterrupt:
        input("Paused...")
    except (zlib.error, zipfile.BadZipFile, RuntimeError, UnicodeDecodeError):
        pass
    else:
        print(f"\nPassword found!")
        break
