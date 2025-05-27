import requests
import json

# API endpoint to get all radio stations
url = "https://api.radio-browser.info/json/stations"
url = "https://de1.api.radio-browser.info/json/stations?limit=70000"

# Fetch the data
response = requests.get(url)

if response.status_code == 200:
    stations = response.json()

    # Save full station details to a JSON file
    with open("radio_stations.json", "w", encoding="utf-8") as file:
        json.dump(stations, file, indent=4)



    # Extract URLs
    #urls = [station["url"] for station in stations]

    # Save to a file
    #with open("radio_urls.txt", "w") as file:
     #   for url in urls:
      #      file.write(url + "\n")

    print("Radio station URLs saved to radio_urls.txt")
else:
    print("Failed to fetch data. Status code:", response.status_code)
