from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

url = "https://www.basketball-reference.com/contracts/players.html"

# Opening up connection, grabbing the page
html = urlopen(url)
soup = BeautifulSoup(html)
headers = ['Player', 'Team', 'Salary 2018-19', 'Salary 2019-20', 'Salary 2020-21', 'Salary 2021-22', 'Salary 2022-23', 'Salary 2023-24', 'Signed Using', 'Guaranteed']
rows = soup.findAll('tr')[1:]
salaries = [[td.getText() for td in rows[i].findAll('td')]
            for i in range(len(rows))]

salaries = pd.DataFrame(salaries, columns = headers).dropna()
salaries = salaries.apply(lambda x: x.str.replace('$', ''))
salaries = salaries.apply(lambda x: x.str.replace(',', ''))

# Handleling missing data
salaries['Salary 2019-20'] = salaries['Salary 2019-20'].replace('', 0)
salaries['Salary 2020-21'] = salaries['Salary 2020-21'].replace('', 0)
salaries['Salary 2021-22'] = salaries['Salary 2021-22'].replace('', 0)
salaries['Salary 2022-23'] = salaries['Salary 2022-23'].replace('', 0)
salaries['Salary 2023-24'] = salaries['Salary 2023-24'].replace('', 0)
salaries['Guaranteed'] = salaries['Guaranteed'].replace('', 0)
salaries['Signed Using'] = salaries['Signed Using'].replace('', 'Other')

# Changing the type from objects to integers
salaries['Salary 2018-19'] = salaries['Salary 2018-19'].astype('int')
salaries['Salary 2019-20'] = salaries['Salary 2019-20'].astype('int')
salaries['Salary 2020-21'] = salaries['Salary 2020-21'].astype('int')
salaries['Salary 2021-22'] = salaries['Salary 2021-22'].astype('int')
salaries['Salary 2022-23'] = salaries['Salary 2022-23'].astype('int')
salaries['Salary 2023-24'] = salaries['Salary 2023-24'].astype('int')
salaries['Guaranteed'] = salaries['Guaranteed'].astype('int')

# Agregating the contracts within the same team
salaries = salaries.groupby(['Player', 'Team', 'Guaranteed'], as_index = False ).sum()

''' test salaries
salaries.loc[salaries['Player'] == 'Dwight Howard']
salaries.loc[salaries['Player'] == 'Cameron Reynolds']
'''


salaries.to_csv('/Users/mac/GitHub/NBA Optimizing Player Selection/Datasets/BR_PSalaries.csv', index=False)
BR_PSalaries = pd.read_csv('/Users/mac/GitHub/NBA Optimizing Player Selection/Datasets/BR_PSalaries.csv')
BR_PSalaries.head()
