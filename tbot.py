#!/usr/bin/python2.7

import socket
import sys
import os
import time
import random
import string

#NOTE: This only works best with Python 2.7 as of current
#In order for the bot to properly check the files in readAdmin and readChan, hostmasks and channels must be on the same
#line on the .txt files, seperated by a space. Eg: #somechannel #thischannel
#In order to add a command to return to a channel, a chan = GetChannel(data) must be defined in order for the bot to send to the target channel.
#Contact Crimson_Tail on irc network PonyChat for more info about this bot
#Will update this later with the core function changed slightly and a few more commands
#Start of functions.

def GetHost(host):
    host = host.split('@')[1]
    host = host.split(' ')[0]
    return host

def readAdmin(host):						#Reads a user's hostmask for staus 0/1
	bestand = open('admins.txt', 'r')
	for line in bestand:
		if host in line:
			status = 1
			return status
		else:
			status = 0
			return status

def readChan(chan):						#Checks if a channel is lsited on allowedchan.txt for some commands
	bestch = open('allowedchan.txt', 'r')
	for line in bestch:
		if chan in line:
			cstatus = 1
			return cstatus
		else:
			cstatus = 0
			return cstatus

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

def part(chan, pmsg): #part a channel
    irc.send('PART '+chan+' :'+pmsg+'\r\n')

def sendno(notice):  #send notice to nick
    irc.send('NOTICE '+nick+' :'+notice+'\r\n')

def kick(knick, reason):
    irc.send('KICK '+chan+' '+knick+ ' :'+reason+'\r\n')

def quit(qmsg):
    irc.send('QUIT :'+qmsg+'\r\n')

def act(action):
    irc.send('PRIVMSG '+chan+ ' \001ACTION :' +action+'\r\n')


    
#end of functions

#settings

server = 'irc.ponychat.net'  #server address here
homechan = '#pinchybot'  #home channel to join
botnick = 'Tbot' #bot's nick


#some vars here

greetswitch = 0

print 'Attempting to connect to server..'

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #this is required to connect to irc
irc.connect((server, 6667))
irc.send('USER '+botnick+' '+botnick+' '+botnick+' :This is a fun bot!\n')
irc.send('NICK '+botnick+'\n')
time.sleep(2)
join(homechan)

while True:
   action = 'none'
   data = irc.recv ( 4096 )
   print data
   
   if data.find ( 'PING' ) != -1:
      irc.send ( 'PONG ' + data.split() [ 1 ] + '\r\n' )

   if data.find ( ':VERSION' ) != -1:  #Pretty much dosen't work properly, returns a VERSION
      nick = GetNick(data)
      irc.send ( 'NOTICE '+nick+' :VERSION :None of your beeswax\r\n')

#Action check

   if data.find('#') != -1:
      action = data.split('#')[0]
      action = action.split(' ')[1]

   if data.find('NICK') != -1:
      if data.find('#') == -1:
         action = 'NICK'


   if action != 'none':

      if action == 'PRIVMSG':
         if data.find('$') != -1:  #'$' is the bot's command prefix
            x = data.split('#')[1]
	    x = x.split('$')[1]
            info = x.split(' ')
	    info[0] = info[0].strip(' \t\n\r')
#Start of commands

#	    if info[0] == 'hi':   #Example command
#	       chan = GetChannel(data)
#	       nick = GetNick(data)
#	       irc.send('PRIVMSG '+chan+' :Hi there, '+nick+ '\r\n')

            if info[0] == 'diabetes':
	       chan = GetChannel(data)
	       diabet = random.choice(open('diabetes.txt', 'r').readlines())
	       irc.send('PRIVMSG '+chan+' :'+diabet+'\r\n')

	    if info[0] == 'join':
	       host = GetHost(data)
	       status = readAdmin(host)
	       nick = GetNick(data)
	       if status == 1:
	          join('#' + info[1])
	       else:
		  sendno('Permission Denied (Your hostmask is not listed)')

	    if info[0] == 'shutdown':
	       host = GetHost(data)
	       status = readAdmin(host)
	       nick = GetNick(data)
	       if status == 1:
	          quit('Shutdown by owner')
		  sys.exit('Shutdown by owner')
	       else:
		  sendno('Permission Denied (Your hostmask is not listed)')

	    if info[0] == 'roulette':
	       nick = GetNick(data)
	       chan = GetChannel(data)
	       roul = random.randint(1,7)
	       if roul == 4:
		  send('*boom*')
		  kick(nick, 'Lost at roulette')
	       elif roul == 7:
		  send('Jammed')
	       else:
		  send('*click*')

	    if info[0] == 'bestpony':
	       chan = GetChannel(data)
	       bestpone = random.choice(open('bestpony.txt', 'r').readlines())
	       send(bestpone)

	    if info[0] == 'quote':
	       chan = GetChannel(data)
	       cstatus = readChan(chan)
	       nick = GetNick(data)
	       if cstatus == 1:
		  quote = random.choice(open('quotes.txt', 'r').readlines())
		  send(quote)
	       else:
		  sendno('Quote is not allowed on ' + chan)

	    if info[0] == 'sauce':
	       chan = GetChannel(data)
	       cstatus = readChan(chan)
	       nick = GetNick(data)
	       if cstatus == 1:
		  sauce = random.choice(open('sauce.txt', 'r').readlines())
		  send(sauce)
	       else:
		  sendno('Sauce is not allowed on ' + chan)

	    if info[0] == 'part':
	       host = GetHost(data)
	       status = readAdmin(host)
	       nick = GetNick(data)
	       chan = GetChannel(data)
	       if status == 1:
	          part(chan, 'Parted by owner')
	       else:
		  sendno('Permission Denied (Your hostmask is not listed)')

	    if info[0] == 'shiny':
	       nick = GetNick(data)
	       chan = GetChannel(data)
	       shi = str(random.randint(1,8192))
	       if shi == 8192:
		  send('You got shiny!')
	       else:
		  send('Nope (' + shi + '/8192)')

	    if info[0] == 'shiny.info':
	       chan = GetChannel(data)
	       send('Chances of a shiny is 1 in 8192 (0.012207%)')

	    if info[0] == 'ping':
	       chan = GetChannel(data)
	       send('Pong')

	    if info[0] == 'kick':
	       host = GetHost(data)
	       status = readAdmin(host)
	       nick = GetNick(data)
	       if status == 1:
		  kick(info[1], 'Kicked by bot owner')
	       else:
		  sendno('Permission Denied (Your hostmask is not listed)')


	    if info[0] == 'dice':
	       nick = GetNick(data)
	       chan = GetChannel(data)
	       num = info[1]
	       try:
		  number = int(num)
		  thingy = str(random.randrange(1, number))
		  send(thingy)
	       except:
		  send("You're doing it wrong")

 
