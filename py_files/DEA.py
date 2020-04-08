# @Author: Pipe galera
# @Date:   07-04-2020
# @Email:  pipegalera@gmail.com
# @Last modified by:   pipegalera
# @Last modified time: 2020-04-08T20:48:08+02:00

# Packages
import pandas as pd
import numpy as np
import matplotlib as plt
from matplotlib.pyplot import style
import os

# Read Datasets
os.chdir("/Users/pipegalera/Documents/GitHub/Optimizing-NBA-Player-Selection")
data_players = pd.read_csv("out_data/players_data.csv")
data_teams = pd.read_csv('out_data/team_data.csv')

# Count number of players
sum_players = data_players['Player'].count()
duplicated_players = len(data_players.loc[data_players['Player'].duplicated()])
n_players = np.subtract(sum_players, duplicated_players)
duplicated_players
n_players

"""
The duplicated are players that both they played for 2 teams, and they are receiving money from 2 teams.
For example, DeMarre Carroll. The data correspond with https://www.spotrac.com/nba/houston-rockets/demarre-carroll-6294/
data_players.loc[data_players['Player'].duplicated()]
data_players.loc[data_players['Player'] == "DeMarre Carroll"]
"""
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
data_players.loc[data_players['Team'] == '{}'.format('Cleveland Cavaliers')].nlargest(20,'PER')[["Player", "PER", "Team"]]

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

# Merge
data_teams_v2 = pd.merge(data_teams, stats_teams, on = "Team")

# Check
data_teams_v2.loc[data_teams_v2['Team'] == 'Cleveland Cavaliers'][['PER: Sum of First Unit', 'Team']]

data_players.loc[data_players['Team'] == '{}'.format('Cleveland Cavaliers')].nlargest(5,'MP')[["Player", "PER"]].sum()
data_teams_v2.loc[data_teams_v2['Team'] == 'Miami Heat'][['DRtg: Sum of First and Second Unit', 'Team']]
data_players.loc[data_players['Team'] == '{}'.format('Miami Heat')].nlargest(10,'MP')[["Player", "DRtg"]].sum()

# Save the dataset
data_teams_v2.to_csv("out_data/teams_data_v2.csv")

# Divide the teams into their conferences

east_per = data_teams_v2.loc[data_teams_v2["Conf"] == "E"][['Team','PER: Sum of First Unit', 'PER: Sum of First and Second Unit']]
west_per = data_teams_v2.loc[data_teams_v2["Conf"] == "W"][['Team','PER: Sum of First Unit', 'PER: Sum of First and Second Unit']]

#Table_4 East: Rank teams according to their PER and real rank
Table_east = pd.merge(east_per, winrate, on = 'Team').sort_values(by = ['W/L%'], ascending = False)
Table_east['Expected_1'] = Table_east['PER: Sum of First Unit'].rank(method = 'max', ascending = False)
Table_east['Expected_2'] = Table_east['PER: Sum of First and Second Unit'].rank(method = 'max', ascending = False)
Table_east['Real'] = Table_east['W/L%'].rank(method = 'max', ascending = False)
Table_east.reset_index(drop = True)
Table_east.to_csv('out_data/team_tables/Table_4 East Rank teams according to their PER and real rank.csv', index = False)

#Table_5 West: Rank teams according to their PER and real rank
Table_west = pd.merge(west_per, winrate, on = 'Team').sort_values(by = ['PER: Sum of First Unit'], ascending = False)
Table_west['Expected_1'] = Table_west['PER: Sum of First Unit'].rank(method = 'max', ascending = False)
Table_west['Expected_2'] = Table_west['PER: Sum of First and Second Unit'].rank(method = 'max', ascending = False)
Table_west['Real'] = Table_west['W/L%'].rank(method = 'max', ascending = False)
Table_west.reset_index(drop = True)
Table_west.to_csv('out_data/team_tables/Table_5 West Rank teams according to their PER and real rank.csv', index = False)

# Check importance of First unit PER vs First and Second Unit PER with W/L%
Table_west.corr() # More correlation W/L% with First and Second Unit PER than with First unit PER
Table_east.corr() # More correlation W/L% with First and Second Unit PER than with First unit PER

# Table 6
net_rating = pd.DataFrame(data_teams_v2[['ORtg/A', 'DRtg/A', 'NRtg/A']].groupby(data_teams_v2['Team']).sum())
net_rating = pd.merge(net_rating, winrate, on = 'Team').sort_values(by = ['NRtg/A'], ascending = False).reset_index(drop = True)
net_rating.to_csv('out_data/team_tables/Table_6 Net Rating rank.csv', index = False)

# Figure 1
net_adjusted = pd.DataFrame(data_teams_v2['NRtg/A'].groupby(data_teams_v2['Team']).sum())
fig1 = pd.merge(net_adjusted, winrate, on = 'Team').sort_values(by = ['NRtg/A'], ascending = False).reset_index(drop = True)
fig1
fig1['NRtg/A'].corr(fig1['W/L%']) # Correlation of 0.962

# Feature Selection

features_sel = data_teams_v2.drop(columns = 'Team')
dummies = pd.get_dummies(features_sel[['Conf', 'Div']])
features_sel = pd.concat([features_sel, dummies], axis = 1)
features_sel

# Correlation Matrix

corr = features_sel.corr(method = 'pearson')
corr = corr.round(2).style.background_gradient(cmap = 'coolwarm')
corr
