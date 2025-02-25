import subprocess
import inspect
import tkinter as tk
import time
import urllib.request
import requests
import os
import csv
import svglib
import reportlab


from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
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
#firefox_options.add_argument("-headless")  # Ensure this argument is correct
browser = webdriver.Firefox(options=firefox_options)

# 'cleans' browser between station websites
refresh_http = "http://www.ri.com.au" # use my basic "empty" website

# global graphis position variables
Ygap = 10;  Ygap2 = 110; Ygap3 = 110
Xgap = 560-70; Xgap2 = 560-70; Xgap3 = 560-70
Xprog = 300

# global variables for combobox selection indexes & button related
numButtons = 10
sizeButton = 62
combobox_index = -1
buttonIndex = -1
addFlag = False


# START ***** Functions that stream radio stations *****

# ALL GOOD
def Radio1(br,Num,sPath):
    stack = inspect.stack()
    station = inspect.stack()[1].function
    logo = station + ".png"
    print(logo)
    print("--")
    
    br.get(refresh_http)
    time.sleep(2)

    br.get(sPath)
    time.sleep(1)
    be = br.find_element(By.TAG_NAME, 'body')
    for _ in range(Num):
        be.send_keys(Keys.TAB)
    be.send_keys(Keys.ENTER)
    time.sleep(1)
    
  # get station logo
    image_path3 = pathImages
    image_path3 = image_path3 + "/" + logo
    image = Image.open(image_path3)
    scaled_image = image.resize((90, 90))  # Adjust the size as needed

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

  # get song image
    try:
        img2_element = be.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div[1]/div/div/div[2]/div[1]/div/div[2]/div[2]/img')
        img2_url = img2_element.get_attribute("src")
        image2_path = pathImages + "/presenter.jpg"
        urllib.request.urlretrieve(img2_url, image2_path)
    except NoSuchElementException:
        print("Image element not found on the webpage.")            
        # Display a blank image
        image2_path = pathImages + "/Blank.png"
    # Display the program image as given in the image2_path global variable
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
    
  # Find program details
    ht = be.get_attribute('innerHTML')
    soup = BeautifulSoup(ht, 'lxml')
    fe = soup.find(attrs={"class": "view-live-now popup"})
    if fe is not None:
        fe1 = fe.get_text(separator="*", strip=True)
    else:
        fe1 = "None"
    print(fe1)    
    # Remove irrelevant info, starting with [*More]
    sub = "*More"
    pos = fe1.find(sub)
    if pos != -1:
        fe1 = fe1[:pos]
    print(fe1)    
    sub = "More from*"
    fe1 = fe1.replace(sub,"")
    print(fe1)    
    sub = "*."
    fe1 = fe1.replace(sub,"")
    print(fe1)    
        
  # find song details    
    fe = soup.find(attrs={"class": "playingNow"})
    if fe is not None:
        fe2 = fe.get_text(separator="*", strip=True)
    else:
        fe2 = "No specific item playing"
    fe3 = fe1+"*"+fe2
    return fe3


# ALL GOOD
def Radio2(br,Num,sPath):
    br.get(refresh_http)
    time.sleep(2)

    br.get(sPath)
    time.sleep(1)
    be = br.find_element(By.TAG_NAME, 'body')
    for _ in range(3):
        be.send_keys(Keys.TAB)
    be.send_keys(Keys.ENTER)
    for _ in range(4):
        be.send_keys(Keys.UP)
    for _ in range(Num):
        be.send_keys(Keys.DOWN)
    be.send_keys(Keys.ENTER)
    for _ in range(3):
        be.send_keys(Keys.TAB)
    be.send_keys(Keys.ENTER)
    time.sleep(1)

  # get station logo
    image_path2 = pathImages + "/ABC_Radio_National.png"
    image = Image.open(image_path2)
    scaled_image = image.resize((90, 90))  # Adjust the size as needed

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

  # get presenter image
    img2_element = be.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div[1]/div/div/header/div/div/img')
    img2_url = img2_element.get_attribute("src")
    image2_path = pathImages + "/presenter.jpg"
    urllib.request.urlretrieve(img2_url, image2_path)
    # Display the station presenter as given in the image2_path global variable
    image2 = Image.open(image2_path)
    width2, height2 = image2.size;
    print(f"width: {width2}, height: {height2}")
    width = int(Xprog*width2/height2)
    scaled_image2 = image2.resize((width, Xprog))  # Adjust the size as needed
    photo2 = ImageTk.PhotoImage(scaled_image2)
    label2.config(image=photo2)
    label2.image = photo2  # Keep a reference to avoid garbage collection
    label2.place(x=Xgap3-(width-Xprog), y=Ygap2)  # Adjust the position
    
  # Find stream details
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


# ALL GOOD
def Radio3(br,Num,sPath):
    stack = inspect.stack()
    station = inspect.stack()[1].function
    first_occurrence = station.find("_")
    second_occurrence = station.find("_", first_occurrence+1)
    station_short = station[:second_occurrence]
    logo = station_short + ".png"
    print(logo)
    print("--")

    br.get(refresh_http)
    time.sleep(2)

    br.get(sPath)
    time.sleep(1)
    be = br.find_element(By.TAG_NAME, 'body')
    for _ in range(5):
        be.send_keys(Keys.TAB)
    be.send_keys(Keys.ENTER)
    for _ in range(4):
        be.send_keys(Keys.UP)
    for _ in range(Num):
        be.send_keys(Keys.DOWN)
    be.send_keys(Keys.ENTER)
    for _ in range(3):
        be.send_keys(Keys.TAB)
    be.send_keys(Keys.ENTER)
    time.sleep(1)

  # get station logo
    image_path3 = pathImages + "/" + logo
    image = Image.open(image_path3)
    scaled_image = image.resize((90, 90))  # Adjust the size as needed

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
    # Display the program image as given in the image2_path global variable
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

  # Find program details
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
    # find song details    
    fe = soup.find(attrs={"class": "playingNow"})
    if fe is not None:
        fe2 = fe.get_text(separator="*", strip=True)
    else:
        fe2 = "No specific item playing"
    fe3 = fe1+"*"+fe2
    return fe3


# ALL GOOD
def Radio4(br,sPath):
    br.get(refresh_http)
    time.sleep(2)

    br.get(sPath)
    time.sleep(1)
    be = br.find_element(By.TAG_NAME, 'body')
    be.send_keys(Keys.TAB)
    be.send_keys(Keys.ENTER)
    for _ in range(3):
        be.send_keys(Keys.TAB)
        
  # adjust amount of tabbing depending on where you end up!
    Adjusted = False
    focused_element = br.execute_script("return document.activeElement")
    if not("Button_btn___qFSk" in focused_element.get_attribute('class')):
           be.send_keys(Keys.SHIFT,Keys.TAB)
           Adjusted = True
           print("ADJUSTED TAB")
    be.send_keys(Keys.ENTER)
    be.send_keys(Keys.SHIFT,Keys.TAB)
    be.send_keys(Keys.TAB)
    be.send_keys(Keys.TAB)
    time.sleep(3)
    
  # get station logo
    img_element = be.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/main/div[1]/div/div/div/a/div/img')
    img_url = img_element.get_attribute("src")
    image_path = pathImages + "/logo.png"
    urllib.request.urlretrieve(img_url, image_path)
    image = Image.open(image_path)
    scaled_image = image.resize((90, 90))  # Adjust the size as needed

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
       
  # get presenter image
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
    # Display the station presenter as given in the image2_path global variable
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
    
  # Find live program details
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
    
  # Find live program synopsis
    fe = soup.find(attrs={"class": "LiveAudioSynopsis_content__DZ6E7"})
    if fe is not None:
        fe2 = fe.get_text(separator="*", strip=True)
    else:
        fe2 = "No Description"
    fe3 = fe3+"* * * * *"+fe2
    return fe3


# ALL GOOD    
def Radio5(br,sPath):
    br.get(refresh_http)
    time.sleep(2)

    browser.get(sPath)
    time.sleep(1)
    be = br.find_element(By.TAG_NAME, 'body')
    be.send_keys(Keys.TAB)
    be.send_keys(Keys.ENTER)
    for _ in range(3):
        be.send_keys(Keys.TAB)
        
  # adjust amount of tabbing depending on where you end up!
    Adjusted = False;
    focused_element = br.execute_script("return document.activeElement")
    if not("Button_btn___qFSk" in focused_element.get_attribute('class')):
           be.send_keys(Keys.SHIFT,Keys.TAB)
           Adjusted = True
           print("ADJUSTED TAB")
    be.send_keys(Keys.ENTER)
    be.send_keys(Keys.TAB)
    be.send_keys(Keys.TAB)
    time.sleep(1)

  # get station logo
    img_element = be.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/main/div[1]/div/div/div/a/div/img')
    img_url = img_element.get_attribute("src")
    image_path = pathImages + "/logo.png"
    urllib.request.urlretrieve(img_url, image_path)
    image = Image.open(image_path)
    scaled_image = image.resize((90, 90))  # Adjust the size as needed

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

  # get presenter image
    try:      
        img2_element = be.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div/main/div[1]/div/div/div/div[1]/div[1]/div/div/div/img')
        img2_url = img2_element.get_attribute("src")
        image2_path = pathImages + "/presenter.jpg"
        urllib.request.urlretrieve(img2_url, image2_path)
    except NoSuchElementException:
        print("Image element not found on the webpage.")            
        # Display a blank image
        image2_path = pathImages + "/ABC_faint.png"
    # Display the station presenter as given in the image2_path global variable
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

  # Find live program details
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
    
  # Find live program synopsis
    fe = soup.find(attrs={"class": "LiveAudioSynopsis_content__DZ6E7"})
    if fe is not None:
        fe2 = fe.get_text(separator="*", strip=True)
    else:
        fe2 = "No Description"
    fe3 = fe3+"* * * * *"+fe2
    return fe3



def Radio6(br,sPath):
    br.get(refresh_http)
    time.sleep(2)

    br.get(sPath)
    time.sleep(1)
    be = br.find_element(By.TAG_NAME, 'body')
    for _ in range(3):
        be.send_keys(Keys.TAB)
    be.send_keys(Keys.ENTER)
    time.sleep(1)

  # get station logo
    image_path3 = pathImages + "/ABC_Kids_listen.png"
    image = Image.open(image_path3)
    scaled_image = image.resize((90, 90))  # Adjust the size as needed

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
    # Display the program image as given in the image2_path global variable
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
    # Find song details     
    fe = soup.find(attrs={"class": "playingNow"})
    if fe is not None:
        fe2 = fe.get_text(separator="*", strip=True)
    else:
        fe2 = "No specific item playing"
    fe3 = fe1+"*"+fe2
    return fe3


def Radio7(br,Num,sPath):
    stack = inspect.stack()
    print("--")
    station = inspect.stack()[1].function
    logo = station + ".png"
    print(logo)
    print("--")

    br.get(refresh_http)
    time.sleep(2)

    br.get(sPath)
    time.sleep(1)
    be = br.find_element(By.TAG_NAME, 'body')
    be.send_keys(Keys.TAB)
    be.send_keys(Keys.ENTER)
    for _ in range(11):
        be.send_keys(Keys.TAB)
    if Num==0:
        be.send_keys(Keys.ENTER)
    elif Num==1:
        be.send_keys(Keys.TAB)
        be.send_keys(Keys.ENTER)
    else: # if Num==2
        be.send_keys(Keys.TAB)
        be.send_keys(Keys.TAB)
        be.send_keys(Keys.ENTER)
        be.send_keys(Keys.ENTER)
    time.sleep(1)

  # get station logo
    image_path3 = pathImages + "/" + logo
    image = Image.open(image_path3)
    scaled_image = image.resize((90, 90))  # Adjust the size as needed

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


def Radio8(br,sPath):
    br.refresh()
    br.get(sPath)
    fe2 = "GOLD 104.3"
    return fe2   


def Smooth(br,sPath):
    stack = inspect.stack()
    print("--")
    station = inspect.stack()[1].function
    logo = station + ".png"
    print(logo)
    print("--")
    
    br.get(refresh_http)
    time.sleep(2)
    br.get(sPath)
    time.sleep(5)
    be = br.find_element(By.TAG_NAME, 'body')
    time.sleep(5)

  # press button with virtual mouse to play stream
    window_size = br.get_window_size()
    print(f"Window size: width = {window_size['width']}, height = {window_size['height']}")
    actions = ActionChains(br)
    actions.move_by_offset(550, 575).click().perform()
    time.sleep(3)

    time.sleep(15) # DETERMINE TIME
  # get station logo
    #img_element = be.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div[1]/div[1]/a[1]/div/img')
    #img_url = img_element.get_attribute("src")
    image_path = pathImages + "/" + logo
   # Display the station logo as given in the image_path global variable
    image = Image.open(image_path)
    scaled_image = image.resize((90, 90))  # Adjust the size as needed

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



  # get song image
    img2_element = be.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div[1]/div[1]/img')
    img2_url = img2_element.get_attribute("src")
    image2_path = pathImages + "/presenter.jpg"
    urllib.request.urlretrieve(img2_url, image2_path)
    image2 = Image.open(image2_path)
    width2, height2 = image2.size;
    print(f"width: {width2}, height: {height2}")
    width = int(Xprog*width2/height2)
    scaled_image2 = image2.resize((width, Xprog))  # Adjust the size as needed
    photo2 = ImageTk.PhotoImage(scaled_image2)
    label2.config(image=photo2)
    label2.image = photo2  # Keep a reference to avoid garbage collection
    label2.place(x=Xgap3-(width-Xprog), y=Ygap2)  # Adjust the position

   
 
  # Find program and song details
    
    ht = be.get_attribute('innerHTML')
    soup = BeautifulSoup(ht, 'lxml')
#    fe = soup.find(attrs={"class": "smooth_music-container__R7rU3"})
    fe = soup.find(attrs={"class": "index_smooth_info-wrapper-desktop__6ZYTT"})
    if fe is not None:
        fe1 = fe.get_text(separator="*", strip=True)
    else:
        fe1 = "None"

    return fe1



def iHeart(br, sPath):
    br.get(refresh_http)
    time.sleep(2)
    br.get(sPath)
    be = br.find_element(By.TAG_NAME, 'body')
    time.sleep(2)

  # press button with virtual mouse to play stream
    window_size = br.get_window_size()
    print(f"Window size: width = {window_size['width']}, height = {window_size['height']}")
    actions = ActionChains(br)
    actions.move_by_offset(300, 250).click().perform()

  # get station logo
    img_element = be.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[1]/div/div/div[1]/div/div/img')
    img_url = img_element.get_attribute("src")
    image_path = pathImages + "/logo.png"
    urllib.request.urlretrieve(img_url, image_path)
    # Display the station logo as given in the image_path global variable
    image = Image.open(image_path)
    scaled_image = image.resize((90, 90))  # Adjust the size as needed

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


  # get song image
    img2_element = be.find_element(By.XPATH, '/html/body/div[1]/div[5]/div/div[1]/div[1]/div/img')
    img2_url = img2_element.get_attribute("src")
    image2_path = pathImages + "/presenter.jpg"
    urllib.request.urlretrieve(img2_url, image2_path)
    image2 = Image.open(image2_path)
    width2, height2 = image2.size;
    print(f"width: {width2}, height: {height2}")
    width = int(Xprog*width2/height2)
    scaled_image2 = image2.resize((width, Xprog))  # Adjust the size as needed
    photo2 = ImageTk.PhotoImage(scaled_image2)
    label2.config(image=photo2)
    label2.image = photo2  # Keep a reference to avoid garbage collection
    label2.place(x=Xgap3-(width-Xprog), y=Ygap2)  # Adjust the position


  # Find program and song details
    ht = be.get_attribute('innerHTML')
    soup = BeautifulSoup(ht, 'lxml')
    fe = soup.find(attrs={"class": "css-1jnehb1 e1aypx0f0"})
    if fe is not None:
        fe1 = fe.get_text(separator="*", strip=True)
    else:
        fe1 = "None"
    fe = soup.find(attrs={"class": "css-1dwaik6 e4xv9s30"})
    if fe is not None:
        fe2 = fe.get_text(separator="*", strip=True)
    else:
        fe2 = "None"
    fe3 = fe2+"* *"+fe1    
    return fe3



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
def ABC_SPORT():
    return Radio7(browser,0,"https://www.abc.net.au/news/sport/audio")
def ABC_SPORT_EXTRA():
    return Radio7(browser,1,"https://www.abc.net.au/news/sport/audio")
def ABC_CRICKET():
    return Radio7(browser,2,"https://www.abc.net.au/news/sport/audio")
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

# FIX - ABC Sport one less tab no graphic
def ABC_Radio_Australia():
    return Radio5(browser,"https://www.abc.net.au/pacific/live")

    
def KIIS1065():
    return iHeart(browser,"https://www.iheart.com/live/kiis-1065-6185/")
def GOLD1017():
    return iHeart(browser,"https://www.iheart.com/live/gold1017-6186/")
def CADA():
    return iHeart(browser,"https://www.iheart.com/live/cada-6179/")
def iHeartCountry_Australia():
    return iHeart(browser,"https://www.iheart.com/live/iheartcountry-australia-7222/")
def KIIS_90s():
    return iHeart(browser,"https://www.iheart.com/live/kiis-90s-10069/")
def GOLD_80s():
    return iHeart(browser,"https://www.iheart.com/live/gold-80s-10073/")    
def iHeartRadio_Countdown_AUS():
    return iHeart(browser,"https://www.iheart.com/live/iheartradio-countdown-aus-6902/")
def TikTok_Trending_on_iHeartRadio():
    return iHeart(browser,"https://www.iheart.com/live/tiktok-trending-on-iheartradio-8876/")
def iHeartDance():
    return iHeart(browser,"https://www.iheart.com/live/iheartdance-6941/")
def The_Bounce():
    return iHeart(browser,"https://www.iheart.com/live/the-bounce-6327/")
def iHeartAustralia():
    return iHeart(browser,"https://www.iheart.com/live/iheartaustralia-7050/")
def fbi_radio():
    return iHeart(browser,"https://www.iheart.com/live/fbiradio-6311/")
def _2SER():
    return iHeart(browser,"https://www.iheart.com/live/2ser-6324/")
def _2MBS_Fine_Music_Sydney():
    return iHeart(browser,"https://www.iheart.com/live/2mbs-fine-music-sydney-6312/")
def KIX_Country():
    return iHeart(browser,"https://www.iheart.com/live/kix-country-9315/")
def SBS_Chill():
    return iHeart(browser,"https://www.iheart.com/live/sbs-chill-7029/")
def Vintage_FM():
    return iHeart(browser,"https://www.iheart.com/live/vintage-fm-8865/")
def My88_FM():
    return iHeart(browser,"https://www.iheart.com/live/my88-fm-8866/")
def Hope_103_2():
    return iHeart(browser,"https://www.iheart.com/live/hope-1032-6314/")
def The_90s_iHeartRadio():
    return iHeart(browser,"https://www.iheart.com/live/the-90s-iheartradio-6793/")
def The_80s_iHeartRadio():
    return iHeart(browser,"https://www.iheart.com/live/the-80s-iheartradio-6794/")
def Mix_102_3():
    return iHeart(browser,"https://www.iheart.com/live/mix1023-6184/")
def Cruise_1323():
    return iHeart(browser,"https://www.iheart.com/live/cruise-1323-6177/")
def Mix_80s():
    return iHeart(browser,"https://www.iheart.com/live/mix-80s-10076/")
def Mix_90s():
    return iHeart(browser,"https://www.iheart.com/live/mix-90s-10072/")

def ABC_Sport():
    return iHeart(browser,"https://www.iheart.com/live/abc-sport-7112/")
def ABC_Sport_Extra():
    return iHeart(browser,"https://www.iheart.com/live/abc-sport-extra-10233/")
def Energy_Groove():
    return iHeart(browser,"https://www.iheart.com/live/energy-groove-6329/")
def Vision_Christian_Radio():
    return iHeart(browser,"https://www.iheart.com/live/vision-christian-radio-9689/")
def Starter_FM():
    return iHeart(browser,"https://www.iheart.com/live/starter-fm-9353/")
def _2ME():
    return iHeart(browser,"https://www.iheart.com/live/2me-10143/")
def SBS_PopAsia():
    return iHeart(browser,"https://www.iheart.com/live/sbs-popasia-7028/")
def _3MBS_Fine_Music_Melbourne():
    return iHeart(browser,"https://www.iheart.com/live/3mbs-fine-music-melbourne-6183/")
def Golden_Days_Radio():
    return iHeart(browser,"https://www.iheart.com/live/golden-days-radio-8676/")
def PBS_106_7FM():
    return iHeart(browser,"https://www.iheart.com/live/pbs-1067fm-6316/")

def smoothfm_953_Sydney():
    return Smooth(browser,"https://smooth.com.au/station/smoothsydney")
def smooth_VINTAGE():
    return Smooth(browser,"https://smooth.com.au/station/smoothvintage")
def smooth_relax():
    return Smooth(browser,"https://smooth.com.au/station/smoothrelax")
def smooth_80s():
    return Smooth(browser,"https://smooth.com.au/station/smooth80s")
def smoothfm_Adelaide():
    return Smooth(browser,"https://smooth.com.au/station/adelaide")
def smoothfm_915_Melbourne():
    return Smooth(browser,"https://smooth.com.au/station/smoothfm915")
def smoothfm_Brisbane():
    return Smooth(browser,"https://smooth.com.au/station/brisbane")
def smoothfm_Perth():
    return Smooth(browser,"https://smooth.com.au/station/smoothfmperth")







# END ******* Functions that stream radio stations *****


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
    ["ABC SPORT EXTRA",ABC_SPORT_EXTRA],
    ["ABC CRICKET",ABC_CRICKET],
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

    ["KISS 1065",KIIS1065],
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
    ["smoothfm Peth",smoothfm_Perth],
    ["smooth 80s",smooth_80s],
    ["smooth relax",smooth_relax],
    ["smooth VINTAGE",smooth_VINTAGE]

] 


# 2D an array of preset radio stations, in long name and index (to aStation[]) format    ["smooth 80s",smooth_80s]

# this is the default, but is actually copied from file at statup and saved to file on exit!
aStation2 = []
for i in range(numButtons):
    station = ["-- EMPTY " + str(i) +" --", -1]
    aStation2.append(station)


def after_GUI_started():
  # select last station after radio was last powered down
    global buttonIndex
    global buttonFlag; buttonFlag = True
    try:
        with open(filepath, 'r') as file:
            buttonIndex = int(file.read())
    except FileNotFoundError:
        print(f'Error: The file {filepath} does not exist.')
        buttonIndex = 0
    if buttonIndex == -1:
        buttonIndex = 0
    print(f'Index of last station played in playlist is {buttonIndex}')    
    on_select2(None)


# do this when closing the window/app
def on_closing():
    browser.quit() # close the WebDriver
    root.destroy() # destroy GUI   
    print("Closing the app...")


# do this when a radio station is selected in combobox
def on_select(event):
    selected_value = combobox.get()
    global combobox_index
    combobox_index = combobox.current()
    print("Selected:", selected_value)
    print("Index:", combobox_index)
    text = aStation[combobox_index][1]()
    fullStationName = aStation[combobox_index][0] 
    text = fullStationName + "*" + text
    print(text)
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

    # hide the annoying blinking cursor though the fudge
    # of selective focus setting
    #combobox.set(fullStationName)
    combobox.focus_set()
    combobox.selection_clear()
    buttons[buttonIndex].focus_set()
    root.update_idletasks()
    print("")               


# do this when a radio station is selected via playlist buttons
def on_select2(event):
    selected_value = aStation2[buttonIndex][0]
    selected_index = int(aStation2[buttonIndex][1])
    print("Selected:", selected_value)
    print("Index:", selected_index)
    print("Button index:", buttonIndex)

    if selected_index != -1:
        print("selected_index != -1")

        # run selected radio station stream, and return associated textual information 
        text = (aStation[selected_index][1])()
        fullStationName = aStation[selected_index][0] 
        text = fullStationName + "*" + text
        print(text)
        text_rows = text.split("*")

        # Make text box editable, so contents can be deleted and rewritten
        text_box.config(state=tk.NORMAL)
        text_box.delete('1.0', tk.END)
        print(text_rows)

        # Insert each row of text into the text box
        for row in text_rows:
            text_box.insert(tk.END, row + "\n")

        # make seleted button synchronize with combobox
        # hide the annoying blinking cursor though the fudge
        # of selective focus setting
        combobox.set(fullStationName)
        combobox.focus_set()
        combobox.selection_clear()
        buttons[buttonIndex].focus_set()
        
        # Disable the text box to make it read-only
        text_box.config(state=tk.DISABLED)
        root.update_idletasks()
    else:
        # There is nothing to stream
        browser.get(refresh_http)
        time.sleep(2)
        text = selected_value + "*No station playing"
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

        # Display the station logo and program graphic as blank
        image_path = pathImages + "/Blank.png"
        image = Image.open(image_path)
        scaled_image = image.resize((90, 90))  # Adjust the size as needed
        photo = ImageTk.PhotoImage(scaled_image)
        label.config(image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection
        scaled_image2 = image.resize((Xprog, Xprog))  # Adjust the size as needed
        photo2 = ImageTk.PhotoImage(scaled_image2)
        label2.config(image=photo2)
        label2.image = photo2  # Keep a reference to avoid garbage collection
        label2.place(x=Xgap, y=Ygap2)  # Adjust the position

    # save number of last playlist radio station that was played (0,...,9), ie buttonIndex.
    with open(filepath, 'w') as file:
        file.write(str(buttonIndex))
    print("")


# do this when the Add button is pressed
def on_button_Add_press(evente):
    button_Add.config(relief="sunken", bg="lightgray")  # Simulate button press
    button_Add.update_idletasks()  # Force update
    time.sleep(1)
    button_Add.config(relief="raised", bg="gray90")  # Simulate button press
    button_Add.update_idletasks()  # Force update

    print("Add button pressed")
    print("From index:", combobox_index)
    print("To index:", buttonIndex)
    # change aStation2[] list to reflect the addition
    global aStation2
    if (combobox_index != -1) and (buttonIndex != -1):
        print("station added")    
        global addFlag
        addFlag = True # so can get and save icon for playlist button

        lastStation = aStation[combobox_index][0]
        aStation2[buttonIndex][0] = lastStation
        aStation2[buttonIndex][1] = combobox_index

        # This will play the newly added station as well as saving the icon
        # to its playlist button number
        on_select2(None)

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


# do this when the Del button is pressed
def on_button_Del_press(event):
    button_Del.config(relief="sunken", bg="lightgray")  # Simulate button press
    button_Del.update_idletasks()  # Force update
    time.sleep(1)
    button_Del.config(relief="raised", bg="gray90")  # Simulate button press
    button_Del.update_idletasks()  # Force update

    print("Del button pressed")
    # change aStation2[] to reflect the deletion
    global aStation2
    index = aStation2[buttonIndex][1]
    print("deleting station:", index, "with playlist index:", buttonIndex)
    if (buttonIndex != -1) and (index != -1):
        print("station deleted")    

        lastStation = "-- EMPTY " + str(buttonIndex) +" --"
        aStation2[buttonIndex][0] = lastStation
        aStation2[buttonIndex][1] = -1

        # get blank station logo
        image_path = pathImages + "/Blank.png"
        image = Image.open(image_path)

        # saving button icon
        buttonImagePath = pathImages + "/button" + str(buttonIndex) + ".png"
        image.save(buttonImagePath)

        # This will "play" the blank station
        on_select2(None)

        # now need to update the icon on the buttonIndex button
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
        print("No station to delete")    
    print("")


def on_button_press(event, i):
    buttons[i].config(relief="sunken", bg="lightgray")  # Simulate button press
    buttons[i].update_idletasks()  # Force update
    time.sleep(1)
    buttons[i].config(relief="raised", bg="gray90")  # Simulate button press
    buttons[i].update_idletasks()  # Force update
    print("Button " + str(i) +" pressed")
    global buttonFlag;  buttonFlag = True
    global buttonIndex; buttonIndex = i
    on_select2(None)    

def on_focus(event, i):
    buttons[i].config(relief="raised", bg="darkgray")  # Simulate button press
    buttons[i].update_idletasks()  # Force update
    print(f"on focus: {i}")

def on_focus_out(event, i):
    buttons[i].config(relief="raised", bg="gray90")  # Simulate button press
    buttons[i].update_idletasks()  # Force update
    print(f"on focus out: {i}")

def on_focus_combobox(event):
    combobox.update_idletasks()  # Force update
    print("on_focus_combobox")

def on_focus_out_combobox(event):
    combobox.update_idletasks()  # Force update
    print("on_focus_out_combobox")


def on_focus_Add(event):
    button_Add.config(relief="raised", bg="darkgray")  # Simulate button press
    button_Add.update_idletasks()  # Force update
    print("on_focus_Add")

def on_focus_out_Add(event):
    button_Add.config(relief="raised", bg="gray90")  # Simulate button press
    button_Add.update_idletasks()  # Force update
    print("on_focus_out_Add")

def on_focus_Del(event):
    button_Del.config(relief="raised", bg="darkgray")  # Simulate button press
    button_Del.update_idletasks()  # Force update
    print("on_focus_Del")

def on_focus_out_Del(event):
    button_Del.config(relief="raised", bg="gray90")  # Simulate button press
    button_Del.update_idletasks()  # Force update
    print("on_focus_out_Del")

# Create the main window
root = tk.Tk()

# Set title, size and position of the main window, and make it non-resizable
strHeightForm = str(int(Xprog + 120))
print(strHeightForm)
root.title("INTERNET RADIO 3.0")  
root.geometry("800x" + strHeightForm + "+0+0")
root.resizable(False, False)  

# Create a combobox (dropdown list)
# Used to display all avialable radio stations
aStringArray = []
for element in aStation:
    aStringArray.append(element[0])
combobox = ttk.Combobox(root, values=aStringArray, height=20, width=33)
combobox.place(x=130, y=2)  # Adjust the position
combobox.bind("<FocusIn>", on_focus_combobox)
combobox.bind("<FocusOut>", on_focus_out_combobox)

combobox.bind("<<ComboboxSelected>>", on_select)
combobox.config(state="readonly")


# Populate if possible the playlist array aStation2 from file saved at shutdown
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
text_box.place(x=10, y=110, width=Xgap-20, height=Xprog)
text_box.config(state=tk.NORMAL) # Enable the text box to insert text
# height=600-110-10


# Create labels used for station logo image (label) and program related image (label2)
# Positioning of latter can vary
label = tk.Label(root)
label.pack()
label.place(x=15, y=5)
label2 = tk.Label(root)
label2.pack()

# Create button used for adding radio station to playlist
button_Add = tk.Button(root, text="Add")
button_Add.place(x=400-25-15+70, y=2, width=40, height=20)
button_Add.bind("<ButtonPress>", on_button_Add_press)
button_Add.bind("<Return>", on_button_Add_press)
button_Add.bind("<FocusIn>", on_focus_Add)
button_Add.bind("<FocusOut>", on_focus_out_Add)
    
# Create button used for deleting radio station from playlist
button_Del = tk.Button(root, text="Del")
button_Del.place(x=450-25-15+70, y=2, width=40, height=20)
button_Del.bind("<ButtonPress>", on_button_Del_press)
button_Del.bind("<Return>", on_button_Del_press)
button_Del.bind("<FocusIn>", on_focus_Del)
button_Del.bind("<FocusOut>", on_focus_out_Del)

# Create the buttons (fully) and add them to the list
buttons = []
for i in range(numButtons):
    button = tk.Button(root, text=f"Button{i}")
    button.place(x=128+(sizeButton+5)*i, y=35, width=sizeButton, height=sizeButton)
    button.config(bg="gray90")

    button.bind("<ButtonPress>", lambda event, i=i: on_button_press(event, i))  # Pass the extra parameter (i)
    button.bind("<Return>", lambda event, i=i: on_button_press(event, i))  # Pass the extra parameter (i)
    button.bind("<FocusIn>", lambda event, i=i: on_focus(event, i))
    button.bind("<FocusOut>", lambda event, i=i: on_focus_out(event, i))

    buttonImage = Image.open(pathImages + "/button" + str(i) +".png")
    buttonImage_resized = buttonImage.resize((sizeButton-5,sizeButton-5), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(buttonImage_resized)
    button.config(image=photo)
    button.image = photo
    button.update_idletasks()
    buttons.append(button)


# doing stuff just after gui is initialised and we are running in the root thread
root.after(1000, after_GUI_started)
print("Radio stream interface")

# Bind the closing event to the on_closing function
root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the GUI loop
root.mainloop()
print("out of GUI loop..")
