#!/usr/bin/env python3

import os, sys, json, time, shutil, urllib3, requests, hashlib, traceback

urllib3.disable_warnings(category=urllib3.exceptions.InsecureRequestWarning)

fab = lambda x: open(x, "rb").read()
fas = lambda f: "".join(map(chr, fab(f)))
safe = lambda x: "".join(i for i in x if i.isalnum() or i in " /-_.,()$")
hash = lambda x: hashlib.sha256(x if type(x) == bytes else x.encode()).hexdigest()

def dump(data, n=None):
    print("\nSHA256:", hash(data))
    for i in range(0, n or len(data), 16):
        hexed = " ".join(f"{ord(x):02x}" for x in data[i:i+16])
        rep = "".join((".", x)[31 < ord(x) < 127] for x in data[i:i+16])
        print(f"{i:08x}  {hexed[:23]:23}  {hexed[24:]:23}  |{rep:16}|")

try:
    DEBUG = "--debug" in sys.argv
    watch = ([0] + [int(x[8:]) for x in sys.argv if x[:8] == "--watch=" and x[8:].isdigit() and int(x[8:]) > 59])[-1]
    host = "/".join(sys.argv[1].split("/", 3)[:3])
    assert host.startswith(("http://", "https://"))

    save = host.lstrip("htps:")[2:]
    for arg in sys.argv:
        if arg.startswith("--save=") and len(arg) > 7:
            directory = arg[7:]
            if os.path.isfile(directory):
                print(f"File {directory} must be a directory. Skipping...")
            else:
                save = directory
    save.rstrip("/")
    if not os.path.isdir(save):
        os.makedirs(save)
    storage = safe(f"{save}/challenges.json")

    s = requests.Session()
    s.verify = False
    s.cookies.set("session", sys.argv[2])
    s.headers["User-Agent"] = "Mozilla/5.0"

    for count in range(1000000 * watch + 1):
        try:
            challs = s.get(f"{host}/api/v1/challenges").json()["data"]
            if os.path.isfile(storage) and json.load(open(storage)) == challs:
                if DEBUG:
                    print("Stored challenge list matches remote list")
                raise IOError
            with open(storage, "w") as f:
                json.dump(challs, f)
        except IOError:
            pass
        except (KeyError, json.decoder.JSONDecodeError):
            print(f"Error, while attempting to get challege data")
        else:
            for cid in sorted(chall["id"] for chall in challs):
                if DEBUG:
                    print(f"Fetching challenge id {cid}", end="\r", flush=True)
                try:
                    chall = s.get(f"{host}/api/v1/challenges/{cid}").json()["data"]
                except (KeyError, json.decoder.JSONDecodeError):
                    print(f"Error, while attempting to get challege data")
                    break
                chall.pop("type")
                locals().update(chall) # category name description connection_info hints files
                desc = [description.replace("\r", "").strip()] if description else []
                desc += [connection_info.replace("\r", "").strip()] if connection_info else []
                path = safe(f"{save}/{category.replace('/', '-').strip()}/{name.replace('/', '-').strip()}")
                for y, i in enumerate(hints):
                    if i["cost"] == 0:
                        try:
                            r = s.get(f"{host}/api/v1/hints/{i['id']}").json()["data"]["content"].strip()
                            desc.append(f"Hint {y+1:2}\n-------\n{r}")
                        except (KeyError, json.decoder.JSONDecodeError):
                            print("Error, while attempting to get hint")
                README = f"{path}/README.txt"
                desc = "\n\n".join(desc)
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
                    os.makedirs(safe(path), exist_ok=True)
                except FileExistsError:
                    pass
                with open(README, "w") as f:
                    f.write(desc)
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
            if DEBUG and count:
                print(f"Runs completed: {count}")
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
