from bs4 import BeautifulSoup
import requests
import json


with open("anal_filtered_suspilne_articles.json", "r", encoding="utf-8") as file:
    suspilne_df = json.load(file)

for article in suspilne_df:
    url = article["article_data"]["link"]
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        possible_classes = [
            "l-article-content__container-inner c-article-content__content",
            "c-article-content c-article-content--bordered c-article-content--fs-m"
        ]
        content_div = None
        for class_name in possible_classes:
            content_div = soup.find("div", class_=class_name)
            if content_div:
                break
        if not content_div:
            content_div = soup.find("div", class_=lambda x: x and "c-article-content" in x)

        if content_div:
            content = content_div.get_text(separator=" ", strip=True)
            article["article_data"]["content"] = content
        else:
            print(f"Основний контент не знайдено для {url}")
    else:
        print(f"Не вдалося завантажити сторінку {url}. Код статусу: {response.status_code}")

with open("anal_filtered_content_suspilne_articles.json", "w", encoding="utf-8") as output_file:
    json.dump(suspilne_df, output_file, ensure_ascii=False, indent=4)