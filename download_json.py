from config import APIKEY_BATTLE_NET
from config import WOW_CHARACTERS

import utils
import json

def download(server, character):
	url = 'https://eu.api.battle.net/wow/character/{0}/{1}?fields=feed,items,pets,statistics,titles,guild,mounts,professions,stats&locale=de_DE&apikey={2}'.format(server, character, APIKEY_BATTLE_NET)
	lastUpdate = utils.checkCreationDate('cache/raw_json/{}-{}.json'.format(server, character))
	if (lastUpdate is None) or (lastUpdate > 3600):
		print('Updating "cache/raw_json/{}-{}.json"...'.format(server, character))
		j = utils.requestJSON(url)
		
		# save raw json
		try:
			with open('cache/raw_json/{}-{}.json'.format(server, character),'w') as f:
				json.dump(j, f)
		except PermissionError:
			print('No permission to open "cache/raw_json/{}-{}.json"!'.format(server, character))
			
		# save images
		# thumb = j.get('thumbnail', None)
		# if thumb is not None:
			# utils.getImageFromUrl('https://render-eu.worldofwarcraft.com/character/{0}'.format(thumb),'cache/thumbs/{}-{}.jpg'.format(server, character),True)
			# utils.getImageFromUrl('https://render-eu.worldofwarcraft.com/character/{0}'.format(thumb).replace('avatar','main'),'cache/render/{}-{}.jpg'.format(server, character),True)
	# else:
		# print('"cache/raw_json/{}-{}.json" is up to date.'.format(server, character))
		
for server in WOW_CHARACTERS:
	for char in WOW_CHARACTERS.get(server,[]):
		download(server, char)