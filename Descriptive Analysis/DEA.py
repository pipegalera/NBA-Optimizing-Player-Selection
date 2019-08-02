
import pandas as pd
import numpy as np
import matplotlib as plt
from matplotlib.pyplot import style

# Me he quedado sacando el Offensive rating de los 5,10 y 5 mid jugadores. Primero tengo que merge en final_DATA

data_players = pd.read_csv('/Users/mac/GitHub/NBA_Scrappers/Final Dataset/Final_Data.csv')
teams = pd.read_csv('/Users/mac/GitHub/NBA_Scrappers/Team Stats/team_stats.csv')
teams_2 = pd.read_csv('/Users/mac/GitHub/NBA_Scrappers/Advanced Stats/Advanced_stats_NBA_2.csv')
data_teams = pd.merge(teams, teams_2, on = 'Team')

# Count number of players
sum_players = data_players['Player'].count()
duplicated_players = len(data_players.loc[data_players['Player'].duplicated()])
n_players = np.subtract(sum_players, duplicated_players)
duplicated_players
n_players

''' Examples of weird contracts
salaries.loc[salaries['Player'].duplicated()]
df.loc[df['Player'] == 'Emanuel Terry']
df.loc[df['Player'] == 'Dwight Howard']
df.loc[df['Player'] == 'Corey Brewer']
df.loc[df['Guaranteed'].isnull()]
df.loc[df['Player'] == 'Tyson Chandler']
'''

# All players PER summed grouped by Team (include residual players)
PER_team = data_players['PER'].groupby(data_players['Team']).sum()
PER_team = pd.DataFrame(PER_team).reset_index()


#Win rate by teams
winrate = data_teams['WIN%'].groupby(data_teams['Team']).sum()
winrate = pd.DataFrame(winrate).reset_index()
winrate

# PER of the 5 and 10 most used Players, and 5 middle used players, by team
# Offensive and Defensive Rating of the 5 and 10 most used Players, and 5 middle used players, by team

east = ['Cleveland Cavaliers','Toronto Raptors', 'Washington Wizards', 'Boston Celtics', 'Chicago Bulls', 'Miami Heat', 'Indiana Pacers', 'Brooklyn Nets', 'Charlotte Hornets', 'Orlando Magic', 'New York Knicks', 'Milwaukee Bucks', 'Atlanta Hawks', 'Detroit Pistons', 'Philadelphia 76ers']
west = ['Dallas Mavericks', 'Denver Nuggets', 'Golden State Warriors', 'Houston Rockets', 'LA Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'Oklahoma City Thunder', 'Phoenix Suns', 'Portland Trail Blazers', 'Sacramento Kings', 'San Antonio Spurs', 'Utah Jazz']
east_per_top5 = {}
west_per_top5 = {}
east_per_top10 = {}
west_per_top10 = {}
east_per_mid5 = {}
west_per_mid5 = {}

for i,x in zip(east, west):
    east_per_top5['{}'.format(i)]  = data_players.loc[data_players['Team'] == '{}'.format(i)].nlargest(5,'MP')['PER'].sum()
    west_per_top5['{}'.format(x)]  = data_players.loc[data_players['Team'] == '{}'.format(x)].nlargest(5,'MP')['PER'].sum()
    east_per_top10['{}'.format(i)] = data_players.loc[data_players['Team'] == '{}'.format(i)].nlargest(10,'MP')['PER'].sum()
    west_per_top10['{}'.format(x)] = data_players.loc[data_players['Team'] == '{}'.format(x)].nlargest(10,'MP')['PER'].sum()
    east_per_mid5['{}'.format(i)] = data_players.loc[data_players['Team'] == '{}'.format(i)].nlargest(10,'MP')['PER'].drop(data_players.loc[data_players['Team'] == '{}'.format(i)].nlargest(10, 'MP')['PER'].index[:5]).sum()
    west_per_mid5['{}'.format(x)] = data_players.loc[data_players['Team'] == '{}'.format(x)].nlargest(10,'MP')['PER'].drop(data_players.loc[data_players['Team'] == '{}'.format(x)].nlargest(10, 'MP')['PER'].index[:5]).sum()

    east_ortg_top5['{}'.format(i)] =
# From dicts to Dataframe
east_per_top5 = pd.DataFrame.from_dict(east_per_top5, orient = 'index').stack().reset_index(level=0)
east_per_top5 = east_per_top5.rename(columns = {'level_0': 'Team', 0: 'PER_top5'}).reset_index(drop = True)

east_per_top10 = pd.DataFrame.from_dict(east_per_top10, orient = 'index').stack().reset_index(level=0)
east_per_top10 = east_per_top10.rename(columns = {'level_0': 'Team', 0: 'PER_top10'}).reset_index(drop = True)

east_per_mid5 = pd.DataFrame.from_dict(east_per_mid5, orient = 'index').stack().reset_index(level=0)
east_per_mid5 = east_per_mid5.rename(columns = {'level_0': 'Team', 0: 'PER_mid5'}).reset_index(drop = True)

west_per_top5 = pd.DataFrame.from_dict(west_per_top5, orient = 'index').stack().reset_index(level=0)
west_per_top5 = west_per_top5.rename(columns = {'level_0': 'Team', 0: 'PER_top5'}).reset_index(drop = True)

west_per_top10 = pd.DataFrame.from_dict(west_per_top10, orient = 'index').stack().reset_index(level=0)
west_per_top10 = west_per_top10.rename(columns = {'level_0': 'Team', 0: 'PER_top10'}).reset_index(drop = True)

west_per_mid5 = pd.DataFrame.from_dict(west_per_mid5, orient = 'index').stack().reset_index(level=0)
west_per_mid5 = west_per_mid5.rename(columns = {'level_0': 'Team', 0: 'PER_mid5'}).reset_index(drop = True)

# Save Sum PER
PER_team_top5  = east_per_top5.append(west_per_top5).set_index('Team')
PER_team_top10 = east_per_top10.append(west_per_top10).set_index('Team')
PER_team_mid5  = east_per_mid5.append(west_per_mid5).set_index('Team')

# Save ORtg and DRtg


#Table 2 of the paper (Top 5 East)
Table_east_top5 = pd.merge(east_per_top5, winrate, on = 'Team').sort_values(by = ['PER_top5'], ascending = False)
Table_east_top5['Expected'] = Table_east_top5['PER_top5'].rank(method = 'max', ascending = False)
Table_east_top5['Real'] = Table_east_top5['WIN%'].rank(method = 'max', ascending = False)
Table_east_top5
Table_east_top5.to_csv('/Users/mac/GitHub/NBA_Scrappers/Descriptive Analysis/Table_east_top5.csv', index = False)

Table_east_top5['PER_top5'].corr(Table_east_top5['WIN%'])

#Table 2 of the paper (Top 5 West) -> Robusttest

Table_west_top5 = pd.merge(west_per_top5, winrate, on = 'Team').sort_values(by = ['PER_top5'], ascending = False)
Table_west_top5['Expected'] = Table_west_top5['PER_top5'].rank(method = 'max', ascending = False)
Table_west_top5['Real'] = Table_west_top5['WIN%'].rank(method = 'max', ascending = False)
Table_west_top5
Table_west_top5.to_csv('/Users/mac/GitHub/NBA_Scrappers/Descriptive Analysis/Table_west_top5.csv', index = False)

Table_west_top5['PER'].corr(Table_west_top5['WIN%'])

#Table 3 of the paper (Top 10 East)
Table_east_top10 = pd.merge(east_per_top10, winrate, on = 'Team').sort_values(by = ['PER_top10'], ascending = False)
Table_east_top10['Expected'] = Table_east_top10['PER_top10'].rank(method = 'max', ascending = False)
Table_east_top10['Real'] = Table_east_top10['WIN%'].rank(method = 'max', ascending = False)
Table_east_top10
Table_east_top10.to_csv('/Users/mac/GitHub/NBA_Scrappers/Descriptive Analysis/Table_east_top10.csv', index = False)

Table_east_top10['PER'].corr(Table_east_top10['WIN%'])

#Table 3 of the paper (Top 10 West) -> Robusttest
Table_west_top10 = pd.merge(west_per_top10, winrate, on = 'Team').sort_values(by = ['PER_top10'], ascending = False)
Table_west_top10['Expected'] = Table_west_top10['PER_top10'].rank(method = 'max', ascending = False)
Table_west_top10['Real'] = Table_west_top10['WIN%'].rank(method = 'max', ascending = False)
Table_west_top10
Table_west_top10.to_csv('/Users/mac/GitHub/NBA_Scrappers/Descriptive Analysis/Table_west_top10.csv', index = False)

Table_west_top10['PER'].corr(Table_west_top10['WIN%'])

# Table 4 Paper
net_rating = data_teams[['ORtg/A', 'DRtg/A', 'NRtg/A']].groupby(data_teams['Team']).sum()
net_rating = pd.DataFrame(net_rating).reset_index()
net_rating

Table4 = pd.merge(net_rating, winrate, on = 'Team').sort_values(by = ['NRtg/A'], ascending = False)
Table4.to_csv('/Users/mac/GitHub/NBA_Scrappers/Descriptive Analysis/Table4.csv', index = False)

# Figure 1
net_adjusted = data_teams['NRtg/A'].groupby(data_teams['Team']).sum()
net_adjusted = pd.DataFrame(net_adjusted)
fig1 = pd.merge(net_adjusted, winrate, on = 'Team').sort_values(by = ['NRtg/A'], ascending = False)
fig1['NRtg/A'].corr(fig1['WIN%']) # Correlation of 0.979

net = data_teams['NRtg'].groupby(data_teams['Team']).sum()
net = pd.DataFrame(net)
fig2 = pd.merge(net, winrate, on = 'Team').sort_values(by = ['NRtg'], ascending = False)
fig2['NRtg'].corr(fig2['WIN%']) # Correlation of 0.983


#Matrix of correlations -> Feature selection
data_teams = pd.merge(data_teams, PER_team_top5, on = 'Team')
data_teams = pd.merge(data_teams, PER_team_top10, on = 'Team')
data_teams = pd.merge(data_teams, PER_team_mid5, on = 'Team')
data_teams
data_teams.to_csv('/Users/mac/GitHub/NBA_Scrappers/Team Stats/final_data.csv', index = False)

features_sel = data_teams.drop(columns = ['Team', 'GP'])
dummies = pd.get_dummies(features_sel[['Conf', 'Div']])
features_sel = pd.concat([features_sel, dummies], axis = 1)
corr = features_sel.corr(method = 'pearson')
corr.style.background_gradient(cmap = 'coolwarm') # Conferencia Este corr 0.13 with win rate


# Why the the second unit efficiency is negatively correlated with winning?
