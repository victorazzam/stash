#!/usr/bin/env python
#https://v0ids3curity.blogspot.ie/2013/06/boston-key-party-ctf-2013-crypto-200.html

# sudo pip install pycrypto
from Crypto.Cipher import AES
import sys

# ECB mode, each block of 16 bytes encrypted independently
plain_text = "54686520666c616720686173206265656e20656e63727970746564207477696365207573696e6720323536204145532d454342".decode('hex')[:16]
cipher_text = "FA96F12368B66345680ACF19B0B48878C1CD058250931A4858FDA5E3661964D0053144A9322A2EC1DC34C5688FA7BAA891630D2E04E8E80D3ECE29335E7D3311".decode('hex')[:16]
enc_message = "3F428788FA7D9B0F984859EA19E3CD093DFE5C35CB4CFA2AC2A5792A1E96FA2FB9CE18A882DF600449D0D51240979E2CF9E187ABD07963CFA781D48705D1E66E".decode('hex')

lookuptable = {}
prefix = '\x00' * 29

for i in range(256):
	sys.stdout.write("%d " % i)
	sys.stdout.flush()
	for j in range(256):
		for k in range(256):
			brute = chr(i) + chr(j) + chr(k)
			cipher = AES.new(prefix + brute, AES.MODE_ECB).encrypt(plain_text)
			lookuptable.update({cipher:prefix + brute})

print "Lookup table Generated!"

for x in range(256):
	for y in range(256):
		for z in range(256):
			brute = chr(x) + chr(y) + chr(z)
			cipher = AES.new(prefix + brute, AES.MODE_ECB).decrypt(cipher_text)
			if lookuptable.has_key(cipher):
				key1 = lookuptable[cipher]
				key2 = prefix + brute
				c1 = AES.new(key2, AES.MODE_ECB).decrypt(enc_message)
				print AES.new(key1, AES.MODE_ECB).decrypt(c1)
				sys.exit(0)