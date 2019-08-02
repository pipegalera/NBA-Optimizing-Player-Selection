from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

url = "https://www.basketball-reference.com/leagues/NBA_2019_ratings.html"

# Opening up connection, grabbing the page
html = urlopen(url)
soup = BeautifulSoup(html)

# Getting headers and removing incorrect column
headers_files = soup.findAll('tr')[1]
headers = [i.getText() for i in headers_files.findAll('th')]
headers.remove('Rk')

# Getting the body
rows = soup.findAll('tr')[1:]
stats = [[i.getText() for i in rows[x].findAll('td')]
            for x in range(len(rows))]
adv_stats_2 = pd.DataFrame(stats).dropna()
adv_stats_2.columns = headers
adv_stats_2 = adv_stats_2.drop(columns = ['W', 'L'])

adv_stats_2.to_csv('/Users/mac/GitHub/Optimizing-NBA-Player-Selection/Datasets/BR_TS.csv', index=False)
BR_TS = pd.read_csv('/Users/mac/GitHub/Optimizing-NBA-Player-Selection/Datasets/BR_TS.csv')
BR_TS.head()
