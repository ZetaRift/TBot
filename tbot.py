#!/usr/bin/bin/python2.7

import socket
import sys
import os
import time
import random
import string
import settings
import datetime
import logging
import goslate
from random import randint
import urllib2
import json
from xml.dom import minidom

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
    

def roll(sides, count):
    r1 = str([randint(1, sides) for i in range(count)])
    r2 = r1.strip("[]")
    return r2


def restart_program():
    python = sys.excutable
    ox.execl(python, python, * sys.argv)

def slate(tran, lang):
    gs = goslate.Goslate()
    tr = gs.translate(tran, lang)
    tr2 = tr.encode('utf8', 'ignore')
    trf = tr2.decode('utf8', 'ignore')
    return tr2


def derpi_img_score(num_id):    #Get score
    url = urllib2.urlopen('https://derpiboo.ru/'+num_id+'.json')
    jso = json.load(url)
    score = str(jso['score'])
    return score

def derpi_img_upvote(num_id):    #Get score
    url = urllib2.urlopen('https://derpiboo.ru/'+num_id+'.json')
    jso = json.load(url)
    upv = jso['upvotes']
    return upv

def derpi_img_downvote(num_id):    #Get score
    url = urllib2.urlopen('https://derpiboo.ru/'+num_id+'.json')
    jso = json.load(url)
    upd = jso['downvotes']
    return upd

def derpi_img_uled(num_id): #Who uploaded the image
    url = urllib2.urlopen('https://derpiboo.ru/'+num_id+'.json')
    jso = json.load(url)
    uploader = jso['uploader']
    return uploader

def derpi_img_tagged(num_id): #Tags on a image
    url = urllib2.urlopen('https://derpiboo.ru/'+num_id+'.json')
    jso = json.load(url)
    tags = jso['tags']
    return tags

def derpi_img_cmts(num_id):  #Comment count of image
    url = urllib2.urlopen('https://derpiboo.ru/'+num_id+'.json')
    jso = json.load(url)
    cmts = jso['comment_count']
    return cmts


def derpi_tagsearch(tag):
    ser1 = str(tag.replace(" ", "+"))
    url = urllib2.urlopen("https://derpiboo.ru/tags/"+ser1+".json")
    jso = json.load(url)
    img_count = jso['tag']['images']
    return img_count

def saysw(switch):
    if switch == 'on':
       echo = 0
    elif switch == 'mod':
       echo = 1
    elif switch == 'off':
       echo = 2
    else:
       syn = "Syntax: echo(on|mod|off)"
       return syn

def dexname(name):
    xmldoc = minidom.parse("dex_xml/"+name+'.xml')
    dexname = xmldoc.getElementsByTagName('dexname')
    num = xmldoc.getElementsByTagName('num')
    typ = xmldoc.getElementsByTagName('typ') 
    hp = xmldoc.getElementsByTagName('hp') 
    atk = xmldoc.getElementsByTagName('atk')
    defe = xmldoc.getElementsByTagName('def')
    spa = xmldoc.getElementsByTagName('spa')
    spd = xmldoc.getElementsByTagName('spd')
    spe = xmldoc.getElementsByTagName('spe')
    tot = xmldoc.getElementsByTagName('tot')
    name = dexname[0].attributes['name'].value
    num = num[0].attributes['name'].value
    typ = typ[0].attributes['name'].value
    hp = hp[0].attributes['name'].value
    atk = atk[0].attributes['name'].value
    defe = defe[0].attributes['name'].value
    spa = spa[0].attributes['name'].value
    spd = spd[0].attributes['name'].value
    spe = spe[0].attributes['name'].value
    tot = tot[0].attributes['name'].value
    res = "Name: "+str(name)+" | Dex No: "+str(num)+" | Type: "+str(typ)+" | Health: "+str(hp)+" | Attack: "+str(atk)+" | Defense: "+str(defe)+" | Special Atk: "+str(spa)+" | Special Def: "+str(spd)+" | Speed: "+str(spe)+" | Total: "+str(tot)
    return res

def tempconv(pfix, value):
    if pfix == 'cf':
       tmp = value * 1.8 + 32
       return str(float(tmp))
    elif pfix == 'fc':
       tmp = (value - 32) * 5 / 9
       return str(float(tmp))
    elif pfix == 'ck':
       tmp = value + 273.15
       return str(float(tmp))
    elif pfix == 'kc':
       tmp = value - 273.15
       return str(float(tmp))

#end of functions

#settings


#some vars here

greetswitch = 0
silence = 0
logsw = 0
echo = 0

print 'Attempting to connect to server..'

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #this is required to connect to irc
irc.connect((settings.server, 6667))
irc.send('NICK '+settings.botnick+'\n')
irc.send('USER '+settings.botnick+' '+settings.botnick+' '+settings.botnick+' :Insert bot here\n')

time.sleep(2)
irc.send('PRIVMSG NickServ :IDENTIFY '+settings.nspass+'\r\n')
join(settings.homechan)
parsedata = 1

while True:
   action = 'none'
   data = irc.recv ( 4096 )
   ts = time.time()
   st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
   print ('[' + st + ']' + data)
   if logsw == 1:
      logging.info('[' + st + '] ' + data)
   
   if data.find ( 'PING' ) != -1:
      irc.send ( 'PONG ' + data.split() [ 1 ] + '\r\n' )

   if data.find ( 'JOIN :' ) != -1:
      if greetswitch == 1:
         nick = GetNick(data)
         chan = GetChannel(data)
         sendno('Hi there, ' + nick + ', and welcome to ' + chan)

   if data.find ( ':VERSION' ) != -1:
      nick = GetNick(data)
      sendno("VERSION TBot 0.68")



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
	          if echo == 0:
	             chan = GetChannel(data)
	             nick = GetNick(data)
	             send(args)
                  elif echo == 1:
                     status = readAdmin(host)
                     if status == 1:
                        chan = GetChannel(data)
	                nick = GetNick(data)
	                send(args)
                     else:
                        nick = GetNick(data)
                        sendno("$say command is limited to bot admin")
		  elif echo == 2:
                     nick = GetNick(data)
                     sendno("$say command is disabled.")

	       if info[0] == 'eval':
	          host = GetHost(data)
	          status = readAdmin(host)
	          nick = GetNick(data)
	          chan = GetChannel(data)
	          if status == 1:
		     try:
		        send(eval(args))
		     except Exception as err:
		        send("Err: " + str(err))
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
	                con = int(float(info[1])) * 1.8 + 32
	                send(str(con))
	             except:
		        send("You're doing it wrong")

	       if info[0] == 'tempconv.ck':
	          if silence == 0:
	             chan = GetChannel(data)
	             try:
	                con = int(float(info[1])) + 273.15
	                send(str(con))
	             except:
		        send("You're doing it wrong")

	       if info[0] == 'tempconv.kc':
	          if silence == 0:
	             chan = GetChannel(data)
	             try:
	                con = int(float(info[1])) - 273.15
	                send(str(con))
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
		     logging.warning('Restart command was used, restarting script...')
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

	       if info[0] == 'log.on':
	          host = GetHost(data)
	          status = readAdmin(host)
	          nick = GetNick(data)
	          if status == 1:
	             logsw = 1
	             sendno('Bot is now logging to file')
	          else:
		     sendno('Permission Denied')

	       if info[0] == 'log.off':
	          host = GetHost(data)
	          status = readAdmin(host)
	          nick = GetNick(data)
	          if status == 1:
	             logsw = 0
	             sendno('Bot has stopped logging to file')
	          else:
		     sendno('Permission Denied')

               if info[0] == 'goslate.de':  #German
                  chan = GetChannel(data)
                  trans = slate(args, 'de')
                  send(trans)

               if info[0] == 'goslate.ru':  #Russian
                  chan = GetChannel(data)
                  trans = slate(args, 'ru')
                  send(trans)

               if info[0] == 'goslate.ja': #Japanese
                  chan = GetChannel(data)
                  trans = slate(args, 'ja')
                  send(trans)

               if info[0] == 'goslate.fi':  #Finnish
                  chan = GetChannel(data)
                  trans = slate(args, 'fi')
                  send(trans)

               if info[0] == 'goslate.ko': #Korean
                  chan = GetChannel(data)
                  trans = slate(args, 'ko')
                  send(trans)

               if info[0] == 'goslate.uk': #Ukrainian
                  chan = GetChannel(data)
                  trans = slate(args, 'uk')
                  send(trans)

               if info[0] == 'goslate.es': #Spanish
                  chan = GetChannel(data)
                  trans = slate(args, 'es')
                  send(trans)

               if info[0] == 'goslate.ar': #Arabic
                  chan = GetChannel(data)
                  trans = slate(args, 'ar')
                  send(trans)

               if info[0] == 'goslate.zh-CN': #Chinese Simple
                  chan = GetChannel(data)
                  trans = slate(args, 'zh-CN')
                  send(trans)

               if info[0] == 'goslate.zh-TW': #Chinese Traditional
                  chan = GetChannel(data)
                  trans = slate(args, 'zh-TW')
                  send(trans)

               if info[0] == 'goslate.fr': #French
                  chan = GetChannel(data)
                  trans = slate(args, 'fr')
                  send(trans)



	       if info[0] == 'reverse':
                  chan = GetChannel(data)
                  rr = args[::-1]
                  irc.send('PRIVMSG '+chan+' :'+rr+'\r\n')

               if info[0] == 'lines':
                  chan = GetChannel(data)
                  lct = str(len(open('tbot.py').readlines()))
                  send("It takes " + lct + " lines to run this bot!")
	    else:
	       sendno("You're blacklisted, sorry")
