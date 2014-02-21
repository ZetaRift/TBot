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

def readAdmin(host):						# Return status 0/1
	bestand = open('admins.txt', 'r')
	for line in bestand:
		if host in line:
			status = 1
			return status
		else:
			status = 0
			return status

def readChan(chan):
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
irc.send('USER '+botnick+' '+botnick+' '+botnick+' :Insert bot here\n')
irc.send('NICK '+botnick+'\n')
time.sleep(2)
join(homechan)

while True:
   action = 'none'
   data = irc.recv ( 4096 )
   print data
   
   if data.find ( 'PING' ) != -1:
      irc.send ( 'PONG ' + data.split() [ 1 ] + '\r\n' )

   if data.find ( ':VERSION' ) != -1:
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
         if data.find('$') != -1:
            x = data.split('#')[1]
	    x = x.split('$')[1]
            info = x.split(' ', 1)
	    info[0] = info[0].strip(' \t\n\r')
            if len(info) > 1:

               cmd, args = info[0], info[1]

            else:

               cmd, args = info[0], " "
#Start of commands

	    if info[0] == 'hi':
	       chan = GetChannel(data)
	       nick = GetNick(data)
	       send('Hi there, ' + nick)

            if info[0] == 'diabetes':
	       chan = GetChannel(data)
	       diabet = random.choice(open('diabetes.txt', 'r').readlines())
	       send(diabet)

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


	    if info[0] == 'cycle':
	       host = GetHost(data)
	       status = readAdmin(host)
	       nick = GetNick(data)
	       if status == 1:
		  chan = GetChannel(data)
		  part(chan, 'Cycling channel..')
		  time.sleep(1)  #Don't wanna flood the server >~>
		  join(chan)
	       else:
		  sendno('Permission Denied (Your hostmask is not listed)')

	    if info[0] == 'say':
	       chan = GetChannel(data)
	       nick = GetNick(data)
	       send(args)

	    if info[0] == 'debug.eval':
	       host = GetHost(data)
	       status = readAdmin(host)
	       nick = GetNick(data)
	       chan = GetChannel(data)
	       if status == 1:
		  try:
		     send(eval(args))
		  except:
		     send('Nope')
	       else:
		  sendno('Permission Denied (Your hostmask is not listed)')

	    if info[0] == 'google':
	       chan = GetChannel(data)
	       nick = GetNick(data)
	       searcharg = str(args.replace(" ", "+"))
	       searchlink = "http://www.lmgtfy.com/?q="+searcharg
	       send(searchlink)

	    if info[0] == 'calc':
	       chan = GetChannel(data)
	       send('This command is not safe to use')

	    if info[0] == 'tempconv.cf':
	       chan = GetChannel(data)
	       try:
	          con = int(info[1]) * 1.8
	          conv = str(eval(str(con + 32)))
	          send(conv)
	       except:
		  send("You're doing it wrong")
