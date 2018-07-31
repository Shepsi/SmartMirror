# class colors of corresponding class by id (as defined by Blizzard)
CLASS_COLORS = {
	1:  (199,156,110,255), # Warrior
	2:  (245,140,186,255), # Paladin
	3:  (171,212,115,255), # Hunter
	4:  (255,245,105,255), # Rogue
	5:  (255,255,255,255), # Priest
	6:  (196, 31, 59,255), # Death Knight
	7:  (  0,112,222,255), # Shaman
	8:  (105,204,240,255), # Mage
	9:  (148,130,201,255), # Warlock
	10: (  0,255,150,255), # Monk
	11: (255,125, 10,255), # Druid
	12: (163, 48,201,255)  # Demon Hunter
}

# class colors of corresponding class by id as hex-strings
CLASS_COLORS_HEX = {
	1:  'C79C6E', # Warrior
	2:  'F58CBA', # Paladin
	3:  'ABD473', # Hunter
	4:  'FFF569', # Rogue
	5:  'FFFFFF', # Priest
	6:  'C41F3B', # Death Knight
	7:  '0070DE', # Shaman
	8:  '40C7EB', # Mage
	9:  '8787ED', # Warlock
	10: '00FF96', # Monk
	11: 'FF7D0A', # Druid
	12: 'A330C9'  # Demon Hunter
}

# item colors of corresponding item quality by id (as defined by Blizzard)
QUALITY_COLORS = {
	0: (157,157,157,255), # Poor
	1: (255,255,255,255), # Common
	2: ( 30,255,  0,255), # Uncommon
	3: (  0,112,221,255), # Rare
	4: (163, 53,238,255), # Epic
	5: (255,128,  0,255), # Legendary
	6: (230,204,128,255), # Artifact
	7: (  0,204,255,255)  # Heirloom
}

# race names by id
RACES = {
	1: 'Mensch',
	2: 'Orc',
	3: 'Zwerg',
	4: 'Nachtelf',
	5: 'Untoter',
	6: 'Tauren',
	7: 'Gnom',
	8: 'Troll',
	9: 'Goblin',
	10: 'Blutelf',
	11: 'Draenei',
	22: 'Worgen',
	24: 'Pandaren',
	25: 'Pandaren',
	26: 'Pandaren',
	27: 'Nachtgeborener',
	28: 'Hochbergtauren',
	29: 'Leerenelf',
	30: 'Lichtgeschmiedeter Draenei'
}

# class names by id
CLASSES = {
	1: 'Krieger',
	2: 'Paladin',
	3: 'Jäger',
	4: 'Schurke',
	5: 'Priester',
	6: 'Todesritter',
	7: 'Schamane',
	8: 'Magier',
	9: 'Hexenmeister',
	10: 'Mönch',
	11: 'Druide',
	12: 'Dämonenjäger'
}

# descriptive strings of stats in 'individualStats'
STATS = {
	'health': 'Gesundheit',
	'str': 'Stärke',
	'agi': 'Agilität',
	'int': 'Intellekt',
	'sta': 'Stamina',
	'critRating': 'Kritische Trefferchance',
	'hasteRating': 'Tempo',
	'masteryRating': 'Meisterschadt',
	'versatility': 'Vielseitigkeit',
	'armor': 'Rüstung',
	'alteracValleyTowersCaptured': 'Türme im Alteractal verteidigt',
	'alteracValleyTowersDefended': 'Türme im Alteractal erobert',
	'eyeOfTheStormFlagsCaptured': 'Flaggen im Auge des Sturms erobert',
	'warsongGulchFlagsCaptured': 'Flaggen in der Kriegshymnenschlucht erobert',
	'warsongGulchFlagsDefended': 'Flaggen in der Kriegshymnenschlucht verteidigt',
	'battlegroundsPlayed': 'Schlachtfelder gespielt',
	'battlegroundsWon': 'Schlachtfelder gewonnen',
	'duelsWon': 'Duelle gewonnen',
	'duelsLost': 'Duelle verloren',
	'honorableKills': 'Ehrenhafte Siege',
	'honorableKillsAlteracValley': 'Ehrenhafte Siege im Alteractal',
	'honorableKillsArathiBasin': 'Ehrenhafte Siege im Arathibecken',
	'honorableKillsWarsongGulch': 'Ehrenhafte Siege in der Kriegshymnenschlucht',
	'honorableKillsWorld': 'Ehrenhafte Siege in der Welt',
	'drowning': 'Tode durch Ertrinken',
	'dungeon': 'Tode in Dungeons',
	'heroicDungeon': 'Tode in heroischen Dungeons',
	'raid': 'Tode in Schlachtzügen',
	'falling': 'Tode durch Fallschaden',
	'fireAndLava': 'Tode durch Feuer und Lava',
	'otherPlayers': 'Tode durch andere Spieler',
	'total': 'Tode',
	'damageDone': 'Schaden verursacht',
	'damageReceived': 'Schaden erlitten',
	'healingDone': 'Heilung verursacht',
	'healingReceived': 'Heilung erhalten',
	'kills': 'Todesstöße',
	'killsCritters': 'Todesstöße an Kleintieren',
	'flightPathsTaken': 'Flüge',
	'hearthstoneUsed': 'Ruhestein-Nutzungen',
	'portalsTaken': 'Portal genutzt',
	'summonsAccepted': 'Beschwörungen angenommen',
	'cheer': 'Jubel',
	'hug': 'Umarmungen',
	'lol': '"LOL"',
	'ohgod': '"/ohgod"',
	'wave': 'Gewunken',
	'completed': 'Quests abgeschlossen',
	'aborted': 'Quests abgebrochen',
	'dailyCompleted': 'Tägliche Quests abgeschlossen',
	'averagePerDay': 'Durchschnittlich abgeschlossene Quests am Tag',
	'cooking': 'Kochkunst',
	'cookingRecipes': 'Rezepte',
	'fishing': 'Angelkunst',
	'fishCaught': 'Fische geangelt',
	'bandages': 'Verbände genutzt',
	'beverages': 'Getränke getrunken',
	'food': 'Mahlzeiten gegessen',
	'differentBeverages': 'Unterschiedliche Getränke getrunken',
	'differentFoods': 'Unterschiedliche Mahlzeiten gegessen',
	'elixirs': 'Elixiere getrunken',
	'flasks': 'Fläschchen getrunken',
	'healingPotions': 'Heiltränke getrunken',
	'manaPotions': 'Manatränke getrunken',
	'healthstones': 'Gesundheitssteine genutzt',
	'epicsLooted': 'Epische Gegenstände erbeutet',
	'rollsGreed': 'Würfe auf "Gier"',
	'rollsNeed': 'Würfe auf "Bedarf"',
	'exaltedFactions': 'Fraktionen auf ehrfürchtig',
	'petBattlesWon': 'Haustierkämpfe gewonnen'
}