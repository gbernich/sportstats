from BaseballReference import *

# Example to get information about a team's record
orioles = Team('BAL')
ParseSchedule(orioles)

print("total record: %2d-%2d (%.3f)" % (orioles.record.wins,     orioles.record.losses,     orioles.record.winPercentage))
print("home  record: %2d-%2d (%.3f)" % (orioles.homeRecord.wins, orioles.homeRecord.losses, orioles.homeRecord.winPercentage))
print("away  record: %2d-%2d (%.3f)" % (orioles.awayRecord.wins, orioles.awayRecord.losses, orioles.awayRecord.winPercentage))

print("Against Yankees: (%.3f)" % (orioles.recordByTeam['NYY'].winPercentage))
print("Against Rays:    (%.3f)" % (orioles.recordByTeam['TBR'].winPercentage))

# Get Pitcher Stats
pitcher  = ParsePitcher('chris tillman')
print('Chris Tillman Win Percentage: %s' %  pitcher.record.winPercentage)