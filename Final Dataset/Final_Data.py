

# Lo ultimo que has hecho es salaries bien, Mira si el merge se hace bien con stats.
# Despues, mira si puedes incorporar stats_2 de nba.com, sino no te comas la cabeza.

import pandas as pd
import numpy as np

stats = pd.read_csv('/Users/mac/GitHub/NBA_Scrappers/Advanced Stats/Advanced_stats_NBA.csv')
salaries = pd.read_csv('/Users/mac/GitHub/NBA_Scrappers/Salaries/Salaries_scrapper_NBA.csv')

''' Draymond ?
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

# Players that play assumption
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
