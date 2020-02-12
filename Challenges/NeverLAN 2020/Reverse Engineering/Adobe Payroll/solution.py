#!/usr/bin/env python3

with open("Adobe_Payroll/Adobe_Employee_Payroll.exe", "rb") as f:
    a = f.read()
    b = b"\x04\x02\x1f"
    print("".join(chr(x[0]) for x in a.split(b)[1:]))
