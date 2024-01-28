from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


from twilio.twiml.messaging_response import MessagingResponse

import os
from dotenv import load_dotenv
import requests
import json
import urllib.request

import sys
import os

# Add the parent directory to the sys.path
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

# Now you can import module.file
import modules.generategif as gg

@csrf_exempt
def sms_response(request):

    load_dotenv()

    API_KEY = os.getenv('GIPHY_API_KEY')

    body = request.POST['Body']
    query = body + " no text"

    parameters = {
        "api_key": API_KEY,
        "q": query,
        "limit": 3,
        "offset": 0,
        "rating": "g",
        "lang": "en",
        "bundle": "messaging_non_clips",
    }

    gg.generateGif(body)
    
    resp = MessagingResponse()
    msg = resp.message("Your prompt has been received: " + body)
    
    return HttpResponse(str(resp))
