from nltk.stem.snowball import SnowballStemmer
import csv
import json

stemmer = SnowballStemmer("russian")

with open("tone-dict-uk.csv", mode="r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)
    tone_dict = []
    for row in reader:
        tone_dict.append(row)

unique_stems = {}
for item in tone_dict:
    stem = stemmer.stem(item["word"])
    score = float(item["score"])
    unique_stems[stem] = score

with open("07_stem-tone-dict.json", mode="w", encoding="utf-8") as file:
    json.dump(unique_stems, file, ensure_ascii=False, indent=4)

print("Словник стемів збережено у 'stem-tone-dict.json'!")