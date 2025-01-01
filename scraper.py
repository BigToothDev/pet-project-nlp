from bs4 import BeautifulSoup
from pprint import pprint
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import json

article_counter = 1
def generate_article_id():
    global article_counter
    article_id = article_counter
    article_counter += 1
    return article_id

raw_suspilne_url = "https://suspilne.media/latest/?page="
suspilne_urls = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

for page_num in range(1, 300):  
    list_suspilne_urls = f"{raw_suspilne_url}{page_num}"
    suspilne_urls.append(list_suspilne_urls)
    print(list_suspilne_urls)

all_data = []

for url in suspilne_urls:
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("div", class_="c-article-card__content")
            
        for article in articles:
            
            headline_element = article.find("h2", class_="c-article-card__headline-inner") 
            if headline_element:
                headline = headline_element.text.strip()

            link_tag = article.find("a", class_="c-article-card__headline")
            if link_tag:
                link = link_tag["href"]

            time_tag = article.find("time", class_="c-article-card__info__time")
            if time_tag:
                datetime = time_tag["datetime"] 

            article_id = generate_article_id()

            data = {
                "id": article_id,
                "article_data": {
                    "headline": headline,
                    "link": link,
                    "datetime": datetime,
                }
            }
            all_data.append(data)
    else:
        print(f"Не вдалося завантажити {url} - Статус: {response.status_code}")

for item in all_data:
    print(item)

with open("suspilne_articles.json", "w", encoding="utf-8") as json_file:
    json.dump(all_data, json_file, ensure_ascii=False, indent=4)