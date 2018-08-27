'''
Input looks something like this:
MULTIPLY(ADD(MULTIPLY(MULTIPLY(MULTIPLY(DIVIDE(962 313) 163) 723) MULTIPLY(754 549)) MULTIPLY(ADD(594 MULTIPLY(82 ADD(390 DIVIDE(MULTIPLY(116 DIVIDE(ADD(ADD(DIVIDE(242 133) ADD(DIVIDE(130 DIVIDE(SUBTRACT(MULTIPLY(306 ADD(554 931)) 555) 345)) 57)) 299) 519)) 743)))) 351)) 753)
'''

from pwn import remote

MULTIPLY = lambda *x: eval("*".join(map(str, x)))
DIVIDE = lambda x, y: float(x) / y
SUBTRACT = lambda x,y: x-y
ADD = lambda x,y: x+y

while 1:
	raw_input("Press enter to continue...")
	r = remote("challs.zerodays.events", 20181)
	r.recvuntil("what is : ")
	data = r.recvuntil("\n").strip("\n?").replace(" ", ",")
	print data
	data = eval(data)
	r.sendline(str(data))
	a = r.recvline() + r.recvline()
	if "ZD2018{" in a:
		exit(a)