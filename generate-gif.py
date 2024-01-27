import requests
import json
import urllib.request

API_KEY = "1Akxy1zQTa8CT2679RPoYKrd39GB1VeM"
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

