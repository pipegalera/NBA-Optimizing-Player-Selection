from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

#######################
# Advanced Statistics #
#######################

url = "https://www.basketball-reference.com/leagues/NBA_2019_advanced.html"

# Opening up connection, grabbing the page
html = urlopen(url)
soup = BeautifulSoup(html)

# Getting headers and removing incorrect columns
headers_files = soup.findAll('tr')[0]
headers = [i.getText() for i in headers_files.findAll('th')]
headers.remove('\xa0')
headers.remove('\xa0')
headers.remove('Rk')
headers = ['Team' if x == 'Tm' else x for x in headers]
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

url2 = 'https://www.basketball-reference.com/leagues/NBA_2019_per_poss.html'
html = urlopen(url2)
soup = BeautifulSoup(html)
headers_files = soup.findAll('tr')[0]
headers = [i.getText() for i in headers_files.findAll('th')]
headers.remove('Rk')
headers = ['Team' if x == 'Tm' else x for x in headers]
rows = soup.findAll('tr')[1:]
stats = [[i.getText() for i in rows[x].findAll('td')]
            for x in range(len(rows))]
stats = pd.DataFrame(stats).dropna()
stats.columns = headers
stats = stats.drop(columns = ['', 'Age', 'G', 'MP'],axis = 1)

'''
test should be True before merging
stats['Player'].loc[565] == adv_stats['Player'].loc[565]
'''

merge = pd.merge(stats, adv_stats, on = 'Player')
merge = merge[merge['Team_x'] == merge['Team_y']].reset_index(drop = True)
merge.shape
merge.loc[merge.Team_x == 'IND'][['Player', 'MP']]
merge
###################################
#  Salaries                       #
###################################

url = "https://www.basketball-reference.com/contracts/players.html"
html = urlopen(url)
soup = BeautifulSoup(html)
headers = ['Player', 'Team', 'Salary 2018-19', 'Salary 2019-20', 'Salary 2020-21', 'Salary 2021-22', 'Salary 2022-23', 'Salary 2023-24', 'Signed Using', 'Guaranteed']
rows = soup.findAll('tr')[1:]
salaries = [[td.getText() for td in rows[i].findAll('td')]
            for i in range(len(rows))]

salaries = pd.DataFrame(salaries, columns = headers).dropna()
salaries = salaries.apply(lambda x: x.str.replace('$', ''))
salaries = salaries.apply(lambda x: x.str.replace(',', ''))

# Handleling missing data
salaries['Salary 2019-20'] = salaries['Salary 2019-20'].replace('', 0)
salaries['Salary 2020-21'] = salaries['Salary 2020-21'].replace('', 0)
salaries['Salary 2021-22'] = salaries['Salary 2021-22'].replace('', 0)
salaries['Salary 2022-23'] = salaries['Salary 2022-23'].replace('', 0)
salaries['Salary 2023-24'] = salaries['Salary 2023-24'].replace('', 0)
salaries['Guaranteed'] = salaries['Guaranteed'].replace('', 0)
salaries['Signed Using'] = salaries['Signed Using'].replace('', 'Other')

# Changing the type from objects to integers
salaries['Salary 2018-19'] = salaries['Salary 2018-19'].astype('int')
salaries['Salary 2019-20'] = salaries['Salary 2019-20'].astype('int')
salaries['Salary 2020-21'] = salaries['Salary 2020-21'].astype('int')
salaries['Salary 2021-22'] = salaries['Salary 2021-22'].astype('int')
salaries['Salary 2022-23'] = salaries['Salary 2022-23'].astype('int')
salaries['Salary 2023-24'] = salaries['Salary 2023-24'].astype('int')
salaries['Guaranteed'] = salaries['Guaranteed'].astype('int')

# Agregating the contracts within the same team
salaries = salaries.groupby(['Player', 'Team', 'Guaranteed'], as_index = False ).sum()

''' test if it worked checking with hoop
salaries.loc[salaries['Player'] == 'Dwight Howard']
salaries.loc[salaries['Player'] == 'Cameron Reynolds']
'''
salaries.columns
#########################################
#  Merging Salaries with all the stats  #
#########################################
data_players = pd.merge(merge, salaries, on = 'Player')
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


# Create First and second units

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
