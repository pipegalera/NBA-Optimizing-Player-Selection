import pandas as pd
import numpy as np

BR_PS = pd.read_csv('/Users/mac/GitHub/NBA Optimizing Player Selection/Datasets/BR_PS.csv')
BR_PSalaries = pd.read_csv('/Users/mac/GitHub/NBA Optimizing Player Selection/Datasets/BR_PSalaries.csv')
NBA_PS = pd.read_csv('/Users/mac/GitHub/NBA Optimizing Player Selection/Datasets/NBA_PS.csv')

''' Draymond can be included, but includes Play-off games
draymond = pd.read_csv('/Users/mac/GitHub/NBA_Scrappers/Final Dataset/draymond.csv')
draymond
draymond = draymond.loc[draymond['season'] == 2018]
draymond
draymond = draymond.drop(['possessions', 'season'], axis = 1)
draymond = draymond.rename(columns = {'player': 'Player', 'DRAYMOND': 'Draymond'}).reset_index()
draymond.loc[draymond['Player'].duplicated()]
'''

# Merging datasets
df = pd.merge(stats, salaries, on = 'Player')

# 'Hiring players to play' assumption
df = df[df['Team_x'] == df['Team_y']]
df = df.loc[df['G'] >= 2]

# Renaming columns
df = df.drop(columns = 'Team_y')
df = df.rename(columns = {'Team_x': 'Team'})
sort_names = ['CLE','TOR', 'WAS', 'BOS', 'CHI', 'MIA', 'IND', 'BRK', 'CHO', 'ORL', 'NYK', 'MIL', 'ATL', 'DET', 'PHI', 'DAL', 'DEN', 'GSW', 'HOU', 'LAC', 'LAL', 'MEM', 'MIN', 'NOP', 'OKC', 'PHO', 'POR', 'SAC', 'SAS', 'UTA']
long_names = ['Cleveland Cavaliers','Toronto Raptors', 'Washington Wizards', 'Boston Celtics', 'Chicago Bulls', 'Miami Heat', 'Indiana Pacers', 'Brooklyn Nets', 'Charlotte Hornets', 'Orlando Magic', 'New York Knicks', 'Milwaukee Bucks', 'Atlanta Hawks', 'Detroit Pistons', 'Philadelphia 76ers', 'Dallas Mavericks', 'Denver Nuggets', 'Golden State Warriors', 'Houston Rockets', 'LA Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'Oklahoma City Thunder', 'Phoenix Suns', 'Portland Trail Blazers', 'Sacramento Kings', 'San Antonio Spurs', 'Utah Jazz']
df['Team'] = df['Team'].replace(sort_names, long_names)

df.to_csv('/Users/mac/GitHub/NBA_Scrappers/Final Dataset/Final_Data.csv', index=False)
df.head()

# NECESITO EL OFFENSIVE AND DEFENSIVE RATING INDIVIDUAL, POR LO QUE TENGO QUE MERGE STATS 1 y 2 (RB y NBA.com)

stats_2
stats.shape
