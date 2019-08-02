import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

data_teams = pd.read_csv('/Users/mac/GitHub/NBA_Scrappers/Team Stats/final_data.csv')



# Missing values: None
data_teams.isnull().sum()

#Preprocessing
data_teams.info()
data_teams = data_teams.set_index('Team')
dummies = pd.get_dummies(data_teams[['Conf', 'Div']])
df = data_teams.drop(columns = ['W', 'L','GP', 'Conf', 'Div']) # GP is constant: 82
df = pd.concat([df, dummies], axis = 1)






#Trainning the model
df.drop(columns = 'WIN%')
y = df.iloc[:,0].values
df.columns
df[['PER_top5', 'PER_mid5', 'ORtg', 'DRtg']]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 42)

# Lineal Regression

reg = linear_model.LinearRegression()
reg.fit(X_train, y_train)
y_pred_reg = reg.predict(X_test)
reg_score = reg.score(X_test, y_test)
reg_score

# Logistic Regression

logreg = LogisticRegression()
logreg.fit(X_train, y_train)
