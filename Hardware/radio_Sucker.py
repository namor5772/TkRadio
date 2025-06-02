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

# Get the directory of the current script & then assumed directory for Images
script_dir = os.path.dirname(os.path.abspath(__file__))
script_dir = script_dir.replace("\\","/")
print(f"This script path is: {script_dir}")

# Create the full filepath to the station websites text file
filename = 'auStationWebsites.csv'
filepath = os.path.join(script_dir, filename)
print(f'The file {filepath} stores a list of station websites')


# Open and setup FireFox browser
firefox_options = Options()
# below is the headless width and height, if not headless +15 & 8 respectively
firefox_options.add_argument("--width=1280")
firefox_options.add_argument("--height=917")
#firefox_options.add_argument("-headless")  # Ensure this argument is correct
browser = webdriver.Firefox(options=firefox_options)

# 'cleans' browser between opening station websites
refresh_http = "http://www.ri.com.au" # use my basic "empty" website

total_anchor_tags = 0
for i in range (1,16+1):
    time.sleep(3)
    browser.get(refresh_http)
    time.sleep(3)
    #sCore = "https://www.fmradiofree.com/?page="
    sCore = "https://www.radio-australia.org/?page="
    sPath = sCore+str(i)
    browser.get(sPath)
    time.sleep(5)

    wait = WebDriverWait(browser, 10)
    div_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "content-column")))
    #print(div_element.text)

    # Find all <a> tags within that div
    anchor_tags = div_element.find_elements(By.TAG_NAME, "a")
    num_anchor_tags = len(anchor_tags)

    # Open or create a CSV file to append the results
    with open(filepath, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        for j, anchor in enumerate(anchor_tags):
            if j >= 60:
                j -= 1  
                break 
            # Use anchor.text if you're interested in the visible text
            anchor_text = anchor.text  
            # Use get_attribute('href') if you want the URL
            anchor_href = anchor.get_attribute('href')
            writer.writerow(["au "+anchor_text, anchor_href])  # Write to CSV file
            print(f"Link text: {anchor_text}, URL: {anchor_href}")

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

