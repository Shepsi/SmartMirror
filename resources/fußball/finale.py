from datetime import datetime, timedelta
import urllib2, json
url = urllib2.urlopen('https://raw.githubusercontent.com/lsv/fifa-worldcup-2018/master/data.json')
obj = json.load(url)

round16matches = obj["knockout"]["round_16"]["matches"]
round8matches = obj["knockout"]["round_8"]["matches"]
round4matches = obj["knockout"]["round_4"]["matches"]
round2matches = obj["knockout"]["round_2"]["matches"]

teams = obj["teams"]
teamDic = {}

# For easy access to team.
for team in teams:
	w1 = {team["id"] : team["fifaCode"]}
	teamDic.update(w1)

def getTeam(teamId):
	try:
		return teamDic[teamId]
	except KeyError:
		return " "

def writeGroup(matchgroup, name):
	countvariable = 0
	for match in matchgroup:
		countvariable = countvariable + 1
		# full_date (2018-07-03T21:00:00+03:00)
		full_date = match["date"]
		# Get Date ('2018-07-03')
		date_split = full_date[:10]
		# Get Time ('21:00')
		time_split = full_date[11:-9]
		
		# Convert whole string to datetime
		dateObject = datetime.strptime(date_split + " " + time_split, '%Y-%m-%d %H:%M')
		
		# Time difference is different for a few stations and is listed ad the end of full date
		timeDiff = int(full_date[21]) - 2
		dateObject = dateObject - timedelta(hours=timeDiff)

		with open(name+str(countvariable)+'.txt','w') as file:
			fileInput = dateObject.strftime("%d.%m.%Y\n")
			fileInput = fileInput + (dateObject.strftime("%H:%M\n"))
			fileInput = fileInput + getTeam(match["home_team"]) + " - " + getTeam(match["away_team"]) + "\n"
			
			if match["home_result"] is None or match["away_result"] is None:
				fileInput = fileInput + ("-- : --")
			else:
				fileInput = fileInput + str(match["home_result"]) + " : " + str(match["away_result"])

			file.write(fileInput)
			
writeGroup(round16matches, "Achtelfinale")
writeGroup(round8matches, "Viertelfinale")
writeGroup(round4matches, "Halbfinale")
writeGroup(round2matches, "Finale")
