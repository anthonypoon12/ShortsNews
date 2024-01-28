import requests, bs4


# Assuming from CNN
def scrape_content(url):
    res = requests.get(url)
    res.raise_for_status()
    text = res.text

    soup = bs4.BeautifulSoup(text, 'html.parser')
    paragraphs = soup.find_all('p')
    content = ""
    for paragraph in paragraphs:
        content += paragraph.getText()
    return content