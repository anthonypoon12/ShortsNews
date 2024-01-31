# ShortsNews
This is a project for McHacks 11. This is a short form content generator based on the news.
## Inspiration
With the recent developments in artificial intelligence, it is clear that the potential for mass manipulation and the spread of misinformation is becoming increasingly clear. In a world that continues to grow polarized on various social issues, we hope to bring light to the extent in which media has an influence over the opinions of the public.
## What it does
Our project allows users to immediately create a short-form video detailing current events and upload this content to Youtube. We intentionally included two versions of each video, one holding a more liberal standpoint and the other catering towards a more conservative group. Ultimately, this project not only allows for automated content generation, but also is a clear message that the manipulation of media and news is easily executed through different tonal shifts and word choices.
## How we built it
We built this project using Python. We used Django (hosted with ngrok) to create an endpoint that receives requests through SMS using the Twilio API. This message received is used to find relevant current news articles using the NewsData.io API, which is stored in the SQLite database. We message the user, listing the options found, from which the user can choose by sending another message. We then use BeautifulSoup to web scrape the article and find relevant text that we summarize and skew to left-wing and right-wing biases using OpenAI's GPT-3.5. We then used the Giphy API to retrieve sets of mp4s, as well as Google Cloud text-to-speech (using our summarized) to get sets of mp3s to pair with them. We used the ffmpeg python library to manipulate and stitch the files together into our two final videos to be uploaded. We then used the Youtube API to automatically upload our videos to the internet.
## Challenges we ran into
We used many APIs and libraries, some of which had very little/poor documentation. We spent the bulk of our time figuring out how to properly use them.

## Accomplishments that we're proud of
We were able to build our product by taking advantage of a wide variety of technologies, many of which we had never touched before.

## What we learned
We learned a lot about working with APIs and integrating our own endpoint into other technologies like Twilio.

## What's next for ShortsNews
We hope to fully flesh out our project to produce higher quality content, both for entertainment and information.
