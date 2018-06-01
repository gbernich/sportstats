import matplotlib.pyplot as plt
import numpy as np
import matplotlib

from BaseballReference import *

################################################################
# Choose a team
teamID  = 'BAL'
orioles = Team(teamID)
ParseSchedule(orioles)

print(orioles.nextGame.awayPitcher.earnedRunAvg)
print(orioles.nextGame.awayPitcher.hits)
print(orioles.nextGame.awayPitcher.earnedRuns)
print(orioles.nextGame.awayPitcher.strikeouts)
print(orioles.nextGame.awayPitcher.walks)
print(orioles.nextGame.awayPitcher.inningsPitched)
print(orioles.nextGame.awayPitcher.homeRunsAllowed)

# Sort data by "Lost by 2 or more" and "rest of games"
# Look at games where they lost by more than 1.5 runs
games1 = orioles.getGamesByRunDifferential('below', -1.5)

# Look at games where they won or lost by less than 1.5 runs
games2 = orioles.getGamesByRunDifferential('above', -1.5)

################################################################
# Format data using numpy
N = 50
data1 = np.empty([2,N])
data2 = np.empty([2,N])

for x in range(0, N):
	data1[0, x] = x
	data1[1, x] = 1.0 * x

	data2[0, x] = x
	data2[1, x] = 2.0 * x

data1 = np.empty([2,len(games1)])
for n in range(0, len(games1)):
	data1[0, n] = games1[n].runsDiff
	data1[1, n] = games1[n].streak

data2 = np.empty([2,len(games2)])
for n in range(0, len(games2)):
	data2[0, n] = games2[n].runsDiff
	data2[1, n] = games2[n].streak

################################################################
# Plot stats

# Get data for plots
# x1 = np.arange(0.0, 50.0, 2.0)
# x2 = np.arange(0.0, 50.0, 2.0)
# y1 = x1 * 1.0
# y2 = x2 * 2.0

# Plot data
# plt.scatter(data1[0,:], data1[1,:], c="r", alpha=0.5,label="< -1.5")
# plt.scatter(data2[0,:], data2[1,:], c="b", alpha=0.5,label="> -1.5")
# plt.xlabel("Run Diff.")
# plt.ylabel("Streak")
# plt.legend(loc=2)
# plt.show()