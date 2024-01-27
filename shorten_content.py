from openai import OpenAI

from dotenv import load_dotenv

testArticle = open("testArticle.txt", "r", encoding='utf-8').read()


class ShortenContent:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI()

    # sway = "left" for left and "right" for right
    def shorten_prompt(self, article, sway):
        opposing = 'left' if sway == 'right' else 'right'
        emulate = 'Senator Alexandria Ocasio-Cortez' if sway == 'left' else 'Tucker Carlson'

        prompt = (f"Your job is to summarize articles to be 130-150 words. Do not exceed 150 words. You will skew the "
                  f"article to have a strong {sway} wing bias. Be as polarizing and engaging as possible. You should "
                  f"use emotional rhetorical appeals. You will use simple language and syntax so that the summary "
                  f"targets a younger audience. You should emulate the speech of {emulate}. You may slightly "
                  f"modify the facts of the article. Do not exceed 150 words.")

        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": prompt},
                {"role": "user", "content": article}
            ]
        )

        content = completion.choices[0].message.content
        if len(content) > 1200:
            print(f'the response is too long. it is {len(content)} long')

        return completion.choices[0].message.content

    def shorten_prompt_rhyme(self, article, sway):
        opposing = 'left' if sway == 'right' else 'right'
        emulate = 'Senator Alexandria Ocasio-Cortez' if sway == 'left' else 'Tucker Carlson'

        prompt = (f"Your job is to summarize articles to be 25 line rhyming poems. Do not exceed 25 lines. You will "
                  f"skew the"
                  f"article to have a strong {sway} wing bias. Be as polarizing and engaging as possible. You should "
                  f"use emotional rhetorical appeals. You will use simple language and syntax so that the summary "
                  f"targets a younger audience. You should emulate the speech of {emulate}. You may slightly "
                  f"modify the facts of the article. Do not exceed 25  lines.")

        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": prompt},
                {"role": "user", "content": article}
            ]
        )

        content = completion.choices[0].message.content
        if len(content) > 1200:
            print(f'the response is too long. it is {len(content)} long')

        return completion.choices[0].message.content


shortener = ShortenContent()
print('right: \n')
print(shortener.shorten_prompt(testArticle, 'right'))
print('left: \n')
print(shortener.shorten_prompt(testArticle, 'left'))
