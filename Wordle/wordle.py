import sys

if len(sys.argv) < 2:
    sys.exit('Usage: wordle /path/to/words.txt')

print('X+  X correct')
print('X-  X not present')
print('X?  X in wrong place')

with open(sys.argv[1]) as f:
    words = sorted(f.read().split(), key = lambda x: 1 - sum(map(x.count, 'aeiou')))

while len(words) > 1:
    word = input('Enter guess results: ').lower().strip()
    for i, (l, p) in enumerate(word.split()):
        if p == '+':
            words = [x for x in words if x[i] == l]
        elif p == '?':
            words = [x for x in words if x[i] != l and l in x]
        elif p == '-':
            words = [x for x in words if (x[i] != l if l+'+' in word or l+'?' in word else l not in x)]
    print(', '.join(words))

print('Final answer:', ', '.join(words))