from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep
import pandas as pd
import numpy as np
import re

# Mimic as much as posible a human user to avoid "max connection entries error"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--profile-directory=Default')
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-plugins-discovery")
chrome_options.add_argument("--start-maximized")
driver_path = '/Users/mac/GitHub/NBA_Scrappers/chromedriver'

# Grab url and run driver
url = 'https://stats.nba.com/teams/traditional/?sort=W_PCT&dir=-1'
# Check page status
timeout = 10
try:
    # Assumption: if the NBA logo loads, then the page loads.
    driver = webdriver.Chrome(driver_path, chrome_options=chrome_options)
    driver.delete_all_cookies()
    driver.get(url)
    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[3]/div/div/select/option[1]')))
    print('Page loaded correctly')
except TimeoutException:
    print('Timed out waiting for page to load')

# Extract table
table = driver.find_element_by_class_name('nba-stat-table__overflow')

# Headers
headers = table.find_elements_by_tag_name('th')
file_header = []
file_header.append([x.text for x in headers])
header = pd.DataFrame(file_header)
header = header[np.arange(1, 28)]
header = header.values.tolist()
header
# Body
body = table.find_elements_by_tag_name('tbody')
file_body = []
for element in body:
    element = element.text
    X= element.split("\n")
    file_body.append(X)
body_unstructured = pd.DataFrame(file_body).T
teams = body_unstructured.iloc[np.arange(1,90,3)].reset_index(drop = True)
stats = body_unstructured.iloc[np.arange(2,90,3)].reset_index(drop = True)
stats = stats[0].str.split(' ', 26, expand = True)
stats.shape
teams.shape
df = pd.concat([teams, stats], axis = 1)
df.columns = header
df = df.rename(columns = {'TEAM': 'Team'})
df.to_csv('/Users/mac/GitHub/NBA Optimizing Player Selection/Datasets/NBA_TS.csv', index=False)
NBA_TS = pd.read_csv('/Users/mac/GitHub/NBA Optimizing Player Selection/Datasets/NBA_TS.csv')
NBA_TS.head()
