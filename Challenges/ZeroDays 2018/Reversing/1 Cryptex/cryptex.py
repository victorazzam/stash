#!/usr/bin/env python

password_guess= raw_input("Enter Password: ")

if len(password_guess) != 14:
  print "Wrong Length"
  exit()


verify_code = [113, 220, 168, 206, 164, 220, 180, 236, 250, 73, 196, 228, 220, 244]
user_code = []

for char in password_guess:
  user_code.append( (((ord(char) << 2) | (ord(char) >> 5)) ^ 123) & 255 )

if (user_code == verify_code):
  print "Well Done the flag is ZD2018{"+password_guess+"}"
else:
  print "Incorrect"