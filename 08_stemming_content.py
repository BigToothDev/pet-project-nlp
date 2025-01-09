import json
from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer("russian")
with open("06_anal_filtered_clean_content_suspilne_articles.json", mode="r", encoding="utf-8") as file:
    data = json.load(file)

for article in data: 
    clean_content = article["article_data"]["clean_content"]
    words = clean_content.split()
    stemmed_words = [stemmer.stem(word) for word in words]
    stemmed_content = " ".join(stemmed_words)
    article["article_data"]["stem_content"] = stemmed_content

with open("08_stemming_content.json", mode="w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)