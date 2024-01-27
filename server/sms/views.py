from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from twilio.twiml.messaging_response import MessagingResponse

import os
from dotenv import load_dotenv
import requests
import json

@csrf_exempt
def sms_response(request):

    load_dotenv()

    API_KEY = os.getenv('GIPHY_API_KEY')

    body = request.POST['Body']
    query = body + " no text"

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

    mp4file = requests.get(mp4url)

    resp = MessagingResponse()
    msg = resp.message("Your prompt has been received: " + str(mp4file.status_code))
    
    return HttpResponse(str(resp))
