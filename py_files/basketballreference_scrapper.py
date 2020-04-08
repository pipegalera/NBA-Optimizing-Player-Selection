# @Author: Pipe galera
# @Date:   05-04-2020
# @Email:  pipegalera@gmail.com
# @Last modified by:   Pipe galera
# @Last modified time: 08-04-2020


# Packages
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import os
os.chdir("/Users/fgm.si/Documents/GitHub/Optimizing-NBA-Player-Selection")

###############################################################################
#                            PLAYERS DATA                                     #
###############################################################################

####################################
#   Player Advanced Statistics     #
####################################

# Take a list of all the url needed

url_list = []
# For more years: year = range(2001,2021)
year = ['2020']
for i in year:
    url = "https://www.basketball-reference.com/leagues/NBA_{}_advanced.html".format(i)
    url_list.append(url)

# Compile the body
adv_stats = pd.DataFrame()
url_list
for u in url_list:
    html = urlopen(u)
    soup = BeautifulSoup(html)
# Getting the body
    rows = soup.findAll('tr')[1:]
    stats = [[i.getText() for i in rows[x].findAll('td')]
            for x in range(len(rows))]
    stats = pd.DataFrame(stats)
    stats["28"] = pd.to_numeric(u[49:53])
    adv_stats = adv_stats.append(stats).dropna()


# Clean the body
adv_stats = adv_stats.drop([18, 23], axis = 1)

# Getting headers and removing incorrect named columns
headers_files = soup.findAll('tr')[0]
headers = [i.getText() for i in headers_files.findAll('th')]
headers.remove('\xa0')
headers.remove('\xa0')
headers.remove('Rk')
headers = ['Team' if x == 'Tm' else x for x in headers]
headers.append("Year")
# Check columns length
len(headers) == len(adv_stats.columns)
adv_stats.columns = headers

adv_stats = adv_stats.reset_index(drop = True)


####################################
#  Statistics per 100 posessions   #
####################################


url_list = []
for i in year:
    url = 'https://www.basketball-reference.com/leagues/NBA_{}_per_poss.html'.format(i)
    url_list.append(url)

regular_stats = pd.DataFrame()
for u in url_list:

    # Getting headers and removing incorrect named columns
    html = urlopen(u)
    soup = BeautifulSoup(html)

    # Getting the body
    rows = soup.findAll('tr')[1:]
    stats = [[i.getText() for i in rows[x].findAll('td')]
            for x in range(len(rows))]
    stats = pd.DataFrame(stats)
    stats["28"] = pd.to_numeric(u[49:53])
    regular_stats = regular_stats.append(stats).dropna()

# Getting headers and removing incorrect named columns
headers_files = soup.findAll('tr')[0]
headers = [i.getText() for i in headers_files.findAll('th')]
headers.remove('Rk')
headers = ['Team' if x == 'Tm' else x for x in headers]
headers.append("Year")

# Check columns length
len(headers) == len(regular_stats.columns)
regular_stats.columns = headers
regular_stats = regular_stats.drop(columns = ['', 'Age', 'G', 'MP'],axis = 1)
regular_stats = regular_stats.reset_index(drop = True)
regular_stats

# Merge datasets
all_stats = pd.merge(adv_stats, regular_stats, on = ["Player", "Team", "Pos", "Year"])
all_stats.columns

# Save dataset
all_stats.to_csv("out_data/players_data.csv", index = False)

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


# Cleanning the format
salaries = salaries.apply(lambda x: x.str.replace('$', ''))
salaries = salaries.apply(lambda x: x.str.replace(',', ''))
salaries.replace('', 0, inplace = True)
salaries['Signed Using'].replace(0, np.nan, inplace = True)

salaries_list = ['Salary 2019-20', 'Salary 2020-21', 'Salary 2021-22', 'Salary 2022-23', 'Salary 2023-24', 'Salary 2023-2024', 'Guaranteed']

for i in salaries_list:
    salaries[i] = salaries[i].replace('', 0)
    salaries[i] = salaries[i].apply(pd.to_numeric)

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

all_stats  = all_stats[all_stats["Year"] == 2020].drop("Year", axis = 1).reset_index(drop = True)

# Check if right:
all_stats[all_stats["Team"] == "BOS"]
salaries[salaries["Team"] == "BOS"]

data_players = pd.merge(all_stats, salaries, on = ['Player', 'Team', ]).reset_index(drop = True)
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

# Mapping teams
data_players['Team'] = data_players['Team'].map(teams_dict)
data_players
data_players.columns

# Clearning data types
data_players.dtypes
data_players.iloc[:,4:-2] = data_players.iloc[:,4:-2].apply(pd.to_numeric)
data_players.dtypes

#############################################################
#  Creating columns for first, second unit, and third unit  #
#############################################################


fu = pd.DataFrame(columns= data_players.columns, dtype = "float64")
su = pd.DataFrame(columns= data_players.columns, dtype = "float64")
tu = pd.DataFrame(columns= data_players.columns, dtype = "float64")

for key, value in teams_dict.items():
    fu = fu.append(data_players.loc[data_players['Team'] == value].nlargest(5,'MP'))
    su = su.append(data_players.loc[data_players['Team'] == value].nlargest(10, 'MP')[5:])
    tu = tu.append(data_players.loc[data_players['Team'] == value].nlargest(20, 'MP')[10:])

fu["Role"] = "First Unit"
su["Role"] = "Second Unit"
tu["Role"] = "Third Unit"
data_players = pd.concat([fu,su, tu])

# Check
data_players.loc[data_players['Team'] == '{}'.format('Miami Heat')].nlargest(20,'MP')[["Player", "MP", "Role"]]

data_players.to_csv('out_data/players_data.csv', index = False)

###############################################################################
###############################################################################

###############################################################################
#                        TEAM'S STATISTICS                                    #
###############################################################################

url_list = []
for i in year: # year = range(2012,x) for more years
        url = "https://www.basketball-reference.com/leagues/NBA_{year}_ratings.html".format(year = i)
        url_list.append(url)

url_list
team_data = pd.DataFrame()
for i in url_list:
    # Opening up connection, grabbing the page
    html = urlopen(url)
    soup = BeautifulSoup(html)
    # Getting headers and removing incorrect column
    headers_files = soup.findAll('tr')[1]
    headers = [i.getText() for i in headers_files.findAll('th')]
    headers.remove('Rk')
    # Getting the body
    rows = soup.findAll('tr')[1:]
    stats = [[i.getText() for i in rows[x].findAll('td')]
            for x in range(len(rows))]
    team_data = team_data.append(stats).dropna()

# Check if it got all the rows:
len(url_list) * 30 == team_data.shape[0]

team_data.columns = headers
team_data = team_data.drop(columns = ['W', 'L'])
team_data.reset_index(drop = True)

#########################
#  Tidying the dataset  #
#########################

# Creating a dictionary to map the conferences of the teams

conferences_dict = {
# East
'Cleveland Cavaliers': "East",
'Toronto Raptors': "East",
'Washington Wizards': "East",
'Boston Celtics': "East",
'Chicago Bulls': "East",
'Miami Heat': "East",
'Indiana Pacers': "East",
'Brooklyn Nets': "East",
'Charlotte Hornets': "East",
'Orlando Magic': "East",
'New York Knicks': "East",
'Milwaukee Bucks': "East",
'Atlanta Hawks': "East",
'Detroit Pistons': "East",
'Philadelphia 76ers': "East",
# West
'Dallas Mavericks': "West",
'Denver Nuggets': "West",
'Golden State Warriors': "West",
'Houston Rockets': "West",
'Los Angeles Clippers': "West",
'Los Angeles Lakers': "West",
'Memphis Grizzlies': "West",
'Minnesota Timberwolves': "West",
'New Orleans Pelicans': "West",
'Oklahoma City Thunder': "West",
'Phoenix Suns': "West",
'Portland Trail Blazers': "West",
'Sacramento Kings': "West",
'San Antonio Spurs': "West",
'Utah Jazz': "West"
}
team_data['Conference'] = team_data['Team'].map(conferences_dict)
team_data
# Save data
team_data.to_csv('out_data/team_data.csv', index = False)
