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
salaries.head()
salaries = salaries.apply(lambda x: x.str.replace('$', ''))
salaries = salaries.apply(lambda x: x.str.replace(',', ''))

salaries.to_csv('/Users/mac/GitHub/NBA_Scrappers/Salaries/Salaries_scrapper_NBA.csv', index=False)
salaries.duplicated
