from openai import OpenAI

from dotenv import load_dotenv

testArticle = open("testArticle.txt", "r", encoding='utf-8').read()

class SummarySegment:
    def __init__(self, content, keyword):
        self.content = content
        self.keyword = keyword

    def __str__(self):
        return self.content + f" [{self.keyword}]. "


class ShortenContent:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI()

    # sway = "left" for left and "right" for right
    def shorten_prompt(self, article, sway):
        emulate = 'Senator Alexandria Ocasio-Cortez' if sway == 'left' else 'Tucker Carlson'

        prompt = (f"Your job is to summarize articles to be 130-150 words. Do not exceed 150 words. You will skew the "
                  f"article to have a strong {sway} wing bias. Be as polarizing and engaging as possible. You should "
                  f"use emotional rhetorical appeals. You will use simple language and syntax so that the summary "
                  f"targets a younger audience. You should emulate the speech of {emulate}. You may slightly "
                  f"modify the facts of the article. Do not exceed 150 words.")

        prompt1 = ("You will be given a piece of text. For each sentence in the text choose one word that best "
                   "describes that sentence and put it in a comma seperated list. You should return a comma seperated "
                   "list no longer than the number of sentences in the text you are given.")

        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": prompt},
                {"role": "user", "content": article},
            ]
        )

        completion1 = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": prompt1},
                {"role": "user", "content": completion.choices[0].message.content},
                {"role": "assistant", "content": "word 1, word 2, word 3, word 4, word 5"}
            ]
        )
        # print('----MAIN CONTENT-----')
        # print(completion.choices[0].message.content)
        # print('----KEYWORDS-----')
        # print(completion1.choices[0].message.content)
        content = completion.choices[0].message.content.split('. ')
        keywords = completion1.choices[0].message.content.split(', ')
        """print('----CONTENT LIST-----')
        for i in range(len(content)):
            print(content[i])
        print('----KEYWORD LIST-----')
        for i in range(len(keywords)):
            print(keywords[i])"""

        segments = []

        for i in range(0, len(content) - 1, 2):
            k = i % len(keywords)
            _content = content[i] + '. ' + content[i + 1] + '. '
            _keywords = keywords[k]
            k = (i + 1) % len(keywords)
            _keywords += ', ' + keywords[k]
            segments.append(SummarySegment(_content, _keywords))

        if len(content) > 10:
            print(f'the response is too long. it is {len(content)} long')

        return segments

    # doesnt work
    def shorten_prompt_rhyme(self, article, sway):
        emulate = 'Senator Alexandria Ocasio-Cortez' if sway == 'left' else 'Tucker Carlson'

        prompt = (f"Your job is to summarize articles to be 26 line rhyming poems. Do not exceed 25 lines. You will "
                  f"skew the"
                  f"article to have a strong {sway} wing bias. Be as polarizing and engaging as possible. You should "
                  f"use emotional rhetorical appeals. You will use simple language and syntax so that the summary "
                  f"targets a younger audience. You should emulate the speech of {emulate}. You may slightly "
                  f"modify the facts of the article. Do not exceed 26 lines. After every 2 lines in square"
                  " brackets [], put a comma separated list of the 3 most influential words in those 2 lines.")

        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": prompt},
                {"role": "user", "content": article},
                {"role": "user", "content": ""}
            ]
        )

        content = completion.choices[0].message.content
        if len(content) > 1200:
            print(f'the response is too long. it is {len(content)} long')

        return completion.choices[0].message.content


shortener = ShortenContent()
contents = shortener.shorten_prompt(testArticle, 'right')
# print('left: \n')
# print(shortener.shorten_prompt(testArticle, 'left'))
#####
