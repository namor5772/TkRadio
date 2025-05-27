import vlc
import time

import requests

# URL of the image
#url = "https://i.ibb.co/Cmm8W7k/ACE-2-UE-APP-SQUARE-3000x3000.jpg"
url = "https://i.ibb.co/Cmm8W7k/ACE-2-UE-APP-SQUARE-3000x3000.jpg"

# Send a GET request to the URL
response = requests.get(url, stream=True)

# Save the file locally
with open("Logo.jpg", "wb") as file:
    for chunk in response.iter_content(1024):
        file.write(chunk)

print("Download complete!")

# Define the radio station URL
radio_url = "https://wz2liw.scahw.com.au/live/2day_128.stream/playlist.m3u8"
#radio_url = "https://fmfm.org.au:8001/2MBSFineMusicSydney.MP3"
#radio_url = "https://worldradio.online/proxy/?q=http://wz2liw.scahw.com.au/live/2ue_128.stream/playlist.m3u8"

# Create a VLC instance and media player and start playing
instance = vlc.Instance()
player = instance.media_player_new()
media = instance.media_new(radio_url)
player.set_media(media)
player.play()




# Keep the script running to allow playback
print("Streaming radio... Press Ctrl+C to stop.")
try:
    while True:
        time.sleep(1)
       
except KeyboardInterrupt:
    print("Stopping radio stream...")
    player.stop()

