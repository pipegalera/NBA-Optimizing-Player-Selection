import pandas as pd
import numpy as np

BR_data_teams = pd.read_csv('/Users/mac/GitHub/NBA Optimizing Player Selection/Datasets/BR_TS.csv')
NBA_data_teams = pd.read_csv('/Users/mac/GitHub/NBA Optimizing Player Selection/Datasets/NBA_TS.csv')

data_teams = pd.merge(NBA_data_teams, BR_data_teams, on = 'Team')
data_teams.columns
data_teams = data_teams.drop(columns = ['W', 'L', 'GP'])
data_teams.to_csv('/Users/mac/GitHub/NBA Optimizing Player Selection/Datasets/total_team_data.csv', index = False)
