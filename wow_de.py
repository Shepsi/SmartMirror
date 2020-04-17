#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
	
# returns a dictionary containing basic character information
def getCharacterInfo(server, character):
	d = {
		'name': None,
		'title': None,
		'gender': None,
		'class': None,
		'race': None,
		'level': None,
		'itemLevel': None,
		'thumbnail': None,
		'render': None,
		'guild': None,
		'individualStats': {
			# 'stats'
			'health': None,
			'str': None,
			'agi': None,
			'int': None,
			'sta': None,
			'critRating': None,
			'hasteRating': None,
			'masteryRating': None,
			'versatility': None,
			'armor': None,
			# 'pvp'
			'alteracValleyTowersCaptured': None,
			'alteracValleyTowersDefended': None,
			'eyeOfTheStormFlagsCaptured': None,
			'warsongGulchFlagsCaptured': None,
			'warsongGulchFlagsDefended': None,
			'battlegroundsPlayed': None,
			'battlegroundsWon': None,
			'duelsWon': None,
			'duelsLost': None,
			'honorableKills': None,
			'honorableKillsAlteracValley': None,
			'honorableKillsArathiBasin': None,
			'honorableKillsWarsongGulch': None,
			'honorableKillsWorld': None,
			# 'deaths'
			'drowning': None,
			'dungeon': None, # doesn't include heroic dungeons
			'heroicDungeon': None,
			'raid': None,
			'falling': None,
			'fireAndLava': None,
			'otherPlayers': None,
			'total': None,
			# 'combat'
			'damageDone': None,
			'damageReceived': None,
			'healingDone': None,
			'healingReceived': None,
			'kills': None,
			'killsCritters': None,
			# 'travel'
			'flightPathsTaken': None,
			'hearthstoneUsed': None,
			'portalsTaken': None,
			'summonsAccepted': None,
			# 'emotes'
			'cheer': None,
			'hug': None,
			'lol': None,
			'ohgod': None,
			'wave': None,
			# 'quests'
			'completed': None,
			'aborted': None,
			'dailyCompleted': None,
			'averagePerDay': None,
			# 'skills'
			'cooking': None,
			'cookingRecipes': None,
			'fishing': None,
			'fishCaught': None,
			# 'consumables'
			'bandages': None,
			'beverages': None,
			'food': None,
			'differentBeverages': None,
			'differentFoods': None,
			'elixirs': None,
			'flasks': None,
			'healingPotions': None,
			'manaPotions': None,
			'healthstones': None,
			# 'misc'
			'epicsLooted': None,
			'rollsGreed': None,
			'rollsNeed': None,
			'exaltedFactions': None,
			'petBattlesWon': None
		},
		'accountStats': {
			'achievementPoints': None,
			'petsCollected': None,
			'petsNotCollected': None,
			'mountsCollected': None,
			'mountsNotCollected': None
		}
	}
	
	j = {}
	try:
		with open('cache/raw_json/{}-{}.json'.format(server, character), 'r') as f:
			j = json.load(f)
	except IOError:
		print('"cache/raw_json/{}-{}.json" not found!'.format(server, character))
		
	# fill first-level entries
	for k in {'name', 'class', 'race', 'gender', 'level', 'thumbnail'}:
		d[k] = j.get(k, None)
	
	# get render image
	url_part = j.get('thumbnail', None)
	if url_part is not None:
		url_part = url_part.replace('avatar','main')
		d['render'] = url_part
	
	# search the currently selected title (out of all titles)
	tmpList = j.get('titles', [])
	for entry in tmpList:
		if entry.get('selected', False):
			d['title'] = entry.get('name', None)
			break
	
	# get/set non-first-level entries
	d['itemLevel'] = j.get('items',{}).get('averageItemLevel', None)
	d['guild'] = j.get('guild',{}).get('name', None)
	d['individualStats']['honorableKills'] = j.get('totalHonorableKills', None)
	d['accountStats']['achievementPoints'] = j.get('achievementPoints', None)
	d['accountStats']['petsCollected'] = j.get('pets', {}).get('numCollected', None)
	d['accountStats']['petsNotCollected'] = j.get('pets', {}).get('numNotCollected', None)
	d['accountStats']['mountsCollected'] = j.get('mounts', {}).get('numCollected', None)
	d['accountStats']['mountsNotCollected'] = j.get('mounts', {}).get('numNotCollected', None)
	for k in {'health', 'str', 'agi', 'int', 'sta', 'critRating', 'hasteRating', 'masteryRating', 'versatility', 'armor'}:
		d['individualStats'][k] = j.get('stats', {}).get(k, None)
	
	# iterate over the subCategories list in the statistics dictionary to find relevant stats
	# counts the number of 'hits' to break out of loops early
	listHits = 0
	subListHits = 0
	subSubListHits = 0
	tmpList = j.get('statistics',{}).get('subCategories',[])
	for entry in tmpList:
		# id 141 is 'Combat'/'Kampf'
		if entry.get('id', 0) == 141:
			listHits += 1
			tmpSubList = entry.get('statistics',[])
			for subEntry in tmpSubList:
				# id 197 is 'Total damage done'/'Verursachter Schaden insgesamt'
				if subEntry.get('id',0) == 197:
					subListHits += 1
					d['individualStats']['damageDone'] = subEntry.get('quantity', 0)
				# id 528 is 'Total damage received'/'Erlittener Schaden insgesamt'
				if subEntry.get('id',0) == 528:
					subListHits += 1
					d['individualStats']['damageReceived'] = subEntry.get('quantity', 0)
				# id 198 is 'Total healing done'/'Heilung durchgeführt insgesamt'
				if subEntry.get('id',0) == 198:
					subListHits += 1
					d['individualStats']['healingDone'] = subEntry.get('quantity', 0)
				# id 830 is 'Total healing received'/'Erhaltene Heilung insgesamt'
				if subEntry.get('id',0) == 830:
					subListHits += 1
					d['individualStats']['healingReceived'] = subEntry.get('quantity', 0)
				if subListHits > 3:
					break
			subListHits = 0
		# id 15219 is 'Pet Battles'/'Haustierkämpfe'
		if entry.get('id', 0) == 15219:
			listHits += 1
			tmpSubList = entry.get('statistics',[])
			for subEntry in tmpSubList:
				# id 8278 is 'Pet Battles won at max level'/'Haustierkämpfe auf der Höchststufe gewonnen'
				if subEntry.get('id',0) == 8278:
					subListHits += 1
					d['individualStats']['petBattlesWon'] = subEntry.get('quantity', 0)
				if subListHits > 1:
					break
			subListHits = 0
		# id 133 is 'Quests'
		if entry.get('id', 0) == 133:
			listHits += 1
			tmpSubList = entry.get('statistics',[])
			for subEntry in tmpSubList:
				# id 98 is 'Quests abgeschlossen'
				if subEntry.get('id', 0) == 98:
					subListHits += 1
					d['individualStats']['completed'] = subEntry.get('quantity', 0)
				# id 95 is 'Durchschnittlich abgeschlossene Quests pro Tag'
				if subEntry.get('id', 0) == 95:
					subListHits += 1
					d['individualStats']['averagePerDay'] = subEntry.get('quantity', 0)
				# id 97 is 'Durchschnittlich abgeschlossene Quests pro Tag'
				if subEntry.get('id', 0) == 97:
					subListHits += 1
					d['individualStats']['dailyCompleted'] = subEntry.get('quantity', 0)
				# id 94 is 'Quests abgebrochen'
				if subEntry.get('id', 0) == 94:
					subListHits += 1
					d['individualStats']['aborted'] = subEntry.get('quantity', 0)
				if subListHits > 4:
					break
			subListHits = 0
		# id 134 is 'Reise'
		if entry.get('id', 0) == 134:
			listHits += 1
			tmpSubList = entry.get('statistics',[])
			for subEntry in tmpSubList:
				# id 349 is 'Bereiste Flugrouten'
				if subEntry.get('id', 0) == 349:
					subListHits += 1
					d['individualStats']['flightPathsTaken'] = subEntry.get('quantity', 0)
				# id 2277 is 'Beschwörungen angenommen'
				if subEntry.get('id', 0) == 2277:
					subListHits += 1
					d['individualStats']['summonsAccepted'] = subEntry.get('quantity', 0)
				# id 350 is 'Benutzte Magierportale'
				if subEntry.get('id', 0) == 350:
					subListHits += 1
					d['individualStats']['portalsTaken'] = subEntry.get('quantity', 0)
				# id 353 is 'Anzahl der Nutzungen des Ruhesteins'
				if subEntry.get('id', 0) == 353:
					subListHits += 1
					d['individualStats']['hearthstoneUsed'] = subEntry.get('quantity', 0)
				if subListHits > 4:
					break
			subListHits = 0
		# id 131 is 'Körpersprache'
		if entry.get('id', 0) == 131:
			listHits += 1
			tmpSubList = entry.get('statistics',[])
			for subEntry in tmpSubList:
				# id 1042 is 'Anzahl Umarmungen'
				if subEntry.get('id', 0) == 1042:
					subListHits += 1
					d['individualStats']['hug'] = subEntry.get('quantity', 0)
				# id 1047 is 'Anzahl der /ohgotts'
				if subEntry.get('id', 0) == 1047:
					subListHits += 1
					d['individualStats']['ohgod'] = subEntry.get('quantity', 0)
				# id 1066 is 'LOLs insgesamt'
				if subEntry.get('id', 0) == 1066:
					subListHits += 1
					d['individualStats']['lol'] = subEntry.get('quantity', 0)
				# id 1045 is 'Jubeln insgesamt'
				if subEntry.get('id', 0) == 1045:
					subListHits += 1
					d['individualStats']['cheer'] = subEntry.get('quantity', 0)
				# id 1065 is 'Winken insgesamt (/winken)'
				if subEntry.get('id', 0) == 1065:
					subListHits += 1
					d['individualStats']['wave'] = subEntry.get('quantity', 0)
				if subListHits > 5:
					break
			subListHits = 0
		# id 122 is 'Deaths'/'Tode'
		if entry.get('id', 0) == 122:
			listHits += 1
			tmpSubList = entry.get('statistics', [])
			for subEntry in tmpSubList:
				# id 60 is 'Total deaths'/'Tode insgesamt'
				if subEntry.get('id',0) == 60:
					subListHits += 1
					d['individualStats']['total'] = subEntry.get('quantity', 0)
				if subListHits > 1:
					break
			subListHits = 0
			tmpSubList = entry.get('subCategories',[])
			for subEntry in tmpSubList:
				# id 125 is 'Dungeons'/'Dungeons'
				if subEntry.get('id' ,0) == 125:
					subListHits += 1
					tmpSubSubList = subEntry.get('statistics', [])
					for subSubEntry in tmpSubSubList:
						# id 918 is 'Tode in 5-Spieler-Dungeons insgesamt'
						if subSubEntry.get('id', 0) == 918:
							subSubListHits += 1
							d['individualStats']['dungeon'] = subSubEntry.get('quantity', 0)
						# id 2219 is 'Tode in heroischen 5-Spieler-Dungeons insgesamt'
						if subSubEntry.get('id', 0) == 2219:
							subSubListHits += 1
							d['individualStats']['heroicDungeon'] = subSubEntry.get('quantity', 0)
						# id 9368 is 'Tode in Schlachtzügen insgesamt'
						if subSubEntry.get('id', 0) == 9368:
							subSubListHits += 1
							d['individualStats']['raid'] = subSubEntry.get('quantity', 0)
						if subSubListHits > 2:
							break
					subSubListHits = 0
				# id 126 is 'World'/'Welt'
				if subEntry.get('id' ,0) == 126:
					subListHits += 1
					tmpSubSubList = subEntry.get('statistics', [])
					for subSubEntry in tmpSubSubList:
						# id 112 is 'Tode durch Ertrinken'
						if subSubEntry.get('id', 0) == 112:
							subSubListHits += 1
							d['individualStats']['drowning'] = subSubEntry.get('quantity', 0)
						# id 114 is 'Tode durch Stürze'
						if subSubEntry.get('id', 0) == 114:
							subSubListHits += 1
							d['individualStats']['falling'] = subSubEntry.get('quantity', 0)
						# id 115 is 'Tode durch Feuer und Lava'
						if subSubEntry.get('id', 0) == 115:
							subSubListHits += 1
							d['individualStats']['fireAndLava'] = subSubEntry.get('quantity', 0)
						if subSubListHits > 2:
							break
					subSubListHits = 0
				if subListHits > 2:
					break
			subListHits = 0
		# id 128 is 'Kills'/'Siege'
		if entry.get('id', 0) == 128:
			listHits += 1
			tmpSubList = entry.get('statistics',[])
			for subEntry in tmpSubList:
				# id 1197 is 'Total kills'/'Siege insgesamt'
				if subEntry.get('id',0) == 1197:
					subListHits += 1
					d['individualStats']['kills'] = subEntry.get('quantity', 0)
				if subListHits > 1:
					break
			subListHits = 0
			tmpSubList = entry.get('subCategories',[])
			for subEntry in tmpSubList:
				# id 135 is 'Creatures'/'Kreaturen'
				if subEntry.get('id' ,0) == 135:
					subListHits += 1
					tmpSubSubList = subEntry.get('statistics', [])
					for subSubEntry in tmpSubSubList:
						# id 108 is 'Kleintiere getötet'
						if subSubEntry.get('id', 0) == 108:
							subSubListHits += 1
							d['individualStats']['killsCritters'] = subSubEntry.get('quantity', 0)
						if subSubListHits > 1:
							break
					subSubListHits = 0
				# id 136 is 'Honorable Kills'/'Ehrenhafte Siege'
				if subEntry.get('id' ,0) == 136:
					subListHits += 1
					tmpSubSubList = subEntry.get('statistics', [])
					for subSubEntry in tmpSubSubList:
						# id 381 is 'Weltweite ehrenhafte Siege'
						if subSubEntry.get('id', 0) == 381:
							subSubListHits += 1
							d['individualStats']['honorableKillsWorld'] = subSubEntry.get('quantity', 0)
						# id 1113 is 'Ehrenhafte Siege im Alteractal'
						if subSubEntry.get('id', 0) == 1113:
							subSubListHits += 1
							d['individualStats']['honorableKillsAlteracValley'] = subSubEntry.get('quantity', 0)
						# id 1114 is 'Ehrenhafte Siege im Arathibecken'
						if subSubEntry.get('id', 0) == 1114:
							subSubListHits += 1
							d['individualStats']['honorableKillsArathiBasin'] = subSubEntry.get('quantity', 0)
						# id 1115 is 'Ehrenhafte Siege in der Kriegshymnenschlucht'
						if subSubEntry.get('id', 0) == 1115:
							subSubListHits += 1
							d['individualStats']['honorableKillsWarsongGulch'] = subSubEntry.get('quantity', 0)
						# id 1116 is 'Ehrenhafte Siege im Auge des Sturms'
						if subSubEntry.get('id', 0) == 1116:
							subSubListHits += 1
							d['individualStats']['honorableKillsEyeOfTheStorm'] = subSubEntry.get('quantity', 0)
						if subSubListHits > 5:
							break
					subSubListHits = 0
				if subListHits > 2:
					break
			subListHits = 0
		# id 21 is 'Player vs. player'/'Spieler gegen Spieler'
		if entry.get('id', 0) == 21:
			listHits += 1
			tmpSubList = entry.get('statistics',[])
			for subEntry in tmpSubList:
				# id 1501 is 'Total deaths from other players'/'Tode durch andere Spieler insgesamt'
				if subEntry.get('id',0) == 1501:
					subListHits += 1
					d['individualStats']['otherPlayers'] = subEntry.get('quantity', 0)
				if subListHits > 1:
					break
			subListHits = 0
			tmpSubList = entry.get('subCategories',[])
			for subEntry in tmpSubList:
				# id 153 is 'Schlachtfelder'
				if subEntry.get('id' ,0) == 153:
					subListHits += 1
					tmpSubSubList = subEntry.get('statistics', [])
					for subSubEntry in tmpSubSubList:
						# id 839 is 'Gespielte Schlachtfelder'
						if subSubEntry.get('id', 0) == 839:
							subSubListHits += 1
							d['individualStats']['battlegroundsPlayed'] = subSubEntry.get('quantity', 0)
						# id 840 is 'Schlachtfelder gewonnen'
						if subSubEntry.get('id', 0) == 840:
							subSubListHits += 1
							d['individualStats']['battlegroundsWon'] = subSubEntry.get('quantity', 0)
						# id 585 is 'Im Auge des Sturms eroberte Flaggen'
						if subSubEntry.get('id', 0) == 840:
							subSubListHits += 1
							d['individualStats']['eyeOfTheStormFlagsCaptured'] = subSubEntry.get('quantity', 0)
						# id 393 is 'Türme im Alteractal verteidigt'
						if subSubEntry.get('id', 0) == 393:
							subSubListHits += 1
							d['individualStats']['alteracValleyTowersDefended'] = subSubEntry.get('quantity', 0)
						# id 394 is 'Türme im Alteractal erobert'
						if subSubEntry.get('id', 0) == 394:
							subSubListHits += 1
							d['individualStats']['alteracValleyTowersCaptured'] = subSubEntry.get('quantity', 0)
						# id 395 is 'In der Kriegshymnenschlucht eingenommene Flaggen'
						if subSubEntry.get('id', 0) == 395:
							subSubListHits += 1
							d['individualStats']['warsongGulchFlagsCaptured'] = subSubEntry.get('quantity', 0)
						# id 586 is 'Verteidigte Flaggen in der Kriegshymnenschlucht'
						if subSubEntry.get('id', 0) == 586:
							subSubListHits += 1
							d['individualStats']['warsongGulchFlagsDefended'] = subSubEntry.get('quantity', 0)
						if subSubListHits > 7:
							break
					subSubListHits = 0
				# id 154 is 'World' / 'Welt'
				if subEntry.get('id', 0) == 154:
					subListHits += 1
					tmpSubSubList = subEntry.get('statistics', [])
					for subSubEntry in tmpSubSubList:
						# id 319 is 'Duelle gewonnen'
						if subSubEntry.get('id', 0) == 319:
							subSubListHits += 1
							d['individualStats']['duelsWon'] = subSubEntry.get('quantity', 0)
						# id 319 is 'Duelle verloren'
						if subSubEntry.get('id', 0) == 320:
							subSubListHits += 1
							d['individualStats']['duelsLost'] = subSubEntry.get('quantity', 0)
						if subSubListHits > 2:
							break
					subSubListHits = 0
				if subListHits > 3:
					break
			subListHits = 0
		# id 130 is 'Charakter'
		if entry.get('id', 0) == 130:
			listHits += 1
			tmpSubList = entry.get('subCategories',[])
			for subEntry in tmpSubList:
				# id 145 is 'Verbrauchsgüter'
				if subEntry.get('id', 0) == 145:
					subListHits += 1
					tmpSubSubList = subEntry.get('statistics', [])
					for subSubEntry in tmpSubSubList:
						# id 344 is 'Angelegte Verbände'
						if subSubEntry.get('id', 0) == 344:
							subSubListHits += 1
							d['individualStats']['bandages'] = subSubEntry.get('quantity', 0)
						# id 345 is 'Heiltränke verbraucht'
						if subSubEntry.get('id', 0) == 345:
							subSubListHits += 1
							d['individualStats']['healingPotions'] = subSubEntry.get('quantity', 0)
						# id 922 is 'Manatränke verbraucht'
						if subSubEntry.get('id', 0) == 922:
							subSubListHits += 1
							d['individualStats']['manaPotions'] = subSubEntry.get('quantity', 0)
						# id 923 is 'Elixiere verbraucht'
						if subSubEntry.get('id', 0) == 923:
							subSubListHits += 1
							d['individualStats']['elixirs'] = subSubEntry.get('quantity', 0)
						# id 811 is 'Fläschchen verbraucht'
						if subSubEntry.get('id', 0) == 811:
							subSubListHits += 1
							d['individualStats']['flasks'] = subSubEntry.get('quantity', 0)
						# id 346 is 'Getränke verbraucht'
						if subSubEntry.get('id', 0) == 346:
							subSubListHits += 1
							d['individualStats']['beverages'] = subSubEntry.get('quantity', 0)
						# id 1774 is 'Verschiedene Getränke verbraucht'
						if subSubEntry.get('id', 0) == 1774:
							subSubListHits += 1
							d['individualStats']['differentBeverages'] = subSubEntry.get('quantity', 0)
						# id 347 is 'Nahrung konsumiert'
						if subSubEntry.get('id', 0) == 347:
							subSubListHits += 1
							d['individualStats']['food'] = subSubEntry.get('quantity', 0)
						# id 1775 is 'Verschiedene Nahrungsmittel konsumiert'
						if subSubEntry.get('id', 0) == 1775:
							subSubListHits += 1
							d['individualStats']['differentFoods'] = subSubEntry.get('quantity', 0)
						# id 812 is 'Gesundheitssteine benutzt'
						if subSubEntry.get('id', 0) == 812:
							subSubListHits += 1
							d['individualStats']['healthstones'] = subSubEntry.get('quantity', 0)
						if subSubListHits > 10:
							break
					subSubListHits = 0
				# id 147 is 'Ruf'
				if subEntry.get('id', 0) == 147:
					subListHits += 1
					tmpSubSubList = subEntry.get('statistics', [])
					for subSubEntry in tmpSubSubList:
						# id 377 is 'Höchste Anzahl Fraktionen auf Ehrfürchtig'
						if subSubEntry.get('id', 0) == 377:
							subSubListHits += 1
							d['individualStats']['exaltedFactions'] = subSubEntry.get('quantity', 0)
						if subSubListHits > 1:
							break
					subSubListHits = 0
				# id 191 is 'Ausrüstung'
				if subEntry.get('id', 0) == 191:
					subListHits += 1
					tmpSubSubList = subEntry.get('statistics', [])
					for subSubEntry in tmpSubSubList:
						# id 342 is 'Erhaltene epuische Gegenstände'
						if subSubEntry.get('id', 0) == 342:
							subSubListHits += 1
							d['individualStats']['epicsLooted'] = subSubEntry.get('quantity', 0)
						# id 1043 is 'Würfe für Gier bei Plünderungen'
						if subSubEntry.get('id', 0) == 1043:
							subSubListHits += 1
							d['individualStats']['rollsGreed'] = subSubEntry.get('quantity', 0)
						# id 1044 is 'Würfe für Bedarf bei Plünderungen'
						if subSubEntry.get('id', 0) == 1044:
							subSubListHits += 1
							d['individualStats']['rollsNeed'] = subSubEntry.get('quantity', 0)
						if subSubListHits > 3:
							break
					subSubListHits = 0
				if subListHits > 3:
					break
			subListHits = 0
		# id 132 is 'Fertigkeiten'
		if entry.get('id', 0) == 132:
			listHits += 1
			tmpSubList = entry.get('subCategories',[])
			for subEntry in tmpSubList:
				# id 178 is 'Sekundäre Fertigkeiten'
				if subEntry.get('id', 0) == 178:
					subListHits += 1
					tmpSubSubList = subEntry.get('statistics', [])
					for subSubEntry in tmpSubSubList:
						# id 1524 is 'Kochfertigkeit'
						if subSubEntry.get('id', 0) == 1524:
							subSubListHits += 1
							d['individualStats']['cooking'] = subSubEntry.get('quantity', 0)
						# id 1745 is 'Bekannte Kochrezepte'
						if subSubEntry.get('id', 0) == 1745:
							subSubListHits += 1
							d['individualStats']['cookingRecipes'] = subSubEntry.get('quantity', 0)
						# id 1519 is 'Angelfertigkeit'
						if subSubEntry.get('id', 0) == 1519:
							subSubListHits += 1
							d['individualStats']['fishing'] = subSubEntry.get('quantity', 0)
						# id 1456 is 'Fische und andere geangelte Dinge'
						if subSubEntry.get('id', 0) == 1456:
							subSubListHits += 1
							d['individualStats']['fishCaught'] = subSubEntry.get('quantity', 0)
						if subSubListHits > 10:
							break
					subSubListHits = 0
				if subListHits > 3:
					break
			subListHits = 0
	return d