import subprocess
import inspect
import tkinter as tk
import time
import urllib.request
import requests
import os
import csv

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


# START #######################################################
# SETUP VARIOUS GLOBAL VARIABLES AND THE FIREFOX BROWSER OBJECT 

# Get the directory of the current script & then assumed directory for Images
script_dir = os.path.dirname(os.path.abspath(__file__))
script_dir = script_dir.replace("\\","/")
pathImages = script_dir + "/Images"
print(f"The Images path is: {pathImages}")

# Create the full filepath to the saved radio station file
filename = 'savedRadioStation.txt'
filepath = os.path.join(script_dir, filename)
print(f'The file {filepath} stores the last streamed station before shutdown.')

# Create the full filepath to the saved playlist file
filename2 = 'playlist.txt'
filepath2 = os.path.join(script_dir, filename2)
print(f'The file {filepath2} stores the playlist before shutdown.')

# Open and setup FireFox browser
firefox_options = Options()
# below is the headless width and height, if not headless +15 & 8 respectively
firefox_options.add_argument("--width=1280")
firefox_options.add_argument("--height=917")
firefox_options.add_argument("-headless")  # Ensure this argument is correct
browser = webdriver.Firefox(options=firefox_options)

# 'cleans' browser between opening station websites
#refresh_http = "http://www.ri.com.au" # use my basic "empty" website
refresh_http = "https://www.blank.org/" # use a basic "empty" website
browser.get(refresh_http)

# global graphis position variables
Ydown = 63
Ygap = 10;  Ygap2 = 110+Ydown; Ygap3 = 110+Ydown
Xgap = 560-70; Xgap2 = 560-70; Xgap3 = 560-70
Xprog = 300

# global variables for combobox selection indexes & button related
numButtons = 18
sizeButton = 62
combobox_index = -1
buttonIndex = -1
addFlag = False
iconSize = 160
eventFlag = True # if on_select & on_select2 are called from event
stopFlag = False
selected_value = "INITIAL"
selected_value_last = "INITIAL"
selected_index = -1
startTime = time.time()
endTime = 0.0
refreshTime = 10.0 # in seconds for program info
stationShort = ""
station = ""
needSleep = 5 # can be less on faster machines
pressButton = True # flag for how stream is started

def SomeFunction():
    # This function is just a placeholder to demonstrate the use of the eventFlag variable
    # It can be replaced with any other function as needed
    pass    

StationName = ""
StationLogo = ""
StationFunction = SomeFunction
nNum = 0
sPath = ""
sClass = ""
nType = 0



# new browser tab related variables
img_url_g = ""
oh = 0
nh = 0
tabNum = 0

# END #########################################################
# SETUP VARIOUS GLOBAL VARIABLES AND THE FIREFOX BROWSER OBJECT 


# Define a custom event class
class CustomEvent:
    def __init__(self, event_type, widget, data=None):
        self.type = event_type
        self.widget = widget
        self.data = data


# START ##################################################
# DEFINE VARIOUS CORE FUNCTIONS THAT STREAM RADIO STATIONS
#
# There are 8 of them: Radio1 ... Radio7 & Commercial1. They are needed because the 
# websites used to stream individual radio stations can differ in their layout, but many are
# similar so can use the same code. Radio1...Radio7 are for the ABC stations, while Commercial1
# is for the commercial stations.

def Radio1(br,nNum,sPath,sClass,nType):
    if eventFlag:
        # use inspect to get the name of the calling function
        # this is used to generate the station name and logo
        logo = StationLogo + ".png"
        print(logo)
        print("--")

        # go to the station website
        br.get(refresh_http)
        time.sleep(1)
        br.get(sPath)
        time.sleep(needSleep)

    # always runs
    be = br.find_element(By.TAG_NAME, 'body')
    time.sleep(1)

    if eventFlag:
        # This where the streaming of the radio station is accomplished
        buttonStream = be.find_element(By.XPATH,'/html/body/div[1]/div/div/div/main/div[1]/div/div/div[1]/div/div[2]/div[12]/div[4]/div/div[1]')
        buttonStream.click()
        time.sleep(1)

        # get station logo
        image_path3 = pathImages
        image_path3 = image_path3 + "/" + logo
        image = Image.open(image_path3)
        scaled_image = image.resize((iconSize, iconSize))  # Adjust the size as needed

        # saving button icon if adding station to playlist 
        global addFlag
        if addFlag:
            buttonImagePath = pathImages + "/button" + str(buttonIndex) + ".png"
            scaled_image.save(buttonImagePath)
            addFlag = False
            print(f"saving button icon {buttonImagePath}")

        # Display the station logo as given in the scaled_image
        photo = ImageTk.PhotoImage(scaled_image)
        label.config(image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection

    # get program image
    try:
        img2_element = be.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/img')
        img2_url = img2_element.get_attribute("src")
        image2_path = pathImages + "/presenter.jpg"
        urllib.request.urlretrieve(img2_url, image2_path)
    except NoSuchElementException:
        print("Image element not found on the webpage.")            
        # Display a blank image
        image2_path = pathImages + "/Blank.png"

    # Display the program image as given in the scaled_image2
    image2 = Image.open(image2_path)
    width2, height2 = image2.size;
    print(f"width: {width2}, height: {height2}")
    crop_box2 = (width2-height2,0,width2,height2)
    cropped_image2 = image2.crop(crop_box2)
    scaled_image2 = cropped_image2.resize((Xprog, Xprog))  # Adjust the size as needed
    photo2 = ImageTk.PhotoImage(scaled_image2)
    label2.config(image=photo2)
    label2.image = photo2  # Keep a reference to avoid garbage collection
    if station == "ABC_Classic2":
        label2.place(x=Xgap, y=Ygap3)  # Adjust the position
    else:
        label2.place(x=Xgap, y=Ygap2)  # Adjust the position
    
    # get station details
    ht = be.get_attribute('innerHTML')
    soup = BeautifulSoup(ht, 'lxml')
    fe = soup.find(attrs={"class": "view-live-now popup"})
    if fe is not None:
        fe1 = fe.get_text(separator="*", strip=True)
    else:
        fe1 = "None"

    # Remove irrelevant info, starting with [*More]
    sub = "*More"
    pos = fe1.find(sub)
    if pos != -1:
        fe1 = fe1[:pos]
    sub = "More from*"
    fe1 = fe1.replace(sub,"")
    sub = "*."
    fe1 = fe1.replace(sub,"")
        
    # append program details to station details    
    fe = soup.find(attrs={"class": "playingNow"})
    if fe is not None:
        fe2 = fe.get_text(separator="*", strip=True)
    else:
        fe2 = "No specific item playing"
    fe3 = fe1+"*"+fe2
    return fe3


def Radio2(br,nNum,sPath,sClass,nType):
    if eventFlag:
        # go to the station website
        br.get(refresh_http)
        time.sleep(1)
        br.get(sPath)
        time.sleep(needSleep)

    # always runs
    be = br.find_element(By.TAG_NAME, 'body')
    time.sleep(1)

    if eventFlag:
        # Select timezone for stream (specific to this actual ABC radio website)
        for _ in range(3):
            be.send_keys(Keys.TAB)
        be.send_keys(Keys.ENTER)
        for _ in range(4):
            be.send_keys(Keys.UP)
        for _ in range(nNum):
            be.send_keys(Keys.DOWN)
        be.send_keys(Keys.ENTER)

        # This where the streaming of the radio station is accomplished
        buttonStream = be.find_element(By.XPATH,'/html/body/div[1]/div/div/div/main/div[1]/div/div/div[2]/div/div[2]/div[12]/div[4]/div/div[1]')
        buttonStream.click()
        time.sleep(1)

        # get station logo
        image_path2 = pathImages + "/ABC_Radio_National.png"
        image = Image.open(image_path2)
        scaled_image = image.resize((iconSize, iconSize))  # Adjust the size as needed

        # saving button icon if adding station to playlist 
        global addFlag
        if addFlag:
            buttonImagePath = pathImages + "/button" + str(buttonIndex) + ".png"
            scaled_image.save(buttonImagePath)
            addFlag = False
            print(f"saving button icon {buttonImagePath}")

        # Display the station logo as given in the scaled_image
        photo = ImageTk.PhotoImage(scaled_image)
        label.config(image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection

    # get program image
    img2_element = be.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div[1]/div/div/header/div/div/img')
    img2_url = img2_element.get_attribute("src")
    image2_path = pathImages + "/presenter.jpg"
    urllib.request.urlretrieve(img2_url, image2_path)

    # Display the program image as given in the scaled_image2
    image2 = Image.open(image2_path)
    width2, height2 = image2.size;
    print(f"width: {width2}, height: {height2}")
    width = int(Xprog*width2/height2)
    scaled_image2 = image2.resize((width, Xprog))  # Adjust the size as needed
    photo2 = ImageTk.PhotoImage(scaled_image2)
    label2.config(image=photo2)
    label2.image = photo2  # Keep a reference to avoid garbage collection
    label2.place(x=Xgap3-(width-Xprog), y=Ygap2)  # Adjust the position
    
    # get station and program details
    ht = be.get_attribute('innerHTML')
    soup = BeautifulSoup(ht, 'lxml')
    fe = soup.find(attrs={"class": "view-live-now popup"})
    if fe is not None:
        fe2 = fe.get_text(separator="*", strip=True)
    else:
        fe2 = "No specific item playing"

    # Remove irrelevant info, starting with [*.*More]
    sub = "*.*More"
    pos = fe2.find(sub)
    if pos != -1:
        fe2 = fe2[:pos]
    return fe2


def Radio3(br,nNum,sPath,sClass,nType):
    if eventFlag:
        # use inspect to get the name of the calling function
        # this is used to generate the station name and logo
        station = StationLogo
        first_occurrence = station.find("_")
        second_occurrence = station.find("_", first_occurrence+1)
        global station_short
        station_short = station[:second_occurrence]
        logo = station_short + ".png"
        print(logo)
        print("--")

        # go to the station website
        br.get(refresh_http)
        time.sleep(1)
        br.get(sPath)
        time.sleep(needSleep)

    # always runs
    be = br.find_element(By.TAG_NAME, 'body')
    time.sleep(1)

    if eventFlag:
        # Select timezone for stream (specific to this actual ABC radio website)
        for _ in range(5):
            be.send_keys(Keys.TAB)
        be.send_keys(Keys.ENTER)
        for _ in range(4):
            be.send_keys(Keys.UP)
        for _ in range(nNum):
            be.send_keys(Keys.DOWN)
        be.send_keys(Keys.ENTER)

        # This where the streaming of the radio station is accomplished
        buttonStream = be.find_element(By.XPATH,'/html/body/div[1]/div/div/div/main/div[1]/div/div/div[2]/div/div[2]/div[12]/div[4]/div/div[1]')
        buttonStream.click()
        time.sleep(1)

        # get station logo
        image_path3 = pathImages + "/" + logo
        image = Image.open(image_path3)
        scaled_image = image.resize((iconSize, iconSize))  # Adjust the size as needed

        # saving button icon if adding station to playlist 
        global addFlag
        if addFlag:
            buttonImagePath = pathImages + "/button" + str(buttonIndex) + ".png"
            scaled_image.save(buttonImagePath)
            addFlag = False
            print(f"saving button icon {buttonImagePath}")

        # Display the station logo as given in the scaled_image
        photo = ImageTk.PhotoImage(scaled_image)
        label.config(image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection

    # get program image
    try:      
        img2_element = be.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div[1]/div/div/div[3]/div[1]/div/div[2]/div[2]/img')
        img2_url = img2_element.get_attribute("src")
        image2_path = pathImages + "/presenter.jpg"
        urllib.request.urlretrieve(img2_url, image2_path)
    except NoSuchElementException:
        print("Image element not found on the webpage.")            
        # Display a blank image
        image2_path = pathImages + "/Blank.png"

    # Display the program image as given in the scaled_image2
    image2 = Image.open(image2_path)
    width2, height2 = image2.size;
    print(f"width: {width2}, height: {height2}")
    crop_box2 = (width2-height2,0,width2,height2)
    cropped_image2 = image2.crop(crop_box2)
    scaled_image2 = cropped_image2.resize((Xprog, Xprog))  # Adjust the size as needed
    photo2 = ImageTk.PhotoImage(scaled_image2)
    label2.config(image=photo2)
    label2.image = photo2  # Keep a reference to avoid garbage collection
    if station_short == "ABC_Classic":
        label2.place(x=Xgap, y=Ygap3)  # Adjust the position
    else:
        label2.place(x=Xgap, y=Ygap2)  # Adjust the position

    # get station details
    ht = be.get_attribute('innerHTML')
    soup = BeautifulSoup(ht, 'lxml')
    fe = soup.find(attrs={"class": "view-live-now popup"})
    if fe is not None:
        fe1 = fe.get_text(separator="*", strip=True)
    else:
        fe1 = "None"

    # Remove irrelevant info, starting with [*More]
    sub = "*More"
    pos = fe1.find(sub)
    if pos != -1:
        fe1 = fe1[:pos]

    # append program details to station details    
    fe = soup.find(attrs={"class": "playingNow"})
    if fe is not None:
        fe2 = fe.get_text(separator="*", strip=True)
    else:
        fe2 = "No specific item playing"
    fe3 = fe1+"*"+fe2
    return fe3


def Radio4(br,nNum,sPath,sClass,nType):
    if eventFlag:
        # go to the station website
        br.get(refresh_http)
        time.sleep(1)
        br.get(sPath)
        time.sleep(needSleep)

    # always runs
    be = br.find_element(By.TAG_NAME, 'body')
    time.sleep(1)

    if eventFlag:
        # This where the streaming of the radio station is accomplished
        buttonStream = be.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/div/main/div[1]/div/div/div/div[2]/button')
        buttonStream.click()
        time.sleep(3)
        
        # get station logo
        img_element = be.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/main/div[1]/div/div/div/a/div/img')
        img_url = img_element.get_attribute("src")
        image_path = pathImages + "/logo.png"
        urllib.request.urlretrieve(img_url, image_path)
        image = Image.open(image_path)
        scaled_image = image.resize((iconSize, iconSize))  # Adjust the size as needed

        # saving button icon if adding station to playlist 
        global addFlag
        if addFlag:
            buttonImagePath = pathImages + "/button" + str(buttonIndex) + ".png"
            scaled_image.save(buttonImagePath)
            addFlag = False
            print(f"saving button icon {buttonImagePath}")
        
        # Display the station logo as given in the scaled_image
        photo = ImageTk.PhotoImage(scaled_image)
        label.config(image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection
       
    # get program image
    try:      
        img2_element = be.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/main/div[1]/div/div/div/div[1]/div[1]/div/div/div/img')
        img2_url = img2_element.get_attribute("src")
        image2_path = pathImages + "/presenter.jpg"
        print(image2_path)
        urllib.request.urlretrieve(img2_url, image2_path)
    except NoSuchElementException:
        print("Image element not found on the webpage.")            
        # Display a blank image
        image2_path = pathImages + "/ABC_faint.png"

    # Display the program image as given in the scaled_image2
    image2 = Image.open(image2_path)
    width2, height2 = image2.size;
    print(f"width: {width2}, height: {height2}")
    crop_box2 = (width2-height2,0,width2,height2)
    cropped_image2 = image2.crop(crop_box2)
    scaled_image2 = cropped_image2.resize((Xprog, Xprog))  # Adjust the size as needed
    photo2 = ImageTk.PhotoImage(scaled_image2)
    label2.config(image=photo2)
    label2.image = photo2  # Keep a reference to avoid garbage collection
    label2.place(x=Xgap2, y=Ygap2)  # Adjust the position
    
    # get station details
    ht = be.get_attribute('innerHTML')
    soup = BeautifulSoup(ht, 'lxml')
    fe = soup.find(attrs={"class": "LiveAudioPlayer_body__y6nYe"})
    if fe is not None:
        fe2 = fe.get_text(separator="*", strip=True)
    else:
        fe2 = "No item playing"

    # Remove irrelevant info [*-]
    sub = "*-"
    fe3 = fe2.replace(sub,"")
    
    # append program details to station details    
    fe = soup.find(attrs={"class": "LiveAudioSynopsis_content__DZ6E7"})
    if fe is not None:
        fe2 = fe.get_text(separator="*", strip=True)
    else:
        fe2 = "No Description"
    fe3 = fe3+"* *"+fe2
    return fe3


def Radio5(br,nNum,sPath,sClass,nType):
    if eventFlag:
        # go to the station website
        br.get(refresh_http)
        time.sleep(1)
        browser.get(sPath)
        time.sleep(needSleep)

    # always runs
    be = br.find_element(By.TAG_NAME, 'body')
    time.sleep(1)

    if eventFlag:
        # This where the streaming of the radio station is accomplished
        buttonStream = be.find_element(By.XPATH,'/html/body/div[1]/div/div/div[1]/div/main/div[1]/div/div/div/div[2]/button')
        buttonStream.click()
        time.sleep(1)

        # get station logo
        img_element = be.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/main/div[1]/div/div/div/a/div/img')
        img_url = img_element.get_attribute("src")
        image_path = pathImages + "/logo.png"
        urllib.request.urlretrieve(img_url, image_path)
        image = Image.open(image_path)
        scaled_image = image.resize((iconSize, iconSize))  # Adjust the size as needed

        # saving button icon if adding station to playlist 
        global addFlag
        if addFlag:
            buttonImagePath = pathImages + "/button" + str(buttonIndex) + ".png"
            scaled_image.save(buttonImagePath)
            addFlag = False
            print(f"saving button icon {buttonImagePath}")
        
        # Display the station logo as given in the scaled_image
        photo = ImageTk.PhotoImage(scaled_image)
        label.config(image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection

    # get program image
    try:      
        img2_element = be.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/main/div[1]/div/div/div/div[1]/div[1]/div/div/div/img')
        img2_url = img2_element.get_attribute("src")
        image2_path = pathImages + "/presenter.jpg"
        urllib.request.urlretrieve(img2_url, image2_path)
    except NoSuchElementException:
        print("Image element not found on the webpage.")            
        # Display a blank image
        image2_path = pathImages + "/ABC_faint.png"

    # Display the program image as given in the scaled_image2
    image2 = Image.open(image2_path)
    width2, height2 = image2.size;
    print(f"width: {width2}, height: {height2}")
    crop_box2 = (width2-height2,0,width2,height2)
    cropped_image2 = image2.crop(crop_box2)
    scaled_image2 = cropped_image2.resize((Xprog, Xprog))  # Adjust the size as needed
    photo2 = ImageTk.PhotoImage(scaled_image2)
    label2.config(image=photo2)
    label2.image = photo2  # Keep a reference to avoid garbage collection
    label2.place(x=Xgap, y=Ygap2)  # Adjust the position

    # get station details
    ht = be.get_attribute('innerHTML')
    soup = BeautifulSoup(ht, 'lxml')
    fe = soup.find(attrs={"class": "LiveAudioPlayer_body__y6nYe"})
    if fe is not None:
        fe2 = fe.get_text(separator="*", strip=True)
    else:
        fe2 = "No item playing"

    # Remove irrelevant info [*-]
    sub = "*-"
    fe3 = fe2.replace(sub,"")
    
    # append program details to station details    
    fe = soup.find(attrs={"class": "LiveAudioSynopsis_content__DZ6E7"})
    if fe is not None:
        fe2 = fe.get_text(separator="*", strip=True)
    else:
        fe2 = "No Description"
    fe3 = fe3+"* *"+fe2
    return fe3


def Radio6(br,nNum,sPath,sClass,nType):
    if eventFlag:
        # go to the station website
        br.get(refresh_http)
        time.sleep(2)
        br.get(sPath)
        time.sleep(needSleep)

    # always runs
    be = br.find_element(By.TAG_NAME, 'body')
    time.sleep(1)

    if eventFlag:
        # This is where the streaming of the radio station is accomplished
        buttonStream = be.find_element(By.XPATH,'/html/body/div[1]/div/div/div/main/div[1]/div/div/div[1]/div/div[2]/div[12]/div[4]/div/div[1]')
        buttonStream.click()
        time.sleep(1)

        # get station logo
        image_path3 = pathImages + "/ABC_Kids_listen.png"
        image = Image.open(image_path3)
        scaled_image = image.resize((iconSize, iconSize))  # Adjust the size as needed

        # saving button icon if adding station to playlist 
        global addFlag
        if addFlag:
            buttonImagePath = pathImages + "/button" + str(buttonIndex) + ".png"
            scaled_image.save(buttonImagePath)
            addFlag = False
            print(f"saving button icon {buttonImagePath}")
        
        # Display the station logo as given in the scaled_image
        photo = ImageTk.PhotoImage(scaled_image)
        label.config(image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection

    # get program image
    try:      
        img2_element = be.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/img')
        img2_url = img2_element.get_attribute("src")
        image2_path = pathImages + "/presenter.jpg"
        urllib.request.urlretrieve(img2_url, image2_path)
    except NoSuchElementException:
        print("Image element not found on the webpage.")            
        # Display a blank image
        image2_path = pathImages + "/Blank.png"

    # Display the program image as given in the scaled_image2
    image2 = Image.open(image2_path)
    width2, height2 = image2.size;
    print(f"width: {width2}, height: {height2}")
    crop_box2 = (width2-height2,0,width2,height2)
    cropped_image2 = image2.crop(crop_box2)
    scaled_image2 = cropped_image2.resize((Xprog, Xprog))  # Adjust the size as needed
    photo2 = ImageTk.PhotoImage(scaled_image2)
    label2.config(image=photo2)
    label2.image = photo2  # Keep a reference to avoid garbage collection
    label2.place(x=Xgap, y=Ygap3)  # Adjust the position
    
    # get station details
    ht = be.get_attribute('innerHTML')
    soup = BeautifulSoup(ht, 'lxml')
    fe = soup.find(attrs={"class": "view-live-now popup"})
    if fe is not None:
        fe1 = fe.get_text(separator="*", strip=True)
    else:
        fe1 = "None"

    # Remove irrelevant info, starting with [*More]
    sub = "*More"
    pos = fe1.find(sub)
    if pos != -1:
        fe1 = fe1[:pos]

    # append program details to station details    
    fe = soup.find(attrs={"class": "playingNow"})
    if fe is not None:
        fe2 = fe.get_text(separator="*", strip=True)
    else:
        fe2 = "No specific item playing"
    fe3 = fe1+"*"+fe2
    return fe3


# *************************** FIX FIX FIX ****************************************
def Radio7(br,nNum,sPath,sClass,nType):
    if eventFlag:
        print("----------")
        logo = StationLogo + ".png"
        print(logo)
        print("----------")
        br.get(refresh_http)
        time.sleep(1)
        br.get(sPath)
        time.sleep(needSleep)

    # always runs
    be = br.find_element(By.TAG_NAME, 'body')
    time.sleep(1)

    if eventFlag:
        # This where the streaming of the radio station is accomplished
        buttonStream = be.find_element(By.XPATH,'/html/body/div[1]/div/div/div/div/div/main/section[2]/div/section/div/section/section/div[2]/div/div[1]/div/div[2]/button')
        buttonStream.click()
        time.sleep(1)

        # get station logo
        image_path3 = pathImages + "/" + logo
        image = Image.open(image_path3)
        scaled_image = image.resize((iconSize, iconSize))  # Adjust the size as needed

        # saving button icon
        global addFlag
        if addFlag:
            buttonImagePath = pathImages + "/button" + str(buttonIndex) + ".png"
            scaled_image.save(buttonImagePath)
            addFlag = False
            print(f"saving button icon {buttonImagePath}")
        
        photo = ImageTk.PhotoImage(scaled_image)
        label.config(image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection

    # Display a blank program image
    image2_path = pathImages + "/Blank.png"
    image2 = Image.open(image2_path)
    width2, height2 = image2.size;
    print(f"width: {width2}, height: {height2}")
    crop_box2 = (width2-height2,0,width2,height2)
    cropped_image2 = image2.crop(crop_box2)
    scaled_image2 = cropped_image2.resize((Xprog, Xprog))  # Adjust the size as needed
    photo2 = ImageTk.PhotoImage(scaled_image2)
    label2.config(image=photo2)
    label2.image = photo2  # Keep a reference to avoid garbage collection
    label2.place(x=Xgap, y=Ygap3)  # Adjust the position
        
    # Find program details
    ht = be.get_attribute('innerHTML')
    soup = BeautifulSoup(ht, 'lxml')
    if nNum==0:
        xid="abc-:rb:-item-0"
        sName = "ABC SPORT"
    elif nNum==1:
        xid="abc-:rb:-item-1"
        sName = "ABC SPORT EXTRA"
    else: # if nNum==2
        xid="abc-:rb:-item-2"
        sName = "ABC CRICKET"
    fe = soup.find(attrs={"id": xid})
    if fe is not None:
        feX = fe.find(attrs={"class": "AudioPlayerCard_programMeta__3VqUy"})
        if feX is not None:
            fe2 = feX.get_text(separator="*", strip=True)
    else:
        fe2 = sName

    # Remove irrelevant info, starting with [*.*More]
    sub = "*Stop"
    pos = fe2.find(sub)
    if pos != -1:
        fe2 = fe2[:pos]
    else:
        sub = "*Listen"
        pos = fe2.find(sub)
        if pos != -1:
            fe2 = fe2[:pos]
    return fe2


def Commercial1(br,nNum,sPath,sClass,nType):
    if eventFlag:
        # use inspect to get the name of the calling function
        print("----------")
        logo = StationLogo + ".png"
        print(logo)
        print("----------")
        
        # go to the station website
        br.get(refresh_http)
        time.sleep(2)
        br.get(sPath)
        time.sleep(needSleep) # bigger on slow machines

    # always runs
    be = br.find_element(By.TAG_NAME, 'body')
    time.sleep(1)

    if eventFlag:
        # This where the streaming of the radio station is accomplished
        # the position of the "Listen Live" button depends on the nType integer parameter
        match nType:
            case 0:
                # iHeart stations
                buttonStream = be.find_element(By.XPATH,'/html/body/div[1]/div[4]/div[1]/div/div/div[2]/div/div[1]/button')
                buttonStream.click()
                print("Case 0")
            case 1:
                # Smooth &  Nova Stations
                buttonStream = be.find_element(By.XPATH,'//*[@id="listenLive"]')
                buttonStream.click()
                print("Case 1")
            case _:
                print("Out of bounds")            
        time.sleep(3)

        # get station logo
        if nType==0:
            # for iHeart stations
            img_element = be.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[1]/div/div/div[1]/div/div/img')
            img_url = img_element.get_attribute("src")
            image_path = pathImages + "/logo.png"
            urllib.request.urlretrieve(img_url, image_path)
        else:
            # for Smooth & Nova stations
            image_path = pathImages + "/" + logo

        # Display the station logo as given in the scaled_image
        image = Image.open(image_path)
        scaled_image = image.resize((iconSize, iconSize))  # Adjust the size as needed

        # saving button icon if adding station to playlist 
        global addFlag
        if addFlag:
            buttonImagePath = pathImages + "/button" + str(buttonIndex) + ".png"
            scaled_image.save(buttonImagePath)
            addFlag = False
            print(f"saving button icon {buttonImagePath}")

        # Display the station logo as given in the scaled_image
        photo = ImageTk.PhotoImage(scaled_image)
        label.config(image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection

    # Display the program image as given in the scaled_image2
    if nType==0: 
        # iHeart stations
        img2_element = be.find_element(By.XPATH, '/html/body/div[1]/div[5]/div/div[1]/div[1]/div/img')
    else:
        # Smooth & Nova stations
        img2_element = be.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div[1]/div[1]/img')
    img2_url = img2_element.get_attribute("src")
    image2_path = pathImages + "/presenter.jpg"
    urllib.request.urlretrieve(img2_url, image2_path)
    image2 = Image.open(image2_path)
    width2, height2 = image2.size;
    print(f"Pic width: {width2}, Pic height: {height2}")
    width = int(Xprog*width2/height2)
    scaled_image2 = image2.resize((width, Xprog))  # Adjust the size as needed
    photo2 = ImageTk.PhotoImage(scaled_image2)
    label2.config(image=photo2)
    label2.image = photo2  # Keep a reference to avoid garbage collection
    label2.place(x=Xgap3-(width-Xprog), y=Ygap2)  # Adjust the position
 
    # get station and program details
    ht = be.get_attribute('innerHTML')
    soup = BeautifulSoup(ht, 'lxml')
    fe = soup.find(attrs={"class": sClass})
    if fe is not None:
        fe1 = fe.get_text(separator="*", strip=True)
    else:
        fe1 = "None"
    return fe1


# format used by the radio-australia.org and related stations format
def Commercial2(br,nNum,sPath,sClass,nType):
    global img_url_g, oh, nh, tabNum

    if eventFlag:
        # go to the station website
        br.get(refresh_http)
        time.sleep(2)
        br.get(sPath)
        time.sleep(needSleep) # bigger on slow machines

    # always runs
    print("--------------------------------------")
    image_path_logo = pathImages + "/" + StationLogo + ".png"
    be = br.find_element(By.TAG_NAME, 'body')
    time.sleep(1)

    if eventFlag:
        # press button with virtual mouse to play stream
        window_size = br.get_window_size()
  #      width = window_size['width']
  #      height = window_size['height']         
        print(f"Window size: width = {window_size['width']}, height = {window_size['height']}")
        widthPx =110
        heightPx = 330#390
        print(f"Move size: width = {widthPx}, height = {heightPx}")
        actions = ActionChains(br)
        actions.move_by_offset(widthPx, heightPx).click().perform()
        time.sleep(3)

        # get station logo
        try:
            # logo is *.png file with station function name
            image = Image.open(image_path_logo)
        except Exception as e:
            # create generic placeholder station logo
            print(f"No station logo file: {e}")
            image_path = pathImages + "/noLogo.png"
            image = Image.open(image_path)
        scaled_image = image.resize((iconSize, iconSize))  # Adjust the size as needed

        # saving button icon if adding station to playlist 
        global addFlag
        if addFlag:
            buttonImagePath = pathImages + "/button" + str(buttonIndex) + ".png"
            scaled_image.save(buttonImagePath)
            addFlag = False
            print(f"saving button icon {buttonImagePath}")
        
        # Display the station logo as given in the scaled_image
        photo = ImageTk.PhotoImage(scaled_image)
        label.config(image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection

    # always runs, get and then display station logo if one does not yet exist
    logoFlag = os.path.exists(image_path_logo)
    if logoFlag and (tabNum == 1):
        print(f"Display just created station logo file: {image_path_logo}")
        image = Image.open(image_path_logo)
        scaled_image = image.resize((iconSize, iconSize))  # Adjust the size as needed
        # Display the station logo as given in the scaled_image
        photo = ImageTk.PhotoImage(scaled_image)
        label.config(image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection
        tabNum = 0
    elif logoFlag:
        print(f"Logo file exists: {image_path_logo}")
    else:
        print("Logo file does not exist, so creating one")
        if eventFlag:
            tabNum = 0

            # try to find a particular image element by path
            xpath = '//*[@id="player_image"]'
            img_element = WebDriverWait(be, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            img_url_g = img_element.get_attribute("src")
            print("Found image URL:", img_url_g)
            oh = br.current_window_handle
            print("Current window handle:", oh)
            br.switch_to.new_window('tab')
            nh = br.current_window_handle
            print("New window handle:", nh)
            br.switch_to.window(oh)
        else:
            if tabNum == 0:
                br.switch_to.window(nh)
                br.get(img_url_g)
                print("Switching 2")
                print(image_path_logo)

                try:
                    headers = {"User-Agent": "Mozilla/5.0"}
                    response = requests.get(img_url_g, headers=headers, stream=True)
                    print(response.headers["Content-Type"])

                    #response = requests.get(img_url_g, stream=True)
                    with open(image_path_logo, 'wb') as file:
                        for chunk in response.iter_content(chunk_size=8192):
                            file.write(chunk)
                    print("Image downloaded successfully.")
                except Exception as e:
                    print(f"Failed to download the image: {e}")
                print("Switching 3")
                br.close()
                br.switch_to.window(oh)
                tabNum = 1
            else: # tabNum == 1
                print("display downloaded station logo!")
    
    # Stations with program image
    image_path = pathImages + "/presenter.jpg"
    foundImage = True
    try:
        # try to find a particular image element by path
        xpath = '/html/body/div[6]/div[1]/div[3]/div/div[1]/div[1]/div[3]/div/div[1]/div/a/img'
        img_element = be.find_element(By.XPATH, xpath)
        img_url = img_element.get_attribute("src")
        urllib.request.urlretrieve(img_url, image_path)
        print("=====> xpath #1")
    except NoSuchElementException:
        try:
            # if failed above try a slightly different path
            xpath = '/html/body/div[6]/div[1]/div[3]/div/div[1]/div[1]/div[3]/div/div[1]/div/img'
            img_element = be.find_element(By.XPATH, xpath)
            img_url = img_element.get_attribute("src")
            urllib.request.urlretrieve(img_url, image_path)
            print("=====> xpath #2")
        except NoSuchElementException:
            try:
                # if failed above try a slightly different path
                xpath = '/html/body/div[6]/div[1]/div[2]/div/div[1]/div[1]/div[3]/div/div[1]/div/img'
                img_element = be.find_element(By.XPATH, xpath)
                img_url = img_element.get_attribute("src")
                urllib.request.urlretrieve(img_url, image_path)
                print("=====> xpath #3")
            except NoSuchElementException:
                try:
                    # if failed above try a slightly different path
                    xpath = '/html/body/div[6]/div[1]/div[2]/div/div[1]/div[1]/div[3]/div/div[1]/div/a/img'
                    img_element = be.find_element(By.XPATH, xpath)
                    img_url = img_element.get_attribute("src")
                    urllib.request.urlretrieve(img_url, image_path)
                    print("=====> xpath #4")
                except NoSuchElementException:
                    try:
                        # if failed above try a slightly different path
                        xpath = '/html/body/div[6]/div[1]/div[3]/div/div[1]/div[1]/div[3]/div/div[2]/div[1]/a/img'
                        img_element = be.find_element(By.XPATH, xpath)
                        img_url = img_element.get_attribute("src")
                        urllib.request.urlretrieve(img_url, image_path)
                        print("=====> xpath #5")
                    except NoSuchElementException:
                        # failed to find image so display a blank image
                        foundImage = False
                        print("=====> xpath NONE")
        
    if foundImage:
        image = Image.open(image_path)
        width2, height2 = image.size;
        print(f"Pic width: {width2}, Pic height: {height2}")
        width = int(Xprog*width2/height2)
        scaled_image = image.resize((width, Xprog))  # Adjust the size as needed
        photo = ImageTk.PhotoImage(scaled_image)
        label2.config(image=photo)
        label2.image = photo  # Keep a reference to avoid garbage collection
        label2.place(x=Xgap3-(width-Xprog), y=Ygap2)  # Adjust the position
    else:    
        image_path = pathImages + "/Blank.png"
        image = Image.open(image_path)
        scaled_image = image.resize((Xprog, Xprog))  # Adjust the size as needed
        photo = ImageTk.PhotoImage(scaled_image)
        label2.config(image=photo)
        label2.image = photo  # Keep a reference to avoid garbage collection
        label2.place(x=Xgap, y=Ygap3)  # Adjust the position

    # get station and program details (if available)
    ht = be.get_attribute('innerHTML')
    soup = BeautifulSoup(ht, 'lxml')

    # get general station details
    fe = soup.find(attrs={"class": "mdc-typography--display1 primary-span-color"})
    fe1 = ""
    if fe is not None: fe1 = fe.get_text(separator="*", strip=True)+"*"

    fe = soup.find(attrs={"class": "slogan secondary-span-color"})
    if fe is not None: fe1 = fe1+fe.get_text(separator="*", strip=True)+"*"

    fe = soup.find(attrs={"class": "secondary-span-color radio-description"})
    if fe is not None:
        fe1 = fe1+fe.get_text(separator="*", strip=True)+"* *"
    else:
        fe1 = fe1+" *"        

    # get program details
    fe = soup.find(attrs={"class": "history-song"})
    if fe is not None:
        fe1 = "*"+fe1+fe.get_text(separator="*", strip=True)
    else:
        fe1 = "*"+fe1+"No program information"

    return fe1


# END ####################################################
# DEFINE VARIOUS CORE FUNCTIONS THAT STREAM RADIO STATIONS


# COMMON BLOCK START *********************************************

# 2D array of radio station information in [long name, station icon name, nNum, sPath, sClass, nType] format
# where nNum, sPath, sClass & nType are arguments for the Commercial1, Commercial2, Radio1, Radio2, Radio3,
# Radio4, Radio5, Radio6 or Radio7 Station calling functions 
# clearly this can be varied if you wish to listen to different stations
# Currently we Have 83 ABC stations and 186 in total!

aStation = [
    ["ABC Classic2","ABC_Classic2",Radio1,7,"https://www.abc.net.au/listen/live/classic2","",0],
    ["ABC Jazz","ABC_Jazz",Radio1,7,"https://www.abc.net.au/listen/live/jazz","",0],
    ["ABC triple j Hottest","ABC_triple_j_Hottest",Radio1,7,"https://www.abc.net.au/triplej/live/triplejhottest","",0],
    ["ABC triple j Unearthed","ABC_triple_j_Unearthed",Radio1,7,"https://www.abc.net.au/triplej/live/unearthed","",0],

    ["ABC Radio National LIVE","ABC_Radio_National_LIVE",Radio2,0,"https://www.abc.net.au/listen/live/radionational","",0],
    ["ABC Radio National QLD","ABC_Radio_National_QLD",Radio2,1,"https://www.abc.net.au/listen/live/radionational","",0],
    ["ABC Radio National WA","ABC_Radio_National_WA",Radio2,2,"https://www.abc.net.au/listen/live/radionational","",0],
    ["ABC Radio National SA","ABC_Radio_National_SA",Radio2,3,"https://www.abc.net.au/listen/live/radionational","",0],
    ["ABC Radio National NT","ABC_Radio_National_NT",Radio2,4,"https://www.abc.net.au/listen/live/radionational","",0],

    ["ABC triple j LIVE","ABC_triple_j_LIVE",Radio3,0,"https://www.abc.net.au/listen/live/triplej","",0],
    ["ABC triple j QLD","ABC_triple_j_QLD",Radio3,1,"https://www.abc.net.au/listen/live/triplej","",0],
    ["ABC triple j WA","ABC_triple_j_WA",Radio3,2,"https://www.abc.net.au/listen/live/triplej","",0],
    ["ABC triple j SA","ABC_triple_j_SA",Radio3,3,"https://www.abc.net.au/listen/live/triplej","",0],
    ["ABC triple j NT","ABC_triple_j_NT",Radio3,4,"https://www.abc.net.au/listen/live/triplej","",0],
    ["ABC Double j LIVE","ABC_Double_j_LIVE",Radio3,0,"https://www.abc.net.au/listen/live/doublej","",0],
    ["ABC Double j QLD","ABC_Double_j_QLD",Radio3,1,"https://www.abc.net.au/listen/live/doublej","",0],
    ["ABC Double j WA","ABC_Double_j_WA",Radio3,2,"https://www.abc.net.au/listen/live/doublej","",0],
    ["ABC Double j SA","ABC_Double_j_SA",Radio3,3,"https://www.abc.net.au/listen/live/doublej","",0],
    ["ABC Double j NT","ABC_Double_j_NT",Radio3,4,"https://www.abc.net.au/listen/live/doublej","",0],
    ["ABC Classic LIVE","ABC_Classic_LIVE",Radio3,0,"https://www.abc.net.au/listen/live/classic","",0],
    ["ABC Classic QLD","ABC_Classic_QLD",Radio3,1,"https://www.abc.net.au/listen/live/classic","",0],
    ["ABC Classic WA","ABC_Classic_WA",Radio3,2,"https://www.abc.net.au/listen/live/classic","",0],
    ["ABC Classic SA","ABC_Classic_SA",Radio3,3,"https://www.abc.net.au/listen/live/classic","",0],
    ["ABC Classic NT","ABC_Classic_NT",Radio3,4,"https://www.abc.net.au/listen/live/classic","",0],

    ["ABC Radio Sydney NSW","ABC_Radio_Sydney_NSW",Radio4,0,"https://www.abc.net.au/listen/live/sydney","",0],
    ["ABC Broken Hill NSW","ABC_Broken_Hill_NSW",Radio4,0,"https://www.abc.net.au/listen/live/brokenhill","",0],
    ["ABC Central Coast NSW","ABC_Central_Coast_NSW",Radio4,0,"https://www.abc.net.au/listen/live/centralcoast","",0],
    ["ABC Central West NSW","ABC_Central_West_NSW",Radio4,0,"https://www.abc.net.au/listen/live/centralwest","",0],
    ["ABC Coffs Coast NSW","ABC_Coffs_Coast_NSW",Radio4,0,"https://www.abc.net.au/listen/live/coffscoast","",0],
    ["ABC Illawarra NSW","ABC_Illawarra_NSW",Radio4,0,"https://www.abc.net.au/listen/live/illawarra","",0],
    ["ABC Mid North Coast NSW","ABC_Mid_North_Coast_NSW",Radio4,0,"https://www.abc.net.au/listen/live/midnorthcoast","",0],
    ["ABC New England North West NSW","ABC_New_England_North_West_NSW",Radio4,0,"https://www.abc.net.au/listen/live/newengland","",0],
    ["ABC Newcastle NSW","ABC_Newcastle_NSW",Radio4,0,"https://www.abc.net.au/listen/live/newcastle","",0],
    ["ABC North Coast NSW","ABC_North_Coast_NSW",Radio4,0,"https://www.abc.net.au/listen/live/northcoast","",0],
    ["ABC Riverina NSW","ABC_Riverina_NSW",Radio4,0,"https://www.abc.net.au/listen/live/riverina","",0],
    ["ABC South East NSW","ABC_South_East_NSW",Radio4,0,"https://www.abc.net.au/listen/live/southeastnsw","",0],
    ["ABC Upper Hunter NSW","ABC_Upper_Hunter_NSW",Radio4,0,"https://www.abc.net.au/listen/live/upperhunter","",0],
    ["ABC Western Plains NSW","ABC_Western_Plains_NSW",Radio4,0,"https://www.abc.net.au/listen/live/westernplains","",0],
    ["ABC Radio Canberra ACT","ABC_Radio_Canberra_ACT",Radio4,0,"https://www.abc.net.au/listen/live/canberra","",0],
    ["ABC Radio Darwin NT","ABC_Radio_Darwin_NT",Radio4,0,"https://www.abc.net.au/listen/live/darwin","",0],
    ["ABC Alice Springs NT","ABC_Alice_Springs_NT",Radio4,0,"https://www.abc.net.au/listen/live/alicesprings","",0],
    ["ABC Radio Melbourne VIC","ABC_Radio_Melbourne_VIC",Radio4,0,"https://www.abc.net.au/listen/live/melbourne","",0],
    ["ABC Ballarat VIC","ABC_Ballarat_VIC",Radio4,0,"https://www.abc.net.au/listen/live/ballarat","",0],
    ["ABC Central Victoria VIC","ABC_Central_Victoria_VIC",Radio4,0,"https://www.abc.net.au/listen/live/centralvic","",0],
    ["ABC Gippsland VIC","ABC_Gippsland_VIC",Radio4,0,"https://www.abc.net.au/listen/live/gippsland","",0],
    ["ABC Goulburn Murray VIC","ABC_Goulburn_Murray_VIC",Radio4,0,"https://www.abc.net.au/listen/live/goulburnmurray","",0],
    ["ABC Mildura-Swan Hill VIC","ABC_Mildura_Swan_Hill_VIC",Radio4,0,"https://www.abc.net.au/listen/live/milduraswanhill","",0],
    ["ABC Shepparton VIC","ABC_Shepparton_VIC",Radio4,0,"https://www.abc.net.au/listen/live/shepparton","",0],
    ["ABC South West Victoria VIC","ABC_South_West_Victoria_VIC",Radio4,0,"https://www.abc.net.au/listen/live/southwestvic","",0],
    ["ABC Wimmera VIC","ABC_Wimmera_VIC",Radio4,0,"https://www.abc.net.au/listen/live/wimmera","",0],
    ["ABC Radio Adelaide SA","ABC_Radio_Adelaide_SA",Radio4,0,"https://www.abc.net.au/listen/live/adelaide","",0],
    ["ABC Eyre Peninsula SA","ABC_Eyre_Peninsula_SA",Radio4,0,"https://www.abc.net.au/listen/live/eyre","",0],
    ["ABC North and West SA","ABC_North_and_West_SA",Radio4,0,"https://www.abc.net.au/listen/live/northandwest","",0],
    ["ABC Riverland SA","ABC_Riverland_SA",Radio4,0,"https://www.abc.net.au/listen/live/riverland","",0],
    ["ABC South East SA","ABC_South_East_SA",Radio4,0,"https://www.abc.net.au/listen/live/southeastsa","",0],
    ["ABC Radio Hobart TAS","ABC_Radio_Hobart_TAS",Radio4,0,"https://www.abc.net.au/listen/live/hobart","",0],
    ["ABC Northern Tasmania TAS","ABC_Northern_Tasmania_TAS",Radio4,0,"https://www.abc.net.au/listen/live/northtas","",0],
    ["ABC Radio Brisbane QLD","ABC_Radio_Brisbane_QLD",Radio4,0,"https://www.abc.net.au/listen/live/brisbane","",0],
    ["ABC Capricornia QLD","ABC_Capricornia_QLD",Radio4,0,"https://www.abc.net.au/listen/live/capricornia","",0],
    ["ABC Far North QLD","ABC_Far_North_QLD",Radio4,0,"https://www.abc.net.au/listen/live/farnorth","",0],
    ["ABC Gold Coast QLD","ABC_Gold_Coast_QLD",Radio4,0,"https://www.abc.net.au/listen/live/goldcoast","",0],
    ["ABC North Queensland QLD","ABC_North_Queensland_QLD",Radio4,0,"https://www.abc.net.au/listen/live/northqld","",0],
    ["ABC North West Queensland QLD","ABC_North_West_Queensland_QLD",Radio4,0,"https://www.abc.net.au/listen/live/northwest","",0],
    ["ABC Southern Queensland QLD","ABC_Southern_Queensland_QLD",Radio4,0,"https://www.abc.net.au/listen/live/southqld","",0],
    ["ABC Sunshine Coast QLD","ABC_Sunshine_Coast_QLD",Radio4,0,"https://www.abc.net.au/listen/live/sunshine","",0],
    ["ABC Tropical North QLD","ABC_Tropical_North_QLD",Radio4,0,"https://www.abc.net.au/listen/live/tropic","",0],
    ["ABC Western Queensland QLD","ABC_Western_Queensland_QLD",Radio4,0,"https://www.abc.net.au/listen/live/westqld","",0],
    ["ABC Wide Bay QLD","ABC_Wide_Bay_QLD",Radio4,0,"https://www.abc.net.au/listen/live/widebay","",0],
    ["ABC Radio Perth WA","ABC_Radio_Perth_WA",Radio4,0,"https://www.abc.net.au/listen/live/perth","",0],
    ["ABC Esperance WA","ABC_Esperance_WA",Radio4,0,"https://www.abc.net.au/listen/live/esperance","",0],
    ["ABC Goldfields WA","ABC_Goldfields_WA",Radio4,0,"https://www.abc.net.au/listen/live/goldfields","",0],
    ["ABC Great Southern WA","ABC_Great_Southern_WA",Radio4,0,"https://www.abc.net.au/listen/live/greatsouthern","",0],
    ["ABC Kimberley WA","ABC_Kimberley_WA",Radio4,0,"https://www.abc.net.au/listen/live/kimberley","",0],
    ["ABC Midwest & Wheatbelt WA","ABC_Midwest_and_Wheatbelt_WA",Radio4,0,"","",0],
    ["ABC Pilbara WA","ABC_Pilbara_WA",Radio4,0,"https://www.abc.net.au/listen/live/pilbara","",0],
    ["ABC South West WA","ABC_South_West_WA",Radio4,0,"https://www.abc.net.au/listen/live/southwestwa","",0],
    ["ABC NewsRadio","ABC_NewsRadio",Radio4,0,"https://www.abc.net.au/listen/live/news","",0],

    ["ABC Country","ABC_Country",Radio5,0,"https://www.abc.net.au/listen/live/country","",0],
    ["ABC Radio Australia","ABC_Radio_Australia",Radio5,0,"https://www.abc.net.au/pacific/live","",0],

    ["ABC Kids listen","ABC_Kids_listen",Radio6,0,"https://www.abc.net.au/listenlive/kidslisten","",0],

    ["ABC SPORT","ABC_SPORT",Radio7,0,"https://www.abc.net.au/news/sport/audio","",0], # FIX
    
    ["KIIS 1065","KIIS1065",Commercial1,0,"https://www.iheart.com/live/kiis-1065-6185/","css-1jnehb1 e1aypx0f0",0],
    ["GOLD101.7","GOLD1017",Commercial1,0,"https://www.iheart.com/live/gold1017-6186/","css-1jnehb1 e1aypx0f0",0],
    ["CADA","CADA",Commercial1,0,"https://www.iheart.com/live/cada-6179/","css-1jnehb1 e1aypx0f0",0],
    ["iHeartCountry Australia","iHeartCountry_Australia",Commercial1,0,"https://www.iheart.com/live/iheartcountry-australia-7222/","css-1jnehb1 e1aypx0f0",0],
    ["KIIS 90s","KIIS_90s",Commercial1,0,"https://www.iheart.com/live/kiis-90s-10069/","css-1jnehb1 e1aypx0f0",0],
    ["GOLD 80s","GOLD_80s",Commercial1,0,"https://www.iheart.com/live/gold-80s-10073/","css-1jnehb1 e1aypx0f0",0],
    ["iHeartRadio Countdown AUS","iHeartRadio_Countdown_AUS",Commercial1,0,"https://www.iheart.com/live/iheartradio-countdown-aus-6902/","css-1jnehb1 e1aypx0f0",0],
    ["TikTok Trending on iHeartRadio","TikTok_Trending_on_iHeartRadio",Commercial1,0,"https://www.iheart.com/live/tiktok-trending-on-iheartradio-8876/","css-1jnehb1 e1aypx0f0",0],
    ["iHeartDance","iHeartDance",Commercial1,0,"https://www.iheart.com/live/iheartdance-6941/","css-1jnehb1 e1aypx0f0",0],
    ["The Bounce","The_Bounce",Commercial1,0,"https://www.iheart.com/live/the-bounce-6327/","css-1jnehb1 e1aypx0f0",0],
    ["iHeartAustralia","iHeartAustralia",Commercial1,0,"https://www.iheart.com/live/iheartaustralia-7050/","css-1jnehb1 e1aypx0f0",0],
    ["fbi.radio","fbi_radio",Commercial1,0,"https://www.iheart.com/live/fbiradio-6311/","css-1jnehb1 e1aypx0f0",0],
    ["2SER","_2SER",Commercial1,0,"https://www.iheart.com/live/2ser-6324/","css-1jnehb1 e1aypx0f0",0],
    ["2MBS Fine Music Sydney","_2MBS_Fine_Music_Sydney",Commercial1,0,"https://www.iheart.com/live/2mbs-fine-music-sydney-6312/","css-1jnehb1 e1aypx0f0",0],
    ["KIX Country","KIX_Country",Commercial1,0,"https://www.iheart.com/live/kix-country-9315/","css-1jnehb1 e1aypx0f0",0],
    ["SBS Chill","SBS_Chill",Commercial1,0,"https://www.iheart.com/live/sbs-chill-7029/","css-1jnehb1 e1aypx0f0",0],
    ["Vintage FM","Vintage_FM",Commercial1,0,"https://www.iheart.com/live/vintage-fm-8865/","css-1jnehb1 e1aypx0f0",0],
    ["My88 FM","My88_FM",Commercial1,0,"https://www.iheart.com/live/my88-fm-8866/","css-1jnehb1 e1aypx0f0",0],
    ["Hope 103.2","Hope_103_2",Commercial1,0,"https://www.iheart.com/live/hope-1032-6314/","css-1jnehb1 e1aypx0f0",0],
    ["The 90s iHeartRadio","The_90s_iHeartRadio",Commercial1,0,"https://www.iheart.com/live/the-90s-iheartradio-6793/","css-1jnehb1 e1aypx0f0",0],
    ["The 80s iHeartRadio","The_80s_iHeartRadio",Commercial1,0,"https://www.iheart.com/live/the-80s-iheartradio-6794/","css-1jnehb1 e1aypx0f0",0],
    ["Mix 102.3","Mix_102_3",Commercial1,0,"https://www.iheart.com/live/mix1023-6184/","css-1jnehb1 e1aypx0f0",0],
    ["Cruise 1323","Cruise_1323",Commercial1,0,"https://www.iheart.com/live/cruise-1323-6177/","css-1jnehb1 e1aypx0f0",0],
    ["Mix 80s","Mix_80s",Commercial1,0,"https://www.iheart.com/live/mix-80s-10076/","css-1jnehb1 e1aypx0f0",0],
    ["Mix 90s","Mix_90s",Commercial1,0,"https://www.iheart.com/live/mix-90s-10072/","css-1jnehb1 e1aypx0f0",0],
    ["ABC Sport","ABC_Sport",Commercial1,0,"https://www.iheart.com/live/abc-sport-7112/","css-1jnehb1 e1aypx0f0",0],
    ["ABC Sport Extra","ABC_Sport_Extra",Commercial1,0,"https://www.iheart.com/live/abc-sport-extra-10233/","css-1jnehb1 e1aypx0f0",0],
    ["Energy Groove","Energy_Groove",Commercial1,0,"https://www.iheart.com/live/energy-groove-6329/","css-1jnehb1 e1aypx0f0",0],
    ["Vision Christian Radio","Vision_Christian_Radio",Commercial1,0,"https://www.iheart.com/live/vision-christian-radio-9689/","css-1jnehb1 e1aypx0f0",0],
    ["Starter FM","Starter_FM",Commercial1,0,"https://www.iheart.com/live/starter-fm-9353/","css-1jnehb1 e1aypx0f0",0],
    ["2ME","_2ME",Commercial1,0,"https://www.iheart.com/live/2me-10143/","css-1jnehb1 e1aypx0f0",0],
    ["SBS PopAsia","SBS_PopAsia",Commercial1,0,"https://www.iheart.com/live/sbs-popasia-7028/","css-1jnehb1 e1aypx0f0",0],
    ["3MBS Fine Music Melbourne","_3MBS_Fine_Music_Melbourne",Commercial1,0,"https://www.iheart.com/live/3mbs-fine-music-melbourne-6183/","css-1jnehb1 e1aypx0f0",0],
    ["Golden Days Radio","Golden_Days_Radio",Commercial1,0,"https://www.iheart.com/live/golden-days-radio-8676/","css-1jnehb1 e1aypx0f0",0],
    ["PBS 106.7FM","PBS_106_7FM",Commercial1,0,"https://www.iheart.com/live/pbs-1067fm-6316/","css-1jnehb1 e1aypx0f0",0],
    ["smoothfm 95.3 Sydney","smoothfm_953_Sydney",Commercial1,0,"https://smooth.com.au/station/smoothsydney","index_smooth_info-wrapper-desktop__6ZYTT",1],
    ["smoothfm 91.5 Melbourne","smoothfm_915_Melbourne",Commercial1,0,"https://smooth.com.au/station/smoothfm915","index_smooth_info-wrapper-desktop__6ZYTT",1],
    ["smoothfm Adelaide","smoothfm_Adelaide",Commercial1,0,"https://smooth.com.au/station/adelaide","index_smooth_info-wrapper-desktop__6ZYTT",1],
    ["smoothfm Brisbane","smoothfm_Brisbane",Commercial1,0,"https://smooth.com.au/station/brisbane","index_smooth_info-wrapper-desktop__6ZYTT",1],
    ["smoothfm Perth","smoothfm_Perth",Commercial1,0,"https://smooth.com.au/station/smoothfmperth","index_smooth_info-wrapper-desktop__6ZYTT",1],
    ["smooth 80s","smooth_80s",Commercial1,0,"https://smooth.com.au/station/smooth80s","index_smooth_info-wrapper-desktop__6ZYTT",1],
    ["smooth relax","smooth_relax",Commercial1,0,"https://smooth.com.au/station/smoothrelax","index_smooth_info-wrapper-desktop__6ZYTT",1],
    ["smooth VINTAGE","smooth_VINTAGE",Commercial1,0,"https://smooth.com.au/station/smoothvintage","index_smooth_info-wrapper-desktop__6ZYTT",1],
    ["nova 969 Sydney","nova_969_Sydney",Commercial1,0,"https://novafm.com.au/station/nova969","index_nova_info-wrapper-desktop__CWW5R",1],
    ["nova 100 Melbourne","nova_100_Melbourne",Commercial1,0,"https://novafm.com.au/station/nova100","index_nova_info-wrapper-desktop__CWW5R",1],
    ["nova 919 Adelaide","nova_919_Adelaide",Commercial1,0,"https://novafm.com.au/station/nova919","index_nova_info-wrapper-desktop__CWW5R",1],
    ["nova 1069 Brisbane","nova_1069_Brisbane",Commercial1,0,"https://novafm.com.au/station/nova1069","index_nova_info-wrapper-desktop__CWW5R",1],
    ["nova 937 Perth","nova_937_Perth",Commercial1,0,"https://novafm.com.au/station/nova937","index_nova_info-wrapper-desktop__CWW5R",1],
    ["nova 90s","nova_90s",Commercial1,0,"https://novafm.com.au/station/nova90s","index_nova_info-wrapper-desktop__CWW5R",1],
    ["nova THROWBACKS","nova_THROWBACKS",Commercial1,0,"https://novafm.com.au/station/throwbacks","index_nova_info-wrapper-desktop__CWW5R",1],
    ["nova FreshCOUNTRY","nova_FreshCOUNTRY",Commercial1,0,"https://novafm.com.au/station/novafreshcountry","index_nova_info-wrapper-desktop__CWW5R",1],
    ["nova NATION","nova_NATION",Commercial1,0,"https://novafm.com.au/station/novanation","index_nova_info-wrapper-desktop__CWW5R",1],

    ["2GB SYDNEY","2GB_SYDNEY",Commercial2,0,"https://www.radio-australia.org/2gb","",0],
    ["2GN GOULBURN","2GN_GOULBURN",Commercial2,0,"https://www.radio-australia.org/2gn","",0],
    ["bbc radio 1","bbc_radio_1",Commercial2,0,"https://www.radio-uk.co.uk/bbc-radio-1","",0],
    ["bbc radio 2","bbc_radio_2",Commercial2,0,"https://www.radio-uk.co.uk/bbc-radio-2","",0],
    ["bbc radio 3","bbc_radio_3",Commercial2,0,"https://www.radio-uk.co.uk/bbc-radio-3","",0],
    ["bbc radio 4","bbc_radio_4",Commercial2,0,"https://www.radio-uk.co.uk/bbc-radio-4","",0],
    ["bbc radio 5 live","bbc_radio_5_live",Commercial2,0,"https://www.radio-uk.co.uk/bbc-radio-5-live","",0],
    ["bbc world service","bbc_world_service",Commercial2,0,"https://www.radio-uk.co.uk/bbc-world-service","",0],
    ["bbc radio 4 extra","bbc_radio_4_extra",Commercial2,0,"https://www.radio-uk.co.uk/bbc-radio-4-extra","",0],
    ["bbc radio london","bbc_radio_london",Commercial2,0,"https://www.radio-uk.co.uk/bbc-london","",0],
    ["bbc radio 1xtra","bbc_radio_1xtra",Commercial2,0,"https://www.radio-uk.co.uk/bbc-1xtra","",0],
    ["1000 hits classical music","_1000_hits_classical_music",Commercial2,0,"https://www.fmradiofree.com/1000-hits-classical-music","",0],
    ["classic fm","classic_fm",Commercial2,0,"https://www.radio-uk.co.uk/classic-fm","",0],
    ["classical california KUSC","classical_california_KUSC",Commercial2,0,"https://www.internetradio-horen.de/us/kusc-classical-915-fm-kdb","",0],
    ["classical mood","classical_mood",Commercial2,0,"https://www.internetradio-horen.de/ae/classical-mood","",0],
    ["classical ultra quiet radio","classical_ultra_quiet_radio",Commercial2,0,"https://www.internetradio-horen.de/ca/ultra-quiet-radio","",0],
    ["classic radio swiss","classic_radio_swiss",Commercial2,0,"https://www.internetradio-horen.de/ch/radio-swiss-classic-fr","",0],
    ["klassik radio","klassik_radio",Commercial2,0,"https://www.internetradio-horen.de/klassik-radio","",0],
    ["klassik radio pure bach","klassik_radio_pure_bach",Commercial2,0,"https://www.internetradio-horen.de/klassik-radio-pure-bach","",0],
    ["klassik radio pure beethoven","klassik_radio_pure_beethoven",Commercial2,0,"https://www.internetradio-horen.de/klassik-radio-pure-beethoven","",0],
    ["klassik radio pure mozart","klassik_radio_pure_mozart",Commercial2,0,"https://www.internetradio-horen.de/klassik-radio-pure-mozart","",0],
    ["klassik radio pure verdi","klassik_radio_pure_verdi",Commercial2,0,"https://www.internetradio-horen.de/klassik-radio-pure-verdi","",0],
    ["klassik radio barock","klassik_radio_barock",Commercial2,0,"https://www.internetradio-horen.de/klassik-radio-barock","",0],
    ["klassik radio piano","klassik_radio_piano",Commercial2,0,"https://www.internetradio-horen.de/klassik-radio-piano","",0],
    ["klassik radio piano new classics","klassik_radio_new_piano",Commercial2,0,"https://www.internetradio-horen.de/klassik-radio-piano-new-classics","",0],
    ["epic piano solo","epic_piano_solo",Commercial2,0,"https://www.internetradio-horen.de/epic-piano-solo-piano","",0],
    ["epic piano coverhits","epic_piano_coverhits",Commercial2,0,"https://www.internetradio-horen.de/epic-piano-piano-coverhits","",0],
    ["epic piano great concerts","epic_piano_greatconcerts",Commercial2,0,"https://www.internetradio-horen.de/epic-piano-great-concerts","",0],
    ["epic piano chillout","epic_piano_chillout",Commercial2,0,"https://www.internetradio-horen.de/epic-piano-chillout-piano","",0],
    ["epic piano modern","epic_piano_modern",Commercial2,0,"https://www.internetradio-horen.de/epic-piano-modern-piano","",0],
    ["epic piano romantic","epic_piano_romantic",Commercial2,0,"https://www.internetradio-horen.de/epic-piano-romantic-piano","",0],
    ["epic piano christmas","epic_piano_christmas",Commercial2,0,"https://www.internetradio-horen.de/epic-piano-piano-christmas","",0],
    ["epic piano Chopin","epic_piano_chopin",Commercial2,0,"https://www.internetradio-horen.de/epic-piano-chopin","",0],
    ["epic piano Tschaikowski","epic_piano_tschaikowski",Commercial2,0,"https://www.internetradio-horen.de/epic-piano-tschaikowski","",0],
    ["epic piano Grieg","epic_piano_grieg",Commercial2,0,"https://www.internetradio-horen.de/epic-piano-grieg","",0],
    ["epic piano Liszt","epic_piano_liszt",Commercial2,0,"https://www.internetradio-horen.de/epic-piano-liszt","",0],
    ["antenne bayern live","antenne_bayern_live",Commercial2,0,"https://www.internetradio-horen.de/antenne-bayern","",0],
    ["antenne bayern schlagersahne","antenne_bayern_schlagersahne",Commercial2,0,"https://www.internetradio-horen.de/antenne-bayern-schlagersahne","",0],
    ["antenne bayern top40","antenne_bayern_top40",Commercial2,0,"https://www.internetradio-horen.de/antenne-bayern-top-40","",0],
    ["antenne bayern 80er kulthits","antenne_bayern_80er_kulthits",Commercial2,0,"https://www.internetradio-horen.de/antenne-bayern-80er-kulthits","",0],
    ["antenne bayern 90er hits","antenne_bayern_90er_hits",Commercial2,0,"https://www.internetradio-horen.de/antenne-bayern-90er-hits","",0],
    ["antenne bayern lovesongs","antenne_bayern_lovesongs",Commercial2,0,"https://www.internetradio-horen.de/antenne-bayern-lovesongs","",0],
    ["antenne bayern 70er hits","antenne_bayern_70er_hits",Commercial2,0,"https://www.internetradio-horen.de/antenne-bayern-70er-hits","",0],
    ["antenne bayern classic rock","antenne_bayern_classic_rock",Commercial2,0,"https://www.internetradio-horen.de/antenne-bayern-classic-rock-live","",0],
    ["antenne bayern greatest hits","antenne_bayern_greatest_hits",Commercial2,0,"https://www.internetradio-horen.de/antenne-bayern-greatest-hits","",0],
    ["antenne bayern coffeemusic","antenne_bayern_coffeemusic",Commercial2,0,"https://www.internetradio-horen.de/antenne-bayern-coffeemusic","",0],
    ["antenne bayern relax","antenne_bayern_relax",Commercial2,0,"https://www.internetradio-horen.de/anja-kurz","",0],
    ["antenne bayern lounge","antenne_bayern_lounge",Commercial2,0,"https://www.internetradio-horen.de/antenne-bayern-country","",0],
    ["totally radio hits","totally_radio_hits",Commercial2,0,"https://www.internetradio-horen.de/au/totally-radio-hits","",0],
    ["totally radio 90s","totally_radio_90s",Commercial2,0,"https://www.internetradio-horen.de/au/totally-radio-90s","",0],
    ["totally radio 80s","totally_radio_80s",Commercial2,0,"https://www.internetradio-horen.de/au/totally-radio-80s","",0],
    ["totally radio 70s","totally_radio_70s",Commercial2,0,"https://www.internetradio-horen.de/au/totally-radio-70s","",0],
    ["totally radio 60s","totally_radio_60s",Commercial2,0,"https://www.internetradio-horen.de/au/totally-radio-60s","",0],

    ["us adagiofm","us_adagiofm",Commercial2,0,"https://www.internetradio-horen.de/us/adagiofm","",0], # PROBLEM
    ["it venice classic radio","it_venice_classic_radio",Commercial2,0,"https://www.internetradio-horen.de/it/venice-classic-radio","",0],
    ["fr radio classique","fr_radio_classique",Commercial2,0,"https://www.internetradio-horen.de/fr/radio-classique","",0],
    ["us whisperings solo piano radio","us_whisperings_solo_piano_radio",Commercial2,0,"https://www.internetradio-horen.de/us/whisperings-solo-piano-radio","",0],
    ["bayern 1","bayern_1",Commercial2,0,"https://www.internetradio-horen.de/bayern-1","",0],
    ["us the big 80s station","us_the_big_80s_station",Commercial2,0,"https://www.internetradio-horen.de/us/the-big-80s-station","",0],
    ["antenne bayern oldies but goldies","antenne_bayern_oldies_but_goldies",Commercial2,0,"https://www.internetradio-horen.de/antenne-bayern-oldies-but-goldies","",0],
    ["br radio 80 fm","br_radio_80_fm",Commercial2,0,"https://www.internetradio-horen.de/br/radio-80-fm","",0],
    ["au its 80s","au_its_80s",Commercial2,0,"https://www.internetradio-horen.de/au/its-80s","",0],
    ["nl 80s alive","nl_80s_alive",Commercial2,0,"https://www.internetradio-horen.de/nl/80s-alive","",0],
    ["ae wonder 80s","ae_wonder_80s",Commercial2,0,"https://www.internetradio-horen.de/ae/wonder-80s","",0],
    ["nl joe 70s 80s","nl_joe_70s_80s",Commercial2,0,"https://www.internetradio-horen.de/nl/joe-70s-80s","",0]
]    

# COMMON BLOCK END ***********************************************


# 2D array of preset radio stations, in long name and index (to aStation[]) format.
# this is the default, but is actually copied from file at statup and saved to file on exit!
aStation2 = []
for i in range(numButtons):
    station = ["-- EMPTY " + str(i) +" --", -1]
    aStation2.append(station)


# does stuff just after gui is initialised and we are running in the root thread
def after_GUI_started():
  # select to stream last station that was streaming just before radio was powered down
    global buttonIndex, buttonFlag; buttonFlag = True
    try:
        with open(filepath, 'r') as file:
            buttonIndex = int(file.read())
    except FileNotFoundError:
        print(f'Error: The file {filepath} does not exist.')
        buttonIndex = 0
    buttons[buttonIndex].focus_set()    
    print(f'Button of last station played in playlist is {buttonIndex}')    
    print("")    
    on_select2(CustomEvent("Auto", buttons[buttonIndex], "Auto from GUI start"))


# do this when closing the window/app
def on_closing():
    browser.quit() # close the WebDriver
    root.destroy() # destroy GUI   
    print("Closing the app...")


# do this when a radio station is selected from combobox
def on_select(event):
    global StationName, StationLogo, StationFunction, nNum, sPath, sClass, nType 

    # determine the timeInterval between calling on_select() or on_select2()
    global startTime, finishTime
    finishTime = time.time()
    timeInterval = finishTime-startTime
    timeIntervalStr = f"{timeInterval:.2f}"
    print("***********************")
    print(f"Time interval: {timeIntervalStr} seconds")
    print("***********************")
    startTime = time.time()
    print(f"Type: {event.type}")
    print(f"Widget: {event.widget}")
    print(f"Data: {event.data}")
    
    # set various flags and parameters related to starting a station stream or accesing its website
    global eventFlag, stopFlag, selected_value, combobox_index, selected_value_last 
    if event.type=="Auto":
        eventFlag = True # if on_select() is called by selecting a combobox entry
        stopFlag = False # if this call of on_select() should be implemented
      # parameters relating to how this funtion was called
        selected_value_last = selected_value
        selected_value = combobox.get()
        combobox_index = combobox.current()
        print("selected_value:", selected_value)
        print("combobox_index:", combobox_index)

    # extract all parameters for the selected radio station
    StationName = aStation[combobox_index][0]
    StationLogo = aStation[combobox_index][1]
    StationFunction = aStation[combobox_index][2]
    nNum = aStation[combobox_index][3]
    sPath = aStation[combobox_index][4]
    sClass = aStation[combobox_index][5]
    nType = aStation[combobox_index][6]

    # setting stop flag, this prevents on_select() from running again
    # "mysterious" code due to timing issues
    if eventFlag:
        stopFlag = False

        # inform user that a station is being started
        text = "Please be patient, the station *" +  StationName + "*is being started"
        text_rows = text.split("*")
        text_box.config(state=tk.NORMAL)
        text_box.delete('1.0', tk.END)
        for row in text_rows:
            text_box.insert(tk.END, row + "\n")
        text_box.config(state=tk.DISABLED)
        root.update_idletasks()

    else: # if (not eventFlag)   
        if stopFlag:
            stopFlag=False
            print("SECOND STOP FAIL")
        elif (timeInterval < refreshTime-0.5):
            stopFlag = True    
            print("FIRST STOP")
    print("stopFlag:",stopFlag)
    print("eventFlag:",eventFlag)

    if stopFlag==False:
        # run selected radio station stream, and return associated textual information 
        try:
            #text = aStation[combobox_index][1]() # THIS BIT ACTUALLY STARTS STREAM
            text = StationFunction(browser,nNum,sPath,sClass,nType)

#            fullStationName = aStation[combobox_index][0] 
#            text = fullStationName + "*" + text
            text = StationName + "*" + text
            text = text + "* *[" + timeIntervalStr + "]"
            text_rows = text.split("*")
            if len(text_rows)>1:
                if text_rows[0]==text_rows[1]:
                        del text_rows[0]

            # Make text box editable, so contents can be deleted and rewritten
            text_box.config(state=tk.NORMAL)
            text_box.delete('1.0', tk.END)
            print(text_rows)
            # Insert each row of text into the text box
            for row in text_rows:
                text_box.insert(tk.END, row + "\n")
            # Disable the text box to make it read-only
            text_box.config(state=tk.DISABLED)

            # on_select() schedules itself to run in nominally refreshTime seconds.
            # this updates the program text and grapic while the selected radio station is streaming
            print("JUST ABOUT TO RUN ROOT")
            eventFlag = False
            root.after(int(refreshTime*1000), lambda: on_select(CustomEvent("Manual", combobox, "Manual from combobox")))
            print("FINISHED RUNNING ROOT")
            print("")

        except urllib.error.HTTPError as e:
            event.type = "Manual" # to prevent saving of buttonIndex

            # inform user that starting station has failed in some way
            text = "<<< ERROR >>>*" + StationName + "*failed to load properly*"
            text = text + "HTTP Error " + str(e.code) + ": " + str(e.reason)
            text = text + "*Try again or select a different station."
            text_rows = text.split("*")
            text_box.config(state=tk.NORMAL)
            text_box.delete('1.0', tk.END)
            for row in text_rows:
                text_box.insert(tk.END, row + "\n")
            text_box.config(state=tk.DISABLED)
            root.update_idletasks()

    else: #if stopFlag==True
        # Makes the scheduled call to on_select() do nothing if
        # it occurs after another station stream has been started
        stopFlag = False
        print("selected_value:",selected_value_last)
        print("DID STOPPING BIT")
        print("")


# do this when a radio station is selected via playlist buttons,
# similar in structure to on_select(), but the way the radio station stream is called differs.
def on_select2(event):
    global StationName, StationLogo, StationFunction, nNum, sPath, sClass, nType 

    global startTime, finishTime
    finishTime = time.time()
    timeInterval = finishTime-startTime
    timeIntervalStr = f"{timeInterval:.2f}"
    print("***********************")
    print(f"Time interval: {timeIntervalStr} seconds")
    print("***********************")
    startTime = time.time()
    print(f"Type: {event.type}")
    print(f"Widget: {event.widget}")
    print(f"Data: {event.data}")

    global eventFlag, stopFlag, selected_value, selected_index, selected_value_last
    if event.type=="Auto":
        eventFlag = True
        selected_value_last = selected_value
        selected_value = aStation2[buttonIndex][0]
        selected_index = int(aStation2[buttonIndex][1])
        print("selected_value:",selected_value)
        print("selected_index:",selected_index)

    # extract all parameters for the selected radio station
    StationName = aStation[selected_index][0]
    StationLogo = aStation[selected_index][1]
    StationFunction = aStation[selected_index][2]
    nNum = aStation[selected_index][3]
    sPath = aStation[selected_index][4]
    sClass = aStation[selected_index][5]
    nType = aStation[selected_index][6]

    # setting stop flag, this prevents on_select2 from running again
    # "mysterious" code due to timing issues
    if eventFlag:
        stopFlag = False

        if selected_index != -1:
            # inform user that a station is being started
            text = "Please be patient, the station *" +  StationName + "*is being started"
            text_rows = text.split("*")
            text_box.config(state=tk.NORMAL)
            text_box.delete('1.0', tk.END)
            for row in text_rows:
                text_box.insert(tk.END, row + "\n")
            text_box.config(state=tk.DISABLED)
            root.update_idletasks()

    else: # if (not eventFlag)   
        if stopFlag:
            stopFlag=False
            print("SECOND STOP FAIL")
        elif (timeInterval < refreshTime-0.5):
            stopFlag = True    
            print("FIRST STOP")
    print("stopFlag:",stopFlag)
    print("eventFlag:",eventFlag)

    if stopFlag==False:
        print("Selected:", selected_value)
        print("Index:", selected_index)
        print("Button index:", buttonIndex)

        if selected_index != -1:
            print("selected_index != -1")

            # run selected radio station stream, and return associated textual information 
            try:
                text = StationFunction(browser,nNum,sPath,sClass,nType)
                text = StationName + "*" + text
                text = text + "* *[" + timeIntervalStr + "]"
                text_rows = text.split("*")
                if len(text_rows)>1:
                    if text_rows[0]==text_rows[1]:
                            del text_rows[0]

                # Make text box editable, so contents can be deleted and rewritten
                text_box.config(state=tk.NORMAL)
                text_box.delete('1.0', tk.END)
                print(text_rows)

                # Insert each row of text into the text box
                for row in text_rows:
                    text_box.insert(tk.END, row + "\n")

                # Disable the text box to make it read-only
                text_box.config(state=tk.DISABLED)
                root.update_idletasks()

                # make seleted button synchronize with combobox
                # hide the annoying blinking cursor though the fudge
                # of selective focus setting
                if event.type=="Auto":
                    combobox.set(StationName)
                    combobox.focus_set()
                    combobox.selection_clear()
                    buttons[buttonIndex].focus_set()
                
                print("JUST ABOUT TO RUN ROOT")
                eventFlag = False
                root.after(int(refreshTime*1000), lambda: on_select2(CustomEvent("Manual", buttons[buttonIndex], "Manual from buttons")))
                print("FINISHED RUNNING ROOT")
                print("")

            except urllib.error.HTTPError as e:
                event.type = "Manual" # to prevent saving of buttonIndex

                # inform user that starting station has failed in some way
                text = "<<< ERROR >>>*" + StationName + "*failed to load properly*"
                text = text + "HTTP Error " + str(e.code) + ": " + str(e.reason)
                text = text + "*Try again or select a different station."
                text_rows = text.split("*")
                text_box.config(state=tk.NORMAL)
                text_box.delete('1.0', tk.END)
                for row in text_rows:
                    text_box.insert(tk.END, row + "\n")
                text_box.config(state=tk.DISABLED)
                root.update_idletasks()

        else:
            # There is nothing to stream
            browser.get(refresh_http)
            time.sleep(2)
            text = selected_value + "*No station playing"
            text = text + "* *[" + timeIntervalStr + "]"
            text_rows = text.split("*")

            # Make text box editable, so contents can be deleted and rewritten
            text_box.config(state=tk.NORMAL)
            text_box.delete('1.0', tk.END)
            print(text_rows)

            # Insert each row of text into the text box
            for row in text_rows:
                text_box.insert(tk.END, row + "\n")

            # Disable the text box to make it read-only
            text_box.config(state=tk.DISABLED)
            root.update_idletasks()

            # Display the station logo and program graphic as blank
            image_path = pathImages + "/Blank.png"
            image = Image.open(image_path)
            scaled_image = image.resize((iconSize, iconSize))  # Adjust the size as needed
            photo = ImageTk.PhotoImage(scaled_image)
            label.config(image=photo)
            label.image = photo  # Keep a reference to avoid garbage collection
            scaled_image2 = image.resize((Xprog, Xprog))  # Adjust the size as needed
            photo2 = ImageTk.PhotoImage(scaled_image2)
            label2.config(image=photo2)
            label2.image = photo2  # Keep a reference to avoid garbage collection
            label2.place(x=Xgap, y=Ygap2)  # Adjust the position
            print("BLANK END")
            print("")

        if event.type=="Auto":
            # save number of last playlist radio station that was played (0,...,9), ie buttonIndex.
            with open(filepath, 'w') as file:
                file.write(str(buttonIndex))

    else: #if stopFlag==True
        print("selected_value:",selected_value_last)
        print("DID STOPPING BIT")
        print("")


# called when playlist button i is in focus and the Enter key is pressed.
# visually simulates a physical button press and initiates the station stream by
# calling the on_select2    () function
def on_button_press(event, i):
    buttons[i].config(relief="sunken", bg="lightgray")  # Simulate button press
    buttons[i].update_idletasks()  # Force update
    time.sleep(1)
    buttons[i].config(relief="raised", bg="gray90")  # Simulate button press
    buttons[i].update_idletasks()  # Force update
    print("Button " + str(i) +" pressed")

    global buttonFlag;  buttonFlag = True
    global buttonIndex; buttonIndex = i
    on_select2(CustomEvent("Auto", buttons[buttonIndex], "Auto from Enter key"))    


# called when playlist button i is in focus and the Delete key is pressed.
# deletes the station from the playlist.
def on_button_delete(event, i):
    global buttonIndex; buttonIndex = i

     # change aStation2[] to reflect the deletion
    global aStation2
    index = aStation2[buttonIndex][1]
    print("deleting station:", index, "with playlist index:", buttonIndex)
    if index != -1:
        print("station deleted")    

        lastStation = "-- EMPTY " + str(buttonIndex) +" --"
        aStation2[buttonIndex][0] = lastStation
        aStation2[buttonIndex][1] = -1

        # get blank station logo
        image_path = pathImages + "/Blank.png"
        image = Image.open(image_path)

        # saving blank button icon
        buttonImagePath = pathImages + "/button" + str(buttonIndex) + ".png"
        image.save(buttonImagePath)

        # now need to update the icon on the buttonIndex button
        image_resized = image.resize((sizeButton-5,sizeButton-5), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image_resized)
        buttons[buttonIndex].config(image=photo)
        buttons[buttonIndex].image = photo
        buttons[buttonIndex].update_idletasks() 

        # This will "play" the blank station for the real purpose of shutting down the current station
        on_select2(CustomEvent("Auto", buttons[buttonIndex], "Auto from Delete key"))

        # save the playlist to file
        with open(filepath2, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(aStation2)
    else:        
        print("No station to delete")    
    print(f"space button {i} pressed")


# called when playlist button i is in focus and the Insert key is pressed.
# Inserts the last station played from the combobox into the playlist.
# If the playlist button is already occupied, the station is replaced.
# In particular it displays the station logo on the button and links it to the station.
def on_button_insert(event, i):
    global buttonIndex; buttonIndex = i
    
    # change aStation2[] list to reflect the addition
    global aStation2
    if (combobox_index != -1):
        print("station added")    
        global addFlag
        addFlag = True # so can get and save icon for playlist button

        lastStation = aStation[combobox_index][0]
        aStation2[buttonIndex][0] = lastStation
        aStation2[buttonIndex][1] = combobox_index

        # This will play the newly added station (from the combobox) as well as saving the icon
        # to its playlist button number
        on_select2(CustomEvent("Auto", buttons[buttonIndex], "Auto from Insert Key"))

        # now need to update the icon on the buttonIndex button
        buttonImagePath = pathImages + "/button" + str(buttonIndex) + ".png"
        image = Image.open(buttonImagePath)
        image_resized = image.resize((sizeButton-5,sizeButton-5), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image_resized)
        buttons[buttonIndex].config(image=photo)
        buttons[buttonIndex].image = photo
        buttons[buttonIndex].update_idletasks()

        # save the playlist to file
        with open(filepath2, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(aStation2)
    else:
        print("No station added")    
    print("")


# called when a playlist button receives focus.
# visually indicates that the button has focus and
# saves the buttonIndex in a global variable
def on_focus(event, i):
    buttons[i].config(relief="raised", bg="darkgray")  # Simulate button press
    buttons[i].update_idletasks()  # Force update
    # global buttonIndex; buttonIndex = i
    print(f"on focus: {i}")

# called when a playlist button loses focus.
# returns the button is a visually "unfocused" state. 
def on_focus_out(event, i):
    buttons[i].config(relief="raised", bg="gray90")  # Simulate button press
    buttons[i].update_idletasks()  # Force update
    print(f"on focus out: {i}")

# called when station combobox receives focus.
# makes sure its display is updated.
def on_focus_combobox(event):
    combobox.update_idletasks()  # Force update
    print("on_focus_combobox")

# called when station combobox loses focus.
# makes sure its display is updated.
def on_focus_out_combobox(event):
    combobox.update_idletasks()  # Force update
    print("on_focus_out_combobox")


####################################
# THIS IS WHERE THE CORE CODE STARTS

# Create the main window
root = tk.Tk()

# Set title, size and position of the main window, and make it non-resizable
strHeightForm = str(int(Xprog + 120 + Ydown)*0+480)
print(strHeightForm)
root.title("INTERNET RADIO - https://github.com/namor5772/TkRadio")  
root.geometry("800x" + strHeightForm + "+0+0")
root.resizable(False, False)  

# Create a combobox (dropdown list)
# Used to display all avialable radio stations
aStringArray = []
for element in aStation:
    aStringArray.append(element[0])
combobox = ttk.Combobox(root, values=aStringArray, height=20, width=33)
combobox.place(x=130+(sizeButton+5), y=2)  # Adjust the position
combobox.bind("<FocusIn>", on_focus_combobox)
combobox.bind("<FocusOut>", on_focus_out_combobox)
combobox.bind("<<ComboboxSelected>>", lambda e: on_select(CustomEvent("Auto", combobox, "ComboBox Event")))
combobox.config(state="readonly")

# Populate if possible the playlist array aStation2[] from file saved at shutdown
try:
    with open(filepath2, 'r') as file:
        reader = csv.reader(file)
        aStation2 = [row for row in reader]             
except FileNotFoundError:
    # will just use the default aStation2[] array created above
    print(f'Error: The file {filepath2} does not exist.')

# Create a text box, position and size it
# used to display the program and song details
text_box = tk.Text(root)
text_box.place(x=10, y=110+Ydown, width=Xgap-20, height=Xprog)
text_box.config(state=tk.NORMAL) # Enable the text box to insert text
# height=600-110-10

# Create labels used for station logo image (label) and program related image (label2)
# Positioning of latter can vary
label = tk.Label(root)
label.pack()
label.place(x=15, y=2)
label2 = tk.Label(root)
label2.pack()

# Create the playlist buttons (fully) and add them to the buttons[] list
# the button icons may fall out of sink with the playlist station values!
buttons = []
for i in range(numButtons):
    # HELP
    button = tk.Button(root, text=f"Button{i}")

    # positioning buttons in 2 rows of 9
    if (i<9):
        button.place(x=128+(sizeButton+5)*(i+1), y=35, width=sizeButton, height=sizeButton)
    else:
        button.place(x=128+(sizeButton+5)*(i-8), y=35+sizeButton+5, width=sizeButton, height=sizeButton)

    button.config(bg="gray90")
    button.bind("<FocusIn>", lambda event, i=i: on_focus(event, i))
    button.bind("<FocusOut>", lambda event, i=i: on_focus_out(event, i))
    button.bind("<ButtonPress>", lambda event, i=i: on_button_press(event, i))  
    button.bind("<Return>", lambda event, i=i: on_button_press(event, i))  
    button.bind("<Delete>", lambda event, i=i: on_button_delete(event, i))  
    button.bind("<Insert>", lambda event, i=i: on_button_insert(event, i))  

    buttonImage = Image.open(pathImages + "/button" + str(i) +".png")
    buttonImage_resized = buttonImage.resize((sizeButton-5,sizeButton-5), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(buttonImage_resized)
    button.config(image=photo)
    button.image = photo
    button.update_idletasks()
    buttons.append(button)


# doing stuff just after the gui is initialised and we are running in the root thread
root.after(1000, after_GUI_started)
print("Radio stream interface")

# Bind the closing event to the on_closing function
root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the GUI loop
root.mainloop()
print("out of GUI loop..")
