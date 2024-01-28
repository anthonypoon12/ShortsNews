import requests
import json
import urllib.request
import os
from dotenv import load_dotenv
import modules.stitch as s
import ffmpeg

load_dotenv()

API_KEY = os.getenv('GIPHY_API_KEY')

def generateGif(query, mp3FileName):
    query = query + " no text"
    outputPaths = []

    timeNeeded = get_duration(mp3FileName)

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
    duration = get_duration(outputPaths[-1])
    timeNeeded -= duration

    counter = 0

    while timeNeeded > 0:
        os.system(f'cp {outputPaths[-1]} {f"tempVid{counter}.mp4"}')
        outputPaths.append(f'tempVid{counter}.mp4')
        counter += 1
        timeNeeded -= duration
        # print('----------duration and time needed-----------')
        # print(f"{duration}  {timeNeeded}")

# Frames are guessed
    if timeNeeded < 0:
        input_file = ffmpeg.input(outputPaths[-1])
        output_file = ffmpeg.output(input_file.trim(start_frame=0, end_frame=24*(duration + timeNeeded)), 'trimmed.mp4')
        ffmpeg.run(output_file)
        os.system(f"rm -f {outputPaths[-1]}")
        outputPaths[-1] = "trimmed.mp4"

    s.stitch(outputPaths, mp3FileName)

    for file in outputPaths:
        os.system(f'rm {file}')

if __name__ == "__main__":
    import sys
    generateGif(sys.argv[1], sys.argv[2])


def get_duration(file_path):
    try:
        probe = ffmpeg.probe(file_path, cmd='ffprobe')
        duration = float(probe['format']['duration'])
        return duration
    except ffmpeg.Error as e:
        print(f"Error: {e.stderr}")