# @Author: Pipe galera
# @Date:   07-04-2020
# @Email:  pipegalera@gmail.com
# @Last modified by:   Pipe galera
# @Last modified time: 08-04-2020

# Packages
import pandas as pd
import numpy as np
import matplotlib as plt
from matplotlib.pyplot import style
import os

# Read Datasets
os.chdir("C:/Users/fgm.si/Documents/GitHub/Optimizing-NBA-Player-Selection/")
data_players = pd.read_csv("out_data/players_data.csv")
data_teams = pd.read_csv('out_data/team_data.csv')

# Count number of players
sum_players = data_players['Player'].count()
duplicated_players = len(data_players.loc[data_players['Player'].duplicated()])
n_players = np.subtract(sum_players, duplicated_players)
duplicated_players
n_players

PER_team = data_players['PER'].groupby(data_players['Team']).sum()
PER_team = pd.DataFrame(PER_team).sort_values(by = 'PER', ascending = False).reset_index()

#Win rate by teams
winrate = data_teams['W/L%'].groupby(data_teams['Team']).sum()
winrate = pd.DataFrame(winrate).sort_values(by = 'W/L%', ascending = False).reset_index()
winrate
Table_1 = pd.merge(PER_team, winrate, on = 'Team').sort_values(by = ['PER'], ascending = False)
Table_1['Expected Rank'] = Table_1['PER'].rank(method = 'max', ascending = False)
Table_1['Real Rank'] = Table_1['W/L%'].rank(method = 'max', ascending = False)
Table_1
Table_1['PER'].corr(Table_1['W/L%'])
Table_1.to_csv('out_data/team_tables/Table_1 Real Rank vs PER.csv', index = False)

# Explote teams
data_players.loc[data_players['Team'] == '{}'.format('Detroit Pistons')].nlargest(20,'PER')[["Player", "PER", "Team"]]

# PER of the 5 and 10 most used Players, and 5 middle used players, by team.
# Offensive and Defensive Rating of the 5 and 10 most used Players, and 5 middle used players, by team.

data_teams
east_west = east + west
east_west
east_per_top5 = {}
west_per_top5 = {}
east_per_top10 = {}
west_per_top10 = {}
east_per_mid5 = {}
west_per_mid5 = {}
east_drtg_top5 = {}
west_drtg_top5 = {}
east_drtg_top10 = {}
west_drtg_top10 = {}
east_drtg_mid5 = {}
west_drtg_mid5 = {}
east_ortg_top5 = {}
west_ortg_top5 = {}
east_ortg_top10 = {}
west_ortg_top10 = {}
east_ortg_mid5 = {}
west_ortg_mid5 = {}

# Table 2: we calculate the minutes played by first, second and third unit.

team_minutes = pd.DataFrame()

for i in data_players.Team.unique():
            dict_team = {"Team": i,
            #Minutes played by the 5 that most minutes played
            "First Unit": data_players.loc[data_players['Team'] == i].nlargest(5,'MP')['MP'].sum(),
            #Minutes played by the 5 that most minutes played, after the top 5.
            "Second Unit": data_players.loc[data_players['Team'] == i].nlargest(10,'MP')["MP"][5:].sum(),
            #Minutes played by the 10 that most minutes played
            "First and Second Unit": data_players.loc[data_players['Team'] == i].nlargest(10,'MP')['MP'].sum(),
            # Minutes played by the players that least minutes played (the rest)
            "Third Unit": data_players.loc[data_players['Team'] == i].nlargest(20,'MP')['MP'][10:].sum()}

            team_minutes = team_minutes.append(dict_team, ignore_index = True)
team_minutes = team_minutes[["Team", "First Unit", "Second Unit", "First and Second Unit", "Third Unit"]]


# Save the table
team_minutes.to_csv("out_data/team_tables/Table_2 Total minutes by unit.csv")

# Table 3: We display them as percentages.
team_minutes_perct = pd.DataFrame()

team_minutes_perct['Team'] = team_minutes['Team']
team_minutes_perct['% Time First Unit'] = team_minutes['First Unit'] / (team_minutes['First and Second Unit'] + team_minutes['Third Unit'])
team_minutes_perct['% Time playing Second Unit'] = team_minutes['Second Unit'] / (team_minutes['First and Second Unit'] + team_minutes['Third Unit'])
team_minutes_perct['% Time playing First and Second Unit'] = team_minutes['First and Second Unit'] / (team_minutes['First and Second Unit'] + team_minutes['Third Unit'])
team_minutes_perct['% Time playing Third Unit'] = team_minutes['Third Unit'] / (team_minutes['First and Second Unit'] + team_minutes['Third Unit'])


# Save data
team_minutes_perct.to_csv("out_data/team_tables/Table_3 Minutes by unit as a percentage.csv")

# Calculating the sum of the PER, ORtg and DRtg, by First, Second and Third Unit.

stats_teams = pd.DataFrame()
for i in data_players.Team.unique():
            dict_team = {"Team": i,

            #PER
            "PER: Sum of First Unit": data_players.loc[data_players['Team'] == i].nlargest(5,'MP')['PER'].sum(),
            "PER: Sum of Second Unit": data_players.loc[data_players['Team'] == i].nlargest(10,'MP')['PER'][5:].sum(),
            "PER: Sum of First and Second Unit":  data_players.loc[data_players['Team'] == i].nlargest(10,'MP')['PER'].sum(),
            "PER: Sum of Third Unit": data_players.loc[data_players['Team'] == i].nlargest(20,'MP')['PER'][10:].sum(),

            # ORtg
            "ORtg: Sum of First Unit": data_players.loc[data_players['Team'] == i].nlargest(5,'MP')['ORtg'].sum(),
            "ORtg: Sum of Second Unit": data_players.loc[data_players['Team'] == i].nlargest(10,'MP')['ORtg'][5:].sum(),
            "ORtg: Sum of First and Second Unit": data_players.loc[data_players['Team'] == i].nlargest(10,'MP')['ORtg'].sum(),
            "ORtg: Sum of Third Unit": data_players.loc[data_players['Team'] == i].nlargest(20,'MP')['ORtg'][10:].sum(),

            # DRtg
            "DRtg: Sum of First Unit": data_players.loc[data_players['Team'] == i].nlargest(5,'MP')['DRtg'].sum(),
            "DRtg: Sum of Second Unit": data_players.loc[data_players['Team'] == i].nlargest(10,'MP')['DRtg'][5:].sum(),
            "DRtg: Sum of First and Second Unit": data_players.loc[data_players['Team'] == i].nlargest(10,'MP')['DRtg'].sum(),
            "DRtg: Sum of Third Unit": data_players.loc[data_players['Team'] == i].nlargest(20,'MP')['DRtg'][10:].sum()
            }
            stats_teams = stats_teams.append(dict_team, ignore_index = True)

# Reorganize columns
cols = stats_teams.columns
cols
stats_teams = stats_teams[['Team',
                           'PER: Sum of First Unit',
                           'PER: Sum of Second Unit',
                           'PER: Sum of First and Second Unit',
                           'PER: Sum of Third Unit',
                           'ORtg: Sum of First Unit',
                           'ORtg: Sum of Second Unit',
                           'ORtg: Sum of First and Second Unit',
                           'ORtg: Sum of Third Unit',
                           'DRtg: Sum of First Unit',
                           'DRtg: Sum of Second Unit',
                           'DRtg: Sum of First and Second Unit',
                           'DRtg: Sum of Third Unit']]

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
data_players["Conference"] = data_players["Team"].map(conferences_dict)


east_players = data_players[data_players["Conference"] == "East"]
west_players = data_players[data_players["Conference"] == "West"]

"""
Tengo que crear:
Equipo -> Top 5 players PER -> Expected rank according to PER -> real rank
Equipo -> Top 10 players PER -> Expected rank according to PER -> real rank
"""

#Table 2 of the paper (Top 5 East)
Table_east_top5 = pd.merge(stats_teams, winrate, on = 'Team').sort_values(by = ['PER: Sum of First Unit'], ascending = False)

Table_east_top5['Expected'] = Table_east_top5['PER_top5'].rank(method = 'max', ascending = False)
Table_east_top5['Real'] = Table_east_top5['W/L%'].rank(method = 'max', ascending = False)

""" BORRAR CUANDO ACABE LAS TABLAS
for i,x in zip(east, west):
    #PER top 5
    east_per_top5['{}'.format(i)]  = data_players.loc[data_players['Team'] == '{}'.format(i)].nlargest(5,'MP')['PER'].sum()
    west_per_top5['{}'.format(x)]  = data_players.loc[data_players['Team'] == '{}'.format(x)].nlargest(5,'MP')['PER'].sum()
    #PER top 10
    east_per_top10['{}'.format(i)] = data_players.loc[data_players['Team'] == '{}'.format(i)].nlargest(10,'MP')['PER'].sum()
    west_per_top10['{}'.format(x)] = data_players.loc[data_players['Team'] == '{}'.format(x)].nlargest(10,'MP')['PER'].sum()
    #PER mid 5
    east_per_mid5['{}'.format(i)] = data_players.loc[data_players['Team'] == '{}'.format(i)].nlargest(10,'MP')['PER'].drop(data_players.loc[data_players['Team'] == '{}'.format(i)].nlargest(10, 'MP')['PER'].index[:5]).sum()
    west_per_mid5['{}'.format(x)] = data_players.loc[data_players['Team'] == '{}'.format(x)].nlargest(10,'MP')['PER'].drop(data_players.loc[data_players['Team'] == '{}'.format(x)].nlargest(10, 'MP')['PER'].index[:5]).sum()

    #ORtg top 5
    east_ortg_top5['{}'.format(i)]  = data_players.loc[data_players['Team'] == '{}'.format(i)].nlargest(5,'MP')['ORtg'].sum()
    west_ortg_top5['{}'.format(x)]  = data_players.loc[data_players['Team'] == '{}'.format(x)].nlargest(5,'MP')['ORtg'].sum()
    #ORtg top 10
    east_ortg_top10['{}'.format(i)] = data_players.loc[data_players['Team'] == '{}'.format(i)].nlargest(10,'MP')['ORtg'].sum()
    west_ortg_top10['{}'.format(x)] = data_players.loc[data_players['Team'] == '{}'.format(x)].nlargest(10,'MP')['ORtg'].sum()
    #ORtg mid 5
    east_ortg_mid5['{}'.format(i)] = data_players.loc[data_players['Team'] == '{}'.format(i)].nlargest(10,'MP')['ORtg'].drop(data_players.loc[data_players['Team'] == '{}'.format(i)].nlargest(10, 'MP')['ORtg'].index[:5]).sum()
    west_ortg_mid5['{}'.format(x)] = data_players.loc[data_players['Team'] == '{}'.format(x)].nlargest(10,'MP')['ORtg'].drop(data_players.loc[data_players['Team'] == '{}'.format(x)].nlargest(10, 'MP')['ORtg'].index[:5]).sum()

    #DRtg top 5
    east_drtg_top5['{}'.format(i)]  = data_players.loc[data_players['Team'] == '{}'.format(i)].nlargest(5,'MP')['DRtg'].sum()
    west_drtg_top5['{}'.format(x)]  = data_players.loc[data_players['Team'] == '{}'.format(x)].nlargest(5,'MP')['DRtg'].sum()
    #DRtg top 10
    east_drtg_top10['{}'.format(i)] = data_players.loc[data_players['Team'] == '{}'.format(i)].nlargest(10,'MP')['DRtg'].sum()
    west_drtg_top10['{}'.format(x)] = data_players.loc[data_players['Team'] == '{}'.format(x)].nlargest(10,'MP')['DRtg'].sum()
    #DRtg mid 5
    east_drtg_mid5['{}'.format(i)] = data_players.loc[data_players['Team'] == '{}'.format(i)].nlargest(10,'MP')['DRtg'].drop(data_players.loc[data_players['Team'] == '{}'.format(i)].nlargest(10, 'MP')['DRtg'].index[:5]).sum()
    west_drtg_mid5['{}'.format(x)] = data_players.loc[data_players['Team'] == '{}'.format(x)].nlargest(10,'MP')['DRtg'].drop(data_players.loc[data_players['Team'] == '{}'.format(x)].nlargest(10, 'MP')['DRtg'].index[:5]).sum()


# PER dicts to Dataframe
east_per_top5 = pd.DataFrame.from_dict(east_per_top5, orient = 'index').stack().reset_index(level=0)
east_per_top5 = east_per_top5.rename(columns = {'level_0': 'Team', 0: 'PER_top5'}).reset_index(drop = True)
west_per_top5 = pd.DataFrame.from_dict(west_per_top5, orient = 'index').stack().reset_index(level=0)
west_per_top5 = west_per_top5.rename(columns = {'level_0': 'Team', 0: 'PER_top5'}).reset_index(drop = True)

east_per_top10 = pd.DataFrame.from_dict(east_per_top10, orient = 'index').stack().reset_index(level=0)
east_per_top10 = east_per_top10.rename(columns = {'level_0': 'Team', 0: 'PER_top10'}).reset_index(drop = True)
west_per_top10 = pd.DataFrame.from_dict(west_per_top10, orient = 'index').stack().reset_index(level=0)
west_per_top10 = west_per_top10.rename(columns = {'level_0': 'Team', 0: 'PER_top10'}).reset_index(drop = True)

east_per_mid5 = pd.DataFrame.from_dict(east_per_mid5, orient = 'index').stack().reset_index(level=0)
east_per_mid5 = east_per_mid5.rename(columns = {'level_0': 'Team', 0: 'PER_mid5'}).reset_index(drop = True)
west_per_mid5 = pd.DataFrame.from_dict(west_per_mid5, orient = 'index').stack().reset_index(level=0)
west_per_mid5 = west_per_mid5.rename(columns = {'level_0': 'Team', 0: 'PER_mid5'}).reset_index(drop = True)

# ORtg dicts to Dataframe
east_ortg_top5 = pd.DataFrame.from_dict(east_ortg_top5, orient = 'index').stack().reset_index(level=0)
east_ortg_top5 = east_ortg_top5.rename(columns = {'level_0': 'Team', 0: 'ORtg_top5'}).reset_index(drop = True)
west_ortg_top5 = pd.DataFrame.from_dict(west_ortg_top5, orient = 'index').stack().reset_index(level=0)
west_ortg_top5 = west_ortg_top5.rename(columns = {'level_0': 'Team', 0: 'ORtg_top5'}).reset_index(drop = True)

east_ortg_top10 = pd.DataFrame.from_dict(east_ortg_top10, orient = 'index').stack().reset_index(level=0)
east_ortg_top10 = east_ortg_top10.rename(columns = {'level_0': 'Team', 0: 'ORtg_top10'}).reset_index(drop = True)
west_ortg_top10 = pd.DataFrame.from_dict(west_ortg_top10, orient = 'index').stack().reset_index(level=0)
west_ortg_top10 = west_ortg_top10.rename(columns = {'level_0': 'Team', 0: 'ORtg_top10'}).reset_index(drop = True)

east_ortg_mid5 = pd.DataFrame.from_dict(east_ortg_mid5, orient = 'index').stack().reset_index(level=0)
east_ortg_mid5 = east_ortg_mid5.rename(columns = {'level_0': 'Team', 0: 'ORtg_mid5'}).reset_index(drop = True)
west_ortg_mid5 = pd.DataFrame.from_dict(west_ortg_mid5, orient = 'index').stack().reset_index(level=0)
west_ortg_mid5 = west_ortg_mid5.rename(columns = {'level_0': 'Team', 0: 'ORtg_mid5'}).reset_index(drop = True)

# DRtg dicts to Dataframe
east_drtg_top5 = pd.DataFrame.from_dict(east_drtg_top5, orient = 'index').stack().reset_index(level=0)
east_drtg_top5 = east_drtg_top5.rename(columns = {'level_0': 'Team', 0: 'DRtg_top5'}).reset_index(drop = True)
west_drtg_top5 = pd.DataFrame.from_dict(west_drtg_top5, orient = 'index').stack().reset_index(level=0)
west_drtg_top5 = west_drtg_top5.rename(columns = {'level_0': 'Team', 0: 'DRtg_top5'}).reset_index(drop = True)

east_drtg_top10 = pd.DataFrame.from_dict(east_drtg_top10, orient = 'index').stack().reset_index(level=0)
east_drtg_top10 = east_drtg_top10.rename(columns = {'level_0': 'Team', 0: 'DRtg_top10'}).reset_index(drop = True)
west_drtg_top10 = pd.DataFrame.from_dict(west_drtg_top10, orient = 'index').stack().reset_index(level=0)
west_drtg_top10 = west_drtg_top10.rename(columns = {'level_0': 'Team', 0: 'DRtg_top10'}).reset_index(drop = True)

east_drtg_mid5 = pd.DataFrame.from_dict(east_drtg_mid5, orient = 'index').stack().reset_index(level=0)
east_drtg_mid5 = east_drtg_mid5.rename(columns = {'level_0': 'Team', 0: 'DRtg_mid5'}).reset_index(drop = True)
west_drtg_mid5 = pd.DataFrame.from_dict(west_drtg_mid5, orient = 'index').stack().reset_index(level=0)
west_drtg_mid5 = west_drtg_mid5.rename(columns = {'level_0': 'Team', 0: 'DRtg_mid5'}).reset_index(drop = True)

# Save Joined East + West Sum PER and DRtg
PER_team_top5  = east_per_top5.append(west_per_top5).reset_index(drop = True)
PER_team_top10 = east_per_top10.append(west_per_top10).reset_index(drop = True)
PER_team_mid5  = east_per_mid5.append(west_per_mid5).reset_index(drop = True)

ORtg_team_top5  = east_ortg_top5.append(west_ortg_top5).reset_index(drop = True)
ORtg_team_top10 = east_ortg_top10.append(west_ortg_top10).reset_index(drop = True)
ORtg_team_mid5  = east_ortg_mid5.append(west_ortg_mid5).reset_index(drop = True)

DRtg_team_top5  = east_drtg_top5.append(west_drtg_top5).reset_index(drop = True)
DRtg_team_top10 = east_drtg_top10.append(west_drtg_top10).reset_index(drop = True)
DRtg_team_mid5  = east_drtg_mid5.append(west_drtg_mid5).reset_index(drop = True)
"""

#Table 2 of the paper (Top 5 East)
Table_east_top5 = pd.merge(east_per_top5, winrate, on = 'Team').sort_values(by = ['PER_top5'], ascending = False)
Table_east_top5['Expected'] = Table_east_top5['PER_top5'].rank(method = 'max', ascending = False)
Table_east_top5['Real'] = Table_east_top5['W/L%'].rank(method = 'max', ascending = False)

Table_east_top5.to_csv('/Users/mac/GitHub/Optimizing-NBA-Player-Selection/Descriptive Analysis/Tables/Table_east_top5.csv', index = False)
Table_east_top5['PER_top5'].corr(Table_east_top5['W/L%'])

#Table 2 of the paper (Top 5 West) -> Robusttest

Table_west_top5 = pd.merge(west_per_top5, winrate, on = 'Team').sort_values(by = ['PER_top5'], ascending = False)
Table_west_top5['Expected'] = Table_west_top5['PER_top5'].rank(method = 'max', ascending = False)
Table_west_top5['Real'] = Table_west_top5['W/L%'].rank(method = 'max', ascending = False)

Table_west_top5.to_csv('/Users/mac/GitHub/Optimizing-NBA-Player-Selection/Descriptive Analysis/Tables/Table_west_top5.csv', index = False)
Table_west_top5['PER_top5'].corr(Table_west_top5['W/L%'])

#Table 3 of the paper (Top 10 East)
Table_east_top10 = pd.merge(east_per_top10, winrate, on = 'Team').sort_values(by = ['PER_top10'], ascending = False)
Table_east_top10['Expected'] = Table_east_top10['PER_top10'].rank(method = 'max', ascending = False)
Table_east_top10['Real'] = Table_east_top10['W/L%'].rank(method = 'max', ascending = False)

Table_2 = pd.merge(east_per_top10, east_per_top5, on = 'Team').sort_values(by = ['PER_top10'], ascending = False)
Table_2 = pd.merge(Table_2, winrate, on = 'Team').sort_values(by = ['W/L%'], ascending = False)
Table_2['Expected Rank Top 5 PER'] = Table_2['PER_top5'].rank(method = 'max', ascending = False)
Table_2['Expected Rank Top 10 PER'] = Table_2['PER_top10'].rank(method = 'max', ascending = False)
Table_2['Real Rank'] = Table_2['W/L%'].rank(method = 'max', ascending = False)
Table_2.columns
Table_2 = Table_2[['Team', 'W/L%', 'Real Rank', 'Expected Rank Top 5 PER', 'Expected Rank Top 10 PER' ]]
Table_2['Real Rank'].corr(Table_2['Expected Rank Top 5 PER'])
Table_2['Real Rank'].corr(Table_2['Expected Rank Top 10 PER'])
Table_2.round(2).to_csv('/Users/mac/GitHub/Optimizing-NBA-Player-Selection/Descriptive Analysis/Tables/Table_2.csv', index = False)

Table_east_top10.to_csv('/Users/mac/GitHub/Optimizing-NBA-Player-Selection/Descriptive Analysis/Tables/Table_east_top10.csv', index = False)
Table_east_top10['PER_top10'].corr(Table_east_top10['W/L%'])

#Table 3 of the paper (Top 10 West) -> Robusttest

Table_west_top10 = pd.merge(west_per_top10, winrate, on = 'Team').sort_values(by = ['PER_top10'], ascending = False)
Table_west_top10['Expected'] = Table_west_top10['PER_top10'].rank(method = 'max', ascending = False)
Table_west_top10['Real'] = Table_west_top10['W/L%'].rank(method = 'max', ascending = False)
Table_west_top10.to_csv('/Users/mac/GitHub/Optimizing-NBA-Player-Selection/Descriptive Analysis/Tables/Table_west_top10.csv', index = False)

Table_west_top10['PER_top10'].corr(Table_west_top10['W/L%'])

# Table 4 Paper
net_rating = data_teams[['ORtg/A', 'DRtg/A', 'NRtg/A']].groupby(data_teams['Team']).sum()
net_rating = pd.DataFrame(net_rating).reset_index()
Table4 = pd.merge(net_rating, winrate, on = 'Team').sort_values(by = ['NRtg/A'], ascending = False).reset_index(drop = True)
Table4.to_csv('/Users/mac/GitHub/Optimizing-NBA-Player-Selection/Descriptive Analysis/Tables/Table4.csv', index = False)
Table4

# Figure 1
net_adjusted = data_teams['NRtg/A'].groupby(data_teams['Team']).sum()
net_adjusted = pd.DataFrame(net_adjusted)
fig1 = pd.merge(net_adjusted, winrate, on = 'Team').sort_values(by = ['NRtg/A'], ascending = False).reset_index(drop = True)
fig1
fig1['NRtg/A'].corr(fig1['W/L%']) # Correlation of 0.977

net = data_teams['NRtg'].groupby(data_teams['Team']).sum()
net = pd.DataFrame(net)
fig2 = pd.merge(net, winrate, on = 'Team').sort_values(by = ['NRtg'], ascending = False).reset_index(drop = True)
fig2['NRtg'].corr(fig2['W/L%']) # Correlation of 0.980
fig2
# Save the new dataset

#list = [PER_team_top5, PER_team_top10, PER_team_mid5, DRtg_team_top5, DRtg_team_top10, DRtg_team_mid5]

merged_data_teams = pd.merge(data_teams, PER_team_top5, on = 'Team')
merged_data_teams = pd.merge(merged_data_teams, PER_team_top10, on = 'Team')
merged_data_teams = pd.merge(merged_data_teams, PER_team_mid5, on = 'Team')

merged_data_teams = pd.merge(merged_data_teams, ORtg_team_top5, on = 'Team')
merged_data_teams = pd.merge(merged_data_teams, ORtg_team_top10, on = 'Team')
merged_data_teams = pd.merge(merged_data_teams, ORtg_team_mid5, on = 'Team')

merged_data_teams = pd.merge(merged_data_teams, DRtg_team_top5, on = 'Team')
merged_data_teams = pd.merge(merged_data_teams, DRtg_team_top10, on = 'Team')
merged_data_teams = pd.merge(merged_data_teams, DRtg_team_mid5, on = 'Team')



merged_data_teams.columns

merged_data_teams.to_csv('/Users/mac/GitHub/Optimizing-NBA-Player-Selection/Datasets/total_team_data.csv', index = False)
merged_data_teams = pd.read_csv('/Users/mac/GitHub/Optimizing-NBA-Player-Selection/Datasets/total_team_data.csv')
merged_data_teams

# Feature Selection

features_sel = merged_data_teams.drop(columns = 'Team')
dummies = pd.get_dummies(features_sel[['Conf', 'Div']])
features_sel = pd.concat([features_sel, dummies], axis = 1)
features_sel

# Correlation Matrix

corr = features_sel.corr(method = 'pearson')
corr = corr.round(2).style.background_gradient(cmap = 'coolwarm')
corr

features_sel
