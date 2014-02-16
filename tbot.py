#!/usr/bin/python2.7

import socket
import sys
import os
import time
import random

#NOTE: This only works best with Python 2.7 as of current
#For !diabetes, !bestpony, !quote
#Start of functions.

def GetNick(data):     #get the nick
    nick = data.split('!')[0]
    nick = nick.replace(':', ' ')
    nick = nick.replace(' ', '')
    nick = nick.rstrip(' \t\n\r')
    return nick

def GetChannel(data):     #This is needed to work on multiple channels
	channel = data.split('#')[1]
	channel = channel.split(':')[0]
	channel = '#' + channel
	channel = channel.strip(' \t\n\r')
	return channel

def send(msg): #send to channel
    irc.send('PRIVMSG '+chan+' :'+msg+'\r\n')

def join(chan): #join a channel
    irc.send('JOIN '+chan+'\r\n')

def part(chan): #part a channel
    irc.send('PART '+chan+'\r\n')

def sendno(notice):  #send notice to nick
    irc.send('NOTICE '+nick+' :'+notice+'\r\n')

def kick(knick, reason):  #kick nick from channel
    irc.send('KICK '+chan+' '+knick+ ' :'+reason+'\r\n')

#end of functions

#settings

server = ''  #server address here
homechan = ''  #home channel to join
botnick = '' #bot's nick

print 'Attempting to connect to server..'

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #this is required to connect to irc
irc.connect((server, 6667))
irc.send('USER '+botnick+' '+botnick+' '+botnick+' :This is a fun bot!\n')
irc.send('NICK '+botnick+'\n')
join(homechan)

while True:    #This loops while the connection is active
   data = irc.recv ( 4096 )
   if data.find ( 'PING' ) != -1:
      irc.send ( 'PONG ' + data.split() [ 1 ] + '\r\n' )


   if data.find ( ':!test' ) != -1:
      chan = GetChannel(data)
      send('This works?')


   if data.find ( '!:bestpony' ) != -1:
      bestpone = random.choice(open('bestpony.txt', 'r').readlines())
      chan = GetChannel(data)
      send(bestpone)


   if data.find ( ':!hi' ) != -1:
      nick = GetNick(data)
      chan = GetChannel(data)
      irc.send('PRIVMSG '+chan+' :Hi there '+nick+' \r\n') 

   if data.find ( ':!diabetes' ) != -1:
      chan = GetChannel(data)
      diabet = random.choice(open('diabetes.txt', 'r').readlines())
      irc.send('PRIVMSG '+chan+' :'+diabet+'\r\n')

   if data.find ( ':!roulette' ) != -1:
      chan = GetChannel(data)
      nick = GetNick(data)
      roul = random.randint(1,7)
      if roul is 5:
         send('*boom*')
         kick(nick, 'Lost at roulette')
      elif roul is 7:
         send('Jammed')
      else:
         send('*click*')

   if data.find ( ':!quote' ) != -1:
      chan = GetChannel(data)
      nick = GetNick(data)
      quote = random.choice(open('quotes.txt', 'r').readlines())
      if chan in (''):  #Define one or more channels here
         send(quote)
      else:
         sendno('!quote is not allowed')
   
   if data.find ( ':!shutdown' ) != -1:
      nick = GetNick(data)
      if nick in (''):  #Define a nick or two here
         irc.send ('QUIT')
         sys.exit('Shutdown by owner')
      else:
         sendno('Permission Denied')
   print data
