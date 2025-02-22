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

# Create an instance of FirefoxOptions
firefox_options = Options()
firefox_options.add_argument("-headless")  # Ensure this argument is correct
browser = webdriver.Firefox(options=firefox_options)

# 'cleans' browser between station websites
refresh_http = "http://www.ri.com.au" 

# global position variables for graphics
Ygap = 10;  Ygap2 = 107; Ygap3 = 300
Xgap = 450; Xgap2 = 202; Xgap3 = 345

# global variables for combobox selection indexes & button related
combobox_index = -1
combobox2_index = -1
buttonFlag = False
buttonIndex = 0
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
    global buttonFlag
    if buttonFlag:
        buttonImagePath = pathImages + "/button_" + str(buttonIndex)
        scaled_image.save(buttonImagePath)
        buttonFlag = False
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
    scaled_image2 = cropped_image2.resize((135, 135))  # Adjust the size as needed
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
    scaled_image2 = image2.resize((int(135*width2/height2), 135))  # Adjust the size as needed
    photo2 = ImageTk.PhotoImage(scaled_image2)
    label2.config(image=photo2)
    label2.image = photo2  # Keep a reference to avoid garbage collection
    label2.place(x=Xgap3, y=Ygap2)  # Adjust the position
    
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
    scaled_image2 = cropped_image2.resize((135, 135))  # Adjust the size as needed
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
    # Display the station logo as given in the image_path global variable
    image = Image.open(image_path)
    scaled_image = image.resize((90, 90))  # Adjust the size as needed
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
    scaled_image2 = cropped_image2.resize((135, 135))  # Adjust the size as needed
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
    # Display the station logo as given in the image_path global variable
    image = Image.open(image_path)
    scaled_image = image.resize((90, 90))  # Adjust the size as needed
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
    scaled_image2 = cropped_image2.resize((135, 135))  # Adjust the size as needed
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
    scaled_image2 = cropped_image2.resize((135, 135))  # Adjust the size as needed
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
    scaled_image2 = cropped_image2.resize((135, 135))  # Adjust the size as needed
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




def Smooth(br,ix,iy,sPath):
 #   print(inspect.stack()[1].function)
    br.refresh()
    br.get(sPath)
    time.sleep(3)
    window_size = br.get_window_size()
    print(f"Window size: width = {window_size['width']}, height = {window_size['height']}")
    actions = ActionChains(br)
    actions.move_by_offset(650, 10).click().perform()
    window_size = br.get_window_size()
    
    print(f"Window size: width = {window_size['width']}, height = {window_size['height']}")
    time.sleep(1)
    actions = ActionChains(br)
    actions.move_by_offset(ix,iy).click().perform()
    time.sleep(10)



def Smooth2(br,sPath):
 #   print(inspect.stack()[1].function)
    br.refresh()
    br.get(sPath)
    time.sleep(3)
    window_size = br.get_window_size()
    actions = ActionChains(br)
    actions.move_by_offset(650, 900).click().perform()
    window_size = br.get_window_size()
    time.sleep(10)



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
    actions.move_by_offset(301, 256).click().perform()

  # get station logo
    img_element = be.find_element(By.XPATH, '/html/body/div[1]/div[4]/div[1]/div/div/div[1]/div/div/img')
    img_url = img_element.get_attribute("src")
    image_path = pathImages + "/logo.png"
    urllib.request.urlretrieve(img_url, image_path)
    # Display the station logo as given in the image_path global variable
    image = Image.open(image_path)
    scaled_image = image.resize((90, 90))  # Adjust the size as needed
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
    scaled_image2 = image2.resize((int(135*width2/height2), 135))  # Adjust the size as needed
    photo2 = ImageTk.PhotoImage(scaled_image2)
    label2.config(image=photo2)
    label2.image = photo2  # Keep a reference to avoid garbage collection
    label2.place(x=Xgap, y=Ygap2)  # Adjust the position

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

    
def smoothfm_953_Sydney():
    Smooth(browser,0,95,"https://smooth.com.au")
def smooth_Vintage():
    Smooth(browser,0,95*2,"https://smooth.com.au")
def smooth_953_Adelaide():
    Smooth(browser,0,95*3,"https://smooth.com.au")
def smooth_80s():
    Smooth2(browser,"https://smooth.com.au/station/smooth80s")
def smooth_relax():
    Smooth2(browser,"https://smooth.com.au/station/smoothrelax")




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
    ["Mix 90s",Mix_90s]
]

# 2D an array of preset radio stations, in long name and index (to aStation[]) format
# this is the default, but is actually copied from file at statup and saved to file on exit!
aStation2 = [
    ["-- EMPTY 0 --",-1],
    ["-- EMPTY 1 --",-1],
    ["-- EMPTY 2 --",-1],
    ["-- EMPTY 3 --",-1],
    ["-- EMPTY 4 --",-1],
    ["-- EMPTY 5 --",-1],
    ["-- EMPTY 6 --",-1],
    ["-- EMPTY 7 --",-1],
    ["-- EMPTY 8 --",-1],
    ["-- EMPTY 9 --",-1],
]


# select last station after radio was last powered down
def select_and_trigger():
    try:
        with open(filepath, 'r') as file:
            lastStation = file.read()
    except FileNotFoundError:
        print(f'Error: The file {filepath} does not exist.')
        lastStation = aStation[0][0]
    print(f'Last station is {lastStation}')    
    combobox.set(lastStation);
    on_select(None)


# populate the playlist array aStation2 from file saved at shutdown
try:
    with open(filepath2, 'r') as file:
        reader = csv.reader(file)
        aStation2 = [row for row in reader]     
except FileNotFoundError:
    print(f'Error: The file {filepath2} does not exist.')
# will just use the default aStation2[] array created above


# do this when closing the window/app
def on_closing():
    # save station name to file (if radio powered off when playing this station)
    with open(filepath, 'w') as file:
        file.write(combobox.get())

    # save the playlist to file
    with open(filepath2, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(aStation2)

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
    print("")


# do this when a radio station is selected in combobox2
def on_select2(event):
    global buttonFlag
    global combobox2_index
    if not buttonFlag:
        selected_value = combobox2.get()
        selected_index = combobox2.current()
        combobox2_index = selected_index # save for use with adding or deleting station from playlist
        selected_index = aStation2[selected_index][1]
        selected_index = int(selected_index)
    else:
        selected_index = int(aStation2[buttonIndex][1])
        selected_value = aStation2[buttonIndex][0]
        buttonFlag = False # make sure to reset buttonFlag once it is used           
    print("Selected:", selected_value)
    print("Index:", selected_index)
    print("Button index:", buttonIndex)

    if selected_index != -1:
        text = (aStation[selected_index][1])() # strangely selected_index has to be cast to int
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
        # save station name to file (if radio powered off when playing this station)
        with open(filepath, 'w') as file:
            file.write(selected_value)
    else:
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
        scaled_image2 = image.resize((135, 135))  # Adjust the size as needed
        photo2 = ImageTk.PhotoImage(scaled_image2)
        label2.config(image=photo2)
        label2.image = photo2  # Keep a reference to avoid garbage collection
        label2.place(x=Xgap, y=Ygap2)  # Adjust the position
    print("")


# do this when the Add button is pressed
def on_button_Add_press(evente):
    print("Add button pressed")
    print("Index:", combobox_index)
    print("Index2:", combobox2_index)
    # change aStation2[] and combobox2 list to reflect the addition
    global aStation2
    if (combobox_index != -1) and (combobox2_index != -1):
        global addFlag
        addFlag = True # so can get and save icon for playlist button

        lastStation = aStation[combobox_index][0]
        aStation2[combobox2_index][0] = lastStation
        aStation2[combobox2_index][1] = combobox_index
        new_values = []
        for element in aStation2:
            new_values.append(element[0])
        combobox2.config(values=new_values)
        combobox2.set(lastStation) # select the just added station, to refresh display
        on_select2(None)
    else:
        print("No station added")    
    print("")

# do this when the Del button is pressed
def on_button_Del_press(event):
    print("Del button pressed")
    print("Index:", combobox_index)
    print("Index2:", combobox2_index)
    # change aStation2[] and combobox2 list to reflect the deletion
    global aStation2
    index = aStation2[combobox2_index][1]
    print("index:", index)
    if (combobox2_index != -1) and (index != -1):
        lastStation = "-- EMPTY " + str(combobox2_index) +" --"
        aStation2[combobox2_index][0] = lastStation
        aStation2[combobox2_index][1] = -1
        new_values = []
        for element in aStation2:
            new_values.append(element[0])
        combobox2.config(values=new_values)
        combobox2.set(lastStation) # select the deleted station, to refresh display
        on_select2(None)
    else:
        print("No station to delete")    
    print("")


def on_button_0_press(event):
    button_0.config(relief="sunken", bg="lightgray")  # Simulate button press
    button_0.update_idletasks()  # Force update
    time.sleep(1)
    button_0.config(relief="raised", bg="SystemButtonFace")  # Simulate button press
    button_0.update_idletasks()  # Force update
    print("Button 0 pressed")
    global buttonFlag;  buttonFlag = True
    global buttonIndex; buttonIndex = 0
    on_select2(None)    

def on_button_0_release(event):
    button_0.config(relief="raised", bg="SystemButtonFace")  # Simulate button press
    button_0.update_idletasks()  # Force update
    print("Button 0 released")


def on_button_1_press(event):
    button_1.config(relief="sunken", bg="lightgray")  # Simulate button press
    button_1.update_idletasks()  # Force update
    print("Button 1 pressed")
    global buttonFlag;  buttonFlag = True
    global buttonIndex; buttonIndex = 1
    on_select2(None)    

def on_button_1_release(event):
    button_1.config(relief="raised", bg="SystemButtonFace")  # Simulate button press
    button_1.update_idletasks()  # Force update
    print("Button 1 released")


def on_button_2_press(event):
    print("Button 2 pressed")
    global buttonFlag;  buttonFlag = True
    global buttonIndex; buttonIndex = 2
    on_select2(None)    

def on_button_3_press(event):
    print("Button 3 pressed")
    global buttonFlag;  buttonFlag = True
    global buttonIndex; buttonIndex = 3
    on_select2(None)    

def on_button_4_press(event):
    print("Button 4 pressed")
    global buttonFlag;  buttonFlag = True
    global buttonIndex; buttonIndex = 4
    on_select2(None)    

def on_button_5_press(event):
    print("Button 5 pressed")
    global buttonFlag;  buttonFlag = True
    global buttonIndex; buttonIndex = 5
    on_select2(None)    

def on_button_6_press(event):
    print("Button 6 pressed")
    global buttonFlag;  buttonFlag = True
    global buttonIndex; buttonIndex = 6
    on_select2(None)    

def on_button_7_press(event):
    print("Button 7 pressed")
    global buttonFlag;  buttonFlag = True
    global buttonIndex; buttonIndex = 7
    on_select2(None)    

def on_button_8_press(event):
    print("Button 8 pressed")
    global buttonFlag;  buttonFlag = True
    global buttonIndex; buttonIndex = 8
    on_select2(None)    

def on_button_9_press(event):
    print("Button 9 pressed")
    global buttonFlag;  buttonFlag = True
    global buttonIndex; buttonIndex = 9
    on_select2(None)    


# Create the main window
root = tk.Tk()

# Set title, size and position of the main window, and make it non-resizable
root.title("INTERNET RADIO 3.0")  
root.geometry("640x480+0+0")
root.resizable(False, False)  

# Create a combobox (dropdown list)
# Used to display all avialable radio stations
aStringArray = []
for element in aStation:
    aStringArray.append(element[0])
combobox = ttk.Combobox(root, values=aStringArray, height=20, width=33)
combobox.place(x=155-25, y=15-10)  # Adjust the position
# Bind the combobox selection event to the on_select function
combobox.bind("<<ComboboxSelected>>", on_select) 

# Create a combobox2 (dropdown list)
# used to display a playlist of up to 10 radio stations
aStringArray2 = []
for element in aStation2:
    aStringArray2.append(element[0])   
combobox2 = ttk.Combobox(root, values=aStringArray2, height=10, width=33)
combobox2.place(x=155-25, y=55-25)  # Adjust the position
# Bind the combobox2 selection event to the on_select2 function
combobox2.bind("<<ComboboxSelected>>", on_select2) 

# Create a text box, position and size it
# used to display the program and song details
text_box = tk.Text(root)
text_box.place(x=10, y=105, width=580, height=335)
text_box.config(state=tk.NORMAL) # Enable the text box to insert text

# used for station logo image (label) and program related image (label2)
# Positioning of latter can vary
label = tk.Label(root)
label.pack()
label.place(x=18, y=5)
label2 = tk.Label(root)
label2.pack()

# button used for adding radio station to playlist
button_Add = tk.Button(root, text="Add")
button_Add.place(x=400-25-15, y=55-25, width=40, height=20)
# Bind the <Button-1> event (left mouse button click) to the function
button_Add.bind("<Button-1>", on_button_Add_press)
    
# button used for deleting radio station from playlist
button_Del = tk.Button(root, text="Del")
button_Del.place(x=450-25-15, y=55-25, width=40, height=20)
# Bind the <Button-1> event (left mouse button click) to the function
button_Del.bind("<Button-1>", on_button_Del_press)



# playlist button #0
button_image0 = Image.open(pathImages + "/button0.png")
button_image0_resized = button_image0.resize((35,35), Image.Resampling.LANCZOS)
tk_image0 = ImageTk.PhotoImage(button_image0_resized)
button_0 = tk.Button(root, image=tk_image0)
button_0.place(x=155-25+45*0, y=55-25+28, width=40, height=40)
button_0.bind("<ButtonPress>", on_button_0_press)
button_0.bind("<ButtonRelease>", on_button_0_release)

# playlist button #1
button_image1 = Image.open(pathImages + "/button1.png")
button_image1_resized = button_image1.resize((35,35), Image.Resampling.LANCZOS)
tk_image1 = ImageTk.PhotoImage(button_image1_resized)
button_1 = tk.Button(root, image=tk_image1)
button_1.place(x=155-25+45*1, y=55-25+28, width=40, height=40)
button_1.bind("<ButtonPress>", on_button_1_press)
button_1.bind("<ButtonRelease>", on_button_1_release)


# playlist button #2
button_image2 = Image.open(pathImages + "/button2.png")
button_image2_resized = button_image2.resize((35,35), Image.Resampling.LANCZOS)
tk_image2 = ImageTk.PhotoImage(button_image2_resized)
button_2 = tk.Button(root, image=tk_image2)
button_2.place(x=155-25+45*2, y=55-25+28, width=40, height=40)
button_2.bind("<Button-1>", on_button_2_press)

# playlist button #3
button_image3 = Image.open(pathImages + "/button3.png")
button_image3_resized = button_image3.resize((35,35), Image.Resampling.LANCZOS)
tk_image3 = ImageTk.PhotoImage(button_image3_resized)
button_3 = tk.Button(root, image=tk_image3)
button_3.place(x=155-25+45*3, y=55-25+28, width=40, height=40)
button_3.bind("<Button-1>", on_button_3_press)

# playlist button #4
button_image4 = Image.open(pathImages + "/button4.png")
button_image4_resized = button_image4.resize((35,35), Image.Resampling.LANCZOS)
tk_image4 = ImageTk.PhotoImage(button_image4_resized)
button_4 = tk.Button(root, image=tk_image4)
button_4.place(x=155-25+45*4, y=55-25+28, width=40, height=40)
button_4.bind("<Button-1>", on_button_4_press)

# playlist button #5
button_image5 = Image.open(pathImages + "/button5.png")
button_image5_resized = button_image5.resize((35,35), Image.Resampling.LANCZOS)
tk_image5 = ImageTk.PhotoImage(button_image5_resized)
button_5 = tk.Button(root, image=tk_image5)
button_5.place(x=155-25+45*5, y=55-25+28, width=40, height=40)
button_5.bind("<Button-1>", on_button_5_press)

# playlist button #6
button_image6 = Image.open(pathImages + "/button6.png")
button_image6_resized = button_image6.resize((35,35), Image.Resampling.LANCZOS)
tk_image6 = ImageTk.PhotoImage(button_image6_resized)
button_6 = tk.Button(root, image=tk_image6)
button_6.place(x=155-25+45*6, y=55-25+28, width=40, height=40)
button_6.bind("<Button-1>", on_button_6_press)

# playlist button #7
button_image7 = Image.open(pathImages + "/button7.png")
button_image7_resized = button_image7.resize((35,35), Image.Resampling.LANCZOS)
tk_image7 = ImageTk.PhotoImage(button_image7_resized)
button_7 = tk.Button(root, image=tk_image7)
button_7.place(x=155-25+45*7, y=55-25+28, width=40, height=40)
button_7.bind("<Button-1>", on_button_7_press)

# playlist button #8
button_image8 = Image.open(pathImages + "/button8.png")
button_image8_resized = button_image8.resize((35,35), Image.Resampling.LANCZOS)
tk_image8 = ImageTk.PhotoImage(button_image8_resized)
button_8 = tk.Button(root, image=tk_image8)
button_8.place(x=155-25+45*8, y=55-25+28, width=40, height=40)
button_8.bind("<Button-1>", on_button_8_press)

# playlist button #9
button_image9 = Image.open(pathImages + "/button9.png")
button_image9_resized = button_image9.resize((35,35), Image.Resampling.LANCZOS)
tk_image9 = ImageTk.PhotoImage(button_image9_resized)
button_9 = tk.Button(root, image=tk_image9)
button_9.place(x=155-25+45*9, y=55-25+28, width=40, height=40)
button_9.bind("<Button-1>", on_button_9_press)


# doing stuff just after gui is initialised and we are running in the root thread
root.after(1000, select_and_trigger)
print("Radio stream interface")

# Bind the closing event to the on_closing function
root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the GUI loop
root.mainloop()

print("out of GUI loop..")

