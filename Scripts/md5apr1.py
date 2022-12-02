from hashlib import md5

# Calculate md5-crypt apr1 (Apache variant)
# Format of htpasswd entries --> USER:$apr1$SALT$HASH
def calc(pwd, salt):
    pwd, salt = pwd.encode(), salt.encode()
    init = md5(pwd + salt + pwd).digest()
    apr1 = md5(pwd + b'$apr1$' + salt + (init * len(pwd))[:len(pwd)])
    for i in bin(len(pwd))[:1:-1]:
        apr1.update((pwd[:1], b'\0')[int(i)])
    perms = [pwd, pwd+pwd, pwd+salt, pwd+salt+pwd, salt+pwd, salt+pwd+pwd]
    offsets = tuple(zip((0,5,5,1,5,5,1,4,5,1,5,5,1,5,4,1,5,5,1,5,5), (3,1,3,2,1,3,3,1,3,3,0,3,3,1,3,3,1,2,3,1,3)))
    for i in range(24):
        for even, odd in offsets[:(17,22)[i<23]]:
            apr1 = md5(perms[odd] + md5(apr1.digest() + perms[even]).digest())
    out, chars = '', './0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    transpose = 12,6,0,13,7,1,14,8,2,15,9,3,5,10,4,11
    for i in (0,3,6,9,12):
        v = [apr1.digest()[transpose[i+x]] for x in (0,1,2)]
        for j in (v[0]&0x3f, (v[1]&0xf)<<2 | v[0]>>6, (v[2]&3)<<4 | v[1]>>4, v[2]>>2):
            out += chars[j]
    v = apr1.digest()[transpose[-1]]
    return out + chars[v & 0x3f] + chars[v >> 6]

if __name__ == '__main__':
    from sys import argv
    if len(argv) < 3:
        print(f'Usage: md5apr1 password salt [user=username]')
    else:
        user = ([''] + [x[5:] for x in argv if x[:5] == 'user='])[-1]
        salt = argv[2]
        result = calc(*argv[1:3])
        print(f'{user}:$apr1${salt}${result}' if user else result)
