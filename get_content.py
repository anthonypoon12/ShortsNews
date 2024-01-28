from newsdataapi import NewsDataApiClient
import requests, bs4
import shorten_content
import web_scrape
import tts

# from selenium import webdriver

# API key authorization, Initialize the client with your API key

api = NewsDataApiClient(apikey="pub_372043babb911c02c68bff05b2d4fce6de861")
domain = 'cnn'


# You can pass empty or with request parameters {ex. (country = "us")}

class ArticleObject:
    def __init__(self, title, link, index):
        self.title = title
        self.link = link
        self.index = index


def get_articles(q):
    response = api.news_api(q=q, country="us", language="en", domain=domain, size=5)

    results = response["results"]

    articles = []

    for i in range(len(results)):
        title = results[i]["title"]
        link = results[i]["link"]
        articles.append(ArticleObject(title, link, i))

    return articles
    # print(f"{source_id}")


print("give a topic: ")
topic = input()
articles = get_articles(topic)
print(f"give a number between 1 and {len(articles)}")
index = int(input()) - 1

article = web_scrape.scrape_content(articles[index].link)

shortener = shorten_content.ShortenContent()
contents = shortener.shorten_prompt(article, 'right')

for i in range(len(contents)):
    tts.writeMP3(contents[i], i)

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
