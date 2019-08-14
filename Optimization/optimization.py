import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pulp import *
import re

data_players = pd.read_csv('/Users/mac/GitHub/Optimizing-NBA-Player-Selection/Datasets/BR_players_data_optimization.csv')

# Preparing of the dataset
dummies = pd.get_dummies(data_players[['Position', 'role']])
data_players = pd.concat([data_players, dummies], axis = 1).drop('Position', axis = 1)

# Prepare data
data_players[['ORtg', 'DRtg']] = data_players[['ORtg', 'DRtg']].apply(pd.to_numeric)
list = ['Player','Team','ORtg','Position_C','Position_PF','Position_PG','Position_SF','Position_SG','role_FU','role_SU','DRtg', 'Salary 2018-19']
list_n = []
for i in list:
     list_n.append(data_players.columns.get_loc('{}'.format(i)))

players = data_players.iloc[:,list_n]

players.shape

# Create Decision Variables: Every player
vars = []
for rownum, row in players.iterrows(): #For every row create a decision variable
    var = str('x' + str(rownum))
    var = pulp.LpVariable(str(var), lowBound = 0, upBound = 1, cat= 'Integer') # Decision problem is binary(0,1)
    vars.append(var)

# Defining the Optimization problem
total_ORtg_top5 = ""
for rownum, row in players.iterrows():
    for i, schedule in enumerate(vars):
        if rownum == i:
            formula = row['ORtg']* row['role_FU'] * schedule
            total_ORtg_top5 += formula

total_ORtg_mid5 = ""
for rownum, row in players.iterrows():
    for i, schedule in enumerate(vars):
        if rownum == i:
            formula = row['ORtg']* row['role_SU'] * schedule
            total_ORtg_mid5 += formula

total_DRtg_top5 = ""
for rownum, row in players.iterrows():
    for i, schedule in enumerate(vars):
        if rownum == i:
            formula = row['DRtg']* row['role_FU'] * schedule
            total_DRtg_top5 += formula

total_DRtg_mid5 = ""
for rownum, row in players.iterrows():
    for i, schedule in enumerate(vars):
        if rownum == i:
            formula = row['DRtg']* row['role_SU'] * schedule
            total_DRtg_mid5 += formula

# Definning the Constrains:

# Salary
salary_cap = 101900000
total_salary = ""
for rownum, row in players.iterrows():
    for i, schedule in enumerate(vars):
        if rownum == i:
            formula = row['Salary 2018-19']* schedule
            total_salary += formula

# Team number
total_number = ""
for rownum, row in players.iterrows():
    for i, schedule in enumerate(vars):
        if rownum == i:
            formula = 1 * schedule
            total_number += formula

# Limit the number of Positions
total_centers = ""
for rownum, row in players.iterrows():
    for i, schedule in enumerate(vars):
        if rownum == i:
            formula = row['Position_C'] * schedule
            total_centers += formula
total_centers

total_powerforwards = ""
for rownum, row in players.iterrows():
    for i, schedule in enumerate(vars):
        if rownum == i:
            formula = row['Position_PF']* schedule
            total_powerforwards += formula
total_powerforwards

total_secondforwards = ""
for rownum, row in players.iterrows():
    for i, schedule in enumerate(vars):
        if rownum == i:
            formula = row['Position_SF']* schedule
            total_secondforwards += formula
total_secondforwards

total_pointguard = ""
for rownum, row in players.iterrows():
    for i, schedule in enumerate(vars):
        if rownum == i:
            formula = row['Position_PG']* schedule
            total_pointguard += formula
total_pointguard

total_secondguard = ""
for rownum, row in players.iterrows():
    for i, schedule in enumerate(vars):
        if rownum == i:
            formula = row['Position_SG']* schedule
            total_secondguard += formula
total_secondguard

# Limit the number of First Unit players
total_FU = ""
for rownum, row in players.iterrows():
    for i, schedule in enumerate(vars):
        if rownum == i:
            formula = row['role_FU']* schedule
            total_FU += formula


# We paremetrice it  with the betas of the linear model
b0 = 0.29527032647275975
b1 = 0.0037166217829991037
b2 = 0.0020560957574373394
b3 = -0.0028170246210830825
b4 = -0.0026370430520007366

# Strategy: Max or min win rate
prob = pulp.LpProblem('Max_stats', pulp.LpMaximize) # Strategy: select players that max stats
prob = pulp.LpProblem('Min_stats', pulp.LpMinimize) # Strategy: select players that min stats
prob += (b1*total_ORtg_top5 + b2*total_ORtg_mid5 + b3*total_DRtg_top5 + b4*total_DRtg_mid5)
prob += (total_salary <= salary_cap)
prob += (total_number == 10)
prob += (total_FU <= 5)
prob += (total_centers <= 2)
prob += (total_powerforwards <= 2)
prob += (total_secondforwards <= 2)
prob += (total_pointguard <= 2)
prob += (total_secondguard <= 2)
'''
# Strategy: Min salary to achive victory
prob = pulp.LpProblem('Min_salary', pulp.LpMinimize)
prob += (total_salary)
prob += (b0 + b1*total_ORtg_top5 + b2*total_ORtg_mid5 + b3*total_DRtg_top5 + b4*total_DRtg_mid5 >= 0.7494040746300286)
prob += (total_number == 10)
prob += (total_FU == 5)
prob += (total_centers == 2)
prob += (total_powerforwards == 2)
prob += (total_secondforwards == 2)
prob += (total_pointguard == 2)
prob += (total_secondguard == 2)
'''
# Solution
optimization_result = prob.solve()
assert optimization_result == pulp.LpStatusOptimal
LpStatus[prob.status]
for i in prob.variables():
    print(i.name, '=', i.varValue)

# Solution Parser

variable_name = []
variable_value = []

for v in prob.variables(): # Get list of decision variables and its solved values
    variable_name.append(v.name)
    variable_value.append(v.varValue)

df = pd.DataFrame({'variable': variable_name, 'value': variable_value})
for rownum, row in df.iterrows():
	value = re.findall(r'(\d+)', row['variable'])
	df.loc[rownum, 'variable'] = int(value[0])

df = df.sort_index(by='variable')
players = players.drop('decision', axis = 1)

for rownum, row in players.iterrows():
    for results_rownum, results_row in df.iterrows():
        if rownum == results_row['variable']:
            players.loc[rownum, 'decision'] = results_row['value']


players.decision.sum()
players.loc[(players.decision == 1)]
# players.loc[players.decision == 1].to_csv('/Users/mac/GitHub/Optimizing-NBA-Player-Selection/Optimization/Team_minvictories_tochamp.csv', index = False)
# players.loc[players.decision == 1].to_csv('/Users/mac/GitHub/Optimizing-NBA-Player-Selection/Optimization/Team_undercap_minvictories.csv', index = False)
# players.loc[players.decision == 1].to_csv('/Users/mac/GitHub/Optimizing-NBA-Player-Selection/Optimization/Team_undercap_maxvictories.csv', index = False)

# Win prediction
np.mean(players.loc[(players.decision == 1) & (players.role_FU == 1)]['ORtg'])
np.mean(players.loc[(players.decision == 1) & (players.role_FU == 0)]['ORtg'])
np.mean(players.loc[(players.decision == 1) & (players.role_FU == 1)]['DRtg'])
np.mean(players.loc[(players.decision == 1) & (players.role_FU == 0)]['DRtg'])

sum_ORtg_top5 = sum(players.loc[(players.decision == 1) & (players.role_FU == 1)]['ORtg'])
sum_ORtg_mid5 = sum(players.loc[(players.decision == 1) & (players.role_FU == 0)]['ORtg'])
sum_DRtg_top5 = sum(players.loc[(players.decision == 1) & (players.role_FU == 1)]['DRtg'])
sum_DRtg_mid5 = sum(players.loc[(players.decision == 1) & (players.role_FU == 0)]['DRtg'])
sum(players.loc[players.decision == 1]['Salary 2018-19'])

win = b0 + b1*sum_ORtg_top5 + b2*sum_ORtg_mid5 + b3*sum_DRtg_top5 + b4*sum_DRtg_mid5
win
min_victories_to_champ = 0.7598130494939783


'''
test = pd.read_csv('/Users/mac/GitHub/Optimizing-NBA-Player-Selection/Datasets/total_team_data.csv')
i = 'Milwaukee Bucks'
test.loc[test.Team == i]['ORtg_mid5'].sum()
mb1 = sum(players.loc[(players.Team == i) & (players.role_FU == 1)]['ORtg'])
mb2 = sum(players.loc[(players.Team == i) & (players.role_SU == 1)]['ORtg'])
mb3 = sum(players.loc[(players.Team == i) & (players.role_FU == 1)]['DRtg'])
mb4 = sum(players.loc[(players.Team == i) & (players.role_SU == 1)]['DRtg'])

win = b0 + b1*mb1 + b2*mb2 + b3*mb3 + b4*mb4
win

test.loc[test.Team == i]['W/L%'].sum()

players.loc[(players.Team == i)]
'''
