#!/usr/bin/python

import subprocess, sys
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

from newsdataapi import NewsDataApiClient
import requests, bs4
import modules.shorten_content as shorten_content
import modules.web_scrape as web_scrape
import modules.tts as tts
# import modules.upload_video as upload_video
import modules.stitch as stitch
import modules.mergeAudioVideo as merge

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

        # insert code to get headlines, we will have an array of news classes:
        #   title
        #   url
        # from selenium import webdriver

        # API key authorization, Initialize the client with your API key

        load_dotenv()

        NEWS_API_KEY = os.getenv('NEWS_API_KEY')

        api = NewsDataApiClient(apikey=NEWS_API_KEY)
        domain = 'cnn,bbc,nypost'

        # You can pass empty or with request parameters {ex. (country = "us")}

        class ArticleObject:
            def __init__(self, title, link, index):
                self.title = title
                self.link = link
                self.index = index

        def get_articles(q):
            response = api.news_api(q=q, language="en", domain=domain, size=5)

            results = response["results"]

            articles = []

            for i in range(len(results)):
                title = results[i]["title"]
                link = results[i]["link"]
                articles.append(ArticleObject(title, link, i))

            return articles
            # print(f"{source_id}")

        articles = get_articles(query)

        if len(articles) == 0:
            resp = MessagingResponse()
            msg = resp.message("No headlines available.")
            return HttpResponse(str(resp))

        linkone = ""
        linktwo = ""
        linkthree = ""
        linkfour = ""
        linkfive = ""

        if len(articles) >= 1:
            linkone = articles[0].link
        if len(articles) >= 2:
            linktwo = articles[1].link
        if len(articles) >= 3:
            linkthree = articles[2].link
        if len(articles) >= 4:
            linkfour = articles[3].link
        if len(articles) >= 5:
            linkfive = articles[4].link
    
        # store news in the database
        h = Headline(link_one=linkone, link_two=linktwo, link_three=linkthree, link_four=linkfour, link_five=linkfive)
        h.save()

        # text the user back with the headlines
        resp = MessagingResponse()
        choice_string = "Choose a headline."

        for n in range(0, len(articles)):
            choice_string += "\nHeadline " + str(n + 1) + ": " + articles[n].title
        
        msg = resp.message(choice_string)
        return HttpResponse(str(resp))
    else:
        # This is the second message!
        chosen_headline = request.POST['Body']

        mod = Headline.objects.all()[0]

        chosen_url = ""

        article_length = 0

        if mod.link_five != "":
            article_length = 5
        elif mod.link_four != "":
            article_length = 4
        elif mod.link_three != "":
            article_length = 3
        elif mod.link_two != "":
            article_length = 2
        elif mod.link_one != "":
            article_length = 1
        else:
            article_length = 0

        if (int(chosen_headline) > article_length):
            resp = MessagingResponse()
            msg = resp.message("That is not a valid headline.")
            return HttpResponse(str(resp))
        else: 
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
        # we should now get summarized text, and a summarized word

        article = web_scrape.scrape_content(chosen_url)

        if len(article) == 0:
            resp = MessagingResponse()
            msg = resp.message("No content found.")
            return HttpResponse(str(resp))
        else:
            shortener = shorten_content.ShortenContent()
            contentsLeft = shortener.shorten_prompt(article, 'left')
            contentsRight = shortener.shorten_prompt(article, 'right')

            if len(contentsLeft) == 0 or len(contentsRight) == 0:
                resp = MessagingResponse()
                msg = resp.message("Not enough content found.")
                return HttpResponse(str(resp))

            # we use summarized text segments to get mp3s
            segment_text_array_left = []
            segment_text_array_right = []

            left_segments = []
            right_segments = []

            for i in range(len(contentsLeft)):
                tts.writeMP3(contentsLeft[i], i, "Left") #outputLeft0, ...
                # generate output videos 
                gg.generateGif(contentsLeft[i].keyword, "outputLeft" + str(i) + ".mp3") # outputLeft0.mp4, outputLeft1.mp4, ...
                merge.merge("outputLeft" + str(i) + ".mp4", f"outputLeft{i}.mp3", f"newOutputLeft{i}.mp4")
                left_segments.append("newOutputLeft" + str(i) + ".mp4")
                # array of text for segments (3 elements per segment)
                segment_text_array_left.append(contentsLeft[i].subtitle_chunk())
                

            stitch.stitchMP4(left_segments, "finalLeft.mp4")


            for i in range(len(contentsRight)):
                tts.writeMP3(contentsRight[i], i, "Right") #outputRight0, ...
                # generate output videos 
                gg.generateGif(contentsRight[i].keyword, "outputRight" + str(i) + ".mp3") # outputRight0.mp4, outputRight1.mp4, ...
                merge.merge("outputRight" + str(i) + ".mp4", f"outputRight{i}.mp3", f"newOutputRight{i}.mp4")
                
                right_segments.append("newOutputRight" + str(i) + ".mp4")

                # array of text for segments (3 elements per segment)
                segment_text_array_right.append(contentsRight[i].subtitle_chunk())

        # stitch videos together

            stitch.stitchMP4(right_segments, "finalRight.mp4")
        # do editing to combine video, subway surfers, mp3

        # put on subtitles (3 subtitles spread across equally for each segment, from segment_text_array)
            # Use ffmpeg to add subtitles
            command = "ffmpeg -i finalRight.mp4 -vf subtitles=../script.srt output_srt.mp4"
            subprocess.run(command, shell = True, executable="/bin/bash")

        # upload video to platform of choice

        # upload_video.upload("left_video.mp4", "Left Wing News", "Left Wing News reporting.", "I, Am, Keywords")
        # upload_video.upload("right_video.mp4", "Right Wing News", "Left Wing News reporting.", "I, Am, Keywords")
    
        resp = MessagingResponse()
        msg = resp.message("Your videos have been uploaded!!")
        
        return HttpResponse(str(resp))