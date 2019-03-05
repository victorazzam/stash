#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# A peer-to-peer game of Battleships because who doesn't like a bit of P2P gaming? Enjoy :D
#
# First edit: November 18th 2015
# Last edit: May 16th 2018
# Author: Victor Azzam

import socket
import readline
import threading
from os import system
from time import sleep
from random import randint
from sys import exit, stdout

"""
      *********************
     ** BATTLESHIP GAME **
    *********************

                            |
      A B C D E F G H I J   |   A B C D E F G H I J
    ┌─────────────────────┐ | ┌─────────────────────┐
  1 │ o o o o o o o o o o │ | │ o o o o o o o o o o │ 1
  2 │ o o o o o o o o o o │ | │ o o o o o o o o o o │ 2
  3 │ o o o o o o o o o o │ | │ o o o o o o o o o o │ 3
  4 │ o o o o o o o o o o │ | │ o o o o o o o o o o │ 4
  5 │ o o o o o o o o o o │ | │ o o o o o o o o o o │ 5
  6 │ o o o o o o o o o o │ | │ o o o o o o o o o o │ 6
  7 │ o o o o o o o o o o │ | │ o o o o o o o o o o │ 7
  8 │ o o o o o o o o o o │ | │ o o o o o o o o o o │ 8
  9 │ o o o o o o o o o o │ | │ o o o o o o o o o o │ 9
 10 │ o o o o o o o o o o │ | │ o o o o o o o o o o │ 10
    └─────────────────────┘ | └─────────────────────┘
              You           |          Enemy
"""

cols = "a b c d e f g h i j".split()
DATA = ""

class Player(object):
	"""
	Defines each player in the game
	and initiates the playing board
	"""
	def __init__(self):
		self.win = 0
		self.guesses = []
		self.board = []
		self.enemy = [list("oooooooooo")] * 10
		self.enemy_name = "" # Enemy name
		self.enip = "" # Enemy IP

	def setup(self):
		clear()
		print "Let's set things up!"
		self.board = player_board()
		self.name = raw_input("Enter your name: ")[:16].strip()
		if not self.name: self.name = "Player 1"
		self.enemy_name = raw_input("Enter your friend's name: ")[:16].strip()
		if not self.enemy_name: self.enemy_name = "Player 2"
		self.enip = raw_input("Enter your friend's IP address: ").strip()

def player_board():
	try:
		with open("board.txt") as f:
			board = [x.replace(" ", "").strip() for x in f if x.strip()]
		if any(len(x) != 10 for x in board) or len(board) != 10:
			close("Your board must be a 10x10 grid (spaces are ignored).")
		col = ["".join(x[i] for x in board) for i in range(10)]
		B = "".join(board + col)
		if B.count("#") == 34 and all(x in B for x in "## ### #### #####".split()):
			return board
		close("Your board must contain 5 ships of sizes 2 3 4 5 and a size 3 submarine.\nUnits are represented with a # symbol.")
	except IOError:
		close("Missing file: board.txt")

def close(reason = "\nCould not connect to friend's IP, maybe the port is busy!\n"):
	clear()
	exit(reason)

def clear():
	system("cls||clear")

def Bind_UDP(port):
	global sock2, DATA
	sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock2.bind(('0.0.0.0', port))
	while 1:
		data, addr = sock2.recvfrom(16)
		if data: DATA = data

def connect(IP, port):
	turn = 0
	dice = randint(100000, 1000000)
	for i in range(5):
		try:
			print "\rTrying to connect...",
			stdout.flush()
			sleep(2) # Give time for other player to connect
			s.connect((IP, port))
			break
		except socket.error, e:
#			print str(e)         ##### DEBUGGING #####
			if i == 4: close() # Deal with closed port
	s.send("-STARTUP-%d-" % dice)
	while not DATA: continue
	if dice > int(DATA.split("-")[2]): turn = 1
	return turn

def main():
	global DATA, s, game_started

	game_started = 0

	# Setup the player
	you = Player()
	you.setup()

	# Setup the connection
	IP = you.enip
	port = 9835
	listen = threading.Thread(target=Bind_UDP, args=(port,)) # Bind in a separate thread
	listen.setDaemon(True) # Exit when script ends
	listen.start()
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	turn = connect(IP, port)

	# Setup the game
	msg = "You're starting first!" if turn else you.enemy_name + " is starting first."

	# Let the games begin!
	DATA = ""
	while not you.win:
		clear()
		game_started = 1
		temp = tuple(" ".join(i) for x in zip(you.board, you.enemy) for i in x)
		print """
      *********************
     ** BATTLESHIP GAME **    Welcome, {}!
    *********************

                            |
      A B C D E F G H I J   |   A B C D E F G H I J
    ┌─────────────────────┐ | ┌─────────────────────┐
  1 │ {} │ | │ {} │ 1
  2 │ {} │ | │ {} │ 2
  3 │ {} │ | │ {} │ 3
  4 │ {} │ | │ {} │ 4
  5 │ {} │ | │ {} │ 5
  6 │ {} │ | │ {} │ 6
  7 │ {} │ | │ {} │ 7
  8 │ {} │ | │ {} │ 8
  9 │ {} │ | │ {} │ 9
 10 │ {} │ | │ {} │ 10
    └─────────────────────┘ | └─────────────────────┘
              You           |          {}

    {}
""".format(you.name, *(temp + (you.enemy_name, msg)))

		if turn:
			guess = raw_input("Fire: ").strip().lower().split()
			if "DISCONNECT" in DATA: return "\n    %s has left the game\n" % you.enemy_name
			if not guess: continue
			if not (guess[0] in map(str, range(1,11)) and guess[1] in cols and len(guess[0]) in (1,2)):
				msg = "Guess must be in the format \"ROW COLUMN\" (without quotes). For example: 8 F"
				continue
			row = int(guess[0]) - 1
			col = cols.index(guess[1])
			if (row, col) in you.guesses:
				msg = "You already made that guess!"
				continue

			# Send guess
			try:
				s.send("-GUESS-%d-%d-12345" % (row, col))
			except socket.error:
				s.close()
				close("\nThere was a problem while sending your guess.\n")
			while not DATA: continue
			if "-HIT-" in DATA:
				you.enemy[row][col] = "x" # Enemy unit hit
				you.win = "-WIN-" in DATA
			elif "-MISS-" in DATA:
				you.enemy[row][col] = "ø" # Miss
			you.guesses.append((row, col))

		else:
			print "Awaiting %s's missile..." % you.enemy_name
			while not DATA: continue
			if "DISCONNECT" in DATA: return "\n    %s has left the game\n" % you.enemy_name

			# Receive guess
			_win = "-HIT-123456-WIN-"
			row, col = map(int, DATA.split("-")[2:4])
			if you.board[row][col] == "#":
				you.board[row][col] = "x"
				_send = "-HIT-1234567890-" if "#" in str(you.board) else _win
				s.send(_send)
				if _send == _win:
					s.close()
					close("\n:( You lost, better luck next time!\n")
			else:
				you.board[row][col] = "ø"
				s.send("-MISS-1234567890")

		turn = not turn
		DATA = msg = ""

	s.close()
	close("\nYou win!\n")

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		if game_started:
			s.send("-DISCONNECT-GAME-")
			s.close()
		exit("\n\nDisconnected\n")