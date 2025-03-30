'''
1. pollFlag implement with button and config poll.txt file
2. Get rid of TEST button
3. find some way to indicate graphically when a combobox has focus
'''


import subprocess
import inspect
import tkinter as tk
import time
import urllib.request
import requests
import os
import csv
import RPi.GPIO as GPIO
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


# START #######################################################
# SETUP GPIO BUTTONS FOR THE RASPBERRY PI 4B AND THEIR ACTIONS

# Set up GPIO
GPIO.setmode(GPIO.BCM)
LeftButton = 21 # scrolls left through horizontal list of possible keys you can press
RightButton = 20 # scrolls right through horizontal list of possible keys you can press
KeypressButton = 16 # simulates the key press of the currently selected key
GPIO.setup(LeftButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(RightButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
GPIO.setup(KeypressButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)  

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


# GPIO button 21 pressed
def on_LeftButton_press(channel):
    global indexKeyList, indexBank, indexVisibleKey
    labels_main[indexVisibleKey].config(bg="darkgray")
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


# GPIO button 20 pressed
def on_RightButton_press(channel):
    global indexKeyList, indexBank, indexVisibleKey
    labels_main[indexVisibleKey].config(bg="darkgray")
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
    labels_main[indexVisibleKey].config(bg="lightblue")


# GPIO button 16 pressed
def on_KeypressButton_press(channel):
    print(f"KeypressButton {KeyList[indexKeyList][1]} Pressed!")
    sKey = KeyList[indexKeyList][1]
    match indexKeyList:
        case 0: # <-Tab
            try:
                if rootFlag:
                    focused_widget = root.focus_get()
                else:
                    focused_widget = setup.focus_get()
                focused_widget.event_generate("<Shift-Tab>")
                print("Shift-Tab key pressed!")
            except KeyError as e:
                # mysterious stuff I have to do to precisely simulate the behaviour
                # of pressing the <Shift-Tab> key within a combobox popup
                print(f"error {e}")
                if rootFlag:
                    combobox.event_generate("<Return>")
                    focused_widget = root.focus_get()
                    print("Shift-Tab key pressed inside combobox popup!")
                else:    
                    combobox_bt.event_generate("<Return>")
                    focused_widget = setup.focus_get()
                    print("Shift-Tab key pressed inside combobox_bt popup!")
                focused_widget.event_generate("<Shift-Tab>")
        case 1: # Tab
            try:
                if rootFlag:
                    focused_widget = root.focus_get()
                else:
                    focused_widget = setup.focus_get()
                focused_widget.event_generate("<Tab>")
                print("Tab key pressed!")
            except KeyError as e:
                # mysterious stuff I have to do to precisely simulate the behaviour
                # of pressing the <Tab> key within a combobox popup
                print(f"error {e}")
                if rootFlag:
                    combobox.event_generate("<Return>")
                    focused_widget = root.focus_get()
                    print("Tab key pressed inside combobox popup!")
                else:
                    combobox_bt.event_generate("<Return>")
                    focused_widget = setup.focus_get()
                    print("Tab key pressed inside combobox_bt popup!")
                focused_widget.event_generate("<Tab>")
        case 2: # Enter
            try:
                if rootFlag:
                    focused_widget = root.focus_get()
                else:
                    focused_widget = setup.focus_get()
                focused_widget.event_generate("<Return>")
                print("Enter key pressed!")
            except KeyError as e:
                # mysterious stuff I have to do to precisely simulate the behaviour
                # of pressing the <Enter> key within a combobox popup
                print(f"error {e}")
                if rootFlag:
                    combobox.event_generate("<Return>")
                    print("Enter key pressed inside combobox popup!")
                else:    
                    combobox_bt.event_generate("<Return>")
                    print("Enter key pressed inside combobox_bt popup!")
        case 3: # Down
            # does nothing (no errors) if pressed outside of combobox
            if rootFlag:
                combobox.event_generate("<Down>")
            else:
                combobox_bt.event_generate("<Down>")
            print("Down key pressed!")
        case 4: # Up
            # does nothing (no errors) if pressed outside of combobox
            if rootFlag:
                combobox.event_generate("<Up>")
            else:
                combobox_bt.event_generate("<Up>")
            print("Up key pressed!")
        case _ if 5<=indexKeyList<sizeKeyList:
            if rootFlag:
                focused_widget = root.focus_get()
            else:
                focused_widget = setup.focus_get()
            focused_widget.event_generate(f"<Key-{sKey}>")
            print(f"<Key-{sKey}> pressed!")


GPIO.add_event_detect(LeftButton, GPIO.FALLING, callback=on_LeftButton_press, bouncetime=200)    
GPIO.add_event_detect(RightButton, GPIO.FALLING, callback=on_RightButton_press, bouncetime=200)    
GPIO.add_event_detect(KeypressButton, GPIO.FALLING, callback=on_KeypressButton_press, bouncetime=200)


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

# global graphic position variables
Ydown = 63
Ygap = 10;  Ygap2 = 110+Ydown; Ygap3 = 110+Ydown
Xgap = 560-70; Xgap2 = 560-70; Xgap3 = 560-70
Xprog = 300

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
refreshTime = 20.0 # seconds between updating station info
stationShort = ""
station = ""
needSleep = 5 # can be less on faster machines
pressButton = True # flag for how stream is started

# other global variables
rootFlag = True # False indicates that you are in the secondary window
pollFlag = True # if true then poll website for program text and picture changes 

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

def Radio1(br,Num,sPath):
    if eventFlag:
        # use inspect to get the name of the calling function
        # this is used to generate the station name and logo
        stack = inspect.stack()
        global station 
        station = inspect.stack()[1].function
        logo = station + ".png"
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
    scaled_image2 = cropped_image2.resize((Xprog-55, Xprog-55))  # Adjust the size as needed
    photo2 = ImageTk.PhotoImage(scaled_image2)
    label2.config(image=photo2)
    label2.image = photo2  # Keep a reference to avoid garbage collection
    if station == "ABC_Classic2":
        label2.place(x=Xgap+55, y=Ygap3+30)  # Adjust the position
    else:
        label2.place(x=Xgap+55, y=Ygap2+30)  # Adjust the position
    
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


def Radio2(br,Num,sPath):
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
        for _ in range(Num):
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
    scaled_image2 = image2.resize((width-55, Xprog-55))  # Adjust the size as needed
    photo2 = ImageTk.PhotoImage(scaled_image2)
    label2.config(image=photo2)
    label2.image = photo2  # Keep a reference to avoid garbage collection
    label2.place(x=Xgap3-(width-Xprog)+55, y=Ygap2+30)  # Adjust the position
    
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


def Radio3(br,Num,sPath):
    if eventFlag:
        # use inspect to get the name of the calling function
        # this is used to generate the station name and logo
        stack = inspect.stack()
        station = inspect.stack()[1].function
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
        for _ in range(Num):
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
    scaled_image2 = cropped_image2.resize((Xprog-55, Xprog-25))  # Adjust the size as needed
    photo2 = ImageTk.PhotoImage(scaled_image2)
    label2.config(image=photo2)
    label2.image = photo2  # Keep a reference to avoid garbage collection
    if station_short == "ABC_Classic":
        label2.place(x=Xgap+55, y=Ygap3+30)  # Adjust the position
    else:
        label2.place(x=Xgap+55, y=Ygap2+30)  # Adjust the position

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


def Radio4(br,sPath):
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
    scaled_image2 = cropped_image2.resize((Xprog-55, Xprog-55))  # Adjust the size as needed
    photo2 = ImageTk.PhotoImage(scaled_image2)
    label2.config(image=photo2)
    label2.image = photo2  # Keep a reference to avoid garbage collection
    label2.place(x=Xgap2+55, y=Ygap2+30)  # Adjust the position
    
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


def Radio5(br,sPath):
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
    scaled_image2 = cropped_image2.resize((Xprog-55, Xprog-55))  # Adjust the size as needed
    photo2 = ImageTk.PhotoImage(scaled_image2)
    label2.config(image=photo2)
    label2.image = photo2  # Keep a reference to avoid garbage collection
    label2.place(x=Xgap+55, y=Ygap2+30)  # Adjust the position

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


def Radio6(br,sPath):
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
    scaled_image2 = cropped_image2.resize((Xprog-55, Xprog-55))  # Adjust the size as needed
    photo2 = ImageTk.PhotoImage(scaled_image2)
    label2.config(image=photo2)
    label2.image = photo2  # Keep a reference to avoid garbage collection
    label2.place(x=Xgap+55, y=Ygap3+30)  # Adjust the position
    
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
def Radio7(br,Num,sPath):
    if eventFlag:
        stack = inspect.stack()
        print("----------")
        station = inspect.stack()[1].function
        logo = station + ".png"
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
    scaled_image2 = cropped_image2.resize((Xprog-55, Xprog-55))  # Adjust the size as needed
    photo2 = ImageTk.PhotoImage(scaled_image2)
    label2.config(image=photo2)
    label2.image = photo2  # Keep a reference to avoid garbage collection
    label2.place(x=Xgap+55, y=Ygap3+30)  # Adjust the position
        
    # Find program details
    ht = be.get_attribute('innerHTML')
    soup = BeautifulSoup(ht, 'lxml')
    if Num==0:
        xid="abc-:rb:-item-0"
        sName = "ABC SPORT"
    elif Num==1:
        xid="abc-:rb:-item-1"
        sName = "ABC SPORT EXTRA"
    else: # if Num==2
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


def Commercial1(br,sPath,sClass,nType):
    if eventFlag:
        # use inspect to get the name of the calling function
        stack = inspect.stack()
        print("----------")
        station = inspect.stack()[1].function
        logo = station + ".png"
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
        # the position of the "Listen Live" button depends on he nType integer parameter
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
    scaled_image2 = image2.resize((width-55, Xprog-55))  # Adjust the size as needed
    photo2 = ImageTk.PhotoImage(scaled_image2)
    label2.config(image=photo2)
    label2.image = photo2  # Keep a reference to avoid garbage collection
    label2.place(x=Xgap3-(width-Xprog)+55, y=Ygap2+30)  # Adjust the position
 
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
def Commercial2(br,sPath):
    if eventFlag:
        # use inspect to get the name of the calling function
        stack = inspect.stack()
        print("----------")
        station = inspect.stack()[1].function
        logo = station + ".png"
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
        # press button with virtual mouse to play stream
        window_size = br.get_window_size()
        width = window_size['width']
        height = window_size['height']         
        print(f"Window size: width = {window_size['width']}, height = {window_size['height']}")
        widthPx =280
        heightPx = 390
        print(f"Move size: width = {widthPx}, height = {heightPx}")
        actions = ActionChains(br)
        actions.move_by_offset(widthPx, heightPx).click().perform()
        time.sleep(3)

        # get station logo
        image_path = pathImages + "/" + logo
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

    # Stations with program image
    try:
        # try to find a particular image element by path
        img_element = be.find_element(By.XPATH, '/html/body/div[6]/div[1]/div[3]/div/div[1]/div[1]/div[3]/div/div[1]/div/a/img')
        img_url = img_element.get_attribute("src")
        image_path = pathImages + "/presenter.jpg"
        urllib.request.urlretrieve(img_url, image_path)
        image = Image.open(image_path)
        width2, height2 = image.size;
        print(f"Pic width: {width2}, Pic height: {height2}")
        width = int(Xprog*width2/height2)
        scaled_image = image.resize((width-30-25, Xprog-30-25))  # Adjust the size as needed
        photo = ImageTk.PhotoImage(scaled_image)
        label2.config(image=photo)
        label2.image = photo  # Keep a reference to avoid garbage collection
        label2.place(x=Xgap3-(width-Xprog)+30+25, y=Ygap2+30)  # Adjust the position
        print("=====> /div/a/img")
    except NoSuchElementException:
        try:
            # if failed above try a slightly different path
            img_element = be.find_element(By.XPATH, '/html/body/div[6]/div[1]/div[3]/div/div[1]/div[1]/div[3]/div/div[1]/div/img')
            img_url = img_element.get_attribute("src")
            image_path = pathImages + "/presenter.jpg"
            urllib.request.urlretrieve(img_url, image_path)
            image = Image.open(image_path)
            width2, height2 = image.size;
            print(f"Pic width: {width2}, Pic height: {height2}")
            width = int(Xprog*width2/height2)
            scaled_image = image.resize((width-55, Xprog-55))  # Adjust the size as needed
            photo = ImageTk.PhotoImage(scaled_image)
            label2.config(image=photo)
            label2.image = photo  # Keep a reference to avoid garbage collection
            label2.place(x=Xgap3-(width-Xprog)+55, y=Ygap2+30)  # Adjust the position
            print("=====>  /div/img")
        except NoSuchElementException:
            # failed to find image so display a blank image
            image_path = pathImages + "/Blank.png"
            image = Image.open(image_path)
            scaled_image = image.resize((Xprog-30-25, Xprog-30-25))  # Adjust the size as needed
            photo = ImageTk.PhotoImage(scaled_image)
            label2.config(image=photo)
            label2.image = photo  # Keep a reference to avoid garbage collection
            label2.place(x=Xgap+55, y=Ygap3+30)  # Adjust the position
            print("=====> No /img")

    # get station and program details (if available)
    ht = be.get_attribute('innerHTML')
    soup = BeautifulSoup(ht, 'lxml')
    fe = soup.find(attrs={"class": "history-song"})
    if fe is not None:
        fe1 = fe.get_text(separator="*", strip=True)
    else:
        fe1 = "No program information"
    return fe1

# END ####################################################
# DEFINE VARIOUS CORE FUNCTIONS THAT STREAM RADIO STATIONS



# START **********************************************************
# INDIVIDUAL FUNCTION DEFINITIONS FOR EACH AVAILABLE RADIO STATION
#
# Each one calls a particular core function defined above with specific parameters,
# dependant on the structure of a specific stations website layout

def ABC_Radio_Sydney_NSW():
    return Radio4(browser,"https://www.abc.net.au/listen/live/sydney")
def ABC_Broken_Hill_NSW():
    return Radio4(browser,"https://www.abc.net.au/listen/live/brokenhill")
def ABC_Central_Coast_NSW():
    return Radio4(browser,"https://www.abc.net.au/listen/live/centralcoast")
def ABC_Central_West_NSW():
    return Radio4(browser,"https://www.abc.net.au/listen/live/centralwest")
def ABC_Coffs_Coast_NSW():
    return Radio4(browser,"https://www.abc.net.au/listen/live/coffscoast")
def ABC_Illawarra_NSW():
    return Radio4(browser,"https://www.abc.net.au/listen/live/illawarra")
def ABC_Mid_North_Coast_NSW():
    return Radio4(browser,"https://www.abc.net.au/listen/live/midnorthcoast")
def ABC_New_England_North_West_NSW():
    return Radio4(browser,"https://www.abc.net.au/listen/live/newengland")
def ABC_Newcastle_NSW():
    return Radio4(browser,"https://www.abc.net.au/listen/live/newcastle")
def ABC_North_Coast_NSW():
    return Radio4(browser,"https://www.abc.net.au/listen/live/northcoast")
def ABC_Riverina_NSW():
    return Radio4(browser,"https://www.abc.net.au/listen/live/riverina")
def ABC_South_East_NSW():
    return Radio4(browser,"https://www.abc.net.au/listen/live/southeastnsw")
def ABC_Upper_Hunter_NSW():
    return Radio4(browser,"https://www.abc.net.au/listen/live/upperhunter")
def ABC_Western_Plains_NSW():
    return Radio4(browser,"https://www.abc.net.au/listen/live/westernplains")
def ABC_Radio_Canberra_ACT():
    return Radio4(browser,"https://www.abc.net.au/listen/live/canberra")
def ABC_Radio_Darwin_NT():
    return Radio4(browser,"https://www.abc.net.au/listen/live/darwin")
def ABC_Alice_Springs_NT():
    return Radio4(browser,"https://www.abc.net.au/listen/live/alicesprings")
def ABC_Radio_Melbourne_VIC():
    return Radio4(browser,"https://www.abc.net.au/listen/live/melbourne")
def ABC_Ballarat_VIC():
    return Radio4(browser,"https://www.abc.net.au/listen/live/ballarat")
def ABC_Central_Victoria_VIC():
    return Radio4(browser,"https://www.abc.net.au/listen/live/centralvic")
def ABC_Gippsland_VIC():
    return Radio4(browser,"https://www.abc.net.au/listen/live/gippsland")
def ABC_Goulburn_Murray_VIC():
    return Radio4(browser,"https://www.abc.net.au/listen/live/goulburnmurray")
def ABC_Mildura_Swan_Hill_VIC():
    return Radio4(browser,"https://www.abc.net.au/listen/live/milduraswanhill")
def ABC_Shepparton_VIC():
    return Radio4(browser,"https://www.abc.net.au/listen/live/shepparton")
def ABC_South_West_Victoria_VIC():
    return Radio4(browser,"https://www.abc.net.au/listen/live/southwestvic")
def ABC_Wimmera_VIC():
    return Radio4(browser,"https://www.abc.net.au/listen/live/wimmera")
def ABC_Radio_Adelaide_SA():
    return Radio4(browser,"https://www.abc.net.au/listen/live/adelaide")
def ABC_Eyre_Peninsula_SA():
    return Radio4(browser,"https://www.abc.net.au/listen/live/eyre")
def ABC_North_and_West_SA():
    return Radio4(browser,"https://www.abc.net.au/listen/live/northandwest")
def ABC_Riverland_SA():
    return Radio4(browser,"https://www.abc.net.au/listen/live/riverland")
def ABC_South_East_SA():
    return Radio4(browser,"https://www.abc.net.au/listen/live/southeastsa")
def ABC_Radio_Hobart_TAS():
    return Radio4(browser,"https://www.abc.net.au/listen/live/hobart")
def ABC_Northern_Tasmania_TAS():
    return Radio4(browser,"https://www.abc.net.au/listen/live/northtas")
def ABC_Radio_Brisbane_QLD():
    return Radio4(browser,"https://www.abc.net.au/listen/live/brisbane")
def ABC_Capricornia_QLD():
    return Radio4(browser,"https://www.abc.net.au/listen/live/capricornia")
def ABC_Far_North_QLD():
    return Radio4(browser,"https://www.abc.net.au/listen/live/farnorth")
def ABC_Gold_Coast_QLD():
    return Radio4(browser,"https://www.abc.net.au/listen/live/goldcoast")
def ABC_North_Queensland_QLD():
    return Radio4(browser,"https://www.abc.net.au/listen/live/northqld")
def ABC_North_West_Queensland_QLD():
    return Radio4(browser,"https://www.abc.net.au/listen/live/northwest")
def ABC_Southern_Queensland_QLD():
    return Radio4(browser,"https://www.abc.net.au/listen/live/southqld")
def ABC_Sunshine_Coast_QLD():
    return Radio4(browser,"https://www.abc.net.au/listen/live/sunshine")
def ABC_Tropical_North_QLD():
    return Radio4(browser,"https://www.abc.net.au/listen/live/tropic")
def ABC_Western_Queensland_QLD():
    return Radio4(browser,"https://www.abc.net.au/listen/live/westqld")
def ABC_Wide_Bay_QLD():
    return Radio4(browser,"https://www.abc.net.au/listen/live/widebay")
def ABC_Radio_Perth_WA():
    return Radio4(browser,"https://www.abc.net.au/listen/live/perth")
def ABC_Esperance_WA():
    return Radio4(browser,"https://www.abc.net.au/listen/live/esperance")
def ABC_Goldfields_WA():
    return Radio4(browser,"https://www.abc.net.au/listen/live/goldfields")
def ABC_Great_Southern_WA():
    return Radio4(browser,"https://www.abc.net.au/listen/live/greatsouthern")
def ABC_Kimberley_WA():
    return Radio4(browser,"https://www.abc.net.au/listen/live/kimberley")
def ABC_Midwest_and_Wheatbelt_WA():
    return Radio4(browser,"https://www.abc.net.au/listen/live/wheatbelt")
def ABC_Pilbara_WA():
    return Radio4(browser,"https://www.abc.net.au/listen/live/pilbara")
def ABC_South_West_WA():
    return Radio4(browser,"https://www.abc.net.au/listen/live/southwestwa")
def ABC_NewsRadio():
    return Radio4(browser,"https://www.abc.net.au/listen/live/news")
def ABC_Radio_National_LIVE():
    return Radio2(browser,0,"https://www.abc.net.au/listen/live/radionational")
def ABC_Radio_National_QLD():
    return Radio2(browser,1,"https://www.abc.net.au/listen/live/radionational")
def ABC_Radio_National_WA():
    return Radio2(browser,2,"https://www.abc.net.au/listen/live/radionational")
def ABC_Radio_National_SA():
    return Radio2(browser,3,"https://www.abc.net.au/listen/live/radionational")
def ABC_Radio_National_NT():
    return Radio2(browser,4,"https://www.abc.net.au/listen/live/radionational")
def ABC_SPORT(): # *************************************************************** FIX ****
    return Radio7(browser,0,"https://www.abc.net.au/news/sport/audio")
def ABC_triple_j_LIVE():
    return Radio3(browser,0,"https://www.abc.net.au/listen/live/triplej")
def ABC_triple_j_QLD():
    return Radio3(browser,1,"https://www.abc.net.au/listen/live/triplej")
def ABC_triple_j_WA():
    return Radio3(browser,2,"https://www.abc.net.au/listen/live/triplej")
def ABC_triple_j_SA():
    return Radio3(browser,3,"https://www.abc.net.au/listen/live/triplej")
def ABC_triple_j_NT():
    return Radio3(browser,4,"https://www.abc.net.au/listen/live/triplej")
def ABC_triple_j_Hottest():
    return Radio1(browser,7,"https://www.abc.net.au/triplej/live/triplejhottest")
def ABC_triple_j_Unearthed():
    return Radio1(browser,7,"https://www.abc.net.au/triplej/live/unearthed")
def ABC_Double_j_LIVE():
    return Radio3(browser,0,"https://www.abc.net.au/listen/live/doublej")
def ABC_Double_j_QLD():
    return Radio3(browser,1,"https://www.abc.net.au/listen/live/doublej")
def ABC_Double_j_WA():
    return Radio3(browser,2,"https://www.abc.net.au/listen/live/doublej")
def ABC_Double_j_SA():
    return Radio3(browser,3,"https://www.abc.net.au/listen/live/doublej")
def ABC_Double_j_NT():
    return Radio3(browser,4,"https://www.abc.net.au/listen/live/doublej")
def ABC_Classic_LIVE():
    return Radio3(browser,0,"https://www.abc.net.au/listen/live/classic")
def ABC_Classic_QLD():
    return Radio3(browser,1,"https://www.abc.net.au/listen/live/classic")
def ABC_Classic_WA():
    return Radio3(browser,2,"https://www.abc.net.au/listen/live/classic")
def ABC_Classic_SA():
    return Radio3(browser,3,"https://www.abc.net.au/listen/live/classic")
def ABC_Classic_NT():
    return Radio3(browser,4,"https://www.abc.net.au/listen/live/classic")
def ABC_Classic2():
    return Radio1(browser,7,"https://www.abc.net.au/listen/live/classic2")
def ABC_Jazz():
    return Radio1(browser,7,"https://www.abc.net.au/listen/live/jazz")
def ABC_Country():
    return Radio5(browser,"https://www.abc.net.au/listen/live/country")
def ABC_Kids_listen():
    return Radio6(browser,"https://www.abc.net.au/listenlive/kidslisten")
def ABC_Radio_Australia():
    return Radio5(browser,"https://www.abc.net.au/pacific/live")
def KIIS1065():
    return Commercial1(browser,"https://www.iheart.com/live/kiis-1065-6185/","css-1jnehb1 e1aypx0f0",0)
def GOLD1017():
    return Commercial1(browser,"https://www.iheart.com/live/gold1017-6186/","css-1jnehb1 e1aypx0f0",0)
def CADA():
    return Commercial1(browser,"https://www.iheart.com/live/cada-6179/","css-1jnehb1 e1aypx0f0",0)
def iHeartCountry_Australia():
    return Commercial1(browser,"https://www.iheart.com/live/iheartcountry-australia-7222/","css-1jnehb1 e1aypx0f0",0)
def KIIS_90s():
    return Commercial1(browser,"https://www.iheart.com/live/kiis-90s-10069/","css-1jnehb1 e1aypx0f0",0)
def GOLD_80s():
    return Commercial1(browser,"https://www.iheart.com/live/gold-80s-10073/","css-1jnehb1 e1aypx0f0",0)    
def iHeartRadio_Countdown_AUS():
    return Commercial1(browser,"https://www.iheart.com/live/iheartradio-countdown-aus-6902/","css-1jnehb1 e1aypx0f0",0)
def TikTok_Trending_on_iHeartRadio():
    return Commercial1(browser,"https://www.iheart.com/live/tiktok-trending-on-iheartradio-8876/","css-1jnehb1 e1aypx0f0",0)
def iHeartDance():
    return Commercial1(browser,"https://www.iheart.com/live/iheartdance-6941/","css-1jnehb1 e1aypx0f0",0)
def The_Bounce():
    return Commercial1(browser,"https://www.iheart.com/live/the-bounce-6327/","css-1jnehb1 e1aypx0f0",0)
def iHeartAustralia():
    return Commercial1(browser,"https://www.iheart.com/live/iheartaustralia-7050/","css-1jnehb1 e1aypx0f0",0)
def fbi_radio():
    return Commercial1(browser,"https://www.iheart.com/live/fbiradio-6311/","css-1jnehb1 e1aypx0f0",0)
def _2SER():
    return Commercial1(browser,"https://www.iheart.com/live/2ser-6324/","css-1jnehb1 e1aypx0f0",0)
def _2MBS_Fine_Music_Sydney():
    return Commercial1(browser,"https://www.iheart.com/live/2mbs-fine-music-sydney-6312/","css-1jnehb1 e1aypx0f0",0)
def KIX_Country():
    return Commercial1(browser,"https://www.iheart.com/live/kix-country-9315/","css-1jnehb1 e1aypx0f0",0)
def SBS_Chill():
    return Commercial1(browser,"https://www.iheart.com/live/sbs-chill-7029/","css-1jnehb1 e1aypx0f0",0)
def Vintage_FM():
    return Commercial1(browser,"https://www.iheart.com/live/vintage-fm-8865/","css-1jnehb1 e1aypx0f0",0)
def My88_FM():
    return Commercial1(browser,"https://www.iheart.com/live/my88-fm-8866/","css-1jnehb1 e1aypx0f0",0)
def Hope_103_2():
    return Commercial1(browser,"https://www.iheart.com/live/hope-1032-6314/","css-1jnehb1 e1aypx0f0",0)
def The_90s_iHeartRadio():
    return Commercial1(browser,"https://www.iheart.com/live/the-90s-iheartradio-6793/","css-1jnehb1 e1aypx0f0",0)
def The_80s_iHeartRadio():
    return Commercial1(browser,"https://www.iheart.com/live/the-80s-iheartradio-6794/","css-1jnehb1 e1aypx0f0",0)
def Mix_102_3():
    return Commercial1(browser,"https://www.iheart.com/live/mix1023-6184/","css-1jnehb1 e1aypx0f0",0)
def Cruise_1323():
    return Commercial1(browser,"https://www.iheart.com/live/cruise-1323-6177/","css-1jnehb1 e1aypx0f0",0)
def Mix_80s():
    return Commercial1(browser,"https://www.iheart.com/live/mix-80s-10076/","css-1jnehb1 e1aypx0f0",0)
def Mix_90s():
    return Commercial1(browser,"https://www.iheart.com/live/mix-90s-10072/","css-1jnehb1 e1aypx0f0",0)
def ABC_Sport():
    return Commercial1(browser,"https://www.iheart.com/live/abc-sport-7112/","css-1jnehb1 e1aypx0f0",0)
def ABC_Sport_Extra():
    return Commercial1(browser,"https://www.iheart.com/live/abc-sport-extra-10233/","css-1jnehb1 e1aypx0f0",0)
def Energy_Groove():
    return Commercial1(browser,"https://www.iheart.com/live/energy-groove-6329/","css-1jnehb1 e1aypx0f0",0)
def Vision_Christian_Radio():
    return Commercial1(browser,"https://www.iheart.com/live/vision-christian-radio-9689/","css-1jnehb1 e1aypx0f0",0)
def Starter_FM():
    return Commercial1(browser,"https://www.iheart.com/live/starter-fm-9353/","css-1jnehb1 e1aypx0f0",0)
def _2ME():
    return Commercial1(browser,"https://www.iheart.com/live/2me-10143/","css-1jnehb1 e1aypx0f0",0)
def SBS_PopAsia():
    return Commercial1(browser,"https://www.iheart.com/live/sbs-popasia-7028/","css-1jnehb1 e1aypx0f0",0)
def _3MBS_Fine_Music_Melbourne():
    return Commercial1(browser,"https://www.iheart.com/live/3mbs-fine-music-melbourne-6183/","css-1jnehb1 e1aypx0f0",0)
def Golden_Days_Radio():
    return Commercial1(browser,"https://www.iheart.com/live/golden-days-radio-8676/","css-1jnehb1 e1aypx0f0",0)
def PBS_106_7FM():
    return Commercial1(browser,"https://www.iheart.com/live/pbs-1067fm-6316/","css-1jnehb1 e1aypx0f0",0)
def smoothfm_953_Sydney():
    return Commercial1(browser,"https://smooth.com.au/station/smoothsydney","index_smooth_info-wrapper-desktop__6ZYTT",1)
def smooth_VINTAGE():
    return Commercial1(browser,"https://smooth.com.au/station/smoothvintage","index_smooth_info-wrapper-desktop__6ZYTT",1)
def smooth_relax():
    return Commercial1(browser,"https://smooth.com.au/station/smoothrelax","index_smooth_info-wrapper-desktop__6ZYTT",1)
def smooth_80s():
    return Commercial1(browser,"https://smooth.com.au/station/smooth80s","index_smooth_info-wrapper-desktop__6ZYTT",1)
def smoothfm_Adelaide():
    return Commercial1(browser,"https://smooth.com.au/station/adelaide","index_smooth_info-wrapper-desktop__6ZYTT",1)
def smoothfm_915_Melbourne():
    return Commercial1(browser,"https://smooth.com.au/station/smoothfm915","index_smooth_info-wrapper-desktop__6ZYTT",1)
def smoothfm_Brisbane():
    return Commercial1(browser,"https://smooth.com.au/station/brisbane","index_smooth_info-wrapper-desktop__6ZYTT",1)
def smoothfm_Perth():
    return Commercial1(browser,"https://smooth.com.au/station/smoothfmperth","index_smooth_info-wrapper-desktop__6ZYTT",1)
def nova_969_Sydney():
    return Commercial1(browser,"https://novafm.com.au/station/nova969","index_nova_info-wrapper-desktop__CWW5R",1)
def nova_90s():
    return Commercial1(browser,"https://novafm.com.au/station/nova90s","index_nova_info-wrapper-desktop__CWW5R",1)
def nova_THROWBACKS():
    return Commercial1(browser,"https://novafm.com.au/station/throwbacks","index_nova_info-wrapper-desktop__CWW5R",1)
def nova_FreshCOUNTRY():
    return Commercial1(browser,"https://novafm.com.au/station/novafreshcountry","index_nova_info-wrapper-desktop__CWW5R",1)
def nova_NATION():
    return Commercial1(browser,"https://novafm.com.au/station/novanation","index_nova_info-wrapper-desktop__CWW5R",1)
def nova_919_Adelaide():
    return Commercial1(browser,"https://novafm.com.au/station/nova919","index_nova_info-wrapper-desktop__CWW5R",1)
def nova_100_Melbourne():
    return Commercial1(browser,"https://novafm.com.au/station/nova100","index_nova_info-wrapper-desktop__CWW5R",1)
def nova_1069_Brisbane():
    return Commercial1(browser,"https://novafm.com.au/station/nova1069","index_nova_info-wrapper-desktop__CWW5R",1)
def nova_937_Perth():
    return Commercial1(browser,"https://novafm.com.au/station/nova937","index_nova_info-wrapper-desktop__CWW5R",1)
def _2GB_SYDNEY():
    return Commercial2(browser,"https://www.radio-australia.org/2gb")
def _2GN_GOULBURN():
    return Commercial2(browser,"https://www.radio-australia.org/2gn")
def bbc_radio_1():
    return Commercial2(browser,"https://www.radio-uk.co.uk/bbc-radio-1")
def bbc_radio_2():
    return Commercial2(browser,"https://www.radio-uk.co.uk/bbc-radio-2")
def bbc_radio_3():
    return Commercial2(browser,"https://www.radio-uk.co.uk/bbc-radio-3")
def bbc_radio_4():
    return Commercial2(browser,"https://www.radio-uk.co.uk/bbc-radio-4")
def bbc_radio_5_live():
    return Commercial2(browser,"https://www.radio-uk.co.uk/bbc-radio-5-live")
def _1000_hits_classical_music():
    return Commercial2(browser,"https://www.fmradiofree.com/1000-hits-classical-music")
def classic_fm():
    return Commercial2(browser,"https://www.radio-uk.co.uk/classic-fm")
def klassik_radio():
    return Commercial2(browser,"https://www.internetradio-horen.de/klassik-radio")
def klassik_radio_pure_bach():
    return Commercial2(browser,"https://www.internetradio-horen.de/klassik-radio-pure-bach")
def klassik_radio_pure_beethoven():
    return Commercial2(browser,"https://www.internetradio-horen.de/klassik-radio-pure-beethoven")
def klassik_radio_pure_mozart():
    return Commercial2(browser,"https://www.internetradio-horen.de/klassik-radio-pure-mozart")
def klassik_radio_pure_verdi():
    return Commercial2(browser,"https://www.internetradio-horen.de/klassik-radio-pure-verdi")
def epic_piano_chopin():
    return Commercial2(browser,"https://www.internetradio-horen.de/epic-piano-chopin")

# END ************************************************************
# INDIVIDUAL FUNCTION DEFINITIONS FOR EACH AVAILABLE RADIO STATION



# 2D array of radio station information in [long name, calling function] format
# clearly this can be varied if you wish to listen to different stations
# Currently we Have 83 ABC stations and 108 in total!
aStation = [
    ["ABC Radio Sydney NSW",ABC_Radio_Sydney_NSW],
    ["ABC Broken Hill NSW",ABC_Broken_Hill_NSW],
    ["ABC Central Coast NSW",ABC_Central_Coast_NSW],
    ["ABC Central West NSW",ABC_Central_West_NSW],
    ["ABC Coffs Coast NSW",ABC_Coffs_Coast_NSW],
    ["ABC Illawarra NSW",ABC_Illawarra_NSW],
    ["ABC Mid North Coast NSW",ABC_Mid_North_Coast_NSW],
    ["ABC New England North West NSW",ABC_New_England_North_West_NSW],
    ["ABC Newcastle NSW",ABC_Newcastle_NSW],
    ["ABC North Coast NSW",ABC_North_Coast_NSW],
    ["ABC Riverina NSW",ABC_Riverina_NSW],
    ["ABC South East NSW",ABC_South_East_NSW],
    ["ABC Upper Hunter NSW",ABC_Upper_Hunter_NSW],
    ["ABC Western Plains NSW",ABC_Western_Plains_NSW],
    ["ABC Radio Canberra ACT",ABC_Radio_Canberra_ACT],
    ["ABC Radio Darwin NT",ABC_Radio_Darwin_NT],
    ["ABC Alice Springs NT",ABC_Alice_Springs_NT],
    ["ABC Radio Melbourne VIC",ABC_Radio_Melbourne_VIC],
    ["ABC Ballarat VIC",ABC_Ballarat_VIC],
    ["ABC Central Victoria VIC",ABC_Central_Victoria_VIC],
    ["ABC Gippsland VIC",ABC_Gippsland_VIC],
    ["ABC Goulburn Murray VIC",ABC_Goulburn_Murray_VIC],
    ["ABC Mildura-Swan Hill VIC",ABC_Mildura_Swan_Hill_VIC],
    ["ABC Shepparton VIC",ABC_Shepparton_VIC],
    ["ABC South West Victoria VIC",ABC_South_West_Victoria_VIC],
    ["ABC Wimmera VIC",ABC_Wimmera_VIC],
    ["ABC Radio Adelaide SA",ABC_Radio_Adelaide_SA],
    ["ABC Eyre Peninsula SA",ABC_Eyre_Peninsula_SA],
    ["ABC North and West SA",ABC_North_and_West_SA],
    ["ABC Riverland SA",ABC_Riverland_SA],
    ["ABC South East SA",ABC_South_East_SA],
    ["ABC Radio Hobart TAS",ABC_Radio_Hobart_TAS],
    ["ABC Northern Tasmania TAS",ABC_Northern_Tasmania_TAS],
    ["ABC Radio Brisbane QLD",ABC_Radio_Brisbane_QLD],
    ["ABC Capricornia QLD",ABC_Capricornia_QLD],
    ["ABC Far North QLD",ABC_Far_North_QLD],
    ["ABC Gold Coast QLD",ABC_Gold_Coast_QLD],
    ["ABC North Queensland QLD",ABC_North_Queensland_QLD],
    ["ABC North West Queensland QLD",ABC_North_West_Queensland_QLD],
    ["ABC Southern Queensland QLD",ABC_Southern_Queensland_QLD],
    ["ABC Sunshine Coast QLD",ABC_Sunshine_Coast_QLD],
    ["ABC Tropical North QLD",ABC_Tropical_North_QLD],
    ["ABC Western Queensland QLD",ABC_Western_Queensland_QLD],
    ["ABC Wide Bay QLD",ABC_Wide_Bay_QLD],
    ["ABC Radio Perth WA",ABC_Radio_Perth_WA],
    ["ABC Esperance WA",ABC_Esperance_WA],
    ["ABC Goldfields WA",ABC_Goldfields_WA],
    ["ABC Great Southern WA",ABC_Great_Southern_WA],
    ["ABC Kimberley WA",ABC_Kimberley_WA],
    ["ABC Midwest & Wheatbelt WA",ABC_Midwest_and_Wheatbelt_WA],
    ["ABC Pilbara WA",ABC_Pilbara_WA],
    ["ABC South West WA",ABC_South_West_WA],
    ["ABC NewsRadio",ABC_NewsRadio],
    ["ABC Radio National LIVE",ABC_Radio_National_LIVE],
    ["ABC Radio National QLD",ABC_Radio_National_QLD],
    ["ABC Radio National WA",ABC_Radio_National_WA],
    ["ABC Radio National SA",ABC_Radio_National_SA],
    ["ABC Radio National NT",ABC_Radio_National_NT],
    ["ABC SPORT",ABC_SPORT],
    ["ABC triple j LIVE",ABC_triple_j_LIVE],
    ["ABC triple j QLD",ABC_triple_j_QLD],
    ["ABC triple j WA",ABC_triple_j_WA],
    ["ABC triple j SA",ABC_triple_j_SA],
    ["ABC triple j NT",ABC_triple_j_NT],
    ["ABC triple j Hottest",ABC_triple_j_Hottest],
    ["ABC triple j Unearthed",ABC_triple_j_Unearthed],
    ["ABC Double j LIVE",ABC_Double_j_LIVE],
    ["ABC Double j QLD",ABC_Double_j_QLD],
    ["ABC Double j WA",ABC_Double_j_WA],
    ["ABC Double j SA",ABC_Double_j_SA],
    ["ABC Double j NT",ABC_Double_j_NT],
    ["ABC Classic LIVE",ABC_Classic_LIVE],
    ["ABC Classic QLD",ABC_Classic_QLD],
    ["ABC Classic WA",ABC_Classic_WA],
    ["ABC Classic SA",ABC_Classic_SA],
    ["ABC Classic NT",ABC_Classic_NT],
    ["ABC Classic2",ABC_Classic2],
    ["ABC Jazz",ABC_Jazz],    ["ABC Country",ABC_Country],
    ["ABC Kids listen",ABC_Kids_listen],
    ["ABC Radio Australia",ABC_Radio_Australia],
    ["KIIS 1065",KIIS1065],
    ["GOLD101.7",GOLD1017],
    ["CADA",CADA],
    ["iHeartCountry Australia",iHeartCountry_Australia],
    ["KIIS 90s",KIIS_90s],
    ["GOLD 80s",GOLD_80s],
    ["iHeartRadio Countdown AUS",iHeartRadio_Countdown_AUS],
    ["TikTok Trending on iHeartRadio",TikTok_Trending_on_iHeartRadio],
    ["iHeartDance",iHeartDance],
    ["The Bounce",The_Bounce],
    ["iHeartAustralia",iHeartAustralia],
    ["fbi.radio",fbi_radio],
    ["2SER",_2SER],
    ["2MBS Fine Music Sydney",_2MBS_Fine_Music_Sydney],
    ["KIX Country",KIX_Country],
    ["SBS Chill",SBS_Chill],
    ["Vintage FM",Vintage_FM],
    ["My88 FM",My88_FM],
    ["Hope 103.2",Hope_103_2],
    ["The 90s iHeartRadio",The_90s_iHeartRadio],
    ["The 80s iHeartRadio",The_80s_iHeartRadio],
    ["Mix 102.3",Mix_102_3],
    ["Cruise 1323",Cruise_1323],
    ["Mix 80s",Mix_80s],
    ["ABC Sport",ABC_Sport],
    ["ABC Sport Extra",ABC_Sport_Extra],
    ["Energy Groove",Energy_Groove],
    ["Vision Christian Radio",Vision_Christian_Radio],
    ["Starter FM",Starter_FM],
    ["2ME",_2ME],
    ["SBS PopAsia",SBS_PopAsia],
    ["3MBS Fine Music Melbourne",_3MBS_Fine_Music_Melbourne],
    ["Golden Days Radio",Golden_Days_Radio],
    ["PBS 106.7FM",PBS_106_7FM],
    ["smoothfm 95.3 Sydney",smoothfm_953_Sydney],
    ["smoothfm 91.5 Melbourne",smoothfm_915_Melbourne],
    ["smoothfm Adelaide",smoothfm_Adelaide],
    ["smoothfm Brisbane",smoothfm_Brisbane],
    ["smoothfm Perth",smoothfm_Perth],
    ["smooth 80s",smooth_80s],
    ["smooth relax",smooth_relax],
    ["smooth VINTAGE",smooth_VINTAGE],
    ["nova 969 Sydney",nova_969_Sydney],
    ["nova 100 Melbourne",nova_100_Melbourne],
    ["nova 919 Adelaide",nova_919_Adelaide],
    ["nova 1069 Brisbane",nova_1069_Brisbane],
    ["nova 937 Perth",nova_937_Perth],
    ["nova 90s",nova_90s],
    ["nova THROWBACKS",nova_THROWBACKS],
    ["nova FreshCOUNTRY",nova_FreshCOUNTRY],
    ["nova NATION",nova_NATION],
    ["2GB SYDNEY",_2GB_SYDNEY],
    ["2GN GOULBURN",_2GN_GOULBURN],
    ["bbc radio 1",bbc_radio_1],
    ["bbc radio 2",bbc_radio_2],
    ["bbc radio 3",bbc_radio_3],
    ["bbc radio 4",bbc_radio_4],
    ["bbc radio 5 live",bbc_radio_5_live],
    ["1000 hits classical music",_1000_hits_classical_music],
    ["classic fm",classic_fm],
    ["klassik radio",klassik_radio],
    ["klassik radio pure bach",klassik_radio_pure_bach],
    ["klassik radio pure beethoven",klassik_radio_pure_beethoven],
    ["klassik radio pure mozart",klassik_radio_pure_mozart],
    ["klassik radio pure verdi",klassik_radio_pure_verdi],
    ["epic piano chopin",epic_piano_chopin]
] 

# 2D array of preset radio stations, in long name and index (to aStation[]) format.
# this is the default, but is actually copied from file at statup and saved to file on exit!
aStation2 = []
for i in range(numButtons):
    station = ["-- EMPTY " + str(i) +" --", -1]
    aStation2.append(station)


# after gui is initialised and we are running in the root thread
def after_GUI_started():
   
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
        BTstatusButton.config(text="BT ON")
        BTstatusButton.config(bg="light green")
    else: # onBluetooth==False
        subprocess_run("sudo systemctl disable bluetooth")                        
        subprocess_run("sudo systemctl stop bluetooth")                        
        BTstatusButton.config(text="BT OFF")
        BTstatusButton.config(bg="light coral")
      
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
    GPIO.cleanup()
    browser.quit() # close the WebDriver
    root.destroy() # destroy GUI   
    print("Closing the app...")


# do this when a radio station is selected from combobox
def on_select(event):
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

    # setting stop flag, this prevents on_select() from running again
    # "mysterious" code due to timing issues
    if eventFlag:
        stopFlag = False

        # inform user that a station is being started
        text = "Please be patient, the station *" +  aStation[combobox_index][0] + "*is being started"
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
            text = aStation[combobox_index][1]() # THIS BIT ACTUALLY STARTS STREAM
            fullStationName = aStation[combobox_index][0] 
            text = fullStationName + "*" + text
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
            if pollFlag:
                root.after(int(refreshTime*1000), lambda: on_select(CustomEvent("Manual", combobox, "Manual from combobox")))
            print("FINISHED RUNNING ROOT")
            print("")

        except urllib.error.HTTPError as e:
            event.type = "Manual" # to prevent saving of buttonIndex

            # inform user that starting station has failed in some way
            text = "<<< ERROR >>>*" + aStation[combobox_index][0] + "*failed to load properly*"
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

    # setting stop flag, this prevents on_select2 from running again
    # "mysterious" code due to timing issues
    if eventFlag:
        stopFlag = False

        if selected_index != -1:
            # inform user that a station is being started
            text = "Please be patient, the station *" +  aStation[selected_index][0] + "*is being started"
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
                text = (aStation[selected_index][1])() # this uses the eventFlag
                fullStationName = aStation[selected_index][0] 
                text = fullStationName + "*" + text
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
                    combobox.set(fullStationName)
                    combobox.focus_set()
                    combobox.selection_clear()
                    buttons[buttonIndex].focus_set()
                
                print("JUST ABOUT TO RUN ROOT")
                eventFlag = False
                if pollFlag:
                    root.after(int(refreshTime*1000), lambda: on_select2(CustomEvent("Manual", buttons[buttonIndex], "Manual from buttons")))
                print("FINISHED RUNNING ROOT")
                print("")

            except urllib.error.HTTPError as e:
                event.type = "Manual" # to prevent saving of buttonIndex

                # inform user that starting station has failed in some way
                text = "<<< ERROR >>>*" + aStation[selected_index][0] + "*failed to load properly*"
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
            scaled_image2 = image.resize((Xprog-55, Xprog-55))  # Adjust the size as needed
            photo2 = ImageTk.PhotoImage(scaled_image2)
            label2.config(image=photo2)
            label2.image = photo2  # Keep a reference to avoid garbage collection
            label2.place(x=Xgap+55, y=Ygap2+30)  # Adjust the position
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
    buttons[i].config(relief="sunken", bg="darkgray")  # Simulate button press
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
    #combobox.config(style="ComboFocusOn")    
    combobox.update_idletasks()  # Force update
    print("on_focus_combobox")


# called when station combobox loses focus.
# makes sure its display is updated.
def on_focus_out_combobox(event):
    #combobox.config(style="ComboFocusOff")
    combobox.update_idletasks()  # Force update
    print("on_focus_out_combobox")


# called when bluetooth device selection combobox_bt receives focus.
# makes sure its display is updated.
def on_focus_combobox_bt(event):
    combobox_bt.update_idletasks()  # Force update
    print("on_focus_combobox_bt")


# called when bluetooth device selection combobox_bt loses focus.
# makes sure its display is updated.
def on_focus_out_combobox_bt(event):
    combobox_bt.update_idletasks()  # Force update
    print("on_focus_out_combobox_bt")


# called when wifi connection device selection combobox_wifi receives focus.
# makes sure its display is updated.
def on_focus_combobox_wifi(event):
    combobox_wifi.update_idletasks()  # Force update
    print("on_focus_combobox_wifi")


# called when wifi connection device selection combobox_wifi loses focus.
# makes sure its display is updated.
def on_focus_out_combobox_wifi(event):
    combobox_wifi.update_idletasks()  # Force update
    print("on_focus_out_combobox_wifi")



# show the setup form (over the top of the main window)
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
        selected_device = combobox_bt.get()
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

    combobox_bt['values'] = aPairable
    global numPairable; numPairable = len(aPairable)
    if numPairable==0:
        label3.config(text="No Bluetooth devices found")
    else:    
        combobox_bt.current(0)
        combobox_bt.focus_set()
        if len(aPairable)==1:
            label3.config(text=f"Found 1 device")
        else:
            label3.config(text=f"Found {numPairable} devices")
    print(f"Found {numPairable} device(s)\n")
    label6.config(text="")
    

# when [combobox_wifi] selected
# Use current selection from the combobox to connect to the internet
def on_select_wifi(event):
    global sSSID
    try:
        print("ACTUAL WIFI CONNECTING STARTS HERE")
        label5.config(text=f"WAITING TO CONNECT - please be patient!")
        setup.update_idletasks()
        selected_wifi = combobox_wifi.get()
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
    command = f'sudo nmcli con up id "{sSSID}"'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    time.sleep(2)
    returnCode = result.returncode
    if returnCode == 0:      # success
        print(f"Command '{command}' succeeded")
        label5.config(text=f"Just connected to: {sSSID}")

        # need to reload last streaming station 
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

    command = f'sudo nmcli dev wifi connect "{sSSID}" password "{sPassword}"'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    time.sleep(2)
    returnCode = result.returncode
    if returnCode == 0:      # success
        print(f"Command '{command}' succeeded")
        label5.config(text=f"Just connected to: {sSSID}")

        # need to reload last streaming station 
        on_select2(CustomEvent("Auto", buttons[buttonIndex], "Auto from GUI start"))
        root.after(100,lambda: mainButton.focus_set()) 
    else: # fail, can try with a new password or not
        print(f"Command '{command}' FAILED, need password")
        label5.config(text=f"Incorrect password for {sSSID} - try again?")
        root.after(100,lambda: wifiPassword.focus_set()) 


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

    combobox_wifi['values'] = aWIFI
    global numWIFI; numWIFI = len(aWIFI)
    if numWIFI==0:
        label5.config(text="No visible wifi networks found")
    else:    
        combobox_wifi.current(0)
        combobox_wifi.focus_set()
        if numWIFI==1:
            label5.config(text=f"Found 1 visible wifi network")
        else:
            label5.config(text=f"Found {numWIFI} visible wifi networks")
    print(f"Found {numWIFI} visible wifi network(s)\n")
    label6.config(text="")


def key_handler(event):
    print(f"Key pressed: {event.keysym}")


##########################################
### THIS IS WHERE THE CORE CODE STARTS ###

# Create the main window
# Set title, size and position of the main window, and make it non-resizable
root = tk.Tk()
root.title("INTERNET RADIO - https://github.com/namor5772/TkRadio")  
root.geometry("800x455+0+0")
#root.overrideredirect(True)
root.resizable(False, False)
root.update_idletasks()

# Create a list of labels for the root/main form to display pressable keys. They are
# at the top of the main form (one bank of sizeBank keys is displayed at a time)
labels_main = []
for i in range(sizeBank):
    label_main = tk.Label(root, text=KeyList[i][0], font=("Arial", 12), bg="darkgray")
    label_main.place(x=10+52*i, y=0, width=50, height=20)
    labels_main.append(label_main)
labels_main[indexKeyList].config(bg="lightblue")    

# Create a combobox (dropdown list)
# Used to display all avialable radio stations
aStringArray = []
for element in aStation:
    aStringArray.append(element[0])
combobox = ttk.Combobox(root, values=aStringArray, height=20*0+25, width=32)
combobox.place(x=130+(sizeButton+5), y=2+30)  # Adjust the position
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
text_box.place(x=10, y=110+30+Ydown, width=Xgap-20+30+25, height=Xprog-30-25)
text_box.config(state=tk.NORMAL) # Enable the text box to insert text

# Create a button on the root form to display the secondary setup form
setupButton = tk.Button(root, text="+")
setupButton.place(x=775, y=24, width=20, height=20)
setupButton.config(takefocus=True)
setupButton.bind("<Return>", show_setup_form)  
setupButton.bind("<ButtonPress>", show_setup_form)  
   
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


# SECONDARY setup FORM RELATED DEFINITIONS
# *** START ******************************

# Create a secondary setup form without title bar and close buttons
# It will be used for examining and configuring setup settings
setup = tk.Toplevel(root)
#setup.geometry("800x480+0+26")
setup.geometry("800x430+0+50")
setup.overrideredirect(True)
setup.withdraw() # Hide the form initially

# button which returns focus and visibility back to the main/root form
mainButton = tk.Button(setup, text="+")
mainButton.place(x=775, y=0, width=20, height=20)
mainButton.config(takefocus=True)
mainButton.bind("<Return>", show_root_form)  
mainButton.bind("<ButtonPress>", show_root_form)  

# button to toggle bluetooth connection on/off
BTstatusButton = tk.Button(setup, text="NONE") 
BTstatusButton.place(x=15, y=10+25, height=25)
BTstatusButton.config(takefocus=True)
BTstatusButton.bind("<Return>", toggle_bluetooth)  
BTstatusButton.bind("<ButtonPress>", toggle_bluetooth)  

# button & label to connect to currently paired bluetooth speakers
cX = 15; cY = 10+25+30
connectButton = tk.Button(setup, text="CONNECT") 
connectButton.place(x=cX, y=cY, height=25)
connectButton.config(takefocus=True)
connectButton.bind("<Return>", _connect_bluetooth)  
connectButton.bind("<ButtonPress>", _connect_bluetooth)  
label4 = tk.Label(setup, text="")
label4.place(x=cX+100, y=cY+2)

# Create a Combobox for bluetooth connection selection & related information label
cX = 15; cY = 125
label3 = tk.Label(setup, text="")
label3.place(x=cX+1, y=cY)
options = [""]
combobox_bt = ttk.Combobox(setup, values=options, height=25, width=40)
combobox_bt.place(x = cX, y = cY+30)
combobox_bt.current(0)
combobox_bt.bind("<FocusIn>", on_focus_combobox_bt)
combobox_bt.bind("<FocusOut>", on_focus_out_combobox_bt)
combobox_bt.bind("<<ComboboxSelected>>", lambda e: on_select_bluetooth(CustomEvent("Auto", combobox_bt, "ComboBox Event")))
combobox_bt.config(state="readonly")

# button to enable scanning for bluetooth devices (which will appear in above combobox)
pairButton = tk.Button(setup, text="SEE BT DEVICES") 
pairButton.place(x=cX, y=cY+60, height=25)
pairButton.config(takefocus=True)
pairButton.bind("<Return>", pair_bluetooth)  
pairButton.bind("<ButtonPress>", pair_bluetooth)
label6 = tk.Label(setup, text="")
label6.place(x=cX+150, y=cY+62)

# vertical separator, between bluetooth an dwifi setup sections
separator = ttk.Separator(setup, orient="vertical")
separator.place(relx=0.5, rely=0, relheight=1, anchor="n")  # Positioned in the center

# Create a Combobox for wifi connection selection
options2 = [""]
label5 = tk.Label(setup, text="")
label5.place(x=cX+1+400, y=cY-30)
combobox_wifi = ttk.Combobox(setup, values=options2, height=25, width=40)
combobox_wifi.place(x = cX+400, y = cY)
combobox_wifi.current(0)
combobox_wifi.bind("<FocusIn>", on_focus_combobox_wifi)
combobox_wifi.bind("<FocusOut>", on_focus_out_combobox_wifi)
combobox_wifi.bind("<<ComboboxSelected>>", lambda e: on_select_wifi(CustomEvent("Auto", combobox_wifi, "ComboBox Event")))
combobox_wifi.config(state="readonly")

# text entry for wifi password, and its info label
wifiPassword = tk.Entry(setup, width=30)
wifiPassword.place(x=cX+400+75, y=cY+30)
wifiPassword.bind("<Return>", process_wifiPassword)
label_wifiPassword = tk.Label(setup, text="Password:")
label_wifiPassword.place(x=cX+400, y=cY+30)

# button to enable scanning for wifi devices (which will appear in above combobox)
wifiButton = tk.Button(setup, text="SEE WIFI") 
wifiButton.place(x=cX+400, y=cY+60, height=25)
wifiButton.config(takefocus=True)
wifiButton.bind("<Return>", find_wifi)  
wifiButton.bind("<ButtonPress>", find_wifi)
label7 = tk.Label(setup, text="")
label7.place(x=cX+400+100, y=cY+62)

tButton = tk.Button(setup, text="TEST") 
tButton.place(x=cX+400, y=cY+60+60, height=25)
tButton.config(takefocus=True)
tButton.bind("<Key>", key_handler)  

# SECONDARY setup FORM RELATED DEFINITIONS
# *** END ********************************


# doing stuff just after the gui is initialised and we are running in the root thread
root.after(1000, after_GUI_started)
print("Radio stream interface")

# Bind the closing event to the on_closing function
root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the GUI loop
root.mainloop()
print("out of GUI loop..")
