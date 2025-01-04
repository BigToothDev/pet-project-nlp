import nltk
import requests
import json
import pandas as pd
import spacy

nlp = spacy.load("uk_core_news_trf")
url = 'https://raw.githubusercontent.com/olegdubetcky/Ukrainian-Stopwords/main/ukrainian'
r = requests.get(url)

stopwords_ua = pd.read_csv("stopwords_ua.txt", header=None, names=['stopwords'])
stop_words_ua = list(stopwords_ua.stopwords)

def remove_stopwords(text, stop_words):
    words = text.split()
    filtered_words = [word for word in words if word not in stop_words]
    return ' '.join(filtered_words)

with open("anal_filtered_content_suspilne_articles.json", "r", encoding="utf-8") as file:
    suspilne_df = json.load(file)
    
for article in suspilne_df:
    content = article["article_data"]["content"]
    doc = nlp(content)
    lemmatized_content= " ".join([token.lemma_ for token in doc])
    article["article_data"]["lemmatized_content"] = lemmatized_content

    clean_content = remove_stopwords(lemmatized_content, stop_words_ua)
    article["article_data"]["clean_content"] = clean_content

with open("anal_filtered_clean_content_suspilne_articles.json", "w", encoding="utf-8") as file:
    json.dump(suspilne_df, file, ensure_ascii=False, indent=4)