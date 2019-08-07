import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pulp import *
import re

total_players_data = pd.read_csv('/Users/mac/GitHub/Optimizing-NBA-Player-Selection/Datasets/BR_players_data.csv')
total_players_data.columns
# Prepare data

list = ['Player','PER', 'DRtg', 'Salary 2018-19']
list_n = []
for i in list:
     list_n.append(total_players_data.columns.get_loc('{}'.format(i)))

players = total_players_data.iloc[:,list_n]
players.columns

# Strategy: select players that max stats
prob = pulp.LpProblem('Max_stats', pulp.LpMaximize)

# Create Decision Variables: Every player

vars = []
for rownum, row in players.iterrows(): #For every row create a decision variable
    var = str('x' + str(rownum))
    var = pulp.LpVariable(str(var), lowBound = 0, upBound = 1, cat= 'Integer') # Decision problem is binary(0,1)
    vars.append(var)
# Objective Function: this is the function that we LpMaximize.
b0 = -0.14752804620561444
b1 = 0.03183355672376642
b2 = -0.02601432313805421


total_PER = ""
for rownum, row in players.iterrows():
    for i, schedule in enumerate(vars):
        if rownum == i:
            formula = row['PER']* schedule
            total_PER += formula
total_PER
prob += (b1*total_PER)
'''
total_ORtg = ""
for rownum, row in players.iterrows():
    for i, schedule in enumerate(vars):
        if rownum == i:
            formula = row['ORtg']* schedule
            total_ORtg += formula
prob += total_ORtg
'''
total_DRtg = ""
for rownum, row in players.iterrows():
    for i, schedule in enumerate(vars):
        if rownum == i:
            formula = row['DRtg']* schedule
            total_DRtg += formula
total_DRtg
prob += (b2*total_DRtg)

# Definning a Constrains:

# Salary
salary_cap = 101900000
total_salary = ""
for rownum, row in players.iterrows():
    for i, schedule in enumerate(vars):
        if rownum == i:
            formula = row['Salary 2018-19']* schedule
            total_salary += formula

prob += (total_salary <= salary_cap)
vars

# Team number
total_number = ""
for rownum, row in players.iterrows():
    for i, schedule in enumerate(vars):
        if rownum == i:
            formula = 1 * schedule
            total_number += formula

prob += (total_number == 10)
prob

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
for rownum, row in players.iterrows():
    for results_rownum, results_row in df.iterrows():
        if rownum == results_row['variable']:
            players.loc[rownum, 'decision'] = results_row['value']


players.decision.sum()
players.loc[players.decision == 1]

players.loc[players.decision == 1]

win = b0 + b1*

players = players.drop('decision', axis = 1)

total_players_data.columns
total_players_data.loc[total_players_data.Player == 'Gary Payton']
