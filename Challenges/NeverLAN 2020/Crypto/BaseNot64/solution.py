#!/usr/bin/env python3

import base64

enc = b"ORUGS43PNZSXG33ONR4TGMRBEEYSC==="
print(base64.b32decode(enc).decode())
