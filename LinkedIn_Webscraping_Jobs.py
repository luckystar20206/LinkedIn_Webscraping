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
driver.get('https://www.linkedin.com/jobs/collections/recommended')

#Defining empty lists for future data collection
job_data = []
company_data = []
location_data = []
data_role = []

#Defining the collection process function
def collection(page):
    for row in page.find_all('li'):
        job = row.find_all('a', class_ = 'disabled ember-view job-card-container__link job-card-list__title')
        company = row.find_all('a', class_ = 'job-card-container__link job-card-container__company-name ember-view')
        location = row.find_all('li', class_ = 'job-card-container__metadata-item')
        x = 0
        for item in job:
            col1 = item.get_text()
            col1 = col1.strip()
            job_data.append(col1)
        for item in company:
            col2 = item.get_text()
            col2 = col2.strip()
            company_data.append(col2)
        for item in location:
            while x < 1:
                col3 = item.get_text()
                col3 = col3.strip()
                location_data.append(col3)
                x+=1

#Collecting all relevant data using bs4
source = driver.page_source
page1 = bs(source, 'lxml')
collection(page1)
time.sleep(5)
driver.find_element(By.XPATH, "//button[@aria-label='Page 2']").click()
source = driver.page_source
page2 = bs(source, 'lxml')
collection(page2)
time.sleep(5)
driver.find_element(By.XPATH, "//button[@aria-label='Page 3']").click()
source = driver.page_source
page3 = bs(source, 'lxml')
collection(page3)
time.sleep(5)
driver.find_element(By.XPATH, "//button[@aria-label='Page 4']").click()
source = driver.page_source
page4 = bs(source, 'lxml')
collection(page4)
time.sleep(5)
driver.find_element(By.XPATH, "//button[@aria-label='Page 5']").click()
source = driver.page_source
page5 = bs(source, 'lxml')
collection(page5)
time.sleep(5)

data = pd.DataFrame({'Name': job_data, 'Company': company_data, 'Location': location_data})

#Adding an additional column to the dataframe that notes whether the role title contains "data"
for item in data['Name']:
    if "Data" in item:
        data_role.append("Data Role")
    else:
        data_role.append("Non-data Role")

data = pd.DataFrame({'Name': job_data, 'Company': company_data, 'Location': location_data, 'Data Role?': data_role})

#Converting the data to csv - enter your desired output location in the open parentheses below
data.to_csv()