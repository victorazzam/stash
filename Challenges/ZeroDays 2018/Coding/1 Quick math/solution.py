'''
Input looks something like this:
11840194 + 32059184 - 27841583
'''

from pwn import remote

raw_input("Press enter to continue...")
r = remote("challs.zerodays.events", 20181)
r.recvuntil("what is : ")
data = r.recvuntil("\n").strip("\n?")
print data
data = eval(data)
r.sendline(str(data))
a = ""
while 1:
	a += r.recvline()
	if "ZD2018{" in a:
		exit(a)