import requests, bs4

# Assuming from CNN
res = requests.get("https://en.wikipedia.org/wiki/Marlin_Luanda_missile_strike")
res.raise_for_status()
text = res.text

soup = bs4.BeautifulSoup(text, 'html.parser')
paragraphs = soup.find_all('p')
content = ""
for paragraph in paragraphs:
    content += paragraph.getText()
print(content)