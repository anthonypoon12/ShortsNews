import requests
import json
import urllib.request
import os
from dotenv import load_dotenv
import modules.stitch as s
import ffmpeg

load_dotenv()

API_KEY = os.getenv('GIPHY_API_KEY')

def generateGif(query):
    query = query + " no text"
    outputPaths = []

    timeNeeded = 10

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

    # Appends url to list and retrieves the video
    mp4url = response.json()['data'][0]['images']['original']['mp4']
    outputPaths.append(f'./templateVid.mp4')
    urllib.request.urlretrieve(mp4url, outputPaths[-1])
    duration = get_video_duration(outputPaths[-1])

    counter = 0

    while timeNeeded > 0:
        timeNeeded -= duration
        os.system(f'cp {outputPaths[-1]} {f"tempVid{counter}.mp4"}')
        outputPaths.append(f'tempVid{counter}.mp4')
        counter += 1

    if timeNeeded < 0:
        input_stream = ffmpeg.input(outputPaths[-1], ss=0)
        os.system(f'rm {outputPaths[-1]}')
        input_stream.output(outputPaths[-1], to=duration + timeNeeded).run()

    s.stitch(outputPaths)

if __name__ == "__main__":
    import sys
    generateGif(sys.argv[1], sys.argv[2])


def get_video_duration(file_path):
    try:
        probe = ffmpeg.probe(file_path, cmd='ffprobe')
        duration = float(probe['format']['duration'])
        return duration
    except ffmpeg.Error as e:
        print(f"Error: {e.stderr}")