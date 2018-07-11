#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python libs
import time
import os.path
import datetime
import math
import random
import codecs
from kivy.uix.image import Image
import re

# own stuff
import utils
from config import APIKEY_OPENWEATHERMAP
from config import APIKEY_BATTLE_NET
from config import CITYCODE
from config import COLOR_NIGHT
from config import COLOR_NOON


#########################################
#               methods                 #
#########################################

# returns the time (hour:minute) as string
def getTime():
    return time.strftime("%H:%M")

# returns a dictionary with current day of month (left-padded with space for 1
# to 9) and month (shortened to first 3 characters)
def getDate():
	day = time.strftime("%d")
	day = day.lstrip('0').rjust(2)
	month = time.strftime("%b")
	return {"day" : day, "month" : month }
	
# returns a color (as float tuple) from the current minutes
def getColorFromTime():
	minutes = int(time.strftime("%H")) * 60 + int(time.strftime("%M"))
	# makes sure the color goes from c2 to c1 if the time is past noon
	if minutes > 720:
		minutes = 1440 - minutes
	c1 = utils.convertToRGBA(hex = COLOR_NIGHT)
	c2 = utils.convertToRGBA(hex = COLOR_NOON)
	color = utils.colorGradient(c1, c2, minutes / 720)
	color = utils.convertToFloat(rgba = color)
	return color

# returns the current temperature measured by the temperature sensor as int
def getRaspberryTemperature():
	#Sucht Datei vom Temperaturmesser des Raspberry
	if os.path.exists("/sys/bus/w1/devices/28-000006374568/w1_slave"):
		tfile = open("/sys/bus/w1/devices/28-000006374568/w1_slave")
		text = tfile.read()
		tfile.close()
		secondline = text.split("\n")[1]
		temperaturdata = secondline.split(" ")[9]
		temperature = float(temperaturdata[2:])
		temperature = temperature / 1000
		value = round(temperature)
	#Exception Handler falls von anderen Geräten gestartet wird
	else:
		value = 12
	return int(value)

# time to halloween or christmas
def holidayCD():
	year = int(time.strftime("%Y"))
	today = datetime.datetime.now() - datetime.timedelta(1)
	cdHalloween = datetime.datetime(year, 10, 31) - today
	cdChristmas = datetime.datetime(year, 12, 24) - today
	halloweenTxt = ""
	christmasTxt = ""
	if (cdHalloween.days < 40 or cdChristmas.days < 100) and cdChristmas.days >= 0:
		if cdHalloween.days > 0:
			if cdHalloween.days == 1:
				halloweenTxt = "Noch " + str(cdHalloween.days) + " Tag bis Halloween"
			else:
				halloweenTxt = "Noch " + str(cdHalloween.days) + " Tage bis Halloween"
		elif cdHalloween.days == 0:
			halloweenTxt = "Happy Halloween!"
		else:
			symbolArray = ["^", " * ", "_", "~"]
			char = random.choice(symbolArray)
			if cdChristmas.days == 1:
				christmasTxt = "[Noch 1 Tag bis Weihnachten]"
			elif cdChristmas.days == 0:
				christmasTxt = "[Frohe~Weihnachten!]"
			else:
				christmasTxt = char + "Noch " + str(cdChristmas.days) + " Tage bis Weihnachten" + char
	return {"halloween" : halloweenTxt, "christmas" : christmasTxt }
	
# get some statics about the Diablo 3 account of a given battleTag
def getDiabloStats(battleTag):
	d = {
		'fallenHeroes': [],
		'guildName': '',
		'highestHardcoreLevel': None,
		'kills': {
			'elites': None,
			'hardcoreMonsters': None,
			'monsters': None
		},
		'heroes': [],
		'paragonLevel': None,
		'paragonLevelHardcore': None,
		'paragonLevelSeason': None,
		'paragonLevelSeasonHardcore': None,
		'timePlayed': {
			'barbarian': None,
			'crusader': None,
			'demon-hunter': None,
			'monk': None,
			'necromancer': None,
			'witch-doctor': None,
			'wizard': None
		}
	}

	url = 'https://eu.api.battle.net/d3/profile/{0}/?locale=en_GB&apikey={1}'.format(battleTag, APIKEY_BATTLE_NET)
	j = utils.requestJSON(url)
		
	# get paragon levels
	for k in {'paragonLevel', 'paragonLevelHardcore', 'paragonLevelSeason', 'paragonLevelSeasonHardcore'}:
		d[k] = j.get(k, None)
		
	# get kill statistics
	kills = j.get('kills', {})
	for k in {'monsters', 'elites', 'hardcoreMonsters'}:
		d['kills'][k] = kills.get(k, None)
		
	d['highestHardcoreLevel'] = j.get('highestHardcoreLevel', None)
	d['guildName'] = j.get('guildName', '')
	
	# get playtime per class in relation to the most played class
	# also create images with corresponding masks
	timePlayed = j.get('timePlayed',{})
	for k in {'barbarian', 'crusader', 'demon-hunter', 'monk', 'necromancer', 'witch-doctor', 'wizard'}:
		d['timePlayed'][k] = timePlayed.get(k,0)
		utils.maskImage('resources/diablo_icons/{0}-bg.png'.format(k), 'resources/diablo_icons/{0}.png'.format(k), d['timePlayed'][k])

	# get list of all heroes
	heroes = j.get('heroes', [])
	hero = { 'class': '', 'dead': None, 'gender': None, 'hardcore': None, 'level': None, 'name': '', 'seasonal': None, 'kills': None, 'id': None }

	for entry in heroes:
		for k in {'dead', 'gender', 'hardcore', 'level', 'seasonal', 'id'}:
			hero[k] = entry.get(k, None)
		for k in {'class', 'name'}:
			hero[k] = entry.get(k, '')
		hero['kills'] = entry.get('kills', {}).get('elites', 0)
		d['heroes'].append(hero.copy())

	# if the heroes list was empty, insert an (empty) dummy hero
	if len(heroes) == 0:
		heroes.append(hero)
		
	return d
	
# returns some basic stats about a Diablo character (given by character id)
# also returns the flavor text of a random* unique/set item of a given char
# relies on the random order of the items dict
def getHeroStats(battleTag, charId):
	d = {
		'damage': None,
		'toughness': None,
		'healing': None,
		'flavorText': ''
	}
	
	url = 'https://eu.api.battle.net/d3/profile/{0}/hero/{1}?locale=en_GB&apikey={2}'.format(battleTag, charId, APIKEY_BATTLE_NET)
	j = utils.requestJSON(url)
	
	d['damage'] = j.get('stats',{}).get('damage', None)
	d['toughness'] = j.get('stats',{}).get('toughness', None)
	d['healing'] = j.get('stats',{}).get('healing', None)
	
	items = j.get('items', {})
	item = {}
	# look for an unique or set item
	for k in items:
		color = items[k].get('displayColor', None)
		if color == 'orange' or color == 'green':
			itemId = items[k].get('id', None)
			url = 'https://eu.api.battle.net/d3/data/item/{0}?locale=de_DE&apikey={1}'.format(itemId,APIKEY_BATTLE_NET)
			item = utils.requestJSON(url)
			break
	
	flavorText = item.get('flavorText', '"Bleibt ein Weilchen und hoert zu." - Deckard Cain')
	# regEx = '"(.*)"(\s*)[-\u2013\u2014](\s*)(.*)'
	# if re.match(regEx, flavorText) is None:
		# itemName = item.get('name', 'Unbekannt')
		# flavorText = '"{0}" - {1}'.format(flavorText, itemName)
		
	d['flavorText'] = flavorText
	
	return d

##################
# Fußball Finale #
##################

def fillAchtelfinale(mirror):
	mirror.f_achtel1.text = getContent("resources/fußball/Achtelfinale1.txt")
	mirror.f_achtel2.text = getContent("resources/fußball/Achtelfinale2.txt")
	mirror.f_achtel3.text = getContent("resources/fußball/Achtelfinale3.txt")
	mirror.f_achtel4.text = getContent("resources/fußball/Achtelfinale4.txt")
	mirror.f_achtel5.text = getContent("resources/fußball/Achtelfinale5.txt")
	mirror.f_achtel6.text = getContent("resources/fußball/Achtelfinale6.txt")
	mirror.f_achtel7.text = getContent("resources/fußball/Achtelfinale7.txt")
	mirror.f_achtel8.text = getContent("resources/fußball/Achtelfinale8.txt")

def fillViertelfinale(self):
	self.f_viertel1.text = getContent("resources/fußball/Viertelfinale1.txt")
	self.f_viertel2.text = getContent("resources/fußball/Viertelfinale2.txt")
	self.f_viertel3.text = getContent("resources/fußball/Viertelfinale3.txt")
	self.f_viertel4.text = getContent("resources/fußball/Viertelfinale4.txt")

def fillHalbfinale(self):
	self.f_halb1.text = getContent("resources/fußball/Halbfinale1.txt")
	self.f_halb2.text = getContent("resources/fußball/Halbfinale2.txt")

def fillfinale(self):
	self.f_finale.text = getContent("resources/fußball/Finale1.txt")

# Returns content of files. If not file is found it will return "".
# Path will automatically convert from windows to raspbian
def getContent(path):
	if os.path.exists(path):
		content = codecs.open(path, "rU", encoding = "utf-8-sig")
	elif os.path.exists("/home/pi/SmartMirror/" + path):
		content = codecs.open("/home/pi/SmartMirror/" + path, "rU", encoding = "utf-8-sig")
	else:
		return ""
	text = content.read()
	content.close()
	return text