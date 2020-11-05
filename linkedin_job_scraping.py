#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# linkedin_login.py
import os
import pandas as pd
from parsel import Selector
from time import sleep
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

if os.path.isfile('./opportunities.csv') is True:
    opportunities = pd.read_csv('opportunities.csv')
else:
    dict = {'Job Title': [], 'Company Name': [], 'Location': [], 'Direct URL': [],'Linkedin Link': []}
    df = pd.DataFrame(dict)
    df.to_csv('opportunities.csv',mode = 'a', header = True, index = False)
    opportunities = pd.read_csv('opportunities.csv')

# install webdrive when needed
driver = webdriver.Chrome(ChromeDriverManager().install())

print('\nExecuting Linkedin Login...')
# driver.get method() will navigate to a page given by the URL address
driver.get('https://www.linkedin.com/login')

# locate email form by element_by_id
username = driver.find_element_by_id('username')

# send_keys() to simulate key strokes
username.send_keys(config.get('LINKEDIN_LOGIN', 'email'))

# locate password form by_class_name
password = driver.find_element_by_id('password')

# send_keys() to simulate key strokes
password.send_keys(config.get('LINKEDIN_LOGIN', 'password'))

# locate submit button by_class_name
log_in_button = driver.find_element_by_class_name('btn__primary--large')

# locate submit button by_xpath
log_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
log_in_button.click()

print('\nStarting Posting Search...')
# driver goest to the jobs page
driver.get('https://www.linkedin.com/jobs/')
sleep(2)

# Start search term
search_job = driver.find_element_by_xpath('//*[@type="text"]')
search_job.send_keys(config.get('LINKEDIN_LOGIN', 'search_term'))
sleep(1)
#search.send_keys(Keys.RETURN)

# location
search_location = driver.find_element_by_xpath('//input[starts-with(@id,"jobs-search-box-location")]')
search_location.send_keys(Keys.COMMAND, 'a') #COMMAND is the mac keyboard control
search_location.send_keys(Keys.BACKSPACE)
search_location.send_keys(config.get('LINKEDIN_LOGIN', 'country'))
search_location.send_keys(Keys.RETURN)
sleep(3)

# Gets the URL from the search result
linkedin_result = driver.current_url

# Scroll job list to the end of first page
recentList = driver.find_elements_by_class_name('jobs-search-results__list-item')
for list in recentList :
    driver.execute_script("arguments[0].scrollIntoView();", list)
    sleep(0.1)

# Get full list of positions name
position_name = driver.find_elements_by_class_name('job-card-list__title')
position_name = [url.text for url in position_name]
position_name
# len(position_name)

# Get listing Company Name
company_name = driver.find_elements_by_css_selector('.job-card-container__company-name')
company_name = [url.text for url in company_name]
company_name
# len(company_name)

# Get listing location
job_location = driver.find_elements_by_xpath('//div[starts-with(@class,"artdeco-entity-lockup__caption")]')
job_location = [url.text for url in job_location]
job_location
# len(job_location)

# Get full list of links positions
position_link = driver.find_elements_by_css_selector("div.artdeco-entity-lockup__title > a")
position_link = [link.get_attribute("href") for link in position_link]
position_link
# len(position_link)

print('\nTotal posts: ',len(position_link))
print('\nStart buinding direct links...')
main_window_name = driver.window_handles[0]

def write_to_csv(posname,compname,joblocation,direct,link):
    print('Writing Position ',posname, 'to CSV\n')
    dict = {'Job Title': [posname], 'Company Name': [compname], 'Location': [joblocation], 'Direct URL': [direct],'Linkedin Link': [link]}
    df = pd.DataFrame(dict)
    df.to_csv('opportunities.csv',mode = 'a', header = True, index = False)

def validate_url(link):
    if link in opportunities.values:
        print('Position already exist')
        return True
    else:
        print('\nPosition does not exist')
        return False

def apply_position():
    apply_btn = driver.find_element_by_xpath("//button[contains(@class,'jobs-apply-button')]")
    apply_btn.click()
    #driver.execute_script("window.open('http://google.com', 'new_window')")
    sleep(5)
    #print(driver.window_handles[counter])
    window_name = driver.window_handles[1]
    driver.switch_to.window(window_name=window_name)
    direct_url.append(driver.current_url)
    driver.close()
    sleep(5)
    driver.switch_to.window(window_name=main_window_name)
    #counter += 1
    #print('Current counter = ', counter)

direct_url = []
for link in position_link :
    driver.get(link)
    sleep(3)
    # status = 'not applied'
    try:
        try:
            driver.find_element_by_xpath("//a//li-icon[contains(@type,'document-icon')]")
            direct_url.append('Applied')
            #counter += 1
            #print('Current counter = ', counter)

        except NoSuchElementException:
            driver.find_element_by_xpath("//button//li-icon[contains(@type,'linkedin-bug')]")
            direct_url.append('Easy Apply')
            sleep(5)
            # window_name = driver.window_handles[counter]
            driver.switch_to.window(window_name=main_window_name)
            #counter += 1
            #print('Current counter = ', counter)

    except NoSuchElementException:
        apply_position()

for posname,compname,joblocation,direct,link in zip(position_name,company_name,job_location,direct_url,position_link):
    if validate_url(link) is True:
        print('\nPosition already recorded: ',posname, 'to CSV')
        pass
    else:
        write_to_csv(posname,compname,joblocation,direct,link)
