from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

url = "https://www.basketball-reference.com/leagues/NBA_2019_advanced.html"

# Opening up connection, grabbing the page
html = urlopen(url)
soup = BeautifulSoup(html)

# Getting headers and removing incorrect columns
headers_files = soup.findAll('tr')[0]
headers = [i.getText() for i in headers_files.findAll('th')]
headers.remove('\xa0')
headers.remove('\xa0')
headers.remove('Rk')
headers = ['Team' if x == 'Tm' else x for x in headers]
# Getting the body
rows = soup.findAll('tr')[1:]
stats = [[i.getText() for i in rows[x].findAll('td')]
            for x in range(len(rows))]
adv_stats = pd.DataFrame(stats).dropna()

adv_stats = adv_stats.drop([18, 23], axis = 1)
adv_stats.columns = headers
adv_stats.shape

adv_stats.to_csv('/Users/mac/GitHub/NBA_Scrappers/Advanced Stats/Advanced_stats_NBA.csv', index=False)
# adv_stats = pd.read_csv('/Users/mac/GitHub/NBA_Scrappers/Advanced Stats/Advanced_stats_NBA.csv')
adv_stats
