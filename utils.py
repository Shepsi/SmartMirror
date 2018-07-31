#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
import re
import os

#from PIL import Image
#from PIL import ImageDraw

# returns a dictionary (json) to a given url
# needs libraries 'requests' and 'time'
def requestJSON(url):
	j = {}
	try:
		r = requests.get(url)
		r.raise_for_status()
		j = r.json()
	finally:
		return j

# converts (r,g,b) and (r,g,b,a) tuples to float tuples (components in [0,1])
# also converts hexadecimal strings to float tuples, either with preceeding # or not and either with alpha component or not
def convertToFloat(rgba = None, hex = None):
	# input is an (r,g,b,a) or (r,g,b) tuple
	if rgba is not None:
		if len(rgba) < 3 or len(rgba) > 4:
			# conditionalPrint('Not a valid color tuple')
			return (0, 0, 0, 0)
		for entry in rgba:
			if entry < 0 or entry > 255:
				# conditionalPrint('Not a valid color tuple. ' + entry + ' is not in [0, 255].')
				return (0, 0, 0, 0)
		if len(rgba) == 3:
			rgba = rgba + (255,)
		return tuple(round(entry/255.0,4) for entry in rgba)
	
	# input is a hex string
	if hex is not None:
		hex = hex.lstrip('#')
		if len(hex) not in {6,8}:
			# conditionalPrint('Not a valid hex color code')
			return (0, 0, 0, 0)
		if len(hex) == 6:
			hex = hex + 'ff'
		if re.search(r'^[0-9A-Fa-f]+$', hex) is None:
			# conditionalPrint('Not a valid hex color code')
			return (0, 0, 0, 0)
		# now hex is of the form 'rrggbbaa'
		return convertToFloat(rgba = tuple(int(hex[i:i+2], 16) for i in (0, 2, 4, 6)))
		
	return (0, 0, 0, 0)
	
# converts float tuples and hex strings to rgb colors
def convertToRGBA(float = None, hex = None):
	# input is an float tuple
	if float is not None:
		if len(float) < 3 or len(float) > 4:
			# conditionalPrint('Not a valid color tuple')
			return (0, 0, 0, 0)
		for entry in float:
			if entry < 0 or entry > 1:
				# conditionalPrint('Not a valid color tuple. ' + entry + ' is not in [0, 255].')
				return (0, 0, 0, 0)
		if len(float) == 3:
			float = float + (1,)
		return tuple(int(entry * 255) for entry in float)
	
	# input is a hex string
	if hex is not None:
		hex = hex.lstrip('#')
		if len(hex) not in {6,8}:
			# conditionalPrint('Not a valid hex color code')
			return (0, 0, 0, 0)
		if len(hex) == 6:
			hex = hex + 'ff'
		if re.search(r'^[0-9A-Fa-f]+$', hex) is None:
			# conditionalPrint('Not a valid hex color code')
			return (0, 0, 0, 0)
		# now hex is of the form 'rrggbbaa'
		return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4, 6))
		
	return (0, 0, 0, 0)

# converts color tuples (either rgba or float) to hex color code with preceeding '#'
def convertToHex(rgba = None, dec = None):
	# input is an (r,g,b,a) or (r,g,b) tuple
	if rgba is not None:
		if len(rgba) < 3 or len(rgba) > 4:
			return '#000000'
		if len(rgba) == 3:
			rgba = rgba + (255,)
		hex_code = '#'
		for entry in rgba:
			if entry < 0 or entry > 255 or type(entry) != int:
				return '#000000'
			hex_code = hex_code + hex(entry).lstrip('0x').zfill(2)
		return hex_code
	
	# input a float string	
	if dec is not None:
		return convertToHex(rgba = tuple(int(entry * 255) for entry in dec))
		
	return '#000000'
	
# returns a color of a given color gradient
# gradient is specified with two seperate colors (points in 3d space)
# color to return is specified with as percentage with 0 -> first color, 1 -> second color
# outputs color in rgb (or rgba) tuple
def colorGradient(startColor, endColor, pointOnLine):
	r = 0
	g = 0
	b = 0
	if len(startColor) < 3 or len(startColor) > 4:
		return (0, 0, 0, 0)
	if len(endColor) < 3 or len(endColor) > 4:
		return (0, 0, 0, 0)
	if pointOnLine < 0 or pointOnLine > 1:
		return (0, 0, 0, 0)
	r = int(startColor[0] + (endColor[0]-startColor[0])*pointOnLine)
	g = int(startColor[1] + (endColor[1]-startColor[1])*pointOnLine)
	b = int(startColor[2] + (endColor[2]-startColor[2])*pointOnLine)
	return (r, g, b, 255)

# saves an image from a given url with a given name and returns its path
# doesn't overwrite existing files by default
# TODO: error handling
def getImageFromUrl(url, filename, overwrite = False):
	if os.path.isfile(filename) and not overwrite:
		return filename

	requested_image = requests.get(url)
	
	img = open(filename, 'wb')
	img.write(requested_image.content)
	img.close()
	
	return filename
	
# makes long number 'readable': 1200000 -> 1,2 Mio.
# outputs a string
def readableNumber(n):
	suffix = ['', 'Tsd.', 'Mio.', 'Mrd.', 'Bio.', 'Brd.']
	i = 0
	while n > 1000 and i < len(suffix)-1:
		n /= 1000.0
		i += 1
	n = '{0:g}'.format(round(n,1))
	return n.replace('.',',') + ' ' + suffix[i]
	
# layers an image over another image
# only shows the bottom pct percent of the foreground image
# TODO: error handling
def maskImage(bg, fg, pct):
	# get filename for saving
	_, f = os.path.split(fg)
	f = 'tmp_'+f
	
	if pct > 1:
		pct = 1
	if pct < 0:
		pct = 0
	
	# open images
	imgFg = Image.open(fg)
	imgBg = Image.open(bg)
	
	# make top 1-pct percent of fg image transparent using alpha mask
	# PIL coordinates start in top left
	transparentArea = ((0, 0, imgFg.size[0], imgFg.size[1]*(1-pct)))
	mask=Image.new('L', imgFg.size, color=255)
	draw=ImageDraw.Draw(mask)
	draw.rectangle(transparentArea, fill=0)
	imgFg.putalpha(mask)
	
	# layer images on top of each other
	imgBg = Image.alpha_composite(imgBg.convert('RGBA'), imgFg)
	
	imgBg.save('tmp/'+f, 'png')

# returns the time in seconds since the files last update
# returns None when the file doesn't exist
def checkCreationDate(filename):
	lastUpdate = None
	if os.path.isfile(filename):
		lastUpdate = round(time.time() - os.path.getmtime(filename))
	return lastUpdate