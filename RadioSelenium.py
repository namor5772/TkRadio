'''
1. Think about easier searching of the very large station list
    Fast scroll or filters mainly in RPI version
2. Russian and China originating internet stations?   
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
import random
try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    GPIO = None

from datetime import datetime
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException


# START #######################################################
# SETUP GPIO BUTTONS FOR THE RASPBERRY PI 4B AND THEIR ACTIONS

# Set up GPIO
if GPIO:
    GPIO.setmode(GPIO.BCM)

# Define GPIO pins for the rotary encoder and push button.
CLK_PIN = 2 #16   # Connect to CLK (A) of the encoder
DT_PIN  = 3 #20   # Connect to DT (B) of the encoder
SW_PIN  = 4 #21  # Connect to the push button

# Setup pins with internal pull-ups.
if GPIO:
    GPIO.setup(CLK_PIN, GPIO.IN)#, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(DT_PIN, GPIO.IN)#, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(SW_PIN, GPIO.IN)#, pull_up_down=GPIO.PUD_UP)

# Global counter for rotation steps
counter = 0
last_counter = 0
# Record the initial state of the CLK pin.
if GPIO:
    last_clk_state = GPIO.input(CLK_PIN)

# KeyList array & related global variables
# horizontal list of keys you can press (in a simulated fashion)
sizeKeyList = 120 # number of keys
indexKeyList = 1 # currently selected key (= indexBank*sizeBank+indexVisibleKey) 
indexVisibleKey = 1 # index of selected key within current bank
sizeBank = 15 # number of keys in a bank                  
indexBank = 0 # bank containing currently selected Key
numBanks = 8 # number of banks (thus numBanks*sizeBank = sizeKeyList)

# In ["what is displayed","actual Python key code"] format 
KeyList = [
    ["<-Tab","ISO_Left_Tab"],
    ["Tab","Tab"],
    ["Enter","Return"],
    ["Down","Down"],
    ["Up","Up"],
    ["Del","Delete"],
    ["Ins","Insert"],
    ["Left","Left"],
    ["Right","Right"],
    ["Home","Home"],
    ["End","End"],
    ["PgUp","Prior"],
    ["PgDn","Next"],
    ["Esc","Escape"],
    ["Back","BackSpace"],
    
    ["a","a"],
    ["b","b"],
    ["c","c"],
    ["d","d"],
    ["e","e"],
    ["f","f"],
    ["g","g"],
    ["h","h"],
    ["i","i"],
    ["j","j"],
    ["k","k"],
    ["l","l"],
    ["m","m"],
    ["n","n"],
    ["o","o"],

    ["p","p"],
    ["q","q"],
    ["r","r"],
    ["s","s"],
    ["t","t"],
    ["u","u"],
    ["v","v"],
    ["w","w"],
    ["x","x"],
    ["y","y"],
    ["z","z"],
    ["A","A"],
    ["B","B"],
    ["C","C"],
    ["D","D"],
    
    ["E","E"],
    ["F","F"],
    ["G","G"],
    ["H","H"],
    ["I","I"],
    ["J","J"],
    ["K","K"],
    ["L","L"],
    ["M","M"],
    ["N","N"],
    ["O","O"],
    ["P","P"],
    ["Q","Q"],
    ["R","R"],
    ["S","S"],

    ["T","T"],
    ["U","U"],
    ["V","V"],
    ["W","W"],
    ["X","X"],
    ["Z","Z"],
    ["0","0"],
    ["1","1"],
    ["2","2"],
    ["3","3"],
    ["4","4"],
    ["5","5"],
    ["6","6"],
    ["7","7"],
    ["8","8"],

    ["9","9"],
    ["~","asciitilde"],
    ["!","exclam"],
    ["@","at"],
    ["#","numbersign"],
    ["$","dollar"],
    ["%","percent"],
    ["^","asciicircum"],
    ["&","ampersand"],
    ["*","asterisk"],
    ["(","parenleft"],
    [")","parenright"],
    ["_","underscore"],
    ["+","plus"],
    ["{","braceleft"],

    ["}","braceright"],
    ["|","bar"],
    [":","colon"],
    ["\"","quotedbl"], # "
    ["<","less"],
    [">","greater"],
    ["?","question"],
    ["`","grave"],
    ["-","minus"],
    ["=","equal"],
    ["[","bracketleft"],
    ["]","bracketright"],
    ["\\","backslash"], # \
    [";","semicolon"],
    ["'","apostrophe"],

    [",","comma"],
    [".","period"],
    ["/","slash"],
    ["Space","space"],
    ["F1","F1"],
    ["F2","F2"],
    ["F3","F3"],
    ["F4","F4"], 
    ["F5","F5"],
    ["F6","F6"],
    ["F7","F7"],
    ["F8","F8"],
    ["F9","F9"],
    ["F10","F10"],
    ["F11","F11"]
]

# To update the label from the GPIO callbacks (which run on a different thread),
# we define a safe update function that uses `after()` to schedule GUI updates.
def safe_update(new_text):
    labelRE.config(text=new_text)


def update_label(new_text):
    # Use root.after to safely update the GUI from outside the main thread.
    root.after(0, safe_update, new_text)


# --- Callback Functions ---
def rotary_callback(channel):
    """Callback for rotary encoder rotation."""
    global indexKeyList, indexBank, indexVisibleKey

    global last_counter, counter, last_clk_state
    current_clk = GPIO.input(CLK_PIN)
    current_dt  = GPIO.input(DT_PIN)

    # When the state of CLK changes, determine rotation direction.
    # This simple method checks the state of DT relative to CLK.
    if current_clk != last_clk_state:
        # If DT is different from current CLK state, rotation is clockwise.
        if current_dt != current_clk:
            counter += 1
            update_label("R" + str(counter))
            rightFlag = True
        else:
            counter -= 1
            update_label("L" + str(counter))
            rightFlag = False

        # only actually do stuff if counter is even    
        if counter % 2 == 0: # counter is even
            labels_main[indexVisibleKey].config(bg="darkgray")
            if rightFlag: # go right
                if indexVisibleKey == sizeBank-1:
                    if indexBank == numBanks-1:
                        indexKeyList = 0
                        indexBank = 0
                    else:
                        indexKeyList += 1
                        indexBank += 1
                    indexVisibleKey = 0

                    # adjust bank of keys visible on top of main form
                    for i in range(sizeBank):
                        labels_main[i].config(text=KeyList[sizeBank*indexBank+i][0])
                else:
                    indexKeyList += 1
                  # indexBank unchanged
                    indexVisibleKey += 1
            else: # if righFlag == False (ie. go left)            
                if indexVisibleKey == 0:
                    if indexBank == 0:
                        indexKeyList = sizeKeyList-1
                        indexBank = numBanks-1
                    else:
                        indexKeyList -= 1
                        indexBank -= 1
                    indexVisibleKey = sizeBank-1
                    
                    # adjust bank of keys visible on top of main form
                    for i in range(sizeBank):
                        labels_main[i].config(text=KeyList[sizeBank*indexBank+i][0])
                else:
                    indexKeyList -= 1
                  # indexBank unchanged
                    indexVisibleKey -= 1
            labels_main[indexVisibleKey].config(bg="lightblue")
    last_clk_state = current_clk


# GPIO button 16 pressed
def on_KeypressButton_press(channel):
    sKey0 = KeyList[indexKeyList][0]
    sKey1 = KeyList[indexKeyList][1]
    if rootFlag:
        focused_widget = root.focus_get()
    else:
        focused_widget = setup.focus_get()
    focused_widget.event_generate(f"<Key-{sKey1}>")
    print(f"sKey0: <Key-{sKey1}> pressed")

# --- GPIO Event Detection ---
if GPIO:
    # Detect state changes on the CLK pin for rotational events.
    GPIO.add_event_detect(CLK_PIN, GPIO.BOTH, callback=rotary_callback, bouncetime=3)
    # Detect a falling edge on the switch pin for button press.
    GPIO.add_event_detect(SW_PIN, GPIO.FALLING, callback=on_KeypressButton_press, bouncetime=200)


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

# Create the full filepath to the list of ALL available radio stations
# as of 19/6/2025 have a file with 79468 radio stations of which 79336 are urls from the Commercial2 aggregator!
filename = 'AllRadioStations.csv'
allStations_filepath = os.path.join(script_dir, filename)
print(f'The file {allStations_filepath} stores csv table of all available radio stations')

# Create the full filepath to the list of saved station information from the text box
filename = 'StationLogs.txt'
StationLogs_filepath = os.path.join(script_dir, filename)
print(f'The file {StationLogs_filepath} stores txt of station logs')

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

# global graphic position variables
Ydown = 63
Ygap = 10;  Ygap2 = 110+Ydown; Ygap3 = 110+Ydown
Xgap = 560-70; Xgap2 = 560-70; Xgap3 = 560-70
Xprog = 300
X1 = 55 # 55 for RP version
Y1 = 30 # 30 for RP version

# global variables related to bluetooth and wifi
onBluetooth = True
currentPair = "No bluetooth speakers paired" # details of currently paired speakers
aPairable = [] # used to list bluetooth visible devices for pairing a speaker
numPairable = 0; # number of pairable devices visible
aWIFI = [] # used to list of visible wifi networks
numWIFI = 0; # number of visible wifi networks
sSSID = "NONE" # SSID of considered wifi network

# Create the full filepath to the bluetooth status text file
filename3 = 'bluetooth.txt'
filepath3 = os.path.join(script_dir, filename3)
print(f'The file {filepath3} stores bluetooth status before shutdown.')

# Create the full filepath to the pollflag status text file
filename4 = 'pollflag.txt'
filepath4 = os.path.join(script_dir, filename4)
print(f'The file {filepath4} stores the pollFlag when it is changed.')

# global variables for combobox selection indexes & button related
numButtons = 18
sizeButton = 62
combobox_index = -1
buttonIndex = -1
addFlag = False
iconSize = 160

eventFlag = True # if on_select & on_select2 are called from event
#stopFlag = False
selected_value = "INITIAL"
selected_value_last = "INITIAL"
selected_index = -1
startTime = time.time()
endTime = 0.0
refreshTime = 10.0 # seconds between updating station info
station = ""
needSleep = 4 # can be less on faster machines
pressButton = True # flag for how stream is started

# global variables for radio station calling functions
def SomeFunction(): pass    
StationName = ""
CountryCode = ""
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
oh2 = 0
nh2 = 0
nh3 = 0
ExtraWindowFlag = False
Streaming = True # if streaming is working

# other global variables
rootFlag = True # False indicates that you are in the secondary window
pollFlag = False # if true then poll website for program text and picture changes 
justDeletedFlag = False # if true then just deleted a station from the aStation[] list
stopLastStream = False # if true then stop current stream call
firstRun = True # if true then first run of a station stream

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
# There are 9 of them: Radio1 ... Radio7, Commercial1 & Commercial2. They are needed because the 
# websites used to stream individual radio stations can differ in their layout, but many are
# similar so can use the same code. Radio1...Radio7 are for the ABC stations, while Commercial1 &
# Commercial2 are for the commercial stations.

def Radio1(br,nNum,sPath,sClass,nType):
    if eventFlag:
        # determine file name for the station logo graphic
        logo = StationLogo + ".png"
        print(logo)

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
        label2.place(x=Xgap+X1, y=Ygap3+Y1)  # Adjust the position
    else:
        label2.place(x=Xgap+X1, y=Ygap2+Y1)  # Adjust the position
    
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
    scaled_image2 = image2.resize((width-X1, Xprog-X1))  # Adjust the size as needed
    photo2 = ImageTk.PhotoImage(scaled_image2)
    label2.config(image=photo2)
    label2.image = photo2  # Keep a reference to avoid garbage collection
    label2.place(x=Xgap3-(width-Xprog)+X1, y=Ygap2+Y1)  # Adjust the position
    
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
        # determine file name for the station logo graphic
        station = StationLogo
        first_occurrence = station.find("_")
        second_occurrence = station.find("_", first_occurrence+1)
        global station_short
        station_short = station[:second_occurrence]
        logo = station_short + ".png"
        print(logo)

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
    scaled_image2 = cropped_image2.resize((Xprog-X1, Xprog-Y1))  # Adjust the size as needed
    photo2 = ImageTk.PhotoImage(scaled_image2)
    label2.config(image=photo2)
    label2.image = photo2  # Keep a reference to avoid garbage collection
    if station_short == "ABC_Classic":
        label2.place(x=Xgap+X1, y=Ygap3+Y1)  # Adjust the position
    else:
        label2.place(x=Xgap+X1, y=Ygap2+Y1)  # Adjust the position

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
    scaled_image2 = cropped_image2.resize((Xprog-X1, Xprog-X1))  # Adjust the size as needed
    photo2 = ImageTk.PhotoImage(scaled_image2)
    label2.config(image=photo2)
    label2.image = photo2  # Keep a reference to avoid garbage collection
    label2.place(x=Xgap2+X1, y=Ygap2+Y1)  # Adjust the position
    
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
    scaled_image2 = cropped_image2.resize((Xprog-X1, Xprog-X1))  # Adjust the size as needed
    photo2 = ImageTk.PhotoImage(scaled_image2)
    label2.config(image=photo2)
    label2.image = photo2  # Keep a reference to avoid garbage collection
    label2.place(x=Xgap+X1, y=Ygap2+Y1)  # Adjust the position

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
    scaled_image2 = cropped_image2.resize((Xprog-X1, Xprog-X1))  # Adjust the size as needed
    photo2 = ImageTk.PhotoImage(scaled_image2)
    label2.config(image=photo2)
    label2.image = photo2  # Keep a reference to avoid garbage collection
    label2.place(x=Xgap+X1, y=Ygap3+Y1)  # Adjust the position
    
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
        # determine file name for the station logo graphic
        logo = StationLogo + ".png"
        print(logo)
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
    scaled_image2 = cropped_image2.resize((Xprog-X1, Xprog-X1))  # Adjust the size as needed
    photo2 = ImageTk.PhotoImage(scaled_image2)
    label2.config(image=photo2)
    label2.image = photo2  # Keep a reference to avoid garbage collection
    label2.place(x=Xgap+X1, y=Ygap3+Y1)  # Adjust the position
        
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
        # determine file name for the station logo graphic
        logo = StationLogo + ".png"
        print(logo)
        
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
    scaled_image2 = image2.resize((width-X1, Xprog-X1))  # Adjust the size as needed
    photo2 = ImageTk.PhotoImage(scaled_image2)
    label2.config(image=photo2)
    label2.image = photo2  # Keep a reference to avoid garbage collection
    label2.place(x=Xgap3-(width-Xprog)+X1, y=Ygap2+Y1)  # Adjust the position
 
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
    global img_url_g, oh, nh, tabNum, oh2, nh2, nh3, ExtraWindowFlag, Streaming, stopOnce
    print("")
    print("---- Commercial2() entered ---------------------------------------------")

    if eventFlag:
        # go to the station website
        br.get(refresh_http)
        time.sleep(2)
        br.get(sPath)
        time.sleep(needSleep) # bigger on slow machines
        print("---- ENTERED STATION WEBSITE ------------------------------------------")

    # always runs
    image_path_logo = pathImages + "/" + StationLogo + ".png"
    be = br.find_element(By.TAG_NAME, 'body')
    time.sleep(1)

    MaybeStreaming = False
    if eventFlag:
        # press button with virtual mouse to play stream
        window_size = br.get_window_size()
        winWidth = window_size['width']
        print(f"Window size: width = {window_size['width']}, height = {window_size['height']}")
        if nType == 0:
            widthPx = 250 #110
        else: # if nType == 1:
            widthPx = 250 #250    
        heightPx = 330
        print(f"Move size: width = {widthPx}, height = {heightPx}")
        actions = ActionChains(br)
        if CountryCode in {"ab","il"} :
            # makes sure that the click is on the right side of the screen
            # beacause we are dealing with countries that write right to left
            actions.move_by_offset(winWidth-widthPx, heightPx).click().perform()
            print(f"RTL country {CountryCode} detected, moving to the right side of the screen")
            pass
        else:    
            actions.move_by_offset(widthPx, heightPx).click().perform()
        time.sleep(16)

        # this is needed to dismiss any alert that may appear (unwanted login popup)
        try:
            alert = br.switch_to.alert  # Switch to alert if present
            print(f"Alert detected: {alert.text}")  # Print alert text for debugging
            alert.dismiss()  # Dismiss or accept as needed
        except NoAlertPresentException:
            print("No alert detected.")
        except UnexpectedAlertPresentException as e:
            print(f"Unexpected alert encountered: {e}")

        # identify whether streaming works using identifiers on a path element
        if len(br.window_handles) > 1:
            # this is a multiple windows case (old nType == 1 example)
            # another window is opened with button that actually starts the stream
            print(br.window_handles)  # Lists all open windows/tabs
            oh2 = br.window_handles[0]  # Original window handle
            nh2 = br.window_handles[1]  # New window handle a fter clicking the first button
            br.switch_to.window(nh2)  # Switch to the new window
            # press the button with virtual mouse to play stream
            actions = ActionChains(br)
            actions.move_by_offset(widthPx, heightPx).click().perform()
            time.sleep(6)

            # identify whether streaming works using identifiers on a path element
            # that display an error in playing graphic on the play button
            Streaming = True
            ht = br.page_source  # Get the full HTML content of the page
            soup = BeautifulSoup(ht, 'lxml')
            div_element = soup.find("div", id="play_pause_container")
            try:
                path_element = div_element.find("path")
                path_element_str = str(path_element)
                print(f"path element: {path_element_str}")
                try:
                    flagChar = path_element_str[10]
                    if flagChar == "4":
                        Streaming = False
                        print("<<< 2 window streaming is not working >>>")
                    ExtraWindowFlag = True
                except IndexError:
                    Streaming = False
                    MaybeStreaming = True
                    br.switch_to.window(nh2)
                    br.close()
                    br.switch_to.window(oh2)
                    print("<<< 2 window streaming might not be working - IndexError >>>")
                br.switch_to.window(oh2) # Switch back to the original window
            except AttributeError:
                # if the div_element is not found, it means the streaming is not working
                Streaming = False
                MaybeStreaming = True
                br.switch_to.window(nh2)
                br.close()
                br.switch_to.window(oh2)
                print("<<< Shut down second window >>>")    
        else:
            # identify whether streaming works using identifiers on a path element
            # that display an error in playing graphic on the play button
            Streaming = True
            ht = be.get_attribute('innerHTML')
            soup = BeautifulSoup(ht, 'lxml')
            div_element = soup.find("div", id="play_pause_container")
            path_element = div_element.find("path")
            path_element_str = str(path_element)
            print(f"path element: {path_element_str}")
            try:
                flagChar = path_element_str[10]
                if flagChar == "4":
                    Streaming = False
                    print("<<< Streaming is not working >>>")
            except IndexError:
                Streaming = False
                MaybeStreaming = True
                print("<<< Streaming might not be working - IndexError >>>")

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

    # always runs if Streaming and pollFlag are True. Get and then display station logo if one does not yet exist
    if Streaming:
        if pollFlag:
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
                    br.switch_to.new_window('Picture')
                    nh3 = br.current_window_handle
                    print("New window handle:", nh3)
                    br.switch_to.window(oh)
                    print(" At this point have an extra tab named [Picture] created" )
                    # At this point have an extra tab named [Picture] created - will be used next time Command2() is called!"
                else:
                    if tabNum == 0:
                        br.switch_to.window(nh3)
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
    except Exception as e: #NoSuchElementException:
        try:
            # if failed above try a slightly different path
            xpath = '/html/body/div[6]/div[1]/div[3]/div/div[1]/div[1]/div[3]/div/div[1]/div/img'
            img_element = be.find_element(By.XPATH, xpath)
            img_url = img_element.get_attribute("src")
            urllib.request.urlretrieve(img_url, image_path)
            print("=====> xpath #2")
        except Exception as e: #NoSuchElementException:
            try:
                # if failed above try a slightly different path
                xpath = '/html/body/div[6]/div[1]/div[2]/div/div[1]/div[1]/div[3]/div/div[1]/div/img'
                img_element = be.find_element(By.XPATH, xpath)
                img_url = img_element.get_attribute("src")
                urllib.request.urlretrieve(img_url, image_path)
                print("=====> xpath #3")
            except Exception as e: #NoSuchElementException:
                try:
                    # if failed above try a slightly different path
                    xpath = '/html/body/div[6]/div[1]/div[2]/div/div[1]/div[1]/div[3]/div/div[1]/div/a/img'
                    img_element = be.find_element(By.XPATH, xpath)
                    img_url = img_element.get_attribute("src")
                    urllib.request.urlretrieve(img_url, image_path)
                    print("=====> xpath #4")
                except Exception as e: #NoSuchElementException:
                    try:
                        # if failed above try a slightly different path
                        xpath = '/html/body/div[6]/div[1]/div[3]/div/div[1]/div[1]/div[3]/div/div[2]/div[1]/a/img'
                        img_element = be.find_element(By.XPATH, xpath)
                        img_url = img_element.get_attribute("src")
                        urllib.request.urlretrieve(img_url, image_path)
                        print("=====> xpath #5")
                    except Exception as e: #NoSuchElementException:
                        # failed to find image so display a blank image
                        foundImage = False
                        print("=====> xpath NONE")
        
    if foundImage:
        image = Image.open(image_path)
        width2, height2 = image.size;
        print(f"Pic width: {width2}, Pic height: {height2}")
        width = int(Xprog*width2/height2)
        scaled_image = image.resize((width-X1, Xprog-X1))  # Adjust the size as needed
        photo = ImageTk.PhotoImage(scaled_image)
        label2.config(image=photo)
        label2.image = photo  # Keep a reference to avoid garbage collection
        label2.place(x=Xgap3-(width-Xprog)+X1, y=Ygap2+Y1)  # Adjust the position
    else:    
        image_path = pathImages + "/Blank.png"
        image = Image.open(image_path)
        scaled_image = image.resize((Xprog-X1, Xprog-X1))  # Adjust the size as needed
        photo = ImageTk.PhotoImage(scaled_image)
        label2.config(image=photo)
        label2.image = photo  # Keep a reference to avoid garbage collection
        label2.place(x=Xgap+X1, y=Ygap3+Y1)  # Adjust the position

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
        if foundImage:
            fe1 = "*"+fe1+fe.get_text(separator="*", strip=True)
        else:
            fe1 = "*"+fe1+fe.get_text(separator="*", strip=True)+"*No program image"
    else:
        if foundImage:
            fe1 = "*"+fe1+"No program information"
        else:
            fe1 = "*"+fe1+"No program information and image"
    if not Streaming:
        if MaybeStreaming:
            if ExtraWindowFlag:
                fe1 = fe1 + "*"+"<<< Maybe 2 window streaming is not working >>>"
            else:
                fe1 = fe1 + "*"+"<<< Maybe streaming is not working >>>"
        else:
            if ExtraWindowFlag:
                fe1 = fe1 + "*"+"<<< 2 window streaming is not working >>>"
            else:
                fe1 = fe1 + "*"+"<<< Streaming is not working >>>"
    return fe1

# END ####################################################
# DEFINE VARIOUS CORE FUNCTIONS THAT STREAM RADIO STATIONS


# ALL STATIONS LOAD BLOCK START *********************************************

# 2D array of radio station information in [long name, station icon name, Streamer Function, nNum, sPath, sClass, nType] format
# where nNum, sPath, sClass & nType are arguments for the Radio1, Radio2, Radio3, Radio4, Radio5, Radio6,
# Radio7, Commercial1 & Commercial2 station calling functions. 
# Clearly this can be varied if you wish to listen to different stations
# Currently we Have all 83 ABC stations (included time shifted versions) and 186 in total.
# This 2D array used to be explicitly populated here:
# eg:
#    aStation = [
#        ["ABC Classic2","ABC_Classic2",Radio1,7,"https://www.abc.net.au/listen/live/classic2","",0],
#        ["ABC Jazz","ABC_Jazz",Radio1,7,"https://www.abc.net.au/listen/live/jazz","",0],
#        ["ABC triple j Hottest","ABC_triple_j_Hottest",Radio1,7,"https://www.abc.net.au/triplej/live/triplejhottest","",0],
#        ["ABC triple j Unearthed","ABC_triple_j_Unearthed",Radio1,7,"https://www.abc.net.au/triplej/live/unearthed","",0],
#        ["ABC Radio Australia","ABC_Radio_Australia",Radio1,7,"https://www.abc.net.au/radio-australia/live/","",0]
#   ]  

# Prepare a mapping from function names (as strings) to actual function objects
# this enables us to load the aStation list from a CSV file with the function names as strings
function_map = {
    'Radio1': Radio1,
    'Radio2': Radio2,
    'Radio3': Radio3,
    'Radio4': Radio4,
    'Radio5': Radio5,
    'Radio6': Radio6,
    'Radio7': Radio7,
    'Commercial1': Commercial1,
    'Commercial2': Commercial2
}

# load the aStation list from a CSV file allStations_filepath
aStation = []
with open(allStations_filepath, mode="r", newline="", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        row = [function_map.get(cell, cell) for cell in row]  # Replace function names with actual references
        row[3] = int(row[3]) if row[3].isdigit() else row[3]  # Convert column 3 to integer 
        row[6] = int(row[6]) if row[6].isdigit() else row[6]  # Convert column 6 to integer 
        aStation.append(row)
print("---- aStation loaded from file: " + allStations_filepath + " ----")

# ALL STATIONS LOAD BLOCK END ***********************************************


# 2D array of preset radio stations, in long name and index (to aStation[]) format.
# this is the default, but is actually copied from file at statup and saved to file on exit!
aStation2 = []
for i in range(numButtons):
    station = ["-- EMPTY " + str(i) +" --", -1]
    aStation2.append(station)


# after gui is initialised and we are running in the root thread
def after_GUI_started():
    # load pollFlag status file and use it to populate this global variable
    global pollFlag
    try:
        with open(filepath4, 'r') as file:
            int_pollFlag = int(file.read())
    except FileNotFoundError:
        int_pollFlag = 1 # set to True as default
        print(f'Error: The file {filepath4} does not exist.')
    if int_pollFlag==0:
        pollFlag = False
        if GPIO:
            pollStatusButton.config(text="Polling is OFF")
            pollStatusButton.config(bg="light coral")
        else:
            setupButton.config(text="OFF")
            setupButton.config(bg="light coral")
    else: #if int_pollFlag==1
        pollFlag = True
        if GPIO:
            pollStatusButton.config(text="Polling is ON")
            pollStatusButton.config(bg="light green")
        else:
            setupButton.config(text="ON")
            setupButton.config(bg="light green")
    print(f'pollFlag : {pollFlag}')

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
   
    if GPIO:    
        # load bluetooth status file and use it to populate global variables
        global onBluetooth
        global currentPair
        try:
            # read the two assumed lines from filepath3 & and strip newlines
            with open(filepath3, 'r') as file:
                lines = file.readlines()
            text_array = [line.strip() for line in lines]

            # determine the onBluetooth and currentPair global variables
            intMy = int(text_array[0])
            if intMy==0:
                onBluetooth = False
            else: #if intMy==1
                onBluetooth = True
            currentPair = text_array[1]
        except FileNotFoundError:
            print(f"File not found: {filepath3}")
            # create a bluetooth status file and give it default values
            onBluetooth = False; line1 = "0"  
            currentPair = "00:00:00:00:00:00 - NOTHING"; line2 = currentPair
            with open(filepath3, 'w') as file:
                file.write(line1 + '\n')  # Write the first line with a newline character
                file.write(line2 + '\n')  # Write the second line with a newline character
            print(f"Default file created {filepath3}")        
        print(f"onBluetooth: {str(onBluetooth)}")
        print(f"currentPair: {currentPair}")

        # update entries on setup form
        label3.config(text = f"Current pairing: {currentPair}")

        # restarts bluetooth interface if it was originally set to on.
        # if a previously paired set of bluetooth speakers is turned on when this runs this will
        # connect and play though them.
        if onBluetooth:
            connect_bluetooth()
            BTstatusButton.config(text="BT is ON")
            BTstatusButton.config(bg="light green")
        else: # onBluetooth==False
            subprocess_run("sudo systemctl disable bluetooth")                        
            subprocess_run("sudo systemctl stop bluetooth")                        
            BTstatusButton.config(text="BT is OFF")
            BTstatusButton.config(bg="light coral")



# Define a reverse lookup dictionary to convert function references back to strings
reverse_function_map = {v: k for k, v in function_map.items()}  # Assuming function_map is available


# do this when closing the window/app
def on_closing():
    print("\n---- on_closing() entered ---------------------------------------------")
    if GPIO:
        GPIO.cleanup()

    browser.quit() # close the WebDriver
    root.destroy() # destroy GUI   
    print("Closing the app...")


# do this when a radio station is selected from combobox
def on_select(event):
    print("\n---- on_select() entered ---------------------------------------------")
    global StationName, CountryCode, StationLogo, StationFunction, nNum, sPath, sClass, nType
    global ExtraWindowFlag, TimeNum, selectedStationIndex, selectedStationName, justDeletedFlag
    global stopLastStream, firstRun, Streaming 

    if stopLastStream:
        stopLastStream = False
        print("stopLastStream is True, so returning")
        print("---- on_select2() finished ---------------------------------------------\n")
        return

    # determine the timeInterval between calling on_select() or on_select2()
    global startTime, finishTime
    finishTime = time.time()
    timeInterval = finishTime-startTime
    timeIntervalStr = f"{timeInterval:.2f}"
    print(f"Time interval: {timeIntervalStr} seconds")
    
    startTime = time.time()
    print(f"Type: {event.type}")
    print(f"Widget: {event.widget}")
    print(f"Data: {event.data}")
    
    # prevent crashing if aStation is deleted
    if pollFlag:
        if justDeletedFlag:
            print("justDeletedFlag is True, so returning")
            justDeletedFlag = False;
            firstRun = True    
            print("---- on_select() finished ---------------------------------------------\n")
            return    

    # set various flags and parameters related to starting a station stream or accesing its website
    global eventFlag, stopFlag, selected_value, combobox_index, selected_value_last 
    if event.type=="Auto":

        if pollFlag:
            if not firstRun:
                stopLastStream = True
        firstRun = False

        if ExtraWindowFlag:
            # if the extra window is open, close it
            ExtraWindowFlag = False
            browser.switch_to.window(nh2)
            browser.close()
            browser.switch_to.window(oh2)
            print("Extra window closed")

        eventFlag = True # if on_select() is called by selecting a combobox entry
        selected_value_last = selected_value
        selected_value = custom_combo.get()
        combobox_index = custom_combo.current()
        print("selected_value:", selected_value)
        print("combobox_index:", combobox_index)

        # clear the icon and program graphic from the last selected station
        # to prevent confusion when loading a new station.
        image_path = pathImages + "/Blank.png"
        image = Image.open(image_path)
        scaled_image = image.resize((iconSize, iconSize))  # Adjust the size as needed
        photo = ImageTk.PhotoImage(scaled_image)
        label.config(image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection
        scaled_image2 = image.resize((Xprog-X1, Xprog-X1))  # Adjust the size as needed
        photo2 = ImageTk.PhotoImage(scaled_image2)
        label2.config(image=photo2)
        label2.image = photo2  # Keep a reference to avoid garbage collection
        label2.place(x=Xgap+X1, y=Ygap2+Y1)  # Adjust the position

    # extract all parameters for the selected radio station
    try:
        StationName = aStation[combobox_index][0]
        CountryCode = StationName[:2]
        print("CountryCode:", CountryCode)
    except IndexError:
        print(f"IndexError: {combobox_index} is out of range!")
        return
    StationLogo = aStation[combobox_index][1]
    StationFunction = aStation[combobox_index][2]
    nNum = aStation[combobox_index][3]
    sPath = aStation[combobox_index][4]
    sClass = aStation[combobox_index][5]
    nType = aStation[combobox_index][6]

    # setting stop flag, this prevents on_select() from running again
    # "mysterious" code due to timing issues
    if eventFlag:
        # inform user that a station is being started
        text = "Please be patient, the station *" +  StationName + "*is being started"
        text_rows = text.split("*")
        text_box.config(state=tk.NORMAL)
        text_box.delete('1.0', tk.END)
        for row in text_rows:
            text_box.insert(tk.END, row + "\n")
        text_box.config(state=tk.DISABLED)
        root.update_idletasks()

    print("eventFlag:",eventFlag)

    # run selected radio station stream, and return associated textual information 
    try:
        print("\nWill run:", StationFunction)
        text = StationFunction(browser,nNum,sPath,sClass,nType)
        text = sPath + "*" + StationName + "*" + text + "* *[" + timeIntervalStr + "]"
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
        
    except urllib.error.HTTPError as e:
        print(f"\nCrashed in on_select(), HTTPError: {e.code} - {e.reason}")
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

    # on_select() schedules itself to run in nominally refreshTime seconds.
    # this updates the program text and grapic while the selected radio station is streaming
    eventFlag = False
    if pollFlag:
        if Streaming:
            print("JUST ABOUT to schedule on_select to run in the future")
            root.after(int(refreshTime*1000), lambda: on_select(CustomEvent("Manual", custom_combo, "Manual from custom_combo")))
            print("DID SCHEDULE on_select to run in the future")
        else:
            print("Streaming==FALSE so DID NOT schedule on_select to run in the future")
            firstRun = True 
    else:
        print("pollFlag==False so DID NOT schedule on_select to run in the future")

    Streaming = True # always reset this to True
    print("---- on_select() finished ---------------------------------------------\n")



# do this when a radio station is selected via playlist buttons,
# similar in structure to on_select(), but the way the radio station stream is called differs.
def on_select2(event):
    print("\n---- on_select2() entered ---------------------------------------------")
    global StationName, CountryCode, StationLogo, StationFunction, nNum, sPath, sClass, nType  
    global ExtraWindowFlag, TimeNum, selectedStationIndex, selectedStationName, justDeletedFlag
    global stopLastStream, firstRun, Streaming

    if stopLastStream:
        stopLastStream = False
        print("stopLastStream is True, so returning")
        print("---- on_select2() finished ---------------------------------------------\n")
        return

    # determine the timeInterval between calling on_select()
    global startTime, finishTime
    finishTime = time.time()
    timeInterval = finishTime-startTime
    timeIntervalStr = f"{timeInterval:.2f}"
    print(f"Time interval: {timeIntervalStr} seconds")

    startTime = time.time()
    print(f"Type: {event.type}")
    print(f"Widget: {event.widget}")
    print(f"Data: {event.data}")

    # prevent crashing if aStation is deleted
    if pollFlag:
        if justDeletedFlag:
            print("justDeletedFlag is True, so returning")
            justDeletedFlag = False;
            firstRun = True    
            print("---- on_select2() finished ---------------------------------------------\n")
            return    

    global eventFlag, stopFlag, selected_value, selected_index, selected_value_last
    if event.type=="Auto":

        if pollFlag:
            if not firstRun:
                stopLastStream = True
        firstRun = False        

        if ExtraWindowFlag:
            # if the extra window is open, close it
            ExtraWindowFlag = False
            browser.switch_to.window(nh2)
            browser.close()
            browser.switch_to.window(oh2)
            print("Extra window closed")

        eventFlag = True
        selected_value_last = selected_value
        selected_value = aStation2[buttonIndex][0]
        selected_index = int(aStation2[buttonIndex][1])
        print("selected_value:",selected_value)
        print("selected_index:",selected_index)

        # clear the icon and program graphic from the last selected station
        # to prevent confusion when loading a new station.
        image_path = pathImages + "/Blank.png"
        image = Image.open(image_path)
        scaled_image = image.resize((iconSize, iconSize))  # Adjust the size as needed
        photo = ImageTk.PhotoImage(scaled_image)
        label.config(image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection
        scaled_image2 = image.resize((Xprog-X1, Xprog-X1))  # Adjust the size as needed
        photo2 = ImageTk.PhotoImage(scaled_image2)
        label2.config(image=photo2)
        label2.image = photo2  # Keep a reference to avoid garbage collection
        label2.place(x=Xgap+X1, y=Ygap2+Y1)  # Adjust the position

    # extract all parameters for the selected radio station
    try:
        StationName = aStation[selected_index][0]
        CountryCode = StationName[:2]
        print("CountryCode:", CountryCode)
    except IndexError:
        print(f"IndexError: {selected_index} is out of range!")
        return
    StationLogo = aStation[selected_index][1]
    StationFunction = aStation[selected_index][2]
    nNum = aStation[selected_index][3]
    sPath = aStation[selected_index][4]
    sClass = aStation[selected_index][5]
    nType = aStation[selected_index][6]

    # setting stop flag, this prevents on_select2 from running again
    # "mysterious" code due to timing issues
    if eventFlag:
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

    print("eventFlag:",eventFlag)

    print("Selected:", selected_value)
    print("Index:", selected_index)
    print("Button index:", buttonIndex)

    # run selected radio station stream, and return associated textual information 
    if selected_index != -1:
        try:
            print("\nWill run:", StationFunction)
            text = StationFunction(browser,nNum,sPath,sClass,nType)
            text = sPath + "*" + StationName + "*" + text + "* *[" + timeIntervalStr + "]"
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
                custom_combo.set(StationName)
                custom_combo.focus_set()
                custom_combo.selection_clear()
                buttons[buttonIndex].focus_set()
            
            eventFlag = False
            if pollFlag:
                if Streaming:
                    print("JUST ABOUT to schedule on_select2 to run in the future")
                    root.after(int(refreshTime*1000), lambda: on_select2(CustomEvent("Manual", buttons[buttonIndex], "Manual from buttons")))
                    print("DID SCHEDULE on_select2 to run in the future")
                else:    
                    print("Streaming==FALSE so DID NOT schedule on_select2 to run in the future")
                    firstRun = True
            else:    
                print("pollFlag==False so DID NOT schedule on_select2 to run in the future")

        except urllib.error.HTTPError as e:
            print(f"\nCrashed in on_select2(), HTTPError: {e.code} - {e.reason}")

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
        scaled_image2 = image.resize((Xprog-X1, Xprog-X1))  # Adjust the size as needed
        photo2 = ImageTk.PhotoImage(scaled_image2)
        label2.config(image=photo2)
        label2.image = photo2  # Keep a reference to avoid garbage collection
        label2.place(x=Xgap+X1, y=Ygap2+Y1)  # Adjust the position
        print("BLANK END")
        print("")

        eventFlag = False
        if pollFlag:
            if Streaming:
                print("JUST ABOUT to schedule on_select2 to run for NO station in the future")
                root.after(int(refreshTime*1000), lambda: on_select2(CustomEvent("Manual", buttons[buttonIndex], "Manual from buttons")))
                print("DID SCHEDULE on_select2 to run in the future")
            else:    
                print("Streaming==FALSE so DID NOT schedule on_select2 to run in the future")
                firstRun = True
        else:    
            print("pollFlag==False so DID NOT schedule on_select2 to run in the future")

    if event.type=="Auto":
        # save number of last playlist radio station that was played (0,...,9), ie buttonIndex.
        with open(filepath, 'w') as file:
            file.write(str(buttonIndex))

    Streaming = True # always reset this to True
    print("---- on_select2() finished ---------------------------------------------\n")



# called when playlist button i is in focus and the Enter key is pressed.
# visually simulates a physical button press and initiates the station stream by
# calling the on_select2() function
def on_button_press(event, i):
    buttons[i].config(relief="sunken", bg="lightgray")  # Simulate button press
    buttons[i].update_idletasks()  # Force update
    time.sleep(1) 
    buttons[i].config(relief="raised", bg="gray90")  # Simulate button press
    buttons[i].update_idletasks()  # Force update

    global buttonFlag;  buttonFlag = True
    global buttonIndex; buttonIndex = i
    print(f"\nPlaylist button {buttonIndex} pressed")
    global justDeletedFlag
    copyFlag = justDeletedFlag
    on_select2(CustomEvent("Auto", buttons[buttonIndex], "Auto from Enter key"))    
    if copyFlag:
        # forces pressing this playlist button twice if necessary
        print(f"Playlist button {buttonIndex} pressed AGAIN")
        on_select2(CustomEvent("Auto", buttons[buttonIndex], "Auto from Enter key"))    
    print(f"COMPLETED pressing the Playlist button {buttonIndex}")



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
        #global PollFlag; pollFlag = True
        on_select2(CustomEvent("Auto", buttons[buttonIndex], "Auto from Delete key"))

        # save the playlist to file
        with open(filepath2, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(aStation2)
    else:        
        print("No station to delete")    


# called when playlist button i is in focus and the Insert key is pressed.
# Inserts the last station played from the combobox into the playlist.
# If the playlist button is already occupied, the station is replaced.
# In particular it displays the station logo on the button and links it to the station.
def on_button_insert(event, i):
    global buttonIndex; buttonIndex = i

    # change aStation2[] list to reflect the addition
    global combobox_index, aStation2
    combobox_index = custom_combo.current()
    print(f"combobox_index: {combobox_index}")
    if (combobox_index != -1):
        print("station added")    
        global addFlag
        addFlag = True # so can get and save icon for playlist button

        lastStation = aStation[combobox_index][0]
        aStation2[buttonIndex][0] = lastStation
        aStation2[buttonIndex][1] = combobox_index
        print("Adding station:", lastStation, "with combobox index:", combobox_index)

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
        with open(filepath2, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(aStation2)
    else:
        print("No station added")    
    print("")


# called when a playlist button receives focus.
# visually indicates that the button has focus and
# saves the buttonIndex in a global variable
def on_focus(event, i):
    buttons[i].config(relief="sunken", bg="darkgray")  # Simulate button press
    buttons[i].update_idletasks()  # Force update


# called when a playlist button loses focus.
# returns the button to a visually "unfocused" state. 
def on_focus_out(event, i):
    buttons[i].config(relief="raised", bg="gray90")  # Simulate button press
    buttons[i].update_idletasks()  # Force update


# called when wifiPassword Entry widget receives focus.
def on_focus_wifiPassword(event):
    style.map("Focused.TEntry",fieldbackground=[("focus", "lightblue")])
    wifiPassword.event_generate("<Right>")
    event.widget.update_idletasks()


# called when wifiPassword Entry widget loses focus.
def on_focus_out_wifiPassword(event):
    style.map("Focused.TEntry",fieldbackground=[("!focus", "white")])    
    event.widget.update_idletasks()


# show the setup form (over the top of the main window)
# Only in RP5B version. Poll status toggle button otherwise  
def show_setup_form(event):
    rootFlag = False
    setup.deiconify()
    mainButton.focus_set()
    print(rootFlag)


# show the root form back over the setup form
def show_root_form(event):
    rootFlag = True
    setup.withdraw()
    setupButton.focus_set()
    print(rootFlag)


# Helper function for subprocess run
def subprocess_run(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    time.sleep(2)
    returnCode = result.returncode
    if returnCode == 0: print(f"Command '{command}' succeeded")
    else: print(f"Command '{command}' FAILED")
    return returnCode    


# Helper function to execute a bluetoothctl command
def run_bluetoothctl_command(command):
    process = subprocess.Popen(['sudo','bluetoothctl'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    stdout, _ = process.communicate(command)
    return stdout


# if BlueTooth is off then restart interface, If it is on then turn it off.
# Also appropriately adjust the onBluetooth flag in thet bluetooth.txt config file
def toggle_bluetooth(event):
    global onBluetooth
    sText = BTstatusButton.cget("text")
    if sText=="BT ON":
        BTstatusButton.config(text="BT OFF")
        BTstatusButton.config(bg="light coral")
        onBluetooth = False; line1 = "0"
        subprocess_run("sudo systemctl disable bluetooth")                        
        subprocess_run("sudo systemctl stop bluetooth")                        
    else: #if sText=="BT OFF"
        BTstatusButton.config(text="BT ON")
        BTstatusButton.config(bg="light green")
        onBluetooth = True; line1 = "1"
        connect_bluetooth()
    label4.config(text=f"")
    with open(filepath3, 'w') as file:
        file.write(line1 + '\n')
        file.write(currentPair + '\n')
    print(f"updated: {filepath3}")        


# if pollFlag is True then set it to False, and vica-versa.
# Also appropriately adjust the pollflag.txt config file
# behaves differently on whether Linux or WIN varsion
# as determined by the GPIO global variable
def toggle_pollStatus(event):
    global pollFlag
    if GPIO:
        sText = pollStatusButton.cget("text")
        if sText=="Polling is ON":
            pollStatusButton.config(text="Polling is OFF")
            pollStatusButton.config(bg="light coral")
            pollFlag = False; line = "0"
        else: #if sText=="Polling is OFF"
            pollStatusButton.config(text="Polling is ON")
            pollStatusButton.config(bg="light green")
            firstRun = True
            pollFlag = True; line = "1"
    else:    
        sText = setupButton.cget("text")
        if sText=="ON":
            setupButton.config(text="OFF")
            setupButton.config(bg="light coral")
            pollFlag = False; line = "0"
        else: #if sText=="OFF"
            setupButton.config(text="ON")
            setupButton.config(bg="light green")
            firstRun = True
            pollFlag = True; line = "1"
    with open(filepath4, 'w') as file:
        file.write(line + '\n')
    print(f"toggling poll status in file: {filepath4}")


def _connect_bluetooth(event):
    if onBluetooth:
        print("CONNECTING FOR REAL")
        returnCode = connect_bluetooth()
        if returnCode != 0:
            label4.config(text=f"FAILED")
        else:
            label4.config(text=f"")
    else:    
        print("NOT CONNECTING")
        label4.config(text=f"TURN ON BT")


# Press [CONNECT] button to restart bluetooth interface.
# if a previously paired set of bluetooth speakers is turned and then this function is run
# if will connect and play though them even if Bluetootch was originally turned off  
def connect_bluetooth():
    mac_address = currentPair.split(" - ")[0]
    device_name = currentPair.split(" - ")[1]
    print(f"Restarting Bluetooth interface with currently paired device: {device_name}")
    subprocess_run("sudo systemctl enable bluetooth")                        
    subprocess_run("sudo systemctl start bluetooth")
    subprocess_run("rfkill unblock bluetooth")
    returnCode = subprocess_run(f"sudo bluetoothctl connect {mac_address}")
    return returnCode


# pres Enter key in [combobox_bt]
# Pair and connect to the current selection from the bluetooth combobox
def on_select_bluetooth(event):
    try:
        print("ACTUAL PAIRING STARTS HERE")
        label3.config(text=f"WAITING TO PAIR - please be patient!")
        setup.update_idletasks()
        selected_device = custom_combo_bt.get()
        mac_address = selected_device.split(" - ")[0]
        device_name = selected_device.split(" - ")[1]
    except IndexError as e:
        print("SELECTION DOES NOT EXIST - CANNOT PAIR")
        label3.config(text=f"NOT A VALID SELECTION - TRY AGAIN?")
        setup.update_idletasks()
        root.after(100,lambda: mainButton.focus_set()) 
        return # all code below is ignored
        
    loop=0
    while True:
        # does the actual pairing to selected mac address - need previous actions else not connectable?   
        process = subprocess.Popen(['sudo','bluetoothctl'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        process.stdin.write("discoverable on\n")
        process.stdin.flush()
        time.sleep(3)
        process.stdin.write("scan on\n")
        process.stdin.flush()
        time.sleep(15)
        process.stdin.write("scan off\n")
        process.stdin.flush()
        time.sleep(3)
        process.stdin.write(f"pair {mac_address}\n")
        process.stdin.flush()
        time.sleep(3)
        process.stdin.write(f"connect {mac_address}\n")
        process.stdin.flush()
        time.sleep(5)
        output, _ = process.communicate()
        process.stdin.close()  # Close the input stream
        process.terminate()    # Politely terminate the process
        process.wait()         # Ensure the process finishes
        print("**** OUTPUT START ******")
        print(output)
        print("**** OUTPUT FINISH *****")
        position = output.find("Connection successful")
        loop += 1
        if position == -1 and loop < 3 :
            print(f"Failed to Pair try {loop}")
        else:
            break
        
    if position == -1:
        print("GAVE UP TRYING TO PAIR - TRY AGAIN!")
        label3.config(text=f"GAVE UP TRYING TO PAIR - TRY AGAIN?")
    else:
        print("SUCESSFULLY PAIRED AND CONNECTED!")
        label3.config(text=f"Paired with: {mac_address} - {device_name}")

    # update the bluetooth.txt config file
    global onBluetooth
    if position == -1:
        if onBluetooth:
            line1 = "1"
        else:
            line1 = "0"
        line2 = "00:00:00:00:00:00 - NOTHING"
    else:    
        onBluetooth = True; line1 = "1"  
        global currentPair; currentPair= f"{mac_address} - {device_name}"; line2 = currentPair
        BTstatusButton.config(text="BT ON")
    with open(filepath3, 'w') as file:
        file.write(line1 + '\n')  # Write the first line with a newline character
        file.write(line2 + '\n')  # Write the second line with a newline character
    print(f"Default file created {filepath3}")
    root.after(100,lambda: mainButton.focus_set()) 


# when [SEE BT DEVICES] button pressed.
# populates the combobox_bt with the pairable devices, but first removes all
# previously paired ones which here should be just one.
def pair_bluetooth(event):
    print("Start Bluetooth PAIRING")
    label6.config(text="WAITING - please be patient!")
    setup.update_idletasks()
    
    # restarts bluetooth so that we can remove all paired devices
    subprocess_run("rfkill unblock bluetooth")
    subprocess_run("sudo systemctl restart bluetooth")
    
    # remove all paired devices
    output = run_bluetoothctl_command("devices\n")
    for line in output.splitlines():
        if "Device" in line:
            device_mac = line.split()[1]
            run_bluetoothctl_command(f"remove {device_mac}\n")
            print(f"Removed device: {device_mac}")

    # create a list aPairable of devices available for possibly pairing to   
    process = subprocess.Popen(['sudo','bluetoothctl'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    process.stdin.write("discoverable on\n")
    process.stdin.flush()
    time.sleep(2)
    process.stdin.write("scan on\n")
    process.stdin.flush()
    time.sleep(20)
    process.stdin.write("scan off\n")
    process.stdin.flush()
    time.sleep(2)
    output, _ = process.communicate()
    process.stdin.close()  # Close the input stream
    process.terminate()    # Politely terminate the process
    process.wait()         # Ensure the process finishes

    process = subprocess.Popen(['sudo','bluetoothctl'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    process.stdin.write("devices\n")
    process.stdin.flush()
    time.sleep(5)
    output, _ = process.communicate()
    process.stdin.close()  # Close the input stream
    process.terminate()    # Politely terminate the process
    process.wait()         # Ensure the process finishes

    global aPairable; aPairable = []
    for line in output.splitlines():
        if "Device" in line:
            line = line.replace("Device ","")
            device_mac, device_name = line.split(" ", 1)
            aPairable.append(f"{device_mac} - {device_name}")
            print(f"device mac: {device_mac}, name: {device_name}")
    print("have extracted discoverable devices into aPairable")

    custom_combo_bt.set_values(aPairable)
    global numPairable; numPairable = len(aPairable)
    if numPairable==0:
        label3.config(text="No Bluetooth devices found")
    else:    
        custom_combo_bt.current(0)
        custom_combo_bt.entry.focus_set()
        if len(aPairable)==1:
            label3.config(text=f"Found 1 device")
        else:
            label3.config(text=f"Found {numPairable} devices")
    print(f"Found {numPairable} device(s)\n")
    label6.config(text="")
   

# when [custom_combo_wifi] selected
# Use current selection from the combobox to connect to the internet
def on_select_wifi(event):
    global sSSID
    try:
        print("ACTUAL WIFI CONNECTING STARTS HERE")
        label5.config(text=f"WAITING TO CONNECT - please be patient!")
        setup.update_idletasks()
        selected_wifi = custom_combo_wifi.get()
        sSSID = selected_wifi.split(" - ")[0]
        sQuality = selected_wifi.split(" - ")[1]
    except IndexError as e:
        print("SELECTION DOES NOT EXIST - CANNOT PAIR")
        label5.config(text=f"NOT A VALID SELECTION - TRY AGAIN?")
        setup.update_idletasks()
        root.after(100,lambda: mainButton.focus_set()) 
        return # all code below is ignored

    # assumes credentials for this network have previously been stored, ie. its
    # password & SSID is known and it has previously been connected to
    command = f'nmcli con up id "{sSSID}"'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    time.sleep(2)
    returnCode = result.returncode
    if returnCode == 0:      # success
        print(f"Command '{command}' succeeded")
        label5.config(text=f"Connected to: {sSSID} - wait for focus")

        # need to reload last streaming station
        #global PollFlag; pollFlag=True
        on_select2(CustomEvent("Auto", buttons[buttonIndex], "Auto from GUI start"))
        root.after(100,lambda: mainButton.focus_set()) 
    else: # fail, so try with password
        print(f"Command '{command}' FAILED, need password")
        label5.config(text=f"NEED password for {sSSID}")
        root.after(100,lambda: wifiPassword.focus_set()) 


# when the Enter key is pressed after text has been keyed into the
# [wifiPassword] Entry widget  
def process_wifiPassword(event):
    global sSSID
    sPassword = wifiPassword.get()
    print(f"You entered: {sPassword}")
    wifiPassword.delete(0, tk.END)  # Clears this widget

    loop=0
    while True:
        command = f'nmcli dev wifi connect "{sSSID}" password "{sPassword}"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if (loop==3) or (result.returncode==0):
            # give up or success
            break
        else: # fail, can try with a new password or not
            loop += 1
            print(f"Attempt {loop}: FAILED")
            
    if loop==3:
        label5.config(text=f"Failed connect for {sSSID} - try again?")
        root.after(100,lambda: wifiPassword.focus_set())
    else:
        print(f"Command '{command}' succeeded")
        label5.config(text=f"Connected to: {sSSID} - wait for focus")
      # need to reload last streaming station
        #global PollFlag; pollFlag=True
        on_select2(CustomEvent("Auto", buttons[buttonIndex], "Auto from GUI start"))
        root.after(100,lambda: mainButton.focus_set())


# when [SEE WIFI] button pressed.
# populates the combobox_wifi with the possible wifi connections
def find_wifi(event):
    print("Start WIFI connecting")
    label7.config(text="WAITING - please be patient!")
    setup.update_idletasks()

    command = "sudo iwlist wlan0 scan | grep -E 'SSID|Signal'"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    time.sleep(2)
    returnCode = result.returncode
    if returnCode == 0: print(f"Command '{command}' succeeded")
    else: print(f"Command '{command}' FAILED")

    print(result.stdout)
    sLines = (result.stdout).splitlines()

    global aWIFI; aWIFI = []
    sQuality = ""; sSSID = ""
    for line in sLines:
        if "Quality" in line:
            match = re.search(r'=(.+?)/', line)
            sQuality = match.group(1) 
            sQuality = f"Q{sQuality}"
        elif "ESSID" in line:
            match = re.search(r'"([^"]*)"', line)
            sSSID = match.group(1)
            if sSSID != "":
                aWIFI.append(f"{sSSID} - {sQuality}")
                print(f"{sSSID} - {sQuality}")
    print("have extracted visible wifi networks into aWIFI")

    custom_combo_wifi.set_values(aWIFI)
    global numWIFI; numWIFI = len(aWIFI)
    if numWIFI==0:
        label5.config(text="No visible wifi networks found")
    else:    
        custom_combo_wifi.current(0)
        custom_combo_wifi.entry.focus_set()
        if numWIFI==1:
            label5.config(text=f"Found 1 visible wifi network")
        else:
            label5.config(text=f"Found {numWIFI} visible wifi networks")
    print(f"Found {numWIFI} visible wifi network(s)\n")
    label7.config(text="")


def on_focus_dostuff(event):
    widget = event.widget
    widget_name = widget.winfo_name()
    print(f"{widget_name} got focus!")
    if GPIO:
        widget.config(bg="lightblue")
    elif (widget_name == "setupButton"):
        pass
    else:
        widget.config(bg="lightblue")


def on_focus_out_dostuff(event):
    widget = event.widget
    widget_name = widget.winfo_name()
    print(f"{widget_name} lost focus!")
    if GPIO:
        widget.config(bg="gray90")
    elif (widget_name == "setupButton"):
        pass
    else:
        widget.config(bg="gray90")


def random_button_pressed(event):
    print("\n*** REAL [RND] BUTTON PRESSED ***")
    numStations = len(aStation)
    randomStation = random.randint(0, numStations - 1)
    custom_combo.set(aStation[randomStation][0])  # Set the combobox to a random station
    custom_combo.on_return(None) # and trigger the on_select function (as if you had pressed Enter in the combobox)  )

    print(f"Number of stations: {numStations}")
    print(f"Randomly selected station index: {randomStation}")
    print(f"This function's name is: {inspect.currentframe().f_code.co_name}")
    print(f"Event argument: {event}")
    print("\n*** COMPLETED - REAL [RND] BUTTON PRESSED ***\n")


# The actual delete action undertaken when the Delete key is pressed
# when the [DEL] button has focus
def delete_key_pressed(event):
    print("\n*** [DEL] BUTTON PRESSED ***")
    global ExtraWindowFlag
    global StationName, justDeletedFlag
    global aStation, aStation2
    delIndex = custom_combo.current()  # Get the current index of the combobox

    print(f"Deleting station at index: {delIndex}")
    StationName = aStation[delIndex][0]  # Get the station name to be deleted
    if pollFlag:
        # to prevent on_select or on_select2 from fully running again (but with correct processing!)
        justDeletedFlag = True

    # Remove the station from the aStation list & save the modifed list back to a csv file
    del aStation[delIndex]
    print("---- Saving the modified aStation list to file: " + allStations_filepath + " ----")
    with open(allStations_filepath, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        for row in aStation:
            row = [reverse_function_map.get(cell, cell) for cell in row]  # Convert function references to strings
            writer.writerow(row)  # Write row to CSV
    print("---- COMPLETED Saving the modified aStation list file")
 
    # Update the combobox values (so the deleted station is no longer shown)
    global aStringArray
    aStringArray = []
    for element in aStation:
        aStringArray.append(element[0])
    custom_combo.set_values(aStringArray)
    custom_combo.current(0)

    # update the playlist to reflect the deletion (if necessary)
    changeFlag = False
    for i in range(numButtons):
        ix = int(aStation2[i][1]) # int to str conversion issues
        print(f"Checking button {i} for deletion, index: {ix}")
        if ix > delIndex:
            # decrement the index of all stations greater than delIndex
            ix -= 1
            aStation2[i][1] = ix
            changeFlag = True                
        if ix == delIndex:
            # if the station is the one deleted, set it to empty
            aStation2[i][0] = "-- EMPTY " + str(i) + " --"
            aStation2[i][1] = -1     
            changeFlag = True                

            # get blank station logo
            image_path = pathImages + "/Blank.png"
            image = Image.open(image_path)

            # saving blank button icon
            buttonImagePath = pathImages + "/button" + str(buttonIndex) + ".png"
            image.save(buttonImagePath)

            # now need to update the icon on the buttonIndex button
            image_resized = image.resize((sizeButton-5,sizeButton-5), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image_resized)
            buttons[i].config(image=photo)
            buttons[i].image = photo
            buttons[i].update_idletasks()

    # if modified save the playlist to file         
    if changeFlag:
        with open(filepath2, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(aStation2)

    # properly shut down the deleted station
    if ExtraWindowFlag:
        # if the extra window is open, close it
        ExtraWindowFlag = False
        browser.switch_to.window(nh2)
        browser.close()
        browser.switch_to.window(oh2)
        print("Extra window closed")

    # There is no station streaming so refresh the browser 
    # and clear icon and program image  and display the "No station playing" message
    # in the text box.
    browser.get(refresh_http)
    time.sleep(2)
    text = "Just deleted the radio station:*" + StationName + "* *NO STATION CURRENTLY PLAYING!"
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
    scaled_image2 = image.resize((Xprog-X1, Xprog-X1))  # Adjust the size as needed
    photo2 = ImageTk.PhotoImage(scaled_image2)
    label2.config(image=photo2)
    label2.image = photo2  # Keep a reference to avoid garbage collection
    label2.place(x=Xgap+X1, y=Ygap2+Y1)  # Adjust the position
    print("*** COMPLETED - [DEL] BUTTON PRESSED ***\n")


def save_button_pressed(event):
    print("\n*** [SAVE] BUTTON PRESSED ***")
    print(f"This function's name is: {inspect.currentframe().f_code.co_name}")
    print(f"Event argument: {event}")
    text_content = text_box.get("1.0", "end-1c")  # Get all text from the textbox
    with open(StationLogs_filepath, "a", encoding="utf-8") as file:
        file.write("*******************************************************\n")
        file.write(f"--- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---\n")
        file.write(text_content)
        file.write("\n")
    print("*** COMPLETED - [SAVE] BUTTON PRESSED ***\n")
     

# Thanks to Copilot (Think Deeper) AI 
class CustomCombobox(tk.Frame):
    def __init__(self, master, values, name, visible_items=5, width=25, *args, **kwargs):
        """
        Initialize a custom combobox.
        
        Parameters:
            master      : Parent widget.
            values      : List of item strings.
            name        : string used to identify actual created object to distinguish function calls
            visible_items: Number of items visible in the dropdown.
            width       : Width of the entry and dropdown fields (in average characters).            
        """
        super().__init__(master, *args, **kwargs)
        self.values = values
        self.name = name # Assign a unique name to the instance
        self.visible_items = visible_items
        self.selected_index = 0  # default selection index
        self.width = width  # Store the width

        # Variable for the displayed item.
        self.var = tk.StringVar(value=self.values[self.selected_index])
        
        # This entry acts as the combobox display field.
        self.entry = tk.Entry(self, textvariable=self.var, width=self.width)
        self.entry.pack(fill="x", expand=True)

        # Store the original background color.
        self.default_bg = self.entry.cget("background")  

        # Initialize the dropdown-related attributes.
        self.dropdown = None
        self.listbox = None  # Make sure self.listbox always exists

        # Bind key events on the entry.
        self.entry.bind("<Down>", self.on_down)
        self.entry.bind("<Up>", self.on_up)
        self.entry.bind("<Return>", self.on_return)
        self.entry.bind("<Escape>", self.on_escape)
        self.entry.bind("<FocusIn>", self.on_focus_combobox)   # Change background on focus in
        self.entry.bind("<FocusOut>", self.on_focus_out)   # Restore background on focus out

    def set_values(self, new_values):
        """
        Updates the list of options in the combobox.
        """
        self.values = new_values  # Update the internal values list

        # If the dropdown is already open, update the Listbox.
        if self.dropdown and self.listbox:
            self.listbox.delete(0, "end")  # Clear the current items
            for value in self.values:
                self.listbox.insert("end", value)
        
        # Reset the current selection if necessary.
        if self.values:
            self.selected_index = 0
            self.var.set(self.values[0])  # Set the first item as the default
        else:
            self.selected_index = -1
            self.var.set("")  # Clear the display if there are no values

    def get(self):
        """
        Returns the current value from the combobox.
        Now you can call custom_combo.get() to retrieve the text.
        """
        return self.var.get()

    def set(self, value):
        """
        Sets the combobox display to the provided value.
        If the value exists in the list of options, update the selected index
        and, if the dropdown is open, the Listbox selection.
        """
        if value in self.values:
            self.selected_index = self.values.index(value)
            self.var.set(self.values[self.selected_index])
            if self.dropdown:
                self.listbox.select_clear(0, "end")
                self.listbox.select_set(self.selected_index)
                self.listbox.activate(self.selected_index)
                self.listbox.see(self.selected_index)
        else:
            # If the provided value is not in the option list,
            # simply update the display text.
            self.var.set(value)

    def current(self, index=None):
        """
        If no index is provided, return the current selection index.
        If an index is provided, update the current selection to that index.
        """
        if index is None:
            return self.selected_index
        else:
            if index < 0 or index >= len(self.values):
                raise IndexError("Selection index out of range.")
            self.selected_index = index
            self.var.set(self.values[index])
            # If the dropdown is open, update the Listbox selection.
            if self.dropdown:
                self.listbox.select_clear(0, "end")
                self.listbox.select_set(index)
                self.listbox.activate(index)
                self.listbox.see(index)
            return index

    def open_dropdown(self):
        """Opens the dropdown Toplevel with a Listbox of items."""
        if self.dropdown:
            return  # Already open

        # Create a borderless Toplevel widget to act as the dropdown
        self.dropdown = tk.Toplevel(self)
        self.dropdown.wm_overrideredirect(True)  # Remove window decorations
        
        # Position the dropdown right below the entry widget.
        x = self.entry.winfo_rootx()
        y = self.entry.winfo_rooty() + self.entry.winfo_height()
        self.dropdown.wm_geometry(f"+{x}+{y}")

        # Create a Listbox to display items.
        self.listbox = tk.Listbox(self.dropdown, height=self.visible_items, width=self.width)
        self.listbox.pack(side="left", fill="both")

        # If there are more items than visible, add a vertical scrollbar.
        if len(self.values) > self.visible_items:
            self.scrollbar = tk.Scrollbar(self.dropdown, orient="vertical", command=self.listbox.yview)
            self.scrollbar.pack(side="right", fill="y")
            self.listbox.configure(yscrollcommand=self.scrollbar.set)

        # Load the values into the listbox.
        for item in self.values:
            self.listbox.insert("end", item)

        # Set the current selection in the listbox to the saved index.
        self.listbox.select_set(self.selected_index)
        self.listbox.activate(self.selected_index)
        self.listbox.see(self.selected_index)

        # Bind mouse click selection in the listbox.
        self.listbox.bind("<ButtonRelease-1>", self.on_listbox_click)

    def close_dropdown(self):
        """Destroys the dropdown if it exists."""
        if self.dropdown:
            self.dropdown.destroy()
            self.dropdown = None

    def on_down(self, event):
        """
        If the dropdown is closed, open it.
        Otherwise, move selection down in the listbox.
        """
        if not self.dropdown:
            self.open_dropdown()
        else:
            current = self.listbox.curselection()
            if current:
                index = current[0]
                if index < self.listbox.size() - 1:
                    self.listbox.select_clear(0, "end")
                    index += 1
                    self.listbox.select_set(index)
                    self.listbox.activate(index)
                    self.listbox.see(index)
            else:
                # If no selection exists, select the first item.
                self.listbox.select_set(0)
                self.listbox.activate(0)
        return "break"  # Prevent default behavior

    def on_up(self, event):
        """
        If the dropdown is open, move the selection up.
        """
        if self.dropdown:
            current = self.listbox.curselection()
            if current:
                index = current[0]
                if index > 0:
                    self.listbox.select_clear(0, "end")
                    index -= 1
                    self.listbox.select_set(index)
                    self.listbox.activate(index)
                    self.listbox.see(index)
        return "break"

    def on_return(self, event):
        """
        When Enter is pressed, confirm the selection, update the value,
        close the dropdown, and maintain focus on the entry.
        """
        global justDeletedFlag
        if self.dropdown:
            current = self.listbox.curselection()
            if current:
                self.selected_index = current[0]
                selected_value = self.values[self.selected_index]
                self.var.set(selected_value)
            self.close_dropdown()
            self.entry.focus_set()
            if self.name=="custom_combo":
                print("\n*** RETURN PRESSED ON COMBOBOX DROPDOWN SELECTION ***")    
                copyFlag = justDeletedFlag
                on_select(CustomEvent("Auto", self, "ComboBox Event"))
                if copyFlag:
                    # to force pressing the RETURN button twice if necessary
                    print("\n*** RETURN PRESSED ON COMBOBOX DROPDOWN SELECTION - AGAIN ***")
                    on_select(CustomEvent("Auto", self, "ComboBox Event"))
                print("\n*** COMPLETED - RETURN PRESSED ON COMBOBOX DROPDOWN SELECTION ***")    
            elif self.name=="custom_combo_bt":    
                on_select_bluetooth(CustomEvent("Auto", self, "ComboBox Event"))
            elif self.name=="custom_combo_wifi":
                on_select_wifi(CustomEvent("Auto", self, "ComboBox Event"))
        else: # dropdown selection was not selected with the Enter key
            print("\n*** Return key pressed on unopened combobox ***")
            copyFlag = justDeletedFlag
            on_select(CustomEvent("Auto", self, "ComboBox Event"))
            if copyFlag:
                # to force pressing the RND button twice if necessary
                print("\n*** Return key pressed on unopened combobox AGAIN ***")
                on_select(CustomEvent("Auto", self, "ComboBox Event"))
            print("*** COMPLETED - Return key pressed on unopened combobox ***\n")
        return "break"

    def on_escape(self, event):
        """
        Pressing Escape will close the dropdown if it is open.
        """
        if self.dropdown:
            self.close_dropdown()
            return "break"

    def on_focus_combobox(self, event):
        """
        Change the background color to light blue when the entry gains focus.
        If the default background is not set, initialize it.
        """
        if not hasattr(self, "default_bg") or self.default_bg is None:
            self.default_bg = self.entry.cget("background")
        self.entry.config(background="light blue")

    def on_focus_out(self, event):
        """
        Restore the background color to its default value and 
        check if we need to close the dropdown.
        """
        self.entry.config(background=self.default_bg)
        self.after(100, self.check_focus)

    def check_focus(self):
        """
        Checks focus of the current widget. Closes the dropdown if focus has moved
        away from both the entry and the dropdown.
        """
        if self.dropdown:
            current_focus = self.focus_get()
            if current_focus not in (self.entry, self.listbox) and not str(current_focus).startswith(str(self.dropdown)):
                self.close_dropdown()

    def on_listbox_click(self, event):
        """
        Handles mouse selection from the listbox.
        """
        index = self.listbox.curselection()
        if index:
            self.selected_index = index[0]
            selected_value = self.values[self.selected_index]
            self.var.set(selected_value)
        self.close_dropdown()
        self.entry.focus_set()


##########################################
### THIS IS WHERE THE CORE CODE STARTS ###

# Create the main window
# Set title, size and position of the main window, and make it non-resizable
root = tk.Tk()
root.title("INTERNET RADIO - https://github.com/namor5772/TkRadio/RadioSelenium.py")  
root.geometry("800x455+0+0")
root.resizable(False, False)
root.update_idletasks()

# Create a label to display actions or the counter value.
if GPIO:
    labelRE = tk.Label(root, text="  0")
    labelRE.place(x=700, y=26)

    # Create a list of labels for the root/main form to display pressable keys. They are
    # at the top of the main form (one bank of sizeBank keys is displayed at a time)
    labels_main = []
    for i in range(sizeBank):
        label_main = tk.Label(root, text=KeyList[i][0], font=("Arial", 12), bg="darkgray")
        label_main.place(x=10+52*i, y=0, width=50, height=20)
        labels_main.append(label_main)
    labels_main[indexKeyList].config(bg="lightblue")  
else:
    labelRE = tk.Label(root, text="       windows version running")
    labelRE.place(x=0, y=0)

# create a list of all the available station names
aStringArray = []
for element in aStation:
    aStringArray.append(element[0])

# Create our custom combobox with 8 rows visible in the dropdown.
custom_combo = CustomCombobox(root, aStringArray, "custom_combo", visible_items=22, width=35)
custom_combo.place(x=130+(sizeButton+5), y=26)

# Populate if possible the playlist array aStation2[] from file saved at shutdown
try:
    with open(filepath2,'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        aStation2 = [row for row in reader]             
except FileNotFoundError:
    # will just use the default aStation2[] array created previously
    print(f'Error: The file {filepath2} does not exist.')

# Create a text box, position and size it, used to display the program and song details
text_box = tk.Text(root, wrap="word")
text_box.place(x=10, y=110+30+Ydown, width=Xgap-20+30+25, height=Xprog-30-25)
text_box.config(state=tk.NORMAL) # Enable the text box to insert text

# button used to select and play a station at random (from all those available)
if GPIO:
    randomButton = tk.Button(root, text="RND", name="randomButton")
    randomButton.place(x=500 , y=24, height=25)
else:
    randomButton = tk.Button(root, text=" RND ", name="randomButton")
    randomButton.place(x=500-7 , y=0, height=25)
randomButton.config(takefocus=True)
randomButton.config(bg="gray90")
randomButton.bind("<Return>", random_button_pressed)  
#randomButton.bind("<ButtonPress>", random_button_pressed)  
randomButton.bind("<FocusIn>", on_focus_dostuff)
randomButton.bind("<FocusOut>", on_focus_out_dostuff)

# button used to delete the currently playing station from the station list.
# this will be saved to the file at shutdown and the playlist button references
# will be adjusted if necessary
if GPIO:
    deleteButton = tk.Button(root, text="DEL", name="deleteButton", relief=tk.RAISED,)
    deleteButton.place(x=559 , y=24, height=25)
else:
    deleteButton = tk.Button(root, text="DEL", name="deleteButton", relief=tk.RAISED,)
    deleteButton.place(x=550-7 , y=0, height=25)
deleteButton.config(takefocus=True)
deleteButton.config(bg="gray90")
deleteButton.bind("<Delete>", delete_key_pressed) # the only way to press the [DEL] button 
deleteButton.bind("<FocusIn>", on_focus_dostuff)
deleteButton.bind("<FocusOut>", on_focus_out_dostuff)

# button used to save the current contents of textbox that shows the station details and program
# to a txt file
if GPIO:
    saveButton = tk.Button(root, text="SAVE", name="saveButton")
    saveButton.place(x=614, y=24, height=25)
else:
    saveButton = tk.Button(root, text="SAVE", name="saveButton")
    saveButton.place(x=590-7, y=0, height=25)
saveButton.config(takefocus=True)
saveButton.config(bg="gray90")
saveButton.bind("<Return>", save_button_pressed)  
#saveButton.bind("<ButtonPress>", save_button_pressed)  
saveButton.bind("<FocusIn>", on_focus_dostuff)
saveButton.bind("<FocusOut>", on_focus_out_dostuff)

# Create a button on the root form to display the secondary setup form
# Note: if windows version this button is used to toggle polling!
setupButton = tk.Button(root, text="+", name="setupButton")
setupButton.default_bg = setupButton.cget("bg") 
if GPIO:
    setupButton.place(x=768 , y=24, width=25, height=25)
else:
    setupButton.place(x=768-7 , y=0, width=25+7, height=25)
setupButton.config(takefocus=True)
if GPIO:
    setupButton.bind("<Return>", show_setup_form)  
#    setupButton.bind("<ButtonPress>", show_setup_form)  
else:
    setupButton.bind("<Return>", toggle_pollStatus)  
#    setupButton.bind("<ButtonPress>", toggle_pollStatus)  
setupButton.bind("<FocusIn>", on_focus_dostuff)
setupButton.bind("<FocusOut>", on_focus_out_dostuff)
   
# Create labels used for station logo image (label) and program related image (label2)
# Positioning of latter can vary
label = tk.Label(root)
label.place(x=15, y=2+30)
label2 = tk.Label(root)

# Create the playlist buttons (fully) and add them to the buttons[] list
buttons = []
for i in range(numButtons):
    button = tk.Button(root, text=f"Button{i}")

    # positioning buttons in 2 rows of 9
    if (i<9):
        button.place(x=128+(sizeButton+5)*(i+1), y=35+30, width=sizeButton, height=sizeButton)
    else:
        button.place(x=128+(sizeButton+5)*(i-8), y=35+30+sizeButton+5, width=sizeButton, height=sizeButton)

    button.config(bg="gray90")
    button.bind("<FocusIn>", lambda event, i=i: on_focus(event, i))
    button.bind("<FocusOut>", lambda event, i=i: on_focus_out(event, i))
#    button.bind("<ButtonPress>", lambda event, i=i: on_button_press(event, i))  
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

# SECONDARY setup FORM RELATED DEFINITIONS
# *** START ******************************

# Create a secondary setup form without title bar and close buttons
# It will be used for examining and configuring setup settings
if GPIO:
    setup = tk.Toplevel(root)
    #setup.geometry("800x480+0+26")
    setup.geometry("800x430+0+50")
    setup.overrideredirect(True)
    setup.withdraw() # Hide the form initially

    # button which returns focus and visibility back to the main/root form
    mainButton = tk.Button(setup, text="+", name="mainButton")
    mainButton.default_bg = mainButton.cget("bg") 
    mainButton.place(x=768, y=0, width=25, height=25)
    mainButton.config(takefocus=True)
    mainButton.bind("<Return>", show_root_form)  
    #mainButton.bind("<ButtonPress>", show_root_form)  
    mainButton.bind("<FocusIn>", on_focus_dostuff)
    mainButton.bind("<FocusOut>", on_focus_out_dostuff)

    # button to toggle bluetooth connection on/off
    BTstatusButton = tk.Button(setup, text="NONE") 
    BTstatusButton.place(x=15, y=10+25, height=25)
    BTstatusButton.config(takefocus=True)
    BTstatusButton.bind("<Return>", toggle_bluetooth)  
    #BTstatusButton.bind("<ButtonPress>", toggle_bluetooth)  

    # button & label to connect to currently paired bluetooth speakers
    cX = 15; cY = 10+25+30
    connectButton = tk.Button(setup, text="CONNECT", name="connectButton") 
    connectButton.default_bg = connectButton.cget("bg") 
    connectButton.place(x=cX, y=cY, height=25)
    connectButton.config(takefocus=True)
    connectButton.bind("<Return>", _connect_bluetooth)  
    #connectButton.bind("<ButtonPress>", _connect_bluetooth)  
    connectButton.bind("<FocusIn>", on_focus_dostuff)
    connectButton.bind("<FocusOut>", on_focus_out_dostuff)
    label4 = tk.Label(setup, text="")
    label4.place(x=cX+100, y=cY+2)

    # button to enable scanning for bluetooth devices (which will appear in above combobox)
    pairButton = tk.Button(setup, text="SEE BT DEVICES", name="pairButton") 
    pairButton.default_bg = pairButton.cget("bg") 
    pairButton.place(x=cX, y=cY+60, height=25)
    pairButton.config(takefocus=True)
    pairButton.bind("<Return>", pair_bluetooth)  
    #pairButton.bind("<ButtonPress>", pair_bluetooth)
    pairButton.bind("<FocusIn>", on_focus_dostuff)
    pairButton.bind("<FocusOut>", on_focus_out_dostuff)
    label6 = tk.Label(setup, text="")
    label6.place(x=cX+150, y=cY+62)

    # Create a Combobox for bluetooth connection selection & related information label
    cX = 15; cY = 155
    label3 = tk.Label(setup, text="")
    label3.place(x=cX+1, y=cY)
    options = [""]
    custom_combo_bt = CustomCombobox(setup, options, "custom_combo_bt", visible_items=4, width=44)
    custom_combo_bt.place(x=cX, y=cY+30)

    # vertical separator, between bluetooth an dwifi setup sections
    separator = ttk.Separator(setup, orient="vertical")
    separator.place(relx=0.5, rely=0, relheight=1, anchor="n")  # Positioned in the center

    # button to toggle bluetooth connection on/off
    pollStatusButton = tk.Button(setup, text="NONE") 
    pollStatusButton.place(x=cX+400, y=10+25, height=25)
    pollStatusButton.config(takefocus=True)
    pollStatusButton.bind("<Return>", toggle_pollStatus)  
    #pollStatusButton.bind("<ButtonPress>", toggle_pollStatus)  

    # button to enable scanning for wifi devices (which will appear in above combobox)
    wifiButton = tk.Button(setup, text="SEE WIFI", name="wifiButton") 
    wifiButton.default_bg = wifiButton.cget("bg") 
    wifiButton.place(x=cX+400, y=cY-30, height=25)
    wifiButton.config(takefocus=True)
    wifiButton.bind("<Return>", find_wifi)  
    #wifiButton.bind("<ButtonPress>", find_wifi)
    wifiButton.bind("<FocusIn>", on_focus_dostuff)
    wifiButton.bind("<FocusOut>", on_focus_out_dostuff)
    label7 = tk.Label(setup, text="")
    label7.place(x=cX+400+100, y=cY+2-30)

    # Create a Combobox for wifi connection selection
    options2 = [""]
    label5 = tk.Label(setup, text="")
    label5.place(x=cX+1+400, y=cY)
    custom_combo_wifi = CustomCombobox(setup, options2, "custom_combo_wifi", visible_items=6, width=44)
    custom_combo_wifi.place(x=cX+400, y=cY+30)

    # text entry for wifi password, and its info label, also styles for focus visibility
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Focused.TEntry",fieldbackground="white", foreground="black")
    wifiPassword = ttk.Entry(setup, style="Focused.TEntry", width=30)
    wifiPassword.place(x=cX+400+75, y=cY+60)
    wifiPassword.bind("<Return>", process_wifiPassword)
    wifiPassword.bind("<FocusIn>", on_focus_wifiPassword)
    wifiPassword.bind("<FocusOut>", on_focus_out_wifiPassword)
    label_wifiPassword = tk.Label(setup, text="Password:")
    label_wifiPassword.place(x=cX+400, y=cY+60)

# SECONDARY setup FORM RELATED DEFINITIONS
# *** END ********************************


# doing stuff just after the gui is initialised and we are running in the root thread
root.after(5000, after_GUI_started) # need 5sec lag to make sure things work
print("Radio stream interface")

# Bind the closing event to the on_closing function
root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the GUI loop
root.mainloop()
print("out of GUI loop..")
