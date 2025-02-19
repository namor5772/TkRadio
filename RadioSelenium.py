import subprocess
import inspect

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Path to Geckodriver executable
#geckodriver_path = 'C:\\Users\\roman\\OneDrive\\MyImportant\\geckodriver.exe'  # Adjust this path

# Create an instance of FirefoxOptions
firefox_options = Options()

# Example: Set headless mode (runs browser in background)
#firefox_options.add_argument("-headless")  # Ensure this argument is correct

# Set up the Firefox driver with options
browser = webdriver.Firefox(options=firefox_options)

# Set up Firefox options
#browser = webdriver.Firefox()



# START ***** Functions that stream radio stations *****

def Radio1(br,Num,sPath):
    print(inspect.stack()[1].function)
    br.refresh()
    br.get(sPath)
    time.sleep(3)
    be = br.find_element(By.TAG_NAME, 'body')
    for _ in range(Num):
        be.send_keys(Keys.TAB)
    be.send_keys(Keys.ENTER)
    time.sleep(3)

def Smooth(br,ix,iy,sPath):
    print(inspect.stack()[1].function)
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
    print(inspect.stack()[1].function)
    br.refresh()
    br.get(sPath)
    time.sleep(3)
    window_size = br.get_window_size()
    actions = ActionChains(br)
    actions.move_by_offset(650, 900).click().perform()
    window_size = br.get_window_size()
    time.sleep(10)

def ABC_radio2(br,sPath):
    print(inspect.stack()[1].function)
    br.refresh()
    br.get(sPath)
    time.sleep(3)
    be = br.find_element(By.TAG_NAME, 'body')
    be.send_keys(Keys.TAB)
    be.send_keys(Keys.ENTER)
    be.send_keys(Keys.TAB)
    be.send_keys(Keys.TAB)
    be.send_keys(Keys.TAB)
    be.send_keys(Keys.ENTER)
    be.send_keys(Keys.SHIFT,Keys.TAB)
    be.send_keys(Keys.TAB)
    be.send_keys(Keys.TAB)
    time.sleep(3)
    
def ABC_radio3(br,Num,sPath):
    print(inspect.stack()[1].function)
    browser.refresh()
    browser.get(sPath)
    time.sleep(3)
    be = br.find_element(By.TAG_NAME, 'body')
    for _ in range(Num):
        be.send_keys(Keys.TAB)
    be.send_keys(Keys.ENTER)
    be.send_keys(Keys.TAB)
    be.send_keys(Keys.TAB)

def iHeart(br,sPath):
    print(inspect.stack()[1].function)
    br.refresh()
    br.get(sPath)
    time.sleep(3)
    window_size = br.get_window_size()
    #print(f"Window size: width = {window_size['width']}, height = {window_size['height']}")
    actions = ActionChains(br)
    actions.move_by_offset(301, 256).click().perform()
    time.sleep(10)

    

def ABC_Radio_SYDNEY():
    ABC_radio2(browser,"https://www.abc.net.au/listen/live/sydney")
def ABC_Radio_National_LIVE():
    Radio1(browser,6,"https://www.abc.net.au/listen/live/radionational")
def ABC_NewsRadio():
    ABC_radio2(browser,"https://www.abc.net.au/listen/live/news")
def ABC_Classic_LIVE():
    Radio1(browser,8,"https://www.abc.net.au/listen/live/classic")
def ABC_Classic2():
    Radio1(browser,7,"https://www.abc.net.au/listen/live/classic2")
def ABC_Jazz():
    Radio1(browser,7,"https://www.abc.net.au/listen/live/jazz")
def ABC_triple_j_LIVE():
    Radio1(browser,8,"https://www.abc.net.au/listen/live/triplej")
def ABC_Double_j_LIVE():
    Radio1(browser,8,"https://www.abc.net.au/listen/live/doublej")
def ABC_triple_j_Unearthed():
    Radio1(browser,7,"https://www.abc.net.au/triplej/live/unearthed")
def ABC_triple_j_Hottest():
    Radio1(browser,7,"https://www.abc.net.au/triplej/live/triplejhottest")
def ABC_Country():
    ABC_radio3(browser,3,"https://www.abc.net.au/listen/live/country#content")
def ABC_Radio_AUSTRALIA():
    ABC_radio3(browser,14,"https://www.abc.net.au/pacific/live")
def KIIS1065():
    iHeart(browser,"https://www.iheart.com/live/kiis-1065-6185/")
def GOLD1017():
    iHeart(browser,"https://www.iheart.com/live/gold1017-6186/")
def CADA():
    iHeart(browser,"https://www.iheart.com/live/cada-6179/")
def iHeartCountry_Australia():
    iHeart(browser,"https://www.iheart.com/live/iheartcountry-australia-7222/")
def KIIS_90s():
    iHeart(browser,"https://www.iheart.com/live/kiis-90s-10069/")
def GOLD_80s():
    iHeart(browser,"https://www.iheart.com/live/gold-80s-10073/")
def iHeartRadio_Countdown_AUS():
    iHeart(browser,"https://www.iheart.com/live/iheartradio-countdown-aus-6902/")
def TikTok_Trending_on_iHeartRadio():
    iHeart(browser,"https://www.iheart.com/live/tiktok-trending-on-iheartradio-8876/")
def iHeartDance():
    iHeart(browser,"https://www.iheart.com/live/iheartdance-6941/")
def The_Bounce():
    iHeart(browser,"https://www.iheart.com/live/the-bounce-6327/")
def iHeartAustralia():
    iHeart(browser,"https://www.iheart.com/live/iheartaustralia-7050/")
def fbi_radio():
    iHeart(browser,"https://www.iheart.com/live/fbiradio-6311/")
def _2SER1073():
    iHeart(browser,"https://www.iheart.com/live/2ser-6324/")
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


        



# 2D array of radio station information in [short name, long name, url] format
# clearly this can be varied if you wish to listen to different 7 stations
aStation = [
    ["ABC Radio AUSTRALIA",ABC_Radio_AUSTRALIA],
    ["ABC Radio National LIVE",ABC_Radio_National_LIVE],
    ["PBW","ABC NewsRadio","https://live-radio01.mediahubaustralia.com/PBW/mp3/"],
    ["2FMW","ABC Classic Sydney","https://live-radio01.mediahubaustralia.com/2FMW/mp3/"],
    ["FM2W","ABC Classic 2","https://live-radio01.mediahubaustralia.com/FM2W/mp3/"],
    ["WSFM","GOLD 101.7","https://playerservices.streamtheworld.com/api/livestream-redirect/ARN_WSFM.mp3"],
    ["SMOOTH953","Smooth FM Sydney 95.3","https://playerservices.streamtheworld.com/api/livestream-redirect/SMOOTH953.mp3"]
]

print("Radio stream interface")

smooth_relax()        ;time.sleep(60)
smooth_80s()          ;time.sleep(60)
smooth_953_Adelaide() ;time.sleep(60)
smooth_Vintage()      ;time.sleep(60)
smoothfm_953_Sydney() ;time.sleep(60)

'''
ABC_Country()             ;time.sleep(15)  
ABC_Radio_AUSTRALIA()     ;time.sleep(15)

ABC_Radio_SYDNEY()        ;time.sleep(15)
ABC_Radio_National_LIVE() ;time.sleep(15)
ABC_NewsRadio()           ;time.sleep(15)
ABC_Classic_LIVE()        ;time.sleep(15)


KIIS1065()
time.sleep(10)

GOLD1017()
time.sleep(10)

CADA()
time.sleep(10)

iHeartCountry_Australia()
time.sleep(10)

KIIS_90s()
time.sleep(10)

GOLD_80s()
time.sleep(10)

iHeartRadio_Countdown_AUS()
time.sleep(10)

TikTok_Trending_on_iHeartRadio()
time.sleep(10)

iHeartDance()
time.sleep(10)

The_Bounce()
time.sleep(10)

iHeartAustralia()
time.sleep(10)

fbi_radio()
time.sleep(10)

_2SER1073()
time.sleep(10)

ABC_Country()
'''


while True:
    startup = False    

