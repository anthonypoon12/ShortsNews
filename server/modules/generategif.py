import requests
import json
import urllib.request
import os
from dotenv import load_dotenv
import modules.stitch as s

load_dotenv()

API_KEY = os.getenv('GIPHY_API_KEY')

def generateGif(query, limit):
    query = query + " no text"
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

    for i in range(limit):
        # Appends url to list and retrieves the video
        mp4url = response.json()['data'][i]['images']['original']['mp4']
        outputPaths.append(f'./tempvid{i}.mp4')
        urllib.request.urlretrieve(mp4url, outputPaths[-1])


    s.stitch(outputPaths, [3, 5, 10])

if __name__ == "__main__":
    import sys
    generateGif(sys.argv[1], sys.argv[2])