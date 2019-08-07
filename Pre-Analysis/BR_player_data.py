import pandas as pd
import numpy as np

BR_PS = pd.read_csv('/Users/mac/GitHub/Optimizing-NBA-Player-Selection/Datasets/BR_PS.csv')
BR_PSalaries = pd.read_csv('/Users/mac/GitHub/Optimizing-NBA-Player-Selection/Datasets/BR_PSalaries.csv')
NBA_PS = pd.read_csv('/Users/mac/GitHub/Optimizing-NBA-Player-Selection/Datasets/NBA_PS.csv')

# Merging BR_PS and BR_PSalaries
data_players = pd.merge(BR_PS, BR_PSalaries, on = 'Player')
data_players.reset_index(drop = True, inplace = True)
data_players = data_players.drop(columns = 'index', axis = 1)

# 'Hiring players to play' assumption
# data_players.columns
data_players = data_players[data_players['Team_x'] == data_players['Team']]
data_players = data_players.loc[data_players['G'] >= 2]
data_players.shape

# Renaming columns and cleaning Dataframe
data_players = data_players.drop(columns = 'Team')
data_players = data_players.rename(columns = {'Team_x': 'Team'})
sort_names = ['CLE','TOR', 'WAS', 'BOS', 'CHI', 'MIA', 'IND', 'BRK', 'CHO', 'ORL', 'NYK', 'MIL',
'ATL', 'DET', 'PHI', 'DAL', 'DEN', 'GSW', 'HOU', 'LAC', 'LAL', 'MEM', 'MIN', 'NOP', 'OKC', 'PHO',
'POR', 'SAC', 'SAS', 'UTA']
teams = ['Cleveland Cavaliers','Toronto Raptors', 'Washington Wizards', 'Boston Celtics',
'Chicago Bulls', 'Miami Heat', 'Indiana Pacers', 'Brooklyn Nets', 'Charlotte Hornets',
'Orlando Magic', 'New York Knicks', 'Milwaukee Bucks', 'Atlanta Hawks', 'Detroit Pistons',
'Philadelphia 76ers', 'Dallas Mavericks', 'Denver Nuggets', 'Golden State Warriors',
'Houston Rockets', 'Los Angeles Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies',
'Minnesota Timberwolves', 'New Orleans Pelicans', 'Oklahoma City Thunder', 'Phoenix Suns',
'Portland Trail Blazers', 'Sacramento Kings', 'San Antonio Spurs', 'Utah Jazz']

data_players['Team'] = data_players['Team'].replace(sort_names, teams)

data_players.to_csv('/Users/mac/GitHub/Optimizing-NBA-Player-Selection/Datasets/BR_players_data.csv', index=False)
