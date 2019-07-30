from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

url = 'https://hoopshype.com/salaries/players/2018-2019/'
html = urlopen(url)
soup = BeautifulSoup(html)
rows = soup.findAll('tr')[1:]

rows
salaries = [[td.getText() for td in rows[i].findAll('td')]
            for i in range(len(rows))]
salaries
