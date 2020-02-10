#!/usr/bin/env python3

import os, sys, time, shutil, requests, hashlib, traceback

fas = lambda f: "".join(map(chr, open(f, "rb").read()))
fab = lambda x: open(x, "rb").read()
hash = lambda x: hashlib.sha256(x if type(x) == bytes else x.encode()).hexdigest()

def dump(data, n=None):
    print("\nSHA256:", hash(data))
    for i in range(0, len(data), 16):
        line = hex(i)[2:].zfill(8)
        hexed = " ".join(hex(ord(x))[2:].zfill(2) for x in data[i:i+16])
        rep = "".join(x if ord(x) in range(32, 127) else "." for x in data[i:i+16])
        print(f"{line}  {hexed[:23]:23}  {hexed[24:]:23}  |{rep:16}|")
        if i == n:
            break

try:
    s = requests.Session()
    s.cookies.set("session", sys.argv[2])
    s.headers["User-Agent"] = "Mozilla/5.0"

    DEBUG = "--debug" in sys.argv
    watch = ([int(x[8:]) for x in sys.argv if x[:8] == "--watch=" and x[8:].isdigit() and int(x[8:]) > 59] + [0])[0]
    host = "/".join(sys.argv[1].split("/", 3)[:3])
    assert host.startswith(("http://", "https://"))

    save = host.lstrip("htps:")[2:]
    for arg in sys.argv:
        if arg.startswith("--save=") and len(arg) > 7:
            dir = arg[7:]
            if os.path.isfile(dir):
                print(f"Cannot save to file {dir}. Skipping...")
            else:
                save = dir
    save.rstrip("/")

    for _ in range(1000000 * watch + 1):
        challs = s.get(f"{host}/api/v1/challenges").json()["data"]
        for cid in sorted(chall["id"] for chall in challs):
            chall = s.get(f"{host}/api/v1/challenges/{cid}").json()["data"]
            chall.pop("type")
            locals().update(chall) # category name description files hints
            desc, path = description.replace("\r", "").strip(), f"{save}/{category.replace('/', '-').strip()}/{name.replace('/', '-').strip()}"
            for y, i in enumerate(hints):
                if i["cost"] == 0:
                    r = s.get(f"{host}/api/v1/hints/{i['id']}").json()["data"]["content"]
                    desc += f"\n\nHint {y+1}\n{'-'*(len(str(y+1))+5)}\n{r}"
            README = f"{path}/README.txt"
            if not os.path.isfile(README):
                print(f"New: {path}")
            elif hash(desc) != hash(fab(README)):
                print(f"Updated: {path}")
                if DEBUG:
                    dump(fas(README))
                    dump(desc)
                    print(fas(README))
                    print(desc)
                    input("Continue?")
            else:
                continue
            try:
                os.makedirs(path)
            except FileExistsError:
                pass
            with open(README, "wb") as f:
                f.write(desc.encode())
            for file in files:
                n = file.split("/")[-1].split("?")[0]
                if os.path.isfile(f"{path}/{n}"):
                    if DEBUG:
                        print(f"Skipping: {n}")
                    continue
                print(f"File: {n}")
                r = s.get(host + file, stream=True)
                if r.status_code == 200:
                    with open(f"{path}/{n}", "wb") as f:
                        r.raw.decode_content = True
                        shutil.copyfileobj(r.raw, f)
                else:
                    print(f"Error {r.status_code} while attempting to fetch {n}")
        if watch:
            print(f"Sleeping for {watch} seconds at {time.strftime('%F %T')}")
            time.sleep(watch)
except (IndexError, AssertionError):
    print("Usage: ctfd <host> <session> [--save=<directory>] [--watch=<seconds>] [--debug]")
    print("Example: ctfd https://fbctf.com 1234abcd-5e6f-a7b8-9c0d-ef1234567890")
    print("Note: --watch value must be 60 seconds or greater")
except Exception:
    if not DEBUG:
        exit("Error, could not retrieve challenges.")
    traceback.print_exc()
except (KeyboardInterrupt, EOFError):
    print()
