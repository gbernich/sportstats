from BaseballReference import *

# Example to get information about a team's record
orioles = Team('BAL')
ParseSchedule(orioles)

print("total record: %2d-%2d (%.3f)" % (orioles.record.wins,     orioles.record.losses,     orioles.record.winPercentage))
print("home  record: %2d-%2d (%.3f)" % (orioles.homeRecord.wins, orioles.homeRecord.losses, orioles.homeRecord.winPercentage))
print("away  record: %2d-%2d (%.3f)" % (orioles.awayRecord.wins, orioles.awayRecord.losses, orioles.awayRecord.winPercentage))