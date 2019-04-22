# Solution by Victor Azzam

A = list(map(chr, range(97, 123)))

for i in range(26):
	for x in range(len(A)):
		if x + i < 26:
			A[x], A[x+i] = A[x+i], A[x]

print("".join(A))