#!/usr/bin/env python3

import os, re
from sys import argv
from PyPDF2.utils import PdfReadError
from PyPDF2 import PdfFileWriter as Write, PdfFileReader as Read

usage = """PDFrip - Extract pages from PDF files
Usage: pdfrip <input> <pages> [output]
Examples:
 • pdfrip example.pdf 2,4,6,8,10 output.pdf
 • pdfrip example.pdf 1-10,11,13,19,22-25"""

def req(tmp):
    a = any(x in tmp for x in "-- ,, -, ,-".split())
    b = any(x in "-," for x in (tmp[0], tmp[-1]))
    c = re.search(r"[^0-9,-]", tmp)
    return a or b or c

def ranges(tmp):
    r = []
    for i in tmp.split(","):
        if "-" in i:
            MIN, MAX = map(int, i.split("-"))
            r.extend(range(MIN, MAX+1))
        else:
            r.append(int(i))
    return sorted(r)

def args():
    if req(argv[2]) or len(argv) not in (3, 4):
        exit(usage)
    if not os.path.isfile(argv[1]):
        exit("File not found.")
    return argv[1], ranges(argv[2]), argv[1::2][-1]

def main(name, pages, f_name):
    f_in = Read(name, "rb")
    f_out = Write()
    for i in pages:
        try:
            f_out.addPage(f_in.getPage(i-1))
        except IndexError:
            exit(f"Page {str(i)} not found.")
    with open(f_name, "wb") as f:
        f_out.write(f)
    print(f"Extracted {len(pages)} pages, written to file {f_name}")

if __name__ == "__main__":
    try:
        main(*args())
    except IndexError:
        print(usage)
    except PdfReadError:
        print("Input must be a PDF file.")
    except (KeyboardInterrupt, EOFError):
        print()
