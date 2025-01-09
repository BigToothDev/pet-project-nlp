from nltk.sentiment.vader import SentimentIntensityAnalyzer
import json

SIA = SentimentIntensityAnalyzer()
with open("07_stem-tone-dict.json", mode="r", encoding="utf-8") as file:
   tone_dict = json.load(file)
SIA.lexicon.update(tone_dict)

with open("08_stemming_content.json", "r", encoding="utf-8") as file:
  suspilne_df = json.load(file)

for article in suspilne_df:
  content = article["article_data"]["stem_content"]
  vs = SIA.polarity_scores(content)
  article["article_data"]["neg_tone"] = vs["neg"]
  article["article_data"]["neu_tone"] = vs["neu"]
  article["article_data"]["pos_tone"] = vs["pos"]
  article["article_data"]["compound_tone"] = vs["compound"]

with open("dataset.json", "w", encoding="utf-8-sig") as file:
    json.dump(suspilne_df, file, ensure_ascii=False, indent=4)