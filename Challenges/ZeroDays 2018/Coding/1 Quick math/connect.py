#!/usr/bin/python  
## -----------------------------------------------------------------
## We noticed last few years that lots of students 
## struggle with connecting to sockets.
## So we've given you some simple sample code to get yoi started
## -----------------------------------------------------------------

## Use telnet library to connect to ZD server
import telnetlib
our_link = telnetlib.Telnet('challs.zerodays.events', 20181)

## Read all the welcome chat, up to the point we're intersted in
prelude = our_link.read_until('what is : ')

## Read everything until end of the question, could also be \n.
question = our_link.read_until('?')

## Print out what we've copied so we can check it.
print(question)

## do some calculates or whatever on the data
answer = 42

## send our response back to the ZD sever
our_link.write(str(answer)+"\n")

## might need to read any ore responses from server
our_link.close()



