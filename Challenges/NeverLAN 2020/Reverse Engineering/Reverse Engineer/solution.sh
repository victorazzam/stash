#!/usr/bin/env bash

cat revseng | pwn disasm --no-color | grep 'c6 00' | tail -n +2 | head -20 | cut -d'x' -f3 | tr -d '\n' | xxd -r -p
echo
