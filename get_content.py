from newsdataapi import NewsDataApiClient
import requests, bs4
# from selenium import webdriver

# API key authorization, Initialize the client with your API key

api = NewsDataApiClient(apikey="pub_372043babb911c02c68bff05b2d4fce6de861")

# You can pass empty or with request parameters {ex. (country = "us")}

response = api.news_api( q= "gaza", country = "us", language="en", domain="nytimes", size=5)

print(response["totalResults"])
results = response["results"]
for i in range(len(results)):
    title = results[i]["title"]
    source_id = results[i]["source_id"]
    link = results[i]["link"]
    print(f"{source_id} : {title}\n\t{link}")
    # print(f"{source_id}")

# browser = webdriver.Firefox()
# browser.get("https://www.nytimes.com/2024/01/27/world/middleeast/gaza-war-israel-hamas-negotiations.html")


# NY Times: StoryBodyCompanionColumn


## Wikipedia articles
# res = requests.get("https://en.wikipedia.org/wiki/Marlin_Luanda_missile_strike")
# res.raise_for_status()
# print(res.text)
# text = res.text

# # Title
# soup = bs4.BeautifulSoup(text, 'html.parser')
# title = soup.select('#firstHeading')[0].getText()
# print(title)

# # Paragraphs
# soup = bs4.BeautifulSoup(text, 'html.parser')
# paragraphs = soup.find_all('p')
# print(len(paragraphs))
# for paragraph in paragraphs:
#     print(paragraph.getText())