#!/usr/bin/python2.7

import socket
import sys
import os
import time
import random
import string
import filelist
import urllib2
from BeautifulSoup import BeautifulSoup
import settings
import datetime
import logging

logging.basicConfig(filename='TBot.log',level=logging.DEBUG)

#NOTE: This only works best with Python 2.7 as of current
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

def sendre(rchan, rmsg): #send to channel
    irc.send('PRIVMSG '+rchan+' :'+rmsg+'\r\n')

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
    irc.send('PRIVMSG '+chan+' :ACTION '+action+'\r\n')


def urlparse(url):
    soup = BeautifulSoup(urllib2.urlopen(url))
    title = 'URL: '+ soup.title.string
    return title

def BlackList(host):					# Return status 0/1
    blfile = open('blacklisted.txt', 'r')
    for line in blfile:
        if host in line:
            black = 1
	    return black
	else:
	    black = 0
	    return black

def Dice(side):
    side1 = int(side)
    die = str(random.randrange(1, side1))   #YOU MUST DIE
    return die
    

def restart_program():
    python = sys.excutable
    ox.execl(python, python, * sys.argv)

#end of functions

#settings


#some vars here

greetswitch = 0
silence = 0

print 'Attempting to connect to server..'

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #this is required to connect to irc
irc.connect((settings.server, 6667))
irc.send('NICK '+settings.botnick+'\n')
irc.send('USER '+settings.botnick+' '+settings.botnick+' '+settings.botnick+' :Insert bot here\n')

time.sleep(2)
irc.send('PRIVMSG NickServ :IDENTIFY '+settings.nspass+'\r\n')
join(settings.homechan)

while True:
   action = 'none'
   data = irc.recv ( 4096 )
   ts = time.time()
   st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
   print ('[' + st + ']' + data)
   logging.info('[' + st + ']' + data)
   
   if data.find ( 'PING' ) != -1:
      irc.send ( 'PONG ' + data.split() [ 1 ] + '\r\n' )

   if data.find ( 'JOIN :' ) != -1:
      if greetswitch == 1:
         nick = GetNick(data)
         chan = GetChannel(data)
         sendno('Hi there, ' + nick + ', and welcome to ' + chan)



#Action check

   if data.find('#') != -1:
      action = data.split('#')[0]
      action = action.split(' ')[1]

   if data.find('NICK') != -1:
      if data.find('#') == -1:
         action = 'NICK'


   if action != 'none':

      if action == 'PRIVMSG':
         if data.find('>') != -1:
            x = data.split('#')[1]
	    x = x.split('>')[1]
            info = x.split(' ', 1)
	    info[0] = info[0].strip(' \t\n\r')
            if len(info) > 1:

               cmd, args = info[0], info[1]

            else:

               cmd, args = info[0], " "
#Start of commands
	    host = GetHost(data)
	    nick = GetNick(data)
	    blist = BlackList(host)
	    if blist == 0:
	       if info[0] == 'hi':
	          nick = GetNick(data)
                  blist = BlackList(host)
	          if silence == 0:
	             chan = GetChannel(data)
	             send('Hi there, ' + nick)

               if info[0] == 'diabetes':
	          if silence == 0:
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
	          if silence == 0:
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
	          if silence == 0:
	             chan = GetChannel(data)
	             bestpone = random.choice(open('bestpony.txt', 'r').readlines())
	             send(bestpone)

	       if info[0] == 'sauce':
	          if silence == 0:
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
	          if silence == 0:
	             nick = GetNick(data)
	             chan = GetChannel(data)
	             shi = str(random.randint(1,8192))
	             if shi == 8192:
		        send('You got shiny!')
	             else:
		        send('Nope (' + shi + '/8192)')

	       if info[0] == 'shiny.info':
	          if silence == 0:
	             chan = GetChannel(data)
	             send('Chances of a shiny is 1 in 8192 (0.012207%)')

	       if info[0] == 'ping':
	          if silence == 0:
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


	       if info[0] == 'cycle':
	          host = GetHost(data)
	          status = readAdmin(host)
	          nick = GetNick(data)
	          if status == 1:
		     chan = GetChannel(data)
		     part(chan, 'Cycling channel..')
		     join(chan)
	          else:
		     sendno('Permission Denied (Your hostmask is not listed)')

	       if info[0] == 'say':
	          if silence == 0:
	             chan = GetChannel(data)
	             nick = GetNick(data)
	             send(args)

	       if info[0] == 'eval':
	          host = GetHost(data)
	          status = readAdmin(host)
	          nick = GetNick(data)
	          chan = GetChannel(data)
	          if status == 1:
		     try:
		        send(eval(args))
		     except NameError:
		        send('Nope(NameError)')
		     except SyntaxError:
		        send('Nope(SyntaxError)')
		     except TypeError:
		        send('Nope(SyntaxError)')
		     except:
		        send('Nope')
	          else:
		     sendno('Permission Denied (Your hostmask is not listed)')

	       if info[0] == 'google':
	          if silence == 0:
	             chan = GetChannel(data)
	             nick = GetNick(data)
	             searcharg = str(args.replace(" ", "+"))
	             searchlink = "http://www.google.com/#q="+searcharg
	             send(searchlink)

	       if info[0] == 'calc':
	          if silence == 0:
	             chan = GetChannel(data)
	             send('This command is not safe to use')

	       if info[0] == 'tempconv.cf':
	          if silence == 0:
	             chan = GetChannel(data)
	             try:
	                con = int(info[1]) * 1.8
	                conv = str(eval(str(con + 32)))
	                send(conv)
	             except:
		        send("You're doing it wrong")

	       if info[0] == 'quote.add':
	          nick = GetNick(data)
	          host = GetHost(data)
	          status = readAdmin(host)
	          if status == 1:
		     try:
		        filelist.write('quotes.txt', args)
		     except:
		        sendno('Nothing.')

	       if info[0] == 'silence.on':
	          host = GetHost(data)
	          status = readAdmin(host)
	          nick = GetNick(data)
	          if status == 1:
	             silence = 1
	             sendno('Bot is now silenced')
	          else:
		     sendno('Permission Denied')

	       if info[0] == 'silence.off':
	          host = GetHost(data)
	          status = readAdmin(host)
	          nick = GetNick(data)
	          if status == 1:
	             silence = 0
	             sendno('Silence disabled')
	          else:
		     sendno('Permission Denied (Your hostmask is not listed)')

	       if info[0] == 'send.msg':
	          host = GetHost(data)
	          status = readAdmin(host)
	          nick = GetNick(data)
	          if status == 1:
		     irc.send('PRIVMSG ' + args + '\r\n')
	          else:
		     sendno('Permission Denied (Your hostmask is not listed)')

	       if info[0] == 'forceidentify':
	          nick = GetNick(data)
	          host = GetHost(data)
	          status = readAdmin(host)
	          if status == 1:
		     irc.send('PRIVMSG NickServ :IDENTIFY '+settings.nspass+'\r\n')
	          else:
		     sendno('Permission Denied (Your hostmask is not listed)')

	       if info[0] == 'act':
	          if silence == 0:
	             chan = GetChannel(data)
	             nick = GetNick(data)
	             act(args)

	       if info[0] == 'hug':
	          if silence == 0:
	             chan = GetChannel(data)
		     nick = GetNick(data)
		     act('hugs ' + nick)

	       if info[0] == 'mode':
	          nick = GetNick(data)
	          host = GetHost(data)
	          chan = GetChannel(data)
	          status = readAdmin(host)
	          if status == 1:
		     irc.send('MODE '+chan+' '+args+'\r\n')
	          else:
		     sendno('Permission Denied (Your hostmask is not listed)')

	       if info[0] == 'bl.check':
	          nick = GetNick(data)
	          host = GetHost(data)
	          chan = GetChannel(data)
	          blist = BlackList(host)
	          if blist == 0:
		     sendno("You ain't blacklisted, yo")
	          else:
		     sendno("You're blacklisted")

	       if info[0] == 'dice':
	          if silence == 0:
	             nick = GetNick(data)
	             chan = GetChannel(data)
	             num = info[1]
	             try:
		        number = int(num)
		        thingy = str(random.randrange(1, number))
		        send(thingy)
	             except:
		        send("You're doing it wrong")

	       if info[0] == 'url.title':
		  if silence == 0:
		     try:
		        chan = GetChannel(data)
		        urltitle = urlparse(args)
		        send(urltitle)
		     except:
			send('URL be broken?')


	       if info[0] == 'remote.say':
	          host = GetHost(data)
	          chan = GetChannel(data)
	          status = readAdmin(host)
		  if status == 1:
		     irc.send('PRIVMSG '+args+'\r\n')
		  else:
		     sendno("Permission Denied (Your hostmask is not listed)")

	       if info[0] == 'exec':
	          host = GetHost(data)
	          status = readAdmin(host)
	          nick = GetNick(data)
	          chan = GetChannel(data)
	          if status == 1:
		     try:
		        exec args
		     except:
		        send('No work')
	          else:
		     sendno('Permission Denied (Your hostmask is not listed)')

	       if info[0] == 'restart':
	          host = GetHost(data)
	          status = readAdmin(host)
	          nick = GetNick(data)
	          if status == 1:
	             quit('Restart by owner')
		     os.execl('./tbot.py', '1')
	          else:
		     sendno('Permission Denied (Your hostmask is not listed)')

	       if info[0] == 'hitme':
		  chan = GetChannel(data)
		  nick = GetNick(data)
                  rand = ['pony', 'derp', 'banhammer', 'bat', 'random object']
		  act('hits ' + nick + ' with a ' +random.choice(rand))

	       if info[0] == 'roll.2':
		  chan = GetChannel(data)
		  di1 = str(random.randrange(0, 9))
		  di2 = str(random.randrange(0, 9))
		  dic = eval(str(di1 + di2))
		  send('You rolled: ' + di1 +' '+ di2)

	       if info[0] == 'roll.3':
		  chan = GetChannel(data)
		  di1 = str(random.randrange(0, 9))
		  di2 = str(random.randrange(0, 9))
		  di3 = str(random.randrange(0, 9))
		  send('You rolled: ' + di1 +' '+ di2 +' '+ di3)

	       if info[0] == 'pokedex':
	          if silence == 0:
	             chan = GetChannel(data)
	             nick = GetNick(data)
		     num = info[1]
	             link = "http://www.psypokes.com/dex/psydex/"+num
	             send(link)

	       if info[0] == 'flipcoin':
		  chan = GetChannel(data)
                  rand = ['Heads', 'Tails']
		  send(random.choice(rand))

	       if info[0] == '8-ball':
		  chan = GetChannel(data)
                  rand = ['Yes', 'No', 'Outlook so so', 'Absolutely', 'My sources say no', 'Yes definitely', 'Very doubtful', 'Most likely', 'Forget about it', 'Are you kidding?', 'Go for it', 'Not now', 'Looking good', 'Who knows', 'A definite yes', 'You will have to wait', 'Yes, in my due time', 'I have my doubts']
		  send(random.choice(rand))
	    else:
	       sendno("You're blacklisted, sorry")
