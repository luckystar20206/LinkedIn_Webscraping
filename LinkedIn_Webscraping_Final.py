#Ensure that you are able to import all libraries below before running
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup as bs
import html5lib
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

#Setting up the Edge webdriver - enter the file path of your driver in the open parentheses below
driver = webdriver.Edge()

#Logging into LinkedIn by passing Username and Password - enter your username and password in the .send_keys open parentheses below.
driver.get('https://www.linkedin.com/uas/login')
time.sleep(5)
username = driver.find_element(By.ID, "username")
username.send_keys()
pword = driver.find_element(By.ID, 'password')
pword.send_keys()
driver.find_element(By.XPATH, "//button[@type='submit']").click()
driver.get('https://www.linkedin.com/mynetwork/invite-connect/connections/')

#Scrolling through the webpage in order to capture all list elements - add or subtract break time as needed.
start = time.time()
initialScroll = 0
finalScroll = 1000 
while True:
    driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
    initialScroll = finalScroll
    finalScroll += 1000
    time.sleep(3)
    end = time.time()
    if round(end - start) > 20:
        break
driver.find_element(By.XPATH, "//button[@class='artdeco-button artdeco-button--muted artdeco-button--1 artdeco-button--full artdeco-button--secondary ember-view scaffold-finite-scroll__load-button']").click()
start = time.time()
initialScroll = 100
finalScroll = 1000
while True:
    driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
    initialScroll = finalScroll
    finalScroll += 1000
    time.sleep(3)
    end = time.time()
    if round(end - start) > 190:
        break

#Collecting all relevant data using bs4
source = driver.page_source
soup = bs(source, 'lxml')
name_data = []
occupation_data = []
for row in soup.find_all('li'):
    name = row.find_all('span', class_ = 'mn-connection-card__name t-16 t-black t-bold')
    occupation = row.find_all('span', class_ = 'mn-connection-card__occupation t-14 t-black--light t-normal')
    for item in name:
        col1 = item.get_text()
        col1 = col1.strip()
        name_data.append(col1)
    for item in occupation:
        col2 = item.get_text()
        col2 = col2.strip()
        occupation_data.append(col2)
data = pd.DataFrame({'Name': name_data, 'Occupation': occupation_data})

#Converting the data to csv - enter your desired output location in the open parentheses below
data.to_csv()