from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

url = "https://www.basketball-reference.com/contracts/players.html"

# Opening up connection, grabbing the page
html = urlopen(url)
soup = BeautifulSoup(html)
headers = ['PLAYER', 'TEAM', '2018-2019', '2019-2020', '2020-2021', '2021-2022', '2022-2023', '2023-2024', 'Signed Using', 'Guaranteed']
rows = soup.findAll('tr')[1:]
salaries = [[td.getText() for td in rows[i].findAll('td')]
            for i in range(len(rows))]
salaries = pd.DataFrame(salaries, columns = headers).dropna()
salaries.head()

salaries.to_csv('/Users/mac/GitHub/NBA Scrappers/Salaries/Salaries_scrapper_NBA.csv', index=False)
