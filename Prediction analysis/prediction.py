
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

data_teams = pd.read_csv('/Users/mac/GitHub/Optimizing-NBA-Player-Selection/Datasets/total_team_data.csv')
data_teams.shape
data_teams.columns

# Missing values: None
data_teams.isnull().any().sum()

# Feature Selection

features_sel = data_teams.drop(columns = 'Team')
dummies = pd.get_dummies(features_sel[['Conf', 'Div']])
features_sel = pd.concat([features_sel, dummies], axis = 1)
corr = features_sel.corr(method = 'pearson')
corr.style.background_gradient(cmap = 'coolwarm')

#Preprocessing
#data_teams.info()
# data_teams = data_teams.set_index('Team')
# dummies = pd.get_dummies(data_teams[['Conf', 'Div']])
df = data_teams.drop(columns = ['Conf', 'Div']) # GP is constant: 82
# df = pd.concat([df, dummies], axis = 1)

###########################################
# Model1 : Win% = B0 + B1*ORtg + B2*DRtg  #
###########################################
list = ['ORtg', 'DRtg']
list_n = []
for i in list:
     list_n.append(df.columns.get_loc('{}'.format(i)))

#Trainning the model
y_1 = df.iloc[:,1].values
X_1 = df.iloc[:,list_n].values
X_train, X_test, y_train, y_test = train_test_split(X_1, y_1, test_size = 0.3, random_state = 42)

# Lineal Regression
reg = linear_model.LinearRegression()
reg.fit(X_train, y_train)
y_pred_reg = reg.predict(X_test)
reg_score = reg.score(X_test, y_test)
reg_score #0.98
r2_score(y_pred_reg, y_test)

reg.intercept_
reg.coef_[0]
reg.coef_[1]
