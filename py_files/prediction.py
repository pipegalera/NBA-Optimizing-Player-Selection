# @Author: pipegalera
# @Date:   2020-04-08T18:30:21+02:00
# @Last modified by:   pipegalera
# @Last modified time: 2020-04-08T21:42:03+02:00



import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn import preprocessing
from sklearn import utils
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import imgkit
import seaborn as sns; sns.set(style="white", color_codes=True)
import matplotlib.pyplot as plt

data_teams = pd.read_csv('/Users/mac/GitHub/Optimizing-NBA-Player-Selection/Datasets/total_team_data.csv')
data_teams_years = pd.read_csv('/Users/mac/GitHub/Optimizing-NBA-Player-Selection/Datasets/BR_TS_allyear.csv')
data_teams.shape
data_teams.columns

# Missing values: None
data_teams.isnull().any().sum()

#Preprocessing
#data_teams.info()
#data_teams = data_teams.set_index('Team')
#dummies = pd.get_dummies(data_teams[['Conf', 'Div']])
# df = pd.concat([df, dummies], axis = 1)

###########################################
# Model1 : Win% = B0 + B1*ORtg + B2*DRtg  #
###########################################
df = data_teams_years
list = ['ORtg', 'DRtg',]
list_n = []
for i in list:
     list_n.append(df.columns.get_loc('{}'.format(i)))
list_n
#Trainning the model
y_1 = df.iloc[:,3].values
X_1 = df.iloc[:,list_n].values
X_train, X_test, y_train, y_test = train_test_split(X_1, y_1, test_size = 0.3, random_state = 42)

# Lineal Regression
reg = linear_model.LinearRegression()
reg.fit(X_train, y_train)
y_pred_reg = reg.predict(X_test)
reg_score = reg.score(X_test, y_test)
reg_score #0.92
r2_score(y_pred_reg, y_test)

reg.intercept_
reg.coef_[0]
reg.coef_[1]

#Visualization of the LinearRegression
list = ['W/L%', 'NRtg']
list_n = []
for i in list:
     list_n.append(data_teams_years.columns.get_loc('{}'.format(i)))
list_n
sns.set(color_codes=True)
g = sns.lmplot(x = 'W/L%', y = 'NRtg',
                data = data_teams_years, line_kws={'color': 'darkslategrey'}, scatter_kws={'color': 'gainsboro'},
                );
g.set(xlabel='Win Rate %', ylabel='Net Rating')
g.savefig("output.png")

#######################################################
# Model2 : Win% = B0 + B1*ORtg_top10 + B2*DRtg_top10  #
#######################################################
df = data_teams.drop(columns = ['Conf', 'Div']) # GP is constant: 82
list = ['ORtg_top10', 'DRtg_top10']
list_n = []
for i in list:
     list_n.append(df.columns.get_loc('{}'.format(i)))

y_2 = df.iloc[:,1].values
X_2 = df.iloc[:,list_n].values
X_train, X_test, y_train, y_test = train_test_split(X_2, y_2, test_size = 0.3, random_state = 42)
reg = linear_model.LinearRegression()
reg.fit(X_train, y_train)
y_pred_reg = reg.predict(X_test)
reg_score = reg.score(X_test, y_test)
reg_score #0.86
r2_score(y_pred_reg, y_test) #0.78
reg.intercept_
reg.coef_[0]
reg.coef_[1]

###################################################################################
# Model3 : Win% = B0 + B1*ORtg_top5 + B2*ORtg_mid5 + B3*DRtg_top5  + B4*DRtg_mid5 #
###################################################################################

list = ['ORtg_top5', 'ORtg_mid5', 'DRtg_top5', 'DRtg_mid5']
list_n = []
for i in list:
     list_n.append(df.columns.get_loc('{}'.format(i)))
y_3 = df.iloc[:,1].values
X_3 = df.iloc[:,list_n].values
X_train, X_test, y_train, y_test = train_test_split(X_3, y_3, test_size = 0.3, random_state = 42)
reg = linear_model.LinearRegression()
reg.fit(X_train, y_train)
y_pred_reg = reg.predict(X_test)
reg_score = reg.score(X_test, y_test)
reg_score #0.92
r2_score(y_pred_reg, y_test) #0.90
reg.intercept_
reg.coef_[0]
reg.coef_[1]
reg.coef_[2]
reg.coef_[3]

###################################################################################
# Model4 : Win% = B0 + B1*PER_top5 + B2*PER_mid5 + B3*DRtg_top5  + B4*DRtg_mid5   #
###################################################################################

list = ['PER_top5', 'PER_mid5', 'DRtg_top5', 'DRtg_mid5']
list_n = []
for i in list:
     list_n.append(df.columns.get_loc('{}'.format(i)))

y_4 = df.iloc[:,1].values
X_4 = df.iloc[:,list_n].values
X_train, X_test, y_train, y_test = train_test_split(X_4, y_4, test_size = 0.3, random_state = 42)
reg = linear_model.LinearRegression()
reg.fit(X_train, y_train)
y_pred_reg = reg.predict(X_test)
reg_score = reg.score(X_test, y_test)
reg_score #0.71
r2_score(y_pred_reg, y_test) #0.62
reg.intercept_
reg.coef_[0]
reg.coef_[1]
reg.coef_[2]
reg.coef_[3]

###################################################################################
# Model5 : y = B0 + B1*ORtg_top5 + B2*ORtg_mid5 + B3*DRtg_top5  + B4*DRtg_mid5    #
#  Win% = 1/(1 + e^−y)                                                            #
###################################################################################

list = ['ORtg_top5', 'ORtg_mid5', 'DRtg_top5', 'DRtg_mid5']
list_n = []
for i in list:
     list_n.append(df.columns.get_loc('{}'.format(i)))
y_5 = df.iloc[:,1].values
y_5_log = []
for i in y_5:
    y_5_log.append(1/(1+ np.exp(-i)))
X_5 = df.iloc[:,list_n].values
X_train, X_test, y_train, y_test = train_test_split(X_5, y_5_log, test_size = 0.3, random_state = 42)
reg.fit(X_train, y_train)
y_pred_reg = reg.predict(X_test)
reg_score = reg.score(X_test, y_test)
reg_score #0.92
r2_score(y_pred_reg, y_test) #0.89
reg.intercept_
reg.coef_[0]
reg.coef_[1]
reg.coef_[2]
reg.coef_[3]
