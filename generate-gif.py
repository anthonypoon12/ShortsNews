import requests
import json
import urllib.request
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('GIPHY_API_KEY')
query = "obama happy" + " no text"

parameters = {
    "api_key": API_KEY,
    "q": query,
    "limit": 1,
    "offset": 0,
    "rating": "g",
    "lang": "en",
    "bundle": "messaging_non_clips",
}

response = requests.get("https://api.giphy.com/v1/gifs/search", params=parameters)

mp4url = response.json()['data'][0]['images']['original']['mp4']

urllib.request.urlretrieve(mp4url, './tempvid.mp4')