'''
This script scrapes radio station websites from a list of countries and saves the results to a CSV file.
The directory for all related files is: script_dir = os.path.dirname(os.path.abspath(__file__))

The "input" is a CSV file allcountries_filepath (ALLCountries.csv) with the fields
base URL for the station list], [CountryCode], [CountryName], [NumberOfPages]
eg a sample file looks like this:
    https://www.radioarabic.org,ab,Arabic,31
    https://www.radios-argentinas.org,ar,argentina,29
    https://www.radio-osterreich.at,at,österreich,6
    https://www.radio-australia.org,au,australia,16
    https://www.radio-belgie.be,be,belgie,13
    https://www.onlineradio-bg.com,bg,bulgaria,3
    https://www.radios-bolivia.com,bo,bolivia,6
This is generated from the AllRadio.xlsx file (Sheet1, column Z)
script_dir = os.path.dirname(os.path.abspath(__file__))

The "output" is a CSV file allstations_filepath (ALL_StationWebsites.csv) with the fields
[StationName], [StationLogo], [StationFunctionStr], [nNum], [sPath2], [sClass], [nType]
on 19/6/2025 genetared a file of 79336 radio stations all for the Commercial2 format
did this in two passes due to a crash of the browser. The number of radio stations in the file varies slightly on a daily basis
(plus or minus about 10?) as the aggregator adds or deletes entries.    
a sample looks like this:
    tw A-Line Radio 聯播網,tw_A-Line_Radio_聯播網,Commercial2,0,https://www.radiotaiwan.tw/a-line-radio,taiwan,0
    tw Kpop Girl Group Radio,tw_Kpop_Girl_Group_Radio,Commercial2,0,https://www.radiotaiwan.tw/kpop-girl-group-radio,taiwan,0
    tw Bao Dao Radio 主人電台 FM96.9,tw_Bao_Dao_Radio_主人電台_FM96-9,Commercial2,0,https://www.radiotaiwan.tw/bao-dao-radio-zhu-ren-dian-tai-fm969,taiwan,0
    ua Хіт FM (Hit FM),ua_Хіт_FM_(Hit_FM),Commercial2,0,https://www.radio-ua.com/khit-fm-hit-fm,ukraine,0
    ua Хіт FM (Hit FM) - Top,ua_Хіт_FM_(Hit_FM)_-_Top,Commercial2,0,https://www.radio-ua.com/khit-fm-hit-fm-top,ukraine,0
    ua Наше Радио (Nashe Radio) 107.9,ua_Наше_Радио_(Nashe_Radio)_107-9,Commercial2,0,https://www.radio-ua.com/nashe-radio-nashe-radio-1079,ukraine,0
'''

import subprocess
import inspect
import tkinter as tk

import time
import urllib.request
import requests
import os
import csv
import re
import sys

from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Get the directory of the current script & then assumed directory for Images
script_dir = os.path.dirname(os.path.abspath(__file__))
script_dir = script_dir.replace("\\","/")
print(f"This script path is: {script_dir}")

# Open and setup FireFox browser
firefox_options = Options()
# below is the headless width and height, if not headless +15 & 8 respectively
firefox_options.add_argument("--width=1280")
firefox_options.add_argument("--height=917")
firefox_options.add_argument("-headless")  # Ensure this argument is correct
browser = webdriver.Firefox(options=firefox_options)

# 'cleans' browser between opening station websites
refresh_http = "http://www.ri.com.au" # use my basic "empty" website

# Create the full filepath to the countries websites csv file
allcountries_filename = 'ALLCountries.csv' # filename of the countries list csv file
allcountries_filepath = os.path.join(script_dir, allcountries_filename)
print(f'The csv file {allcountries_filepath} stores a list of station websites')

# load the countries list file into the 2D aCountries[] array
aCountries = []
with open(allcountries_filepath, mode="r", newline="", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        aCountries.append(row)
for row in aCountries:
    print(row)

# Create the full filepath to csv file that will store all the radio station websites
allstations_filename = 'ALL_StationWebsites.csv'
allstations_filepath = os.path.join(script_dir, allstations_filename)
print()
print(f'The csv file {allstations_filepath} stores a list of station websites')
total_anchor_tags = 0

# Open or create a CSV file to append the scraped radio station results
with open(allstations_filepath, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)

    for row in aCountries:
            
        sCore = row[0] + "/?page=" # base URL for the station list
        aCountry = row[1] # country code for the station list
        sCountry = row[2] # country name for the station list
        nPages = int(row[3]) # number of pages for the station list
        continueFlag = True
        textFlag = ""
#        iPage = 1

        for i in range (1,nPages+1):
            time.sleep(2)
            browser.get(refresh_http)
            time.sleep(2)
            sPath = sCore+str(i) # construct the URL for the current page
            browser.get(sPath) # open the URL in the browser
            time.sleep(3)

            # Wait for the page to load and find the div with class "content-column"
            wait = WebDriverWait(browser, 10)
            div_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "content-column")))

            # Find all <a> tags within that div
            anchor_tags = div_element.find_elements(By.TAG_NAME, "a")
            num_anchor_tags = len(anchor_tags)

            # extracting information for up to 60 stations from the openend web page
            # There might be more but the extra ones (if any) are part of a list of interesting links 
            for j, anchor in enumerate(anchor_tags):
                if j >= 60:
                    j -= 1  
                    break 
                anchor_text = anchor.text  
                anchor_href = anchor.get_attribute('href')
                stationName = aCountry+" "+anchor_text
                stationLogo = stationName.translate(str.maketrans({char: "-" for char in "\\/,."}))
                stationLogo = stationLogo.replace(" ", "_")
                stationFunctionStr = "Commercial2"
                nNum = 0
                sPath2 = anchor_href
                sClass = sCountry
                nType = 0

                # append the station information to the file    
                stationRow = [stationName, stationLogo, stationFunctionStr, nNum, sPath2, sClass, nType]
                writer.writerow(stationRow)
                #print(f"{stationRow}")

            total_anchor_tags = total_anchor_tags + j+1
            print(f"page: {i}, {j+1} links from page {sPath} have been written to {allstations_filepath}")
        print(f"**** A total of {total_anchor_tags} links have been written to {allstations_filepath}")


print("Press Ctrl+C to stop.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Closing the app...")
    browser.quit() # close the WebDriver
