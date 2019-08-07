from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

url_list = []
year = [2019]
for i in year: # year = range(2012,2019) for more years
        url = "https://www.basketball-reference.com/leagues/NBA_{year}_ratings.html".format(year = i)
        url_list.append(url)

url_list
stats_df = pd.DataFrame()
for i in url_list:
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
    stats_df = stats_df.append(stats).dropna()


stats_df.columns = headers
stats_df = stats_df.drop(columns = ['W', 'L'])
stats_df.shape
len(url_list) * 30
stats_df.columns
stats_df.reset_index(drop = True)
stats_df.to_csv('/Users/mac/GitHub/Optimizing-NBA-Player-Selection/Datasets/BR_TS.csv', index=False)
BR_TS = pd.read_csv('/Users/mac/GitHub/Optimizing-NBA-Player-Selection/Datasets/BR_TS.csv')
BR_TS.shape
