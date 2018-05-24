import mlbgame


for day in range(1,3):
	month = mlbgame.games(2018, 5, day, away='Orioles', home='Orioles')
	games = mlbgame.combine_games(month)
	for game in games:
	    print(game)