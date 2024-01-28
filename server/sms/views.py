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

from .models import Headline

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
        news = []

        # store news in the database
        h = Headline(link_one=news[0].url, link_two=news[1].url, link_three=news[2].url, link_four=news[3].url, link_five=news[4].url)
        h.save()

        # text the user back with the headlines
        resp = MessagingResponse()
        msg = resp.message("Choose a headline." +
                            "\nHeadline 1: " + news[0].title +
                            "\nHeadline 2: " + news[1].title +
                            "\nHeadline 3: " + news[2].title +
                            "\nHeadline 4: " + news[3].title +
                            "\nHeadline 5: " + news[4].title)
        return HttpResponse(str(resp))
    else:
        # This is the second message!
        chosen_headline = request.POST['Body']

        mod = Headline.objects.all()[0]

        chosen_url = ""
        
        match chosen_headline:
            case "1":
                chosen_url = mod.link_one
            case "2":
                chosen_url = mod.link_two
            case "3":
                chosen_url = mod.link_three
            case "4":
                chosen_url = mod.link_four
            case "5":
                chosen_url = mod.link_five
            case _:
                resp = MessagingResponse()
                msg = resp.message("That is not a valid headline.")
                return HttpResponse(str(resp))

        # we got our url, so now we can delete our database record.
        Headline.objects.all()[0].delete()

        # use url to get our stuff to web scrape
        # we should now have summarized text, and a summarized word

        # first, we use summarized text to get the mp3

        # next, we use the summary word and pass it to giphy
        summary_word = ""

        load_dotenv()

        API_KEY = os.getenv('GIPHY_API_KEY')

        query = summary_word + " no text"

        GIF_COUNT = 3
        gg.generateGif(query, GIF_COUNT)

        # stitch video together

        # do editing to combine video, subway surfers, mp3

        # upload video to platform of choice
    
        resp = MessagingResponse()
        msg = resp.message("Your videos have been uploaded!!")
        
        return HttpResponse(str(resp))
