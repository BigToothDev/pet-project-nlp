import spacy
import json

nlp = spacy.load("uk_core_news_trf")

with open("suspilne_articles.json", "r", encoding="utf-8") as file:
    articles_data = json.load(file)

updated_articles = []
for article in articles_data:
    article_id = article["id"]
    link = article["article_data"]["link"]
    headline = article["article_data"]["headline"]
    datetime = article["article_data"]["datetime"]
    doc = nlp(headline)
    lemmatized_headline = " ".join([token.lemma_ for token in doc])

    updated_article = {
        "ID": article_id,
        "article_data": {
            "link": link,
            "headline": headline,
            "lemmatized_headline": lemmatized_headline,
            "datetime": datetime
        }
    }

    updated_articles.append(updated_article)

with open("anal_suspilne_articles.json", "w", encoding="utf-8") as file:
    json.dump(updated_articles, file, ensure_ascii=False, indent=4)