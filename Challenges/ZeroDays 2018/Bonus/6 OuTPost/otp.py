#!/usr/bin/python
#
# Straddling checkerboard implementation
# Author: Victor Azzam

from sys import stdout as s

# Used in the checkerboard, length must be 10 with 2 spaces
word = " ZERO DAYS"

word = list("{:10}".format(word.upper()))
tmp = [chr(x) for x in range(65, 91) if chr(x) not in word]
one, two = [" "] + tmp[:9], [" "] + tmp[9:]
board = [word, one, two]

# Position of empty (space) chars in the word
mt = list(filter(lambda x: word[x] == " ", range(10)))

# Prepare a printed version of the checkerboard
display = [[""] + list("0123456789"), [" "] + word, [str(mt[0])] + one, [str(mt[1])] + two]

a = "66475 19274 92028 78494 24146 68542 17507 39398 32348 59378 70636".replace(" ", "") # MP3
b = "92083 41866 05027 32206 36769 12418 56909 16718 63762 61762 33471".replace(" ", "") # Given

# Get each (a + b) mod 10
# Also some OTP requirements
n = [(int(x) + int(y)) % 10 for x, y in zip(a, b)]
t = []
tmp = ""
for i in n:
	if tmp:
		t += [tmp + str(i)]
		tmp = ""
		continue
	if not tmp and i in mt:
		tmp += str(i)
		continue
	if not i: continue
	t += [str(i)]
t = " ".join(t)

# Print the checkerboard
print "\n\033[7m",
print "\n".join(" {} ".format(" ".join(x)) for x in display)
print "\033[0m\n" + t + "\n"

for i in t.split():
	if int(i[0]) in mt:
		pre = (i[0] != str(mt[0])) + 1
		s.write(board[pre][int(i[1])])
	else:
		s.write(board[0][int(i)])

print "\n"