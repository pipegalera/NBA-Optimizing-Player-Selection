import pandas as pd
import numpy as np

BR_PS = pd.read_csv('/Users/mac/GitHub/Optimizing-NBA-Player-Selection/Datasets/BR_PS.csv')
BR_PSalaries = pd.read_csv('/Users/mac/GitHub/Optimizing-NBA-Player-Selection/Datasets/BR_PSalaries.csv')
NBA_PS = pd.read_csv('/Users/mac/GitHub/Optimizing-NBA-Player-Selection/Datasets/NBA_PS.csv')


# Merging BR_PS and BR_PSalaries
df = pd.merge(BR_PS, BR_PSalaries, on = 'Player')
df.shape
# 'Hiring players to play' assumption
df.columns
df = df[df['Team_x'] == df['Team']]
df = df.loc[df['G'] >= 2]
df.shape

# Renaming columns and cleaning Dataframe
df = df.drop(columns = 'Team')
df = df.rename(columns = {'Team_x': 'Team'})
sort_names = ['CLE','TOR', 'WAS', 'BOS', 'CHI', 'MIA', 'IND', 'BRK', 'CHO', 'ORL', 'NYK', 'MIL',
'ATL', 'DET', 'PHI', 'DAL', 'DEN', 'GSW', 'HOU', 'LAC', 'LAL', 'MEM', 'MIN', 'NOP', 'OKC', 'PHO',
'POR', 'SAC', 'SAS', 'UTA']
long_names = ['Cleveland Cavaliers','Toronto Raptors', 'Washington Wizards', 'Boston Celtics',
'Chicago Bulls', 'Miami Heat', 'Indiana Pacers', 'Brooklyn Nets', 'Charlotte Hornets',
'Orlando Magic', 'New York Knicks', 'Milwaukee Bucks', 'Atlanta Hawks', 'Detroit Pistons',
'Philadelphia 76ers', 'Dallas Mavericks', 'Denver Nuggets', 'Golden State Warriors',
'Houston Rockets', 'Los Angeles Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies',
'Minnesota Timberwolves', 'New Orleans Pelicans', 'Oklahoma City Thunder', 'Phoenix Suns',
'Portland Trail Blazers', 'Sacramento Kings', 'San Antonio Spurs', 'Utah Jazz']

df['Team'] = df['Team'].replace(sort_names, long_names)
df.to_csv('/Users/mac/GitHub/Optimizing-NBA-Player-Selection/Datasets/BR_players_data.csv', index=False)
df.shape
