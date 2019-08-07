import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pulp import *


total_players_data = pd.read_csv('/Users/mac/GitHub/Optimizing-NBA-Player-Selection/Datasets/BR_players_data.csv')

# Prepare data

list = ['PER', 'DRtg', 'Salary 2018-19']
for i in list:
     print(total_players_data.columns.get_loc('{}'.format(i)))

players = total_players_data.iloc[:,[0,31,25, 52]]
players.columns

# Strategy: select players to achieve the maximum team winning percentage under limited budget

prob = pulp.LpProblem('Minfuntion', pulp.LpMinimize)

# Create Decision Variables

vars = []
for rownum, row in players.iterrows(): #For every row create a decision variable
    var = str('x' + str(rownum))
    var = pulp.LpVariable(str(var), lowBound = 0, upBound = 1, cat= 'Integer')
    vars.append(var)

str(len(vars))
str(vars)

# Objective Function

total_salary = ""
for rownum, row in players.iterrows():
    for i, schedule in enumerate(vars):
        if rownum == i:
            formula = row['Salary 2018-19']* schedule
            total_salary += formula

prob += total_salary
total_salary # Every decision variable times the salary
players

# STOPPED HERE: I HAD TO CATEGORIZE THE PLAYERS in BR_player_data
# Definning a Constrains: The Winning thresshold has to be 70% winning

win = 70
total_win = ""
for rownum, row in players.iterrows():
    for i, schedule in enumerate(vars):
        for rownum == i:
            formula = row['Salary 2018-19']* schedule
            total_salary += formula
