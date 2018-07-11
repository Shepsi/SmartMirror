#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python libs
import time
import os.path
import datetime
import math
import random
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
#            weather methods            #
#########################################

# returns a dictionary containing basic weather information
def getWeather():
	# default dictionary (will be returned like this on error)
	d = {
			'description': '',
			'icon': '',
			'temp': None,
			'windchill': None
	}
	
	url = 'http://api.openweathermap.org/data/2.5/weather?id={0}&APPID={1}&units=metric&lang=de'.format(CITYCODE, APIKEY_OPENWEATHERMAP)
	# Check if os is raspbian. Otherwise, it will send no request during debugging
	if (os.path.exists("/sys")):
		j = utils.requestJSON(url)
	else:
		d = {
			'description': 'Klarer Zauberhimmel',
			'icon': 'resources/weather_icons/d/000.png',
			'temp': 5.8,
			'windchill': 8.5
			}
		return d

	# stores temperature and calculates windchill (if wind fast enough)
	main = j.get('main', {})
	wind = j.get('wind', {})
	temp = main.get('temp', None)
	speed = wind.get('speed', None)
	if temp is not None:
		temp = int(round(temp))
	d['temp'] = temp
	if speed is not None and speed > 5:
		d['windchill'] = int(round(13.12 + 0.6215 * temp + (0.3965 * temp - 11.37) * speed ** 0.16))
	else:
		d['windchill'] = temp
	
	# weather description and icon
	current = (j.get('weather',[{}]))[0]
	d['description'] = current.get('description',None)
	d['icon'] = 'resources/weather_icons/'
	if current.get('icon','')[:-1] == 'n':
		d['icon'] += 'n/'
	else:
		d['icon'] += 'd/'
	d['icon'] += str(current.get('id','000')) + '.png'
	
	return d

def generateSnow(snowflakes, amount):
	for i in range(amount):
		randomX = (random.randint(0,1280))
		randomY = (random.randint(0,1024))
		randomImg = (random.randint(1,2))
		randomSize = (random.randint(10,15))
		snowflakes.append(Image(
			source='resources/weather_animation/' + str(randomImg) + '.png',
			size_hint=(None, None),
			size=(randomSize, randomSize),
			pos=[randomX, randomY]))

def generateMagic(magic, amount):
	for i in range(amount):
		randomX = (random.randint(0,1280))
		randomY = (random.randint(0,1024))
		magic.append(Image(
			size_hint=(None, None),
			source='resources/weather_animation/4.png',
			pos=[randomX, randomY]))

def generateRain(raindrops, amount):
	for i in range(amount):
		randomX = (random.randint(0,1280))
		randomY = (random.randint(0,1024))
		#randomSize = (random.randint(10,15))
		raindrops.append(Image(
			source='resources/weather_animation/3.png',
			size_hint=(None, None),
			size=(5, 5),
			pos=[randomX, randomY]))

def addRain(selfobj):
	if len(selfobj.weatherparticles) < 1:
		amount = 10
		generateRain(selfobj.weatherparticles, amount)
		for raindrop in selfobj.weatherparticles:
			selfobj.add_widget(raindrop)

def addSnow(selfobj, *args):
	if len(selfobj.weatherparticles) < 1:
		amount = 10
		generateSnow(selfobj.weatherparticles, amount)
		for snowflake in selfobj.weatherparticles:
			selfobj.add_widget(snowflake)

def addMagic(selfobj, *args):
	if len(selfobj.weatherparticles) < 1:
		amount = 1
		generateMagic(selfobj.weatherparticles, amount)
		for magic in selfobj.weatherparticles:
			selfobj.add_widget(magic)

def moveWeatherparticle(selfobj, weathercondition):
	for particle in selfobj.weatherparticles:
		posX = particle.pos[0]
		posY = particle.pos[1]
		if (posY <= 0 and (weathercondition is not "Magic")):
			posY = 1024
			posX = (random.randint(0,1280))
		elif (weathercondition is "Magic"):
			if posX >= 1280:
				posX = -100
				posY = (random.randint(0,1000))
			particle.pos = (posX + 1, posY + math.sin(posX/40))

		if weathercondition == "Snow":
			speedyFlake = True
			if speedyFlake:
				particle.pos = (posX + math.sin(posY/10), posY - 0.7)
				speedyFlake = False
			else:
				particle.pos = (posX + math.sin(posY/10), posY - 0.5)
				speedyFlake = True

		if weathercondition == "Rain":
			particle.pos = (posX + 1, posY - 8)
			
def removeParticle(selfobj):
	if len(selfobj.weatherparticles) > 1:
		for particle in selfobj.weatherparticles:
			selfobj.remove_widget(particle)
	selfobj.weatherparticles = []
