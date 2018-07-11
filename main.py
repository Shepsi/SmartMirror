#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.graphics import Color
from kivy.core.text import markup
from kivy.uix.screenmanager import Screen, ScreenManager

from sources import *
from weathersources import *
from functools import partial
import random
import time
import datetime
import collections
import math
import os

from kivy.config import Config
Config.set('graphics', 'width', 1280)
Config.set('graphics', 'height', 1024)
Config.set('graphics', 'maxfps', 60)

import langDE
import utils

from config import BATTLETAGS
from config import COLORS

class MirrorRoot(ScreenManager):
	pass

class Werte(Screen):
	#ObjectProperties for KV File
	currentTime = ObjectProperty()
	currentDay = ObjectProperty()
	currentMonth = ObjectProperty()
	
	weatherTemperature = ObjectProperty()
	weatherCondition = ObjectProperty()
	weatherIcon = ObjectProperty()
	sensorTemperature = ObjectProperty()
	
	daysToHolidays = ObjectProperty()
	
	# Diablo
	#characterName = ObjectProperty()
	#quotation = ObjectProperty()
	#seasonalIcon = ObjectProperty()
	#hardcoreIcon = ObjectProperty()
	#damageIcon = ObjectProperty()
	#toughnessIcon = ObjectProperty()
	#healingIcon = ObjectProperty()
	#damage = ObjectProperty()
	#toughness = ObjectProperty()
	#healing = ObjectProperty()
	#levelText = ObjectProperty()
	#levelIcon = ObjectProperty()
	#totalKillsText = ObjectProperty()
	#playtimeBarbarian = ObjectProperty()
	#playtimeCrusader = ObjectProperty()
	#playtimeDemonHunter = ObjectProperty()
	#playtimeMonk = ObjectProperty()
	#playtimeNecromancer = ObjectProperty()
	#playtimeWitchDoctor = ObjectProperty()
	#playtimeWizard = ObjectProperty()

	# Weather condition
	weatherparticles = []
	weathercondition = ""

	#Alexa_Response
	alexa_Response = ObjectProperty()

	# Fussball
	f_achtel1 = ObjectProperty()
	f_achtel2 = ObjectProperty()
	f_achtel3 = ObjectProperty()
	f_achtel4 = ObjectProperty()
	f_achtel5 = ObjectProperty()
	f_achtel6 = ObjectProperty()
	f_achtel7 = ObjectProperty()
	f_achtel8 = ObjectProperty()
	f_viertel1 = ObjectProperty()
	f_viertel2 = ObjectProperty()
	f_viertel3 = ObjectProperty()
	f_viertel4 = ObjectProperty()
	f_halb1 = ObjectProperty()
	f_halb2 = ObjectProperty()
	f_finale = ObjectProperty()

	def setCurrentTime(self, *args):
		self.currentTime.text = getTime()

	def setCurrentDate(self, *args):
		dateDict = getDate()
		self.currentDay.text = str(dateDict.get('day', ''))
		self.currentMonth.text = langDE.monthsShort[str(dateDict.get('month', ''))]

	def setRaspiTemperature(self, *args):
		self.sensorTemperature.text = ' / ' + str(getRaspberryTemperature()) + '°'
	
	def setIconColor(self, *args):
		self.weatherIcon.color = utils.convertToFloat(hex = COLORS['diablo.paragon'])

	def setWeather(self, *args):
		with open('mirrorlog.txt', 'a') as file:
			file.write('Setzt das Wetter (setWeather)\n')
		weatherDic = getWeather()
		if weatherDic.get('windchill', None) is not None:
			self.weatherTemperature.text = str(weatherDic['windchill']) + '°'
		if weatherDic.get('description', None) is not None:
			self.weatherCondition.text = weatherDic['description']
		if weatherDic.get('icon', '') is not '':
			self.weatherIcon.source = weatherDic['icon']
		self.weatherIcon.color = utils.convertToFloat(hex = COLORS['diablo.paragon'])
		# set weather animation
		iconnumber = weatherDic.get('icon', 'resources/weather_icons/d/000.png')
		iconnumber = int(iconnumber[-7:-4])
		if iconnumber == 000:
			self.weathercondition = 'Magic'
			addMagic(self)
		elif 200 <= iconnumber <= 232 or 300 <= iconnumber <= 321 or 500 <= iconnumber <= 504 or 520 <= iconnumber <= 531:
			self.weathercondition = 'Rain'
			addRain(self)
		elif 600 <= iconnumber <= 622 or iconnumber == 903 or iconnumber == 906:
			self.weathercondition = 'Snow'
			addSnow(self)
		else:
			removeParticle(self)

	# Bewegt die Wetterpartikel je nach Wetterlage
	def letItWeather(self, *args):
		if self.weathercondition == "Snow":
			moveWeatherparticle(self, "Snow")
		elif self.weathercondition == "Rain":
			moveWeatherparticle(self, "Rain")
		elif self.weathercondition == "Magic":
			moveWeatherparticle(self, "Magic")

	def setDaysToHolidays(self, *args):
		with open('mirrorlog.txt', 'a') as file:
			file.write('Setzt Tage bis Feiertage (setDaysToHolidays)\n')
		holidayDic = holidayCD()
		if holidayDic["halloween"] != "":
			self.daysToHolidays.text = holidayDic["halloween"]
			self.daysToHolidays.font_name = 'resources/font/October-Crow.ttf'
		if holidayDic["christmas"] != "":
			self.daysToHolidays.text = holidayDic["christmas"]
			self.daysToHolidays.font_name = 'resources/font/I-Love-Christmas.ttf'
			
	def setDiablo(self, *args):
		with open('mirrorlog.txt', 'a') as file:
			file.write('Setzt Diablo (setDiablo)\n')
		# Init
		random.seed()
		battleTag = random.choice(BATTLETAGS)
		diabloDict = getDiabloStats(battleTag)
		hero = random.choice(diabloDict['heroes'])
		
		# Character name, uses markup to make first letter larger
		smallLetters = int(self.characterName.font_size * 0.8)
		self.characterName.text = hero['name'][0] + '[size='+ str(smallLetters) + ']' + hero['name'][1:] + '[/size]'
		self.characterName.font_name = 'resources/font/exocet.ttf'
		
		# get/set stats for the chosen hero
		heroId = hero.get('id', 0)
		heroStats = getHeroStats(battleTag, heroId)
		self.quotation.text = heroStats['flavorText']
		self.damage.text = utils.readableNumber(heroStats['damage'])
		self.toughness.text = utils.readableNumber(heroStats['toughness'])
		self.healing.text = utils.readableNumber(heroStats['healing'])
		
		# manages the hardcore and seasonal icon
		if hero['seasonal']:
			self.seasonalIcon.opacity = 1
		else:
			self.seasonalIcon.opacity = 0
		if hero['hardcore']:
			self.hardcoreIcon.opacity = 1
		else:
			self.hardcoreIcon.opacity = 0
			
		# color damage/toughness/healing icons according to class color
		colorKey = 'diablo.{0}'.format(hero['class'])
		if colorKey in COLORS:
			self.damageIcon.color = utils.convertToFloat(hex = COLORS[colorKey])
			self.toughnessIcon.color = utils.convertToFloat(hex = COLORS[colorKey])
			self.healingIcon.color = utils.convertToFloat(hex = COLORS[colorKey])
		else:
			self.damageIcon.color = (1,1,1,1)
			self.toughnessIcon.color = (1,1,1,1)
			self.healingIcon.color = (1,1,1,1)
		
		# manages the character level, level will be gray for dead hardcore heroes and Paragon level will match the type of the character (normal, seasonal, hardcore, seasonal hardcore).
		# Paragon level only shows if character is level 70
		# displays suitable icon to the right of the label (level, paragon level, dead hardcore character)
		heroLvl = hero['level']
		self.levelIcon.source = 'resources/diablo_icons/level.png'
		self.levelText.color = (1, 1, 1, 1)
		if heroLvl == 70:
			pLvlKey = 'paragonLevel' + hero['seasonal']*'Season' +  hero['hardcore']*'Hardcore'
			heroLvl = diabloDict.get(pLvlKey, 0)
			self.levelText.color = utils.convertToFloat(hex = COLORS['diablo.paragon'])
			self.levelIcon.source = 'resources/diablo_icons/paragon.png'
		self.levelText.text = str(heroLvl)
		
		# sets the amount of killed monsters
		if hero['hardcore']:
			kills = diabloDict.get('kills',{}).get('hardcoreMonsters',0)
		else:
			kills = diabloDict.get('kills',{}).get('monsters',0)
			
		self.totalKillsText.text = utils.readableNumber(kills)
		
		# makes the character name less opaque if it is a dead hardcore character
		if hero['dead']:
			self.characterName.opacity = .5
		else:
			self.characterName.opacity = 1
		
		# creates and sets the image for the playtime per class
		tmpDict = {'barbarian': self.playtimeBarbarian, 'crusader':self.playtimeCrusader, 'demon-hunter': self.playtimeDemonHunter, 'monk': self.playtimeMonk, 'necromancer': self.playtimeNecromancer, 'witch-doctor': self.playtimeWitchDoctor, 'wizard': self.playtimeWizard}
		for k in tmpDict:
			if os.path.isfile('tmp/tmp_{0}.png'.format(k)):
				tmpDict[k].source = 'tmp/tmp_{0}.png'.format(k)
			else:
				tmpDict[k].source = 'resources/diablo_icons/{0}-bg.png'.format(k)
			tmpDict[k].reload()

	# Alexa on mirror
	def getAlexa(self, *args):
		alexaresponse = getContent("resources/alexa-response/ausgabe.txt").replace('\r','').replace('\n','')
		if alexaresponse == "hoerenAn":
			size = self.alexa_Response.size
			#if size[0] < 300 and size[1] < 300:
			Clock.schedule_interval(partial(fadeAlexaIn, self), 0.016)
			
			Increment(0)
			self.alexa_Response.source = "resources/alexa-response/alexa_listening.zip"
		elif alexaresponse == "redenAn":
			Increment(0)
			self.alexa_Response.source = "resources/alexa-response/alexa_talking.zip"
		elif alexaresponse == "redenAus" or alexaresponse == "hoerenAus":
			if Increment(1) <= 25 and Increment(1) <= 35:
				self.alexa_Response.source = "resources/alexa-response/alexa_silent.zip"
			else:
				Clock.schedule_interval(partial(fadeAlexaOut, self), 0.016)


	def setFussball(self, *args):
		today = datetime.datetime.now()
		fillAchtelfinale(self)

		#showViertelOn = datetime.datetime(2018,7,5)
		#if (today >= showViertelOn):
		fillViertelfinale(self)

		#showHalbOn = datetime.datetime(2018,7,9)
		#if (today >= showHalbOn):
		fillHalbfinale(self)
		fillfinale(self)

class SmartMirrorApp(App):
	def build(self):
		print('Programm startete am {0} um {1} Uhr.'.format(time.strftime('%d.%m.%Y'), time.strftime('%H:%M')))
		print('Lädt...')
		#Lädt Widgets in Rootwidget.  Vorsorge falls man irgendwann andere Screens
		#möchte.
		parent = MirrorRoot()
		childWidgets = Werte()
		parent.add_widget(childWidgets)

		#Lädt einzelne Widgets
		print('Schaut auf die Uhr.')
		childWidgets.setCurrentTime()
		print('Schaut auf den Kalender.')
		childWidgets.setCurrentDate()
		print('Fühlt, wie warm es hier ist')
		childWidgets.setRaspiTemperature()
		print('Guckt für dich raus nach dem Wetter.')
		childWidgets.setWeather()
		print('Ist schon Halloween? Ist schon Weihnachten!?')
		childWidgets.setDaysToHolidays()
		print('Packt den Pinsel aus.')
		childWidgets.setIconColor()
		print('Alexa wird aufgeweckt')
		childWidgets.getAlexa()
		print("Ball wird angerollt.")
		childWidgets.setFussball()
		#Needs PIL to be installed
		#print('Wandert nach Sanktuario.')
		#childWidgets.setDiablo()

		#Updaten der einzelnen widgets in s
		Clock.schedule_interval(childWidgets.setCurrentTime, 10)
		Clock.schedule_interval(childWidgets.setCurrentDate, 10)
		Clock.schedule_interval(childWidgets.setRaspiTemperature, 60)
		Clock.schedule_interval(childWidgets.setWeather, 3600)
		# Clock.schedule_interval(childWidgets.setIconColor, 60)
		Clock.schedule_interval(childWidgets.setDaysToHolidays, 60)
		#Clock.schedule_interval(childWidgets.setDiablo, 600)
		Clock.schedule_interval(childWidgets.letItWeather, 0.016)
		Clock.schedule_interval(childWidgets.setFussball, 60)
		Clock.schedule_interval(childWidgets.getAlexa, 0.5)
		return parent

if __name__ == '__main__':
	SmartMirrorApp().run()