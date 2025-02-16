import json
import random
import re
random.seed(191)

with open("./datajson/02_anal_suspilne_articles.json", "r", encoding="utf-8") as file:
    articles = json.load(file)

def clean(lemmatized_headline):
    clean_text = re.sub(r'[^\w\s]', '', lemmatized_headline)
    return clean_text

selected_elements = random.sample(articles, 300)
unselected_elements = [item for item in articles if item not in selected_elements]


with open('data_tf-idf/4training_sample.json', 'w', encoding='utf-8') as file:
    json.dump(selected_elements, file, ensure_ascii=False, indent=4)

with open('data_tf-idf/remaining_data.json', 'w', encoding='utf-8') as file:
    json.dump(unselected_elements, file, ensure_ascii=False, indent=4)