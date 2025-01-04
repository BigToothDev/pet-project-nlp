import json

with open ("./manually_ed_data/lemma_war_vocab_ed.json", "r", encoding="utf-8") as file:
    keywords = json.load(file)
with open ("anal_suspilne_articles.json", "r", encoding="utf-8") as file:
    articles = json.load(file)
filtered_articles = [
    article for article in articles
    if any(word in keywords for word in article["article_data"]["lemmatized_headline"].split())
]
with open("anal_filtered_suspilne_articles.json", "w", encoding="utf-8") as file:
    json.dump(filtered_articles, file, ensure_ascii=False, indent=4)