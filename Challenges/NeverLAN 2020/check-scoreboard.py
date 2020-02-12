#!/usr/bin/env python3

import bs4, requests

try:
    r = requests.get("https://ctf.neverlanctf.com/scoreboard")
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    _, data = [x.text for x in soup.findAll("table", {"class": "table"})]
    a = data.replace(" ", "\0").split()
    print("Place   Team                               Points")
    print("-----   ----                               ------")
    for i in range(3, len(a), 3):
        place, team, points = a[i], a[i+1].replace("\0", " "), a[i+2]
        print(f"{place:>5}   {team:32}   {points:>6}")
except Exception as e:
    print(e)
