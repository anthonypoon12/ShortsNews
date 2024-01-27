import requests
import json
import urllib.request
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('GIPHY_API_KEY')
query = "obama happy" + " no text"
limit = 3
outputPaths = []

parameters = {
    "api_key": API_KEY,
    "q": query,
    "limit": limit,
    "offset": 0,
    "rating": "g",
    "lang": "en",
    "bundle": "messaging_non_clips",
}

response = requests.get("https://api.giphy.com/v1/gifs/search", params=parameters)

for i in range(3):
    # Appends url to list and retrieves the video
    mp4url = response.json()['data'][i]['images']['original']['mp4']
    outputPaths.append(f'./tempvid{i}.mp4')
    urllib.request.urlretrieve(mp4url, outputPaths[-1])

<<<<<<< Updated upstream
=======
urllib.request.urlretrieve(mp4url, './tempvid.mp4')
>>>>>>> Stashed changes
