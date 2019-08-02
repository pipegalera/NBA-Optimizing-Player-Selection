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

# Stats per 100 possesions
url2 = 'https://www.basketball-reference.com/leagues/NBA_2019_per_poss.html'
html = urlopen(url2)
soup = BeautifulSoup(html)
headers_files = soup.findAll('tr')[0]
headers = [i.getText() for i in headers_files.findAll('th')]
headers.remove('Rk')
headers = ['Team' if x == 'Tm' else x for x in headers]
headers
rows = soup.findAll('tr')[1:]
stats = [[i.getText() for i in rows[x].findAll('td')]
            for x in range(len(rows))]
stats = pd.DataFrame(stats).dropna()
stats.columns = headers
stats = stats.drop(columns = ['', 'Pos', 'Age', 'G', 'MP'],axis = 1)

# stats['Player'].loc[562] == adv_stats['Player'].loc[562]

merge = pd.merge(stats, adv_stats, on = 'Player')
merge = merge[merge['Team_x'] == merge['Team_y']].reset_index()

merge.to_csv('/Users/mac/GitHub/Optimizing-NBA-Player-Selection/Datasets/BR_PS.csv', index=False)
BR_PS = pd.read_csv('/Users/mac/GitHub/Optimizing-NBA-Player-Selection/Datasets/BR_PS.csv')
BR_PS.head()
BR_PS.columns
