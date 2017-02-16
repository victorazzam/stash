#!/usr/bin/python
#
# Finds the private key from its public counterpart.
# Mostly taken from SE and 0day.work and tons of reading.
# Plz don't use 1024-bit keys, point proven below ;)
#
# Written in hisSSSssSSsSSsssSsSsSSS
# Author: Victor Azzam

import os
import base64
import pyasn1.type.univ
import pyasn1.codec.der.encoder
from random import randint
from sys import argv, exit
from bs4 import BeautifulSoup
from urllib2 import Request, urlopen, URLError

def Args():
    if len(argv) != 2:
        print "Specify the public key file!"
        exit(1)
    if not os.path.isfile(argv[1]):
        print "No such file!"
        exit(1)
    try:
        if "PUBLIC" not in open(argv[1], 'r').read().strip()[0:20]:
            print "File not valid!"
            exit(1)
    except IOError:
        print "Cannot read file!"
        exit(1)

def Modulus():
    global e, n # Make hex exponent and hex modulus usable
    stdout = os.popen("openssl rsa -pubin -in %s -modulus -text" % argv[1]).read() # General output
    e = int(stdout.split("Exponent")[1].split("\n")[0][-8:-1], 16) # Exponent in hex form
    tmp = stdout.split("Exponent")[0].split("Modulus:\n")[1]
    n = int("0x" + "".join([x.strip() for x in tmp.split("\n")]).replace(":", ""), 16) # Modulus in hex form
    return str(int(stdout.split("Modulus=")[1].split("\n")[0].lower(), 16)) # Modulus decimal

def Primes(modulus):
    try:
        a = Request("http://factordb.com/index.php?query=" + modulus)
        a = str(BeautifulSoup(urlopen(a).read(), 'html.parser')).split('id="moreinfo"')[0]
        a = [x.split('"')[0] for x in a.split("index.php?id=")[2:]]
        primes = []
        for i in a:
            b = Request("http://factordb.com/index.php?showid=" + i)
            b = str(BeautifulSoup(urlopen(b).read(), 'html.parser')).split("Number</td>")[1].split("</td>")[0]
            primes.append("".join([x for x in b if x.isdigit()]))
        return map(int, primes)
    except URLError:
        print "Error while retrieving primes, check your internet connection."
        exit(1)

def main():
    Args()                                      # Make sure input is valid
    modulus = Modulus()                         # Get modulus as decimal & hex, and get exponent
    p, q = Primes(modulus)                      # Find primes using factordb.com
    phi = (p-1) * (q-1)                         # Calculate phi(n)
    d = modinv(e, phi)                          # Calculate modular inverse of phi(n)
    dp = modinv(e, p-1)
    dq = modinv(e, q-1)
    qi = modinv(q, p)
    key = pempriv(n, e, d, p, q, dp, dq, qi)    # Get the key
    try:
        tofile(key)                             # Write to a KEY file
    except IOError:
        print "Could not write the key to a file, check your permissions and try again."
        print "Key file contents:\n" + key

# Modular inverse
# Part 1
def modinv(a, m):
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None
    else:
        return x % m

# Part 2
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

# Convert to PEM cert
def pempriv(n, e, d, p, q, dP, dQ, qInv):
    template = '-----BEGIN RSA PRIVATE KEY-----\n{}-----END RSA PRIVATE KEY-----\n'
    seq = pyasn1.type.univ.Sequence()
    for x in [0, n, e, d, p, q, dP, dQ, qInv]:
        seq.setComponentByPosition(len(seq), pyasn1.type.univ.Integer(x))
    der = pyasn1.codec.der.encoder.encode(seq)
    return template.format(base64.encodestring(der).decode('ascii'))

def tofile(key):
    f = open("private_%d.key" % randint(1000,10000), "w")
    f.write(key)
    f.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print
    exit()
