'''
I cannot merge NBA.com stats with Basketball Reference STATS
because:
        1) They count the minutes played differently.
        2) NBA do not differentiate the stats of one player
        that playing for different teams.
'''

import pandas as pd
import numpy as np

BR_PS = pd.read_csv('/Users/mac/GitHub/NBA Optimizing Player Selection/Datasets/BR_PS.csv')
BR_PSalaries = pd.read_csv('/Users/mac/GitHub/NBA Optimizing Player Selection/Datasets/BR_PSalaries.csv')
NBA_PS = pd.read_csv('/Users/mac/GitHub/NBA Optimizing Player Selection/Datasets/NBA_PS.csv')

# Merge all BR database
BR_PS = pd.merge(BR_PS, BR_PSalaries, on = 'Player')
BR_PS = BR_PS[BR_PS['Team_x'] == BR_PS['Team_y']]
BR_PS = BR_PS.drop(columns = 'Team_y')
BR_PS = BR_PS.rename(columns = {'Team_x': 'Team'})

# Preprocessing NBA data
NBA_PS['MP'] = NBA_PS['MIN'] * NBA_PS['GP']
NBA_PS = NBA_PS.rename(columns = {'TEAM': 'Team'})
NBA_PS['Team'] = NBA_PS['Team'].replace(['BKN','CHA','PHX'], ['BRK','CHO','PHO'])
NBA_PS

team = ['CLE','TOR', 'WAS', 'BOS', 'CHI', 'MIA', 'IND', 'BRK', 'CHO', 'ORL',
'NYK', 'MIL', 'ATL', 'DET', 'PHI', 'DAL', 'DEN', 'GSW', 'HOU', 'LAC', 'LAL',
'MEM', 'MIN', 'NOP', 'OKC', 'PHO', 'POR', 'SAC', 'SAS', 'UTA']
top300_BR  = pd.DataFrame()
top300_NBA = pd.DataFrame()

for x in team:
    top300_BR = top300_BR.append(BR_PS.loc[BR_PS['Team'] == '{}'.format(x)].nlargest(10,'MP'))
    top300_NBA = top300_NBA.append(NBA_PS.loc[NBA_PS['Team'] == '{}'.format(x)].nlargest(10,'MP'))
top300_BR.shape
top300_NBA.shape

'''
We have 1 player that played significant amount of games
with more than 1 team: Jeremy Lin
top300_BR.loc[top300_BR['Player'] == 'Jeremy Lin']
top300_BR.loc[top300_BR['Team'] == 'TOR'].nlargest(10,'MP')
top300_BR.loc[top300_BR['Team'] == 'ATL'].nlargest(10,'MP')

top300_NBA.loc[top300_NBA['Player'] == 'Jeremy Lin']



top300_NBA.nlargest(6,'MP')
top300_BR.nlargest(7,'MP')
'''

''' Draymond can be included, but includes Play-off games so might bias the results

DR = pd.read_csv('/Users/mac/GitHub/NBA Optimizing Player Selection/Datasets/Draymond Dataset.csv')
DR = DR.loc[DR['season'] == 2018]
DR = DR.drop(['possessions', 'season'], axis = 1)
DR = DR.rename(columns = {'player': 'Player', 'DRAYMOND': 'Draymond'}).reset_index()
DR.loc[DR['Player'].duplicated()]

'''
