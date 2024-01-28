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

from models import Headline

@csrf_exempt
def sms_response(request):

    links = Headline.objects.all()
    if not links:
        # this is the first message!
        # get the headlines
        query = request.POST['Body']

        # insert code to get headlines, we will have an array of news class:
        #   title
        #   url

        # store news in the database
        h = Headline(link_one=news[0].url, link_two=news[1].url, link_three=news[2].url, link_four=news[3].url, link_five=news[4].url)
        
        # text the user back with the headlines
        resp = MessagingResponse()
        msg = resp.message("Choose a headline." +
                            "\nHeadline 1: " + news[0].title +
                            "\nHeadline 2: " + news[1].title +
                            "\nHeadline 3: " + news[2].title +
                            "\nHeadline 4: " + news[3].title +
                            "\nHeadline 5: " + news[4].title)
        



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

    gg.generateGif(body, 3)
    
    resp = MessagingResponse()
    msg = resp.message("Your prompt has been received: " + body)
    
    return HttpResponse(str(resp))
