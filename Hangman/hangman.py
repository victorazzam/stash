#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# I was bored :P
# Author: Victor Azzam

import random
import urllib2
import readline
from sys import argv, exit
from os import name, system

clear = "cls" if name == "nt" else "clear;clear"

usage = """
Hangman

Usage:  python hangman.py [options]

Option        Description
------        -----------
--easy        easy mode (guessing whole words won't add to previous attempts)
--hard        hard mode (disables consecutive vowel guesses)
--risk        risk mode (hard + guessing whole words incorrectly is game over)
--theme=?     word/phrase theme (default: english)

Theme         Description              a-z A-Z  0-9  space  symbols
-----         -----------              -------  ---  -----  -------
english       english words               ✔︎      ✘     ✘       ✘
movies        movie titles                ✔︎      ✔︎     ✔︎       ✔︎
passwords     most common passwords       ✔︎      ✔︎     ✘       ✔︎
"""

logo = """
 |__| |‾‾| |\ | |‾‾  |\/| |‾‾| |\ |
 |  | |‾‾| | \| |__| |  | |‾‾| | \|"""

figs = """
\n\n\n\n
 ──┴──:
\n   │\n   │\n   │\n   │\n ──┴──:
   ┌───\n   │\n   │\n   │\n   │\n ──┴──:
   ┌─────┐\n   │\n   │\n   │\n   │\n ──┴──:
   ┌─────┐\n   │     O\n   │\n   │\n   │\n ──┴──:
   ┌─────┐\n   │     O\n   │     │\n   │\n   │\n ──┴──:
   ┌─────┐\n   │     O\n   │     │\n   │     ;\n   │\n ──┴──:
   ┌─────┐\n   │     O\n   │    /│\n   │     ;\n   │\n ──┴──:
   ┌─────┐\n   │     O\n   │    /│\\\n   │     ;\n   │\n ──┴──:
   ┌─────┐\n   │     O\n   │    /│\\\n   │     ;\n   │    /\n ──┴──:
   ┌─────┐
   │\033[91m     0\033[0m
   │\033[91m    /│\\\033[0m
   │\033[91m     ;\033[0m
   │\033[91m    / \\\033[0m
 ──┴──""".split(":")

planB = {
		"english": ('Awkward', 'Bagpipes', 'Banjo', 'Bungler', 'Croquet', 'Crypt', 'Dwarves', 'Fervid', 'Fishhook', 'Fjord', 'Gazebo', 'Gypsy', 'Haiku', 'Haphazard', 'Hyphen', 'Ivory', 'Jazzy', 'Jiffy', 'Jinx', 'Jukebox', 'Kayak', 'Kiosk', 'Klutz', 'Memento', 'Mystify', 'Numbskull', 'Ostracize', 'Oxygen', 'Pajama', 'Phlegm', 'Pixel', 'Polka', 'Quad', 'Quip', 'Rhythmic', 'Rogue', 'Sphinx', 'Squawk', 'Swivel', 'Toady', 'Twelfth', 'Unzip', 'Waxy', 'Wildebeest', 'Yacht', 'Zealous', 'Zigzag', 'Zippy', 'Zombie'),
		"movies": ('Star Wars: Episode VII - The Force Awakens', 'Avatar', 'Titanic', 'Jurassic World', "Marvel's The Avengers", 'The Dark Knight', 'Rogue One: A Star Wars Story', 'Beauty and the Beast', 'Finding Dory', 'Star Wars: Episode I - The Phantom Menace', 'Star Wars: Episode IV - A New Hope', 'Avengers: Age of Ultron', 'The Dark Knight Rises', 'Shrek 2', 'E. T. The Extra-Terrestrial', 'The Hunger Games: Catching Fire', "Pirates of the Caribbean: Dead Man's Chest", 'The Lion King', 'Toy Story 3', 'Wonder Woman', 'Iron Man 3', 'Captain America: Civil War', 'The Hunger Games', 'Spider-Man', 'Jurassic Park', 'Transformers: Revenge of the Fallen', 'Frozen', 'Guardians of the Galaxy Vol. 2', 'Harry Potter and the Deathly Hallows, Part 2', 'Finding Nemo', 'Star Wars: Episode III - Revenge of the Sith', 'The Lord of the Rings: The Return of the King', 'Spider-Man 2', 'The Passion of the Christ', 'The Secret Life of Pets', 'Despicable Me 2', 'The Jungle Book', 'Deadpool', 'Inside Out', 'Furious 7', 'Transformers: Dark of the Moon', 'American Sniper', 'The Lord of the Rings: The Two Towers', 'Zootopia', 'The Hunger Games: Mockingjay - Part 1', 'Spider-Man 3', 'Minions', 'Alice in Wonderland', 'Spider-Man: Homecoming', 'Guardians of the Galaxy'),
		"passwords": ('123456', 'password', '12345678', 'qwerty', '123456789', '12345', '1234', '111111', '1234567', 'dragon', '123123', 'baseball', 'abc123', 'football', 'monkey', 'letmein', '696969', 'shadow', 'master', '666666', 'qwertyuiop', '123321', 'mustang', '1234567890', 'michael', '654321', 'pussy', 'superman', '1qaz2wsx', '7777777', 'fuckyou', '121212', '000000', 'qazwsx', '123qwe', 'killer', 'trustno1', 'jordan', 'jennifer', 'zxcvbnm', 'asdfgh', 'hunter', 'buster', 'soccer', 'harley', 'batman', 'andrew', 'tigger', 'sunshine', 'iloveyou'),
		}

def pick():
	global mode
	mode = "lol"
	theme = "english"
	themes = ("english", "movies", "passwords")
	for i in argv:
		i = i.lower()
		if i in ("--easy", "--hard", "--risk"):
			mode = i[2:]
		elif i in ["--theme=" + x for x in themes]:
			theme = i.split("=")[1]
	try:
		url = "https://raw.githubusercontent.com/victorazzam/stash/master/Hangman/%s.txt" % theme
		words = urllib2.urlopen(url).read().split("\n")
		return random.choice(words)
	except (urllib2.URLError, urllib2.HTTPError):
		return random.choice(planB[theme])

def die(word):
	return "%s\n%s\n\n Hangman died, what a shame!\n Correct word: %s\n" % (logo, figs[-1], word)

def win():
	return """%s

 \033[96m┌──────────────────┐
 │ Congratulations! │
 └─────\033[93m•\033[96m──────\033[93m•\033[96m─────┘\033[93m
        \\_ツ_/
          ||
          ||
         /‾‾\\
        /    \\\033[0m
""" % logo

def main():
	again = "yes"
	while again in "yes yea ye ya y".split():
		word = pick()
		w = [("_" if x.isalnum() else x) for x in word]
		incorrect = 0
		guesses = []
		error = ""
		err1, err2 = ("\033[1;4;91m", "\033[0m") if name != "nt" else ("", "")
		while 1:
			if w == list(word):
				winlose = 1
				break
			system(clear)
			print logo
			print figs[incorrect]
			print "\n Word: " + " ".join(w)
			print "\n Guesses: " + ", ".join(guesses)
			if error: print "\n %sError: %s%s" % (err1, error, err2)
			choice = raw_input("\n Choice: ").lower().strip()
			if choice in guesses + [""]:
				continue
			if choice in (word.lower(), filter(str.isalnum, word.lower())):
				winlose = 1
				break
			if len(choice) == len(word):
				if mode == "easy":
					continue
				elif mode == "risk":
					winlose = 0
					break
			if mode in ("hard", "risk") and guesses and guesses[-1] in list("aeiou"):
				if choice in list("aeiou"):
					error = "cannot consecutively use vowels in %s mode!" % mode
					continue
			if choice in word.lower() and len(choice) == 1:
				indices = [i for i, x in enumerate(word) if x.lower() == choice]
				for i in indices:
					w[i] = word[i]
			else:
				incorrect += 1
			if incorrect == len(figs) - 1:
				winlose = 0
				break
			guesses.append(choice)
			error = ""
		system(clear)
		print win() if winlose else die(word)
		again = raw_input(" Play again? ").lower().strip()
	print "\n Thanks for playing hangman!\n"

if __name__ == '__main__':
	try:
		if "-h" in argv or "--help" in argv:
			exit(usage)
		exit(main())
	except (KeyboardInterrupt, EOFError):
		exit("")
