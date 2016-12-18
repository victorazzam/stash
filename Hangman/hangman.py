#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# I was bored :P
# Author: Victor Azzam

import random
import urllib2
import readline
from os import system
from sys import platform, exit

clear = "clear;clear"
if platform.lower() in ["win", "cygwin"]:
    clear = "cls"

logo = """
 |__| |‾‾| |\ | |‾‾  |\/| |‾‾| |\ |
 |  | |‾‾| | \| |__| |  | |‾‾| | \|"""

figs = """
\n\n\n\n
 ──┴──:

   │
   │
   │
   │
 ──┴──:
   ┌─────┐
   │
   │
   │
   │
 ──┴──:
   ┌─────┐
   │     O
   │
   │
   │
 ──┴──:
   ┌─────┐
   │     O
   │     │
   │
   │
 ──┴──:
   ┌─────┐
   │     O
   │     │
   │     ;
   │
 ──┴──:
   ┌─────┐
   │     O
   │    /│\\
   │     ;
   │
 ──┴──:
   ┌─────┐
   │\033[91m     0\033[0m
   │\033[91m    /│\\\033[0m
   │\033[91m     ;\033[0m
   │\033[91m    / \\\033[0m
 ──┴──""".split(":")

def pick():
    try:
        url = "https://raw.githubusercontent.com/victorazzam/stash/master/Hangman/hangman.txt"
        words = urllib2.urlopen(url).read().split()
        return random.choice(words)
    except urllib2.URLError:
        return "hangman"

def die(word):
    system(clear)
    print logo
    print figs[-1]
    print "\n Hangman died, what a shame!\n Correct word: %s\n" % word

def win():
    system(clear)
    print logo
    print """
 \033[96m┌──────────────────┐
 │ Congratulations! │
 └─────\033[93m•\033[96m──────\033[93m•\033[96m─────┘\033[93m
        \\_ツ_/
          ||
          ||
         /‾‾\\
        /    \\\033[0m
"""

def main():
    again = "yes"
    while again in ["yes", "yea", "ye", "ya", "y"]:
        word = pick()
        w = ["_" for i in word]
        incorrect = 0
        winlose = 2
        guesses = []
        while 1:
            if w == list(word):
                winlose = 1
                break
            system(clear)
            print logo
            print figs[incorrect]
            print "\n Word: " + " ".join(w)
            print "\n Guesses: " + ", ".join(guesses)
            choice = raw_input("\n Choice: ").lower().strip()
            if choice in guesses + [""]:
                continue
            if choice == word:
                winlose = 1
                break
            if choice in word and len(choice) == 1:
                indices = [i for i, x in enumerate(word) if x == choice]
                for i in indices:
                    w[i] = word[i]
            else:
                incorrect += 1
            if incorrect == len(figs) - 1:
                winlose = 0
                break
            guesses.append(choice)
        if winlose == 0:
            die(word)
        else:
            win()
        again = "no"
        again = raw_input(" Play again? ").lower().strip()
    print "\n Thanks for playing hangman!\n"

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "\n"
    exit(1)
