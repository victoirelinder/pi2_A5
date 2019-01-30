from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as ec

from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from requests.exceptions import ConnectionError
from urllib3.exceptions import MaxRetryError

import regex as re
import getpass
import requests
import os
import sys
import time
import pandas as pd
import credentials_linkedin as cred

from threading import Thread


class LinkedIn_Analysis(Thread):
    """ copyright© 2019 — Luc Bertin - License MIT """
    def __init__(self, keyword='', page_limit=None, output_filename='LinkedInCompanies.csv', STOP_EXECUTION=0):
        Thread.__init__(self)
        self.keyword = keyword
        self.page_exit = 0
        self.output_filename = output_filename
        if page_limit is None:
            self.page_limit = 100 ## Maximum scrappable pages
        else:
            self.page_limit = page_limit
        self.STOP_EXECUTION = STOP_EXECUTION

    @staticmethod
    def remove_duplicates(lst):
        res = []
        for x in lst:
            if x not in set(res):
                res.append(x)
        return res

    
    def run(self):
        self.STOP_EXECUTION = 1
        # Options for the web driver (here incognito mode for Chrome, optional)
        options = webdriver.ChromeOptions()
        options.add_argument(' — incognito')
        # Get the webdriver from its location path
        driver = webdriver.Chrome(executable_path='/Users/lucbertin/Desktop/chromedriver', options = options)
        # Go to LinkedIn main connection page
        driver.get("https://www.linkedin.com/uas/login")
        timeout = 4
        # Handling TimeOutException if connection is bad or even nonxistent
        try:
            WebDriverWait(driver, timeout).until(ec.visibility_of_all_elements_located((By.CSS_SELECTOR, "input[id=username]")))
        except TimeoutException:
            print("Timed out waiting for page to load")
            driver.quit()
            sys.exit(1)

        # Enter ID/password
        driver.find_element(By.CSS_SELECTOR, "input[id='username']").send_keys(cred.USER_ID)
        driver.find_element(By.CSS_SELECTOR, "input[id='password']").send_keys(cred.USER_PASSWORD)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(2)

        companies_name = []
        companies_url = []
        a=True
        page_number=1
        halt=False
        while page_number<=self.page_limit:
            try:
                url = "https://www.linkedin.com/search/results/companies/"
                if len(self.keyword)>1:
                    url += '?keywords='+str(self.keyword)+'&origin=SWITCH_SEARCH_VERTICAL&page='+str(page_number)
                else:
                    url+= '?origin=SWITCH_SEARCH_VERTICAL&page='+str(page_number)
                driver.get(url)
                #driver.get('https://www.linkedin.com/search/results/companies/?origin=SWITCH_SEARCH_VERTICAL&page='+str(page_number))
                WebDriverWait(driver, timeout).until(
                    ec.visibility_of_all_elements_located((By.CSS_SELECTOR, "ul[class='search-results__list list-style-none mt2']")))
                
                temp_elements = driver.find_elements(By.CSS_SELECTOR, "a[data-control-name='search_srp_result']")
                temp_companies_name = [x.text for x in temp_elements if len(x.text)>1]
                
                temp_companies_urls = [str(x.get_attribute('href'))+ "about/"  for x in temp_elements]
                
                ## Attaching to main list, removing duplicates whilst preserving order
                companies_name.extend(self.remove_duplicates(temp_companies_name))
                companies_url.extend(self.remove_duplicates(temp_companies_urls))
                
                page_number+=1
                print("page number "+ str(page_number)+ " over 100\n")
            except:
                if self.STOP_EXECUTION==2:
                    self.STOP_EXECUTION=0
                    halt=True
                    driver.quit()
                    break
                print('Retrying in 5 secondes...')
                time.sleep(5)
                #break
                #driver.quit()
        print(len(companies_name))
        print(len(companies_url))
        print(companies_name)
        print("\n")
        print(companies_url)
        if halt != True:
        

            """
            with open("companies_list_and_urls.txt",'w') as f:
                f.write(repr(companies_name))
                f.write('\n')
                f.write(repr(companies_url))
            """
    
            ## Downloading about from companies
            about_companies = []
            companies_followers_nb = []
            companies_category = []
            companies_location =[]
    
            progress = 100/len(companies_name)
            
    
            for url in companies_url:
                try:
                    driver.get(url)
                    WebDriverWait(driver, timeout).until(
                        ec.visibility_of_all_elements_located((By.CSS_SELECTOR, "p[class='break-words white-space-pre-wrap mb5 t-14 t-black--light t-normal']")))
                    print("progress : "+ str(round(progress,2))+ " % \n")
                    ## about from companies
                    element = driver.find_element(By.CSS_SELECTOR, "p[class='break-words white-space-pre-wrap mb5 t-14 t-black--light t-normal']")
                    about_companies.append(repr(element.text))
            
                    ## number of followers
                    element = driver.find_element(By.CSS_SELECTOR, "div[class='org-top-card-primary-content__info-item org-top-card-primary-content__follower-  count']")
                    nb_followers = "".join(re.findall(r'\d+', element.text))
                    companies_followers_nb.append(nb_followers)
    
                    ## company category
                    element = driver.find_element(By.CSS_SELECTOR, "div[class='org-top-card-primary-content__info-item org-top-card-primary-content__industry']")
                    companies_category.append(repr(element.text))
    
                    ## company location
                    try:
                        element =  driver.find_element(By.CSS_SELECTOR, "div[class='org-top-card-primary-content__info-item org-top-card-primary-   content__headquarter']")
                        companies_location.append(repr(element.text))
                    except:
                        companies_location.append('')
                    #print('location '+str(repr(element.text)))
                    #print(companies_location)
                    progress+=1*100/len(companies_name)
                    #print("progress : "+ str(round(progress,2))+ " % \n")
                except:
                    print('Retrying in 5 secondes...')
                    time.sleep(5)
        
            #print(about_companies)
            print(len(about_companies))
            print(len(companies_location))
            print(len(companies_followers_nb))
    
            dataframe = pd.DataFrame({
                'companies'         : companies_name,
                'url'               : companies_url,
                'location'          : companies_location,
                'category'          : companies_category,
                'nb_of_followers'   : companies_followers_nb,
                'about'             : about_companies
            
            })
            dataframe.to_csv(self.output_filename, encoding='utf-8', index=False, sep=';')

