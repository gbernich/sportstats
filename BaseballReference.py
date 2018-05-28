### Libraries ###
import requests
from bs4 import BeautifulSoup
import sys

### Objects ###
class Pitcher:

	def __init__(self, name, stats):
		self.name                 = name 
		self.record               = Record()
		self.record.wins          = stats['wins']
		self.record.losses        = stats['losses']
		self.record.winPercentage = "%.3f" % (float(stats['wins'])/float(stats['gamesStarted']))

class Game:
	
	def __init__(self, stats):
		self.gameID         = stats['gameID']
		self.opponentID     = stats['opponentID']
		self.result         = stats['result']
		self.runsScored     = stats['runsScored']
		self.runsAllowed    = stats['runsAllowed']
		self.record         = stats['record']
		self.gamesBack      = stats['gamesBack']
		self.winningPitcher = stats['winningPitcher']
		self.losingPitcher  = stats['losingPitcher']
		self.dayNight       = stats['dayNight']
		self.streak         = stats['streak']

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
		self.record       = Record()
		self.homeRecord   = Record()
		self.awayRecord   = Record()
		self.recordByTeam = {}

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


### Functions to Create Objects
def ParseSchedule(team):

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
