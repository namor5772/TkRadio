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
from selenium.common.exceptions import NoAlertPresentException, UnexpectedAlertPresentException


# Get the directory of the current script & images
script_dir = os.path.dirname(os.path.abspath(__file__))
script_dir = script_dir.replace("\\","/")
print(f"This script path is: {script_dir}")
pathImages = script_dir + "/Images"
print(f"The Images path is: {pathImages}")

# Create the full filepath to the station websites csv file
filename = 'auStationWebsites.csv'
basicStations_filepath = os.path.join(script_dir, filename)
print(f'The file {basicStations_filepath} stores a basic list of station websites')

filename = 'au_Stations.csv'
au_Stations_filepath = os.path.join(script_dir, filename)
print(f'The file {au_Stations_filepath} stores a full list of station websites')

# Open and setup FireFox browser
firefox_options = Options()
# below is the headless width and height, if not headless +15 & 8 respectively
firefox_options.add_argument("--width=1280")
firefox_options.add_argument("--height=917")
#firefox_options.add_argument("-headless")  # Ensure this argument is correct
browser = webdriver.Firefox(options=firefox_options)

# 'cleans' browser between opening station websites
refresh_http = "http://www.ri.com.au" # use my basic "empty" website

# global graphic related variables
Ydown = 63
Ygap = 10;  Ygap2 = 110+Ydown; Ygap3 = 110+Ydown
Xgap = 560-70; Xgap2 = 560-70; Xgap3 = 560-70
Xprog = 300
X1 = 55 # 55 for RP version
Y1 = 30 # 30 for RP version
iconSize = 160

# global variables
def SomeFunction(): pass    
StationName = ""
StationLogo = ""
StationFunction = SomeFunction
nNum = 0
sPath = ""
sClass = ""
nType = 0
eventFlag = True # if on_select are called from event (and not just to update the text box and program image)
needSleep = 5 # can be less on faster machines
refreshTime = 7.0 # seconds between updating station info
pollFlag = True # if true then poll website for program text and picture changes 
selectedStationIndex = 0
selectedStationName = ""

selected_value = "INITIAL"
selected_value_last = "INITIAL"
selected_index = -1
startTime = time.time()
finishTime = time.time()
startTime2 = time.time()
finishTime2 = time.time()
TimeNum = 0

img_url_g = ""
oh = 0
nh = 0
tabNum = 0
oh2 = 0
nh2 = 0
ExtraWindowFlag = False
Streaming = True # if streaming is working



# format used by the radio-australia.org and related stations format
def Commercial2(br,nNum,sPath,sClass,nType):
    global img_url_g, oh, nh, tabNum, oh2, nh2, ExtraWindowFlag, Streaming
    global StationName, StationLogo, StationFunction
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

    if eventFlag:
        # press button with virtual mouse to play stream
        window_size = br.get_window_size()
        print(f"Window size: width = {window_size['width']}, height = {window_size['height']}")
        if nType == 0:
            widthPx = 250 #110
        else: # if nType == 1:
            widthPx = 250    
        heightPx = 330
        print(f"Move size: width = {widthPx}, height = {heightPx}")
        actions = ActionChains(br)
        actions.move_by_offset(widthPx, heightPx).click().perform()
        time.sleep(6)

        # this is needed to dismiss any alert that may appear (unwanted login popup)
        try:
            alert = br.switch_to.alert  # Switch to alert if present
            print(f"Alert detected: {alert.text}")  # Print alert text for debugging
            alert.dismiss()  # Dismiss or accept as needed
        except NoAlertPresentException:
            print("No alert detected.")
        except UnexpectedAlertPresentException as e:
            print(f"Unexpected alert encountered: {e}")

        # this is a multiple windows case (old nType == 1 example)
        if len(br.window_handles) > 1:
            # another window is opened with button that actually starts the stream
            print(br.window_handles)  # Lists all open windows/tabs
            oh2 = br.window_handles[0]  # Original window handle
            nh2 = br.window_handles[1]  # New window handle a fter clicking the first button
            br.switch_to.window(nh2)  # Switch to the new window
            # press the button with virtual mouse to play stream
            actions = ActionChains(br)
            actions.move_by_offset(widthPx, heightPx).click().perform()
            time.sleep(6)
            br.switch_to.window(oh2) # Switch back to the original window
            nNum = 1 # indicate multiple windows case
            ExtraWindowFlag = True

        # identify whether streaming works using identifiers on a path element
        # that display an error in playing graphic on the play button
        Streaming = True
        nType = 0
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
                nType = 1
                print("<<< Streaming is not working >>>")
        except IndexError:
            Streaming = False
            nType = 2
            print("<<< Streaming is not working - IndexError >>>")

        # Open or create a CSV file to append the station array row  to the station list
        #global StationName, StationLogo, StationFunction, nNum, sPath, sClass, nType
        with open(au_Stations_filepath, "a", newline="", encoding="utf-8-sig") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([StationName, StationLogo, StationFunction, nNum, sPath, sClass, nType])  # Write to CSV file
            print("")
            print(f"**************** Station array element created: {selectedStationIndex},{nType}")
            print("")

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
        fe1 = fe1 + "*"+"<<< Streaming is not working >>>"
    return fe1



aStationCSV = []
with open(basicStations_filepath, "r", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        aStationCSV.append(row)

for row in aStationCSV:
    print(" | ".join(row))



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



# Define a custom event class
class CustomEvent:
    def __init__(self, event_type, widget, data=None):
        self.type = event_type
        self.widget = widget
        self.data = data



# do this when a radio station is selected from combobox
def on_select(event):
    global StationName, StationLogo, StationFunction, nNum, sPath, sClass, nType
    global ExtraWindowFlag, TimeNum, selectedStationIndex, selectedStationName
    print("---- on_select() entered ---------------------------------------------")
 
    if ExtraWindowFlag:
        # if the extra window is open, close it
        ExtraWindowFlag = False
        browser.switch_to.window(nh2)
        browser.close()
        browser.switch_to.window(oh2)
        print("Extra window closed")

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

    # set various flags and parameters related to starting a station stream or accesing its website
    global eventFlag, stopFlag, selected_value, combobox_index, selected_value_last 
    if event.type=="Auto":
        eventFlag = True # if on_select() is called by selecting a combobox entry
        stopFlag = False # if this call of on_select() should be implemented
      # parameters relating to how this funtion was called
        selected_value_last = selected_value
        selected_value = selectedStationName
        combobox_index = selectedStationIndex
        print("selected_value:", selected_value)
        print("combobox_index:", combobox_index)
    else: # if event.type=="Manual"
        # "Safely" load the next station in the list
        if (timeInterval > refreshTime) and (timeInterval < refreshTime+3.0) and (TimeNum < 2):
            TimeNum += 1
            print(f"TimeNum: {TimeNum}, TimeInterval: {timeInterval}")
        elif (timeInterval > refreshTime) and (timeInterval < refreshTime+3.0) and (TimeNum == 2):
            TimeNum = 0
            selectedStationIndex += 1
            selectedStationName = aStation[selectedStationIndex][0]
            root.after(int(refreshTime*500), lambda: on_select(CustomEvent("Auto", root, "ComboBox Event")))
            print("")
            print(f"<<< SELECTED STATION: {selectedStationIndex} >>>")
            global startTime2, finishTime2
            finishTime2 = time.time()
            timeInterval2 = finishTime2-startTime2
            timeIntervalStr2 = f"{timeInterval2:.2f}"
            startTime2 = finishTime2
            print(f"Time interval between selections: {timeIntervalStr2} seconds")               

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
        elif (timeInterval < refreshTime-3.0):
            stopFlag = True    
            print("FIRST STOP")
    print("stopFlag:",stopFlag)
    print("eventFlag:",eventFlag)

    if stopFlag==False:
        # run selected radio station stream, and return associated textual information 
        try:
            text = StationFunction(browser,nNum,sPath,sClass,nType)
            text = StationName + "*" + text + "* *[" + timeIntervalStr + "]"
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
        print("JUST ABOUT TO RUN ROOT")
        eventFlag = False
        if pollFlag:
            root.after(int(refreshTime*1000), lambda: on_select(CustomEvent("Manual", event.widget, "Manual from custom_combo")))
        print("FINISHED RUNNING ROOT")
        print("")

    else: #if stopFlag==True
        # Makes the scheduled call to on_select() do nothing if
        # it occurs after another station stream has been started
        stopFlag = False
        print("selected_value:",selected_value_last)
        print("DID STOPPING BIT")
        print("")



# after gui is initialised and we are running in the root thread
def after_GUI_started():
    global selectedStationIndex, selectedStationName, TimeNum
    TimeNum = 0
    selectedStationIndex = 823
    selectedStationName = aStation[selectedStationIndex][0]
    on_select(CustomEvent("Auto", root, "ComboBox Event"))



# do this when closing the window/app
def on_closing():
    browser.quit() # close the WebDriver
    root.destroy() # destroy GUI   
    print("Closing the app...")



##########################################
### THIS IS WHERE THE CORE CODE STARTS ###

# Create the main window
# Set title, size and position of the main window, and make it non-resizable
root = tk.Tk()
root.title("INTERNET RADIO - https://github.com/namor5772/TkRadio - radio_Commercial2_Tester.py")  
root.geometry("800x455+0+0")
root.resizable(False, False)
root.update_idletasks()

# Create a text box, position and size it, used to display the program and song details
text_box = tk.Text(root)
text_box.place(x=10, y=110+30+Ydown, width=Xgap-20+30+25, height=Xprog-30-25)
text_box.config(state=tk.NORMAL) # Enable the text box to insert text

# Create labels used for station logo image (label) and program related image (label2)
# Positioning of latter can vary
label = tk.Label(root)
label.place(x=15, y=2+30)
label2 = tk.Label(root)

# Bind the closing event to the on_closing function
root.protocol("WM_DELETE_WINDOW", on_closing)

# doing stuff just after the gui is initialised and we are running in the root thread
root.after(7000, after_GUI_started) # need 7sec lag to make sure things work
print("run the GUI loop..")

# Run the GUI loop
root.mainloop()
print("out of GUI loop..")



