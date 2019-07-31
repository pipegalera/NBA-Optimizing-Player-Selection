
import pandas as pd
import numpy as np
import matplotlib as plt
from matplotlib import style
# Me he quedado en hacer la matrix de correlaciones para elegir las features.
# Idea: convertir division y conference a dummies

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
PER_team

#Win rate by teams
winrate = data_teams['WIN%'].groupby(data_teams['Team']).sum()
winrate = pd.DataFrame(winrate).reset_index()
winrate

#PER of the 5 and 10 most used Players, by team

east = ['Cleveland Cavaliers','Toronto Raptors', 'Washington Wizards', 'Boston Celtics', 'Chicago Bulls', 'Miami Heat', 'Indiana Pacers', 'Brooklyn Nets', 'Charlotte Hornets', 'Orlando Magic', 'New York Knicks', 'Milwaukee Bucks', 'Atlanta Hawks', 'Detroit Pistons', 'Philadelphia 76ers']
west = ['Dallas Mavericks', 'Denver Nuggets', 'Golden State Warriors', 'Houston Rockets', 'LA Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'Oklahoma City Thunder', 'Phoenix Suns', 'Portland Trail Blazers', 'Sacramento Kings', 'San Antonio Spurs', 'Utah Jazz']
east_per_top5 = {}
west_per_top5 = {}
east_per_top10 = {}
west_per_top10 = {}

for i,x in zip(east, west):
    east_per_top5['{}'.format(i)]  = data_players.loc[data_players['Team'] == '{}'.format(i)].nlargest(5,'MP')['PER'].sum()
    west_per_top5['{}'.format(x)]  = data_players.loc[data_players['Team'] == '{}'.format(x)].nlargest(5,'MP')['PER'].sum()
    east_per_top10['{}'.format(i)] = data_players.loc[data_players['Team'] == '{}'.format(i)].nlargest(10,'MP')['PER'].sum()
    west_per_top10['{}'.format(x)] = data_players.loc[data_players['Team'] == '{}'.format(x)].nlargest(10,'MP')['PER'].sum()

# From dicts to Dataframe
east_per_top5 = pd.DataFrame.from_dict(east_per_top5, orient = 'index').stack().reset_index(level=0)
east_per_top5 = east_per_top5.rename(columns = {'level_0': 'Team', 0: 'PER'}).reset_index(drop = True)
east_per_top10 = pd.DataFrame.from_dict(east_per_top10, orient = 'index').stack().reset_index(level=0)
east_per_top10 = east_per_top10.rename(columns = {'level_0': 'Team', 0: 'PER'}).reset_index(drop = True)
west_per_top5 = pd.DataFrame.from_dict(west_per_top5, orient = 'index').stack().reset_index(level=0)
west_per_top5 = west_per_top5.rename(columns = {'level_0': 'Team', 0: 'PER'}).reset_index(drop = True)
west_per_top10 = pd.DataFrame.from_dict(west_per_top10, orient = 'index').stack().reset_index(level=0)
west_per_top10 = west_per_top10.rename(columns = {'level_0': 'Team', 0: 'PER'}).reset_index(drop = True)


#Table 2 of the paper (Top 5 East)
Table_east_top5 = pd.merge(east_per_top5, winrate, on = 'Team').sort_values(by = ['PER'], ascending = False)
Table_east_top5['Expected'] = Table_east_top5['PER'].rank(method = 'max', ascending = False)
Table_east_top5['Real'] = Table_east_top5['WIN%'].rank(method = 'max', ascending = False)
Table_east_top5
Table_east_top5.to_csv('/Users/mac/GitHub/NBA_Scrappers/Descriptive Analysis/Table_east_top5.csv', index = False)

Table_east_top5['PER'].corr(Table_east_top5['WIN%'])

#Table 2 of the paper (Top 5 West) -> Robusttest

Table_west_top5 = pd.merge(west_per_top5, winrate, on = 'Team').sort_values(by = ['PER'], ascending = False)
Table_west_top5['Expected'] = Table_west_top5['PER'].rank(method = 'max', ascending = False)
Table_west_top5['Real'] = Table_west_top5['WIN%'].rank(method = 'max', ascending = False)
Table_west_top5
Table_west_top5.to_csv('/Users/mac/GitHub/NBA_Scrappers/Descriptive Analysis/Table_west_top5.csv', index = False)

Table_west_top5['PER'].corr(Table_west_top5['WIN%'])

#Table 3 of the paper (Top 10 East)
Table_east_top10 = pd.merge(east_per_top10, winrate, on = 'Team').sort_values(by = ['PER'], ascending = False)
Table_east_top10['Expected'] = Table_east_top10['PER'].rank(method = 'max', ascending = False)
Table_east_top10['Real'] = Table_east_top10['WIN%'].rank(method = 'max', ascending = False)
Table_east_top10
Table_east_top10.to_csv('/Users/mac/GitHub/NBA_Scrappers/Descriptive Analysis/Table_east_top10.csv', index = False)

Table_east_top10['PER'].corr(Table_east_top10['WIN%'])

#Table 3 of the paper (Top 10 West) -> Robusttest
Table_west_top10 = pd.merge(west_per_top10, winrate, on = 'Team').sort_values(by = ['PER'], ascending = False)
Table_west_top10['Expected'] = Table_west_top10['PER'].rank(method = 'max', ascending = False)
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
features_sel = data_teams.drop(columns = 'Team')
features_sel.info()
