import subprocess
import inspect
import tkinter as tk

import time
import urllib.request
import requests
import os
import csv
import re

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

#sCore = "https://www.fmradiofree.com/?page=" # USD
#sCore = "https://www.radio-australia.org/?page=" # AUSTRALIA"
#sCore = "https://www.radio-polska.pl/?page=" # POLAND

# Get the directory of the current script & then assumed directory for Images
script_dir = os.path.dirname(os.path.abspath(__file__))
script_dir = script_dir.replace("\\","/")
print(f"This script path is: {script_dir}")

# Open and setup FireFox browser
firefox_options = Options()
# below is the headless width and height, if not headless +15 & 8 respectively
firefox_options.add_argument("--width=1280")
firefox_options.add_argument("--height=917")
#firefox_options.add_argument("-headless")  # Ensure this argument is correct
browser = webdriver.Firefox(options=firefox_options)

# 'cleans' browser between opening station websites
refresh_http = "http://www.ri.com.au" # use my basic "empty" website


# ***** VARIABLES NEEDED TO CUSTOMIZE THE SCRAPER *******
sCore = "https://www.radio-polska.pl/?page=" # POLAND
nPages = 12 # number of pages to scrape
# Create the full filepath to the station websites text file
filename = 'plStationWebsites.csv' # filename of the station list csv file
aCountry = "pl" # country code for the station list
# *******************************************************


# Create the full filepath to the station websites text file
filepath = os.path.join(script_dir, filename)
print(f'The csv file {filepath} stores a list of station websites')
total_anchor_tags = 0

# Open or create a CSV file to append the scraped radio station results
with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
    for i in range (1,nPages+1):
        time.sleep(3)
        browser.get(refresh_http)
        time.sleep(3)
        sPath = sCore+str(i)
        browser.get(sPath)
        time.sleep(5)

        wait = WebDriverWait(browser, 10)
        div_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "content-column")))
        #print(div_element.text)

        # Find all <a> tags within that div
        anchor_tags = div_element.find_elements(By.TAG_NAME, "a")
        num_anchor_tags = len(anchor_tags)

        writer = csv.writer(csvfile)
        for j, anchor in enumerate(anchor_tags):
            if j >= 60:
                j -= 1  
                break 
            anchor_text = anchor.text  
            anchor_href = anchor.get_attribute('href')

            stationName = aCountry+" "+anchor_text
            stationName = stationName.replace("/", "v")
            stationName = stationName.replace(",", "")
            stationLogo = stationName.replace(" ", "_")
            stationFunctionStr = "Commercial2"
            nNum = 0
            sPath = anchor_href
            sClass = ""
            nType = 0
   
            stationRow = [stationName, stationLogo, stationFunctionStr, nNum, sPath, sClass, nType]
            writer.writerow(stationRow)
              # Write to CSV file
            print(f"{stationRow}")

        total_anchor_tags = total_anchor_tags + j+1
        print(f"{j+1} links from page {sPath} have been written to {filepath}")
print(f"**** A total of {total_anchor_tags} links have been written to {filepath}")

print("Press Ctrl+C to stop.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Closing the app...")
    browser.quit() # close the WebDriver

# 2D array of preset radio stations, in long name and index (to aStation[]) format.
# this is the default, but is actually copied from file at statup and saved to file on exit!
aStation = []
for row in aStationCSV:
    stationName = row[0]
    stationName = stationName.replace("/", "v")
    stationName = stationName.replace(",", "")
    stationLogo = stationName.replace(" ", "_")
    nNum = 0
    sPath = row[1]
    sClass = ""
    nType = 0
    station = [stationName, stationLogo, Commercial2, nNum, sPath, sClass, nType]
    aStation.append(station)
for row in aStation:
    print(row)
