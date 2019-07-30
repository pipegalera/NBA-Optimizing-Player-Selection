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

adv_stats_2.to_csv('/Users/mac/GitHub/NBA_Scrappers/Advanced Stats/Advanced_stats_NBA_2.csv', index=False)
# adv_stats_2 = pd.read_csv('/Users/mac/GitHub/NBA_Scrappers/Advanced Stats/Advanced_stats_NBA_2.csv')
