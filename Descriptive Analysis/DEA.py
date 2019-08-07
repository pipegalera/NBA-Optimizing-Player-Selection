
import pandas as pd
import numpy as np
import matplotlib as plt
from matplotlib.pyplot import style


data_players = pd.read_csv('/Users/mac/GitHub/Optimizing-NBA-Player-Selection/Datasets/BR_players_data.csv')
data_teams = pd.read_csv('/Users/mac/GitHub/Optimizing-NBA-Player-Selection/Datasets/BR_TS.csv')

# Count number of players
sum_players = data_players['Player'].count()
duplicated_players = len(data_players.loc[data_players['Player'].duplicated()])
n_players = np.subtract(sum_players, duplicated_players)
duplicated_players
n_players

# All players PER summed grouped by Team (include residual players)
PER_team = data_players['PER'].groupby(data_players['Team']).sum()
PER_team = pd.DataFrame(PER_team).sort_values(by = 'PER', ascending = False).reset_index()
PER_team

#Win rate by teams
winrate = data_teams['W/L%'].groupby(data_teams['Team']).sum()
winrate = pd.DataFrame(winrate).sort_values(by = 'W/L%', ascending = False).reset_index()
winrate

# PER of the 5 and 10 most used Players, and 5 middle used players, by team
# Offensive and Defensive Rating of the 5 and 10 most used Players, and 5 middle used players, by team

east = ['Cleveland Cavaliers','Toronto Raptors', 'Washington Wizards', 'Boston Celtics', 'Chicago Bulls',
'Miami Heat', 'Indiana Pacers', 'Brooklyn Nets', 'Charlotte Hornets', 'Orlando Magic', 'New York Knicks',
'Milwaukee Bucks', 'Atlanta Hawks', 'Detroit Pistons', 'Philadelphia 76ers']
west = ['Dallas Mavericks', 'Denver Nuggets', 'Golden State Warriors', 'Houston Rockets', 'Los Angeles Clippers',
'Los Angeles Lakers', 'Memphis Grizzlies', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'Oklahoma City Thunder',
'Phoenix Suns', 'Portland Trail Blazers', 'Sacramento Kings', 'San Antonio Spurs', 'Utah Jazz']
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

# data_players.loc[data_players['Team'] == '{}'.format('Cleveland Cavaliers')].nlargest(5,'MP')['DRtg'].sum()

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


east_ortg_top5
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
