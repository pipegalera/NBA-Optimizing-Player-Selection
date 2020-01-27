"""
title: "NBA Scrapers"
author: "Pipe Galera"
Last data: "27/01/2020"
"""


from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

#######################
# Advanced Statistics #
#######################

url_list = []
year = range(2001,2019)

for i in 2019: # Choose the year
    url = "https://www.basketball-reference.com/leagues/NBA_{}_advanced.html".format(i)
    url_list.append(url)

# Opening up connection, grabbing the page
html = urlopen(url)
soup = BeautifulSoup(html)

'''
To know what to specifically look for you should inspect the webpage. For
example, in this "soup" the headers of the dataset are within the class "tr"
'''

# Getting headers and removing incorrect named columns
headers_files = soup.findAll('tr')[0]
headers = [i.getText() for i in headers_files.findAll('th')]
headers.remove('\xa0')
headers.remove('\xa0')
headers.remove('Rk')
headers = ['Team' if x == 'Tm' else x for x in headers]
headers

# Getting the body
rows = soup.findAll('tr')[1:]
stats = [[i.getText() for i in rows[x].findAll('td')]
            for x in range(len(rows))]
adv_stats = pd.DataFrame(stats).dropna()

adv_stats = adv_stats.drop([18, 23], axis = 1)
adv_stats.columns = headers

###################################
#  Statistics per 100 posessions  #
###################################

for i in 2019:
    url = 'https://www.basketball-reference.com/leagues/NBA_{}_per_poss.html'.format(i)
    url_list.append(url)

# Getting headers and removing incorrect named columns
html = urlopen(url)
soup = BeautifulSoup(html)
headers_files = soup.findAll('tr')[0]
headers = [i.getText() for i in headers_files.findAll('th')]
headers.remove('Rk')
headers = ['Team' if x == 'Tm' else x for x in headers]

# Getting the body
rows = soup.findAll('tr')[1:]
stats = [[i.getText() for i in rows[x].findAll('td')]
            for x in range(len(rows))]
stats = pd.DataFrame(stats).dropna()

stats.columns = headers
stats = stats.drop(columns = ['', 'Age', 'G', 'MP'],axis = 1)

"""
Test: The following boolean should be True before merging
stats['Player'].loc[565] == adv_stats['Player'].loc[565]
"""

all_stats = pd.merge(stats, adv_stats, on = 'Player')
all_stats['Team_x'] == all_stats['Team_y']
all_stats.shape
all_stats = all_stats[all_stats['Team_x'] == all_stats['Team_y']].reset_index(drop = True)
all_stats.shape

###################################
#  Salaries                       #
###################################
"""
DISCLAIMER: Basketball reference update the webpage of contracts, so I have used the
archive of the webpage
"""
# Getting headers and removing incorrect named columns
url = "https://web.archive.org/web/20181214210832/https://www.basketball-reference.com/contracts/players.html"
html = urlopen(url)
soup = BeautifulSoup(html)
headers = ['Player', 'Team', 'Salary 2018-19', 'Salary 2019-20', 'Salary 2020-21', 'Salary 2021-22', 'Salary 2022-23', 'Salary 2023-24', 'Signed Using', 'Guaranteed']

# Getting the body
rows = soup.findAll('tr')[1:]
salaries = [[td.getText() for td in rows[i].findAll('td')]
            for i in range(len(rows))]
salaries = pd.DataFrame(salaries, columns = headers).dropna()
salaries = salaries.apply(lambda x: x.str.replace('$', ''))
salaries = salaries.apply(lambda x: x.str.replace(',', ''))

# Cleaning missing data
cleaning = ['Salary 2018-19', 'Salary 2019-20', 'Salary 2020-21', 'Salary 2021-22', 'Salary 2022-23', 'Salary 2023-24', 'Guaranteed']

for i in cleaning:
    salaries[i] = salaries[i].replace('', 0)
salaries['Signed Using'] = salaries['Signed Using'].replace('', 'NaN')

# Changing the type from objects to integers
for i in cleaning:
    salaries[i] = salaries[i].astype('int')
"""
Agregating the contracts within the same team.
salaries = salaries.groupby(['Player', 'Team', 'Guaranteed'], as_index = False ).sum()
salaries.loc[salaries.Player == "Dwight Howard"]
salaries = salaries.groupby(['Player', 'Team', 'Guaranteed'], as_index = False ).sum()
salaries.loc[salaries.Player == "Dwight Howard"]
"""
#########################################
#  Merging Salaries with all the stats  #
#########################################

data_players = pd.merge(all_stats, salaries, on = 'Player')
data_players.reset_index(drop = True, inplace = True)

# 'Hiring players to play' assumption
data_players.columns
data_players = data_players[data_players['Team_x'] == data_players['Team']]
data_players = data_players[data_players['Pos_x'] == data_players['Pos_y']]

data_players.shape
data_players = data_players.drop(columns = ['Team_y', 'Pos_y', 'Team'])
data_players.columns
data_players = data_players.rename(columns = {'Team_x': 'Team','Pos_x': 'Position'})
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
data_players.reset_index(drop = True)
data_players.columns
data_players.to_csv('/Users/mac/GitHub/Optimizing-NBA-Player-Selection/Datasets/BR_players_data.csv', index = False)
data_players = pd.read_csv('/Users/mac/GitHub/Optimizing-NBA-Player-Selection/Datasets/BR_players_data.csv')


################################################
#  Creating columns for first and second unit  #
################################################

list_teams = data_players.Team.unique().tolist()
fu = pd.DataFrame()
su = pd.DataFrame()
for i in list_teams:
    fu = fu.append(data_players.loc[data_players['Team'] == '{}'.format(i)].nlargest(5,'MP'))
    fu['Role'] = 'FU'
    su = su.append(data_players.loc[data_players['Team'] == '{}'.format(i)].nlargest(5,'MP').drop(data_players.loc[data_players['Team'] == '{}'.format(i)].nlargest(10, 'MP').index[:5]))
    su['Role'] = 'SU'


data_optimization = pd.concat([fu,su])
data_optimization.to_csv('/Users/mac/GitHub/Optimizing-NBA-Player-Selection/Datasets/BR_players_data_optimization.csv', index = False )

data_players.loc[data_players['Team'] == '{}'.format('Miami Heat')].nlargest(6,'MP')
