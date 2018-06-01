### Libraries ###
import requests
from bs4 import BeautifulSoup
import sys

### Objects ###
class Pitcher:

	def __init__(self, name, stats):
		self.name                 = name 
		self.record               = Record()
		self.record.wins          = int(stats['wins'])
		self.record.losses        = int(stats['losses'])
		#self.record.winPercentage = float(stats['wins'])/float(stats['gamesStarted'])

		self.hits            = 0
		self.earnedRunAvg   = 0.0
		self.earnedRuns      = 0
		self.strikeouts      = 0
		self.walks           = 0
		self.inningsPitched  = 0
		self.homeRunsAllowed = 0

class Game:
	
	def __init__(self, stats):
		self.gameID         = stats['gameID']
		self.opponentID     = stats['opponentID']
		self.result         = stats['result']
		self.runsScored     = int(stats['runsScored'])
		self.runsAllowed    = int(stats['runsAllowed'])
		self.runsDiff       = self.runsScored - self.runsAllowed
		self.record         = stats['record']
		self.gamesBack      = stats['gamesBack']
		self.winningPitcher = stats['winningPitcher']
		self.losingPitcher  = stats['losingPitcher']
		self.dayNight       = stats['dayNight']

		if ( '+' in stats['streak'] ):
			self.streak = len(stats['streak'])
		else:
			self.streak = -1 * len(stats['streak'])

		if ( stats['homeAway'] == '@'):
			self.homeAway = 'A'
		else:
			self.homeAway = 'H'

class Record:

	def __init__(self):
		self.wins          = 0
		self.losses        = 0
		self.totalGames    = 0
		self.winPercentage = 0

	def addWin(self):
		self.wins       += 1
		self.totalGames += 1
		self.updateWinPercentage()

	def addLoss(self):
		self.losses     += 1
		self.totalGames += 1
		self.updateWinPercentage()

	def updateWinPercentage(self):
		self.winPercentage = self.wins / self.totalGames

class Team:
	
	def __init__(self, team):
		self.teamID       = team
		self.games        = []
		self.nextGame     = None
		self.record       = Record()
		self.homeRecord   = Record()
		self.awayRecord   = Record()
		self.recordByTeam = {}
		self.nextGame     = Preview(self)

	def addGame(self, game):
		self.games.append(game)

		if ('W' in game.result):
			self.record.addWin()
			if ( game.homeAway == 'A'):
				self.awayRecord.addWin()
			else:
				self.homeRecord.addWin()
		elif ('L' in game.result):
			self.record.addLoss()
			if ( game.homeAway == 'A'):
				self.awayRecord.addLoss()
			else:
				self.homeRecord.addLoss()

		self.updateRecordByTeam(game)

	def updateRecordByTeam(self, game):
		if (game.opponentID in self.recordByTeam.keys()):
			if ('W' in game.result):
				self.recordByTeam[game.opponentID].addWin()
			else:
				self.recordByTeam[game.opponentID].addLoss()
		else:
			self.recordByTeam[game.opponentID] = Record()
			if ('W' in game.result):
				self.recordByTeam[game.opponentID].addWin()
			else:
				self.recordByTeam[game.opponentID].addLoss()

	def getGamesByRunDifferential(self, aboveBelow, diff):

		games = []

		for game in self.games:
			if (aboveBelow == 'above'):
				if (int(game.runsDiff) > diff):
					games.append(game)
			else:
				if (int(game.runsDiff) < diff):
					games.append(game)

		return games

class Preview:
	
	def __init__(self, team):
		self.url = ''
		self.team = team
		self.homePitcher = None
		self.awayPitcher = None

	def ParsePreview(self, url, homeAway):
		self.url = url

		# Load webpage data
		session   = requests.Session()
		#url       = 'https://www.baseball-reference.com/previews/' + year + '/' + teamID + year + month + day +'0.shtml'
		response  = session.get(self.url)
		
		# Remove comments in HTML
		source = response.text
		source = source.replace('<div class="placeholder"></div>\n<!--', '<div class="placeholder"></div>\n')
		#source = source.replace('-->', '')

		rows   = BeautifulSoup(source, "html.parser").findAll('th', {'data-stat':'split_name'})
		foundAwayTeam = False
		#print(rows)

		for row in rows:
			try:
				contents = row.string
			except:
				contents = ''

			if contents != None:
				if '2018' == contents:
					# This either the home or away pitcher
					stats = {}
					stats['era'] = BeautifulSoup(str(row.parent), "html.parser").find('td', {'data-stat':'earned_run_avg'}).string
					winsLosses   = BeautifulSoup(str(row.parent), "html.parser").find('td', {'data-stat':'DECISION'}).string
					stats['wins']   = winsLosses.split('-')[0]
					stats['losses'] = winsLosses.split('-')[1]		

					stats['hits']            = BeautifulSoup(str(row.parent), "html.parser").find('td', {'data-stat':'H'}).string
					stats['earnedRuns']      = BeautifulSoup(str(row.parent), "html.parser").find('td', {'data-stat':'ER'}).string
					stats['strikeouts']      = BeautifulSoup(str(row.parent), "html.parser").find('td', {'data-stat':'SO'}).string
					stats['walks']           = BeautifulSoup(str(row.parent), "html.parser").find('td', {'data-stat':'BB'}).string
					stats['inningsPitched']  = BeautifulSoup(str(row.parent), "html.parser").find('td', {'data-stat':'IP'}).string
					stats['homeRunsAllowed'] = BeautifulSoup(str(row.parent), "html.parser").find('td', {'data-stat':'HR'}).string


					if ( not foundAwayTeam ):
						self.awayPitcher                 = Pitcher('', stats)
						self.awayPitcher.hits            = stats['hits']
						self.awayPitcher.earnedRunAvg    = stats['era']
						self.awayPitcher.earnedRuns      = stats['earnedRuns']
						self.awayPitcher.strikeouts      = stats['strikeouts']
						self.awayPitcher.walks           = stats['walks']
						self.awayPitcher.inningsPitched  = stats['inningsPitched']
						self.awayPitcher.homeRunsAllowed = stats['homeRunsAllowed']
						foundAwayTeam = True
					else:
						self.homePitcher                 = Pitcher('', stats)
						self.homePitcher.hits            = stats['hits']
						self.homePitcher.earnedRunAvg    = stats['era']
						self.homePitcher.earnedRuns      = stats['earnedRuns']
						self.homePitcher.strikeouts      = stats['strikeouts']
						self.homePitcher.walks           = stats['walks']
						self.homePitcher.inningsPitched  = stats['inningsPitched']
						self.homePitcher.homeRunsAllowed = stats['homeRunsAllowed']


### Functions to Create Objects
def ParseSchedule(team):

	# Initalizations
	foundNextGame = False

	# Load webpage data
	session  = requests.Session()
	url      = 'https://www.baseball-reference.com/teams/' + team.teamID + '/2018-schedule-scores.shtml'
	response = session.get(url)

	# Parse games
	table    = BeautifulSoup(response.text, "html.parser").find('tbody')
	gameRows = BeautifulSoup(str(table),    "html.parser").findAll('tr')

	for row in gameRows:

		# Make sure there is a valid bs4 object
		try:
			stat = BeautifulSoup(str(row), "html.parser").find('td', {'data-stat':'win_loss_result'}).string
		except:
			if ( not foundNextGame ):
				try:
					stats = {}
					stats['homeAway'] = BeautifulSoup(str(row), "html.parser").find('td', {'data-stat':'homeORvis'}).string
					if ( stats['homeAway'] == '@'):
						homeAway = 'A'
					else:
						homeAway = 'H'

					url = BeautifulSoup(str(row), "html.parser").find('td', {'data-stat':'boxscore'}).find('a')['href']
					url = 'https://www.baseball-reference.com/previews/2018/BAL201806010.shtml'
					#url = 'https://www.baseball-reference.com' + url
					foundNextGame = True
				except:
					continue
				if (foundNextGame):
					team.nextGame.ParsePreview(url, homeAway)

			continue

		# Make sure this is not None type
		if (stat == None):
			continue

		# Create Game from data
		try:
			stats = {}
			stats['gameID']          = BeautifulSoup(str(row), "html.parser").find('th', {'data-stat':'team_game'}).string
			stats['opponentID']      = BeautifulSoup(str(row), "html.parser").find('td', {'data-stat':'opp_ID'}).string
			stats['result']          = BeautifulSoup(str(row), "html.parser").find('td', {'data-stat':'win_loss_result'}).string
			stats['runsScored']      = BeautifulSoup(str(row), "html.parser").find('td', {'data-stat':'R'}).string
			stats['runsAllowed']     = BeautifulSoup(str(row), "html.parser").find('td', {'data-stat':'RA'}).string
			stats['record']          = BeautifulSoup(str(row), "html.parser").find('td', {'data-stat':'win_loss_record'}).string
			stats['gamesBack']       = BeautifulSoup(str(row), "html.parser").find('td', {'data-stat':'games_back'}).string
			stats['winningPitcher']  = BeautifulSoup(str(row), "html.parser").find('td', {'data-stat':'winning_pitcher'}).string
			stats['losingPitcher']   = BeautifulSoup(str(row), "html.parser").find('td', {'data-stat':'losing_pitcher'}).string
			stats['dayNight']        = BeautifulSoup(str(row), "html.parser").find('td', {'data-stat':'day_or_night'}).string
			stats['streak']          = BeautifulSoup(str(row), "html.parser").find('td', {'data-stat':'win_loss_streak'}).string
			stats['homeAway']        = BeautifulSoup(str(row), "html.parser").find('td', {'data-stat':'homeORvis'}).string
		except: # catch all
			e = sys.exc_info()[0]
			print( "Error: %s" % e )
			#print(row)
			continue

		team.addGame(Game(stats))


#def ParsePreview(teamID, year, month, day):
# def ParsePreview(url):
# 	# Load webpage data
# 	session   = requests.Session()
# 	#url       = 'https://www.baseball-reference.com/previews/' + year + '/' + teamID + year + month + day +'0.shtml'
# 	response  = session.get(url)
	
# 	# Remove comments in HTML
# 	source = response.text
# 	source = source.replace('<div class="placeholder"></div>\n<!--', '<div class="placeholder"></div>\n')
# 	#source = source.replace('-->', '')

# 	rows   = BeautifulSoup(source, "html.parser").findAll('th', {'data-stat':'split_name'})

# 	for row in rows:
# 		print(str(row.parent))

def ParsePitcher(pitcher):

	# Load webpage data
	session   = requests.Session()
	firstname = pitcher.split(' ')[0]
	lastname  = pitcher.split(' ')[1]
	initial   = lastname[0]
	url       = 'https://www.baseball-reference.com/players/' + initial + '/' + lastname[0:5] + firstname[0:2] + '01.shtml'
	response  = session.get(url)

	# Parse pitching stats
	table = BeautifulSoup(response.text, "html.parser").find('tr', {'id':'pitching_standard.2018'})

	stats = {}
	stats['wins']         = BeautifulSoup(str(table), "html.parser").find('td', {'data-stat':'W'}).string
	stats['losses']       = BeautifulSoup(str(table), "html.parser").find('td', {'data-stat':'L'}).string
	stats['gamesStarted'] = BeautifulSoup(str(table), "html.parser").find('td', {'data-stat':'GS'}).string

	return Pitcher(pitcher, stats)
