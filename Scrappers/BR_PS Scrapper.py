# @Author: Pipe galera
# @Date:   05-04-2020
# @Email:  pipegalera@gmail.com
# @Last modified by:   Pipe galera
# @Last modified time: 06-04-2020



"""
title: "NBA Scrapers"
author: "Pipe Galera"
Last data: "27/01/2020"
"""


from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import os
os.chdir("/Users/fgm.si/Documents/GitHub/Optimizing-NBA-Player-Selection")
# Scraping the Datasets

###################################
#   Basketball reference data     #
###################################

# Advanced Statistics

url_list = []
year = range(2001,2021)

for i in year:
    url = "https://www.basketball-reference.com/leagues/NBA_{}_advanced.html".format(i)
    url_list.append(url)

url_list

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


# Getting the body
rows = soup.findAll('tr')[1:]
stats = [[i.getText() for i in rows[x].findAll('td')]
            for x in range(len(rows))]
adv_stats = pd.DataFrame(stats).dropna()

adv_stats = adv_stats.drop([18, 23], axis = 1)
adv_stats.columns = headers
adv_stats

#  Statistics per 100 posessions  #


for i in year:
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
Test: The following boolean should be True before merging:
stats['Player'].loc[565] == adv_stats['Player'].loc[565]
Try other numbers
"""
stats
all_stats = pd.merge(stats, adv_stats, on = ["Player", "Team", "Pos"])
all_stats.shape

###################################
#  Salaries                       #
###################################
"""
DISCLAIMER: Basketball reference update the webpage of contracts, so I have used the archive of the webpage
"""
# Getting headers and removing incorrect named columns
url = "https://web.archive.org/web/20200229105705/https://www.basketball-reference.com/contracts/players.html"
html = urlopen(url)
soup = BeautifulSoup(html)
headers = ['Player', 'Team', 'Salary 2019-20', 'Salary 2020-21', 'Salary 2021-22', 'Salary 2022-23', 'Salary 2023-24', 'Salary 2023-2024', 'Signed Using', 'Guaranteed']

# Getting the body
rows = soup.findAll('tr')[1:]
salaries = [[td.getText() for td in rows[i].findAll('td')]
            for i in range(len(rows))]
salaries = pd.DataFrame(salaries, columns = headers).dropna()
salaries = salaries.apply(lambda x: x.str.replace('$', ''))
salaries = salaries.apply(lambda x: x.str.replace(',', ''))


# Cleaning missing data
salaries_list = ['Salary 2019-20', 'Salary 2020-21', 'Salary 2021-22', 'Salary 2022-23', 'Salary 2023-24', 'Salary 2023-2024', 'Guaranteed']

for i in salaries_list:
    salaries[i] = salaries[i].replace('', 0)
salaries['Signed Using'] = salaries['Signed Using'].replace('', 'NaN')

# Changing the type from objects to integers
salaries.dtypes
for i in salaries_list:
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

salaries
data_players = pd.merge(all_stats, salaries, on = ['Player', 'Team'])
data_players.reset_index(drop = True, inplace = True)
data_players

#########################
#  Tidying the dataset  #
#########################

# Creating a dictionary to map the name of the teams

teams_dict = {
'CLE': 'Cleveland Cavaliers',
'TOR': 'Toronto Raptors',
'WAS': 'Washington Wizards',
'BOS': 'Boston Celtics',
'CHI': 'Chicago Bulls',
'MIA': 'Miami Heat',
'IND': 'Indiana Pacers',
'BRK': 'Brooklyn Nets',
'CHO': 'Charlotte Hornets',
'ORL': 'Orlando Magic',
'NYK': 'New York Knicks',
'MIL': 'Milwaukee Bucks',
'ATL': 'Atlanta Hawks',
'DET': 'Detroit Pistons',
'PHI': 'Philadelphia 76ers',
'DAL': 'Dallas Mavericks',
'DEN': 'Denver Nuggets',
'GSW': 'Golden State Warriors',
'HOU': 'Houston Rockets',
'LAC': 'Los Angeles Clippers',
'LAL': 'Los Angeles Lakers',
'MEM': 'Memphis Grizzlies',
'MIN': 'Minnesota Timberwolves',
'NOP': 'New Orleans Pelicans',
'OKC': 'Oklahoma City Thunder',
'PHO': 'Phoenix Suns',
'POR': 'Portland Trail Blazers',
'SAC': 'Sacramento Kings',
'SAS': 'San Antonio Spurs',
'UTA': 'Utah Jazz'
}


data_players['Team'] = data_players['Team'].map(teams_dict)
data_players
data_players.columns

# Clearning data types

data_players.dtypes
data_players.iloc[:,3:-5] = data_players.iloc[:,3:-5].apply(pd.to_numeric)
data_players.dtypes

#############################################################
#  Creating columns for first, second unit, and third unit  #
#############################################################

fu = pd.DataFrame(columns= data_players.columns, dtype = "float64")
su = pd.DataFrame(columns= data_players.columns, dtype = "float64")
tu = pd.DataFrame(columns= data_players.columns, dtype = "float64")

for key, value in teams_dict.items():
    fu = fu.append(data_players.loc[data_players['Team'] == '{}'.format(value)].nlargest(5,'MP'))
    su = su.append(data_players.loc[data_players['Team'] == '{}'.format(value)].nlargest(10, 'MP')[5:])
    tu = tu.append(data_players.loc[data_players['Team'] == '{}'.format(value)].nlargest(20, 'MP')[11:])

fu["Role"] = "First Unit"
su["Role"] = "Second Unit"
tu["Role"] = "Third Unit"

# Check
data_players.loc[data_players['Team'] == '{}'.format('Miami Heat')].nlargest(20,'MP')[["Player", "MP", "Role"]]


data_players = pd.concat([fu,su, tu])
data_players.to_csv('out_data/players_data.csv', index = False)
