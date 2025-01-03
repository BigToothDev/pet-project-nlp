import json
from nltk.corpus import wordnet
from deep_translator import GoogleTranslator
import spacy

def get_related_words(word):
    related_words = set()
    for synset in wordnet.synsets(word):
        for lemma in synset.lemmas():
            related_words.add(lemma.name())

        for hypernym in synset.hypernyms():
            for lemma in hypernym.lemmas():
                related_words.add(lemma.name())

        for hyponym in synset.hyponyms():
            for lemma in hyponym.lemmas():
               related_words.add(lemma.name())

        for meronym in synset.part_meronyms():
            for lemma in meronym.lemmas():
                related_words.add(lemma.name())

        for holonym in synset.member_holonyms():
            for lemma in holonym.lemmas():
                related_words.add(lemma.name())

    return related_words

war_associated_words = [
    # Загальні поняття
    "war", "conflict", "violence", "combat", "hostilities", "occupation",

    # Збройні сили та військова техніка
    "army", "military", "infantry", "artillery", "tank", "drone", "missile", "warship", 
    "aircraft", "rifle", "munition", "radar",

    # Стратегія і тактика
    "strategy", "tactic", "mobilization", "siege", "blockade", "fortification", 
    "reconnaissance", "espionage", "cyberwarfare",

    # Наслідки війни
    "casualties", "destruction", "migration", "refugees", "famine", "suffering", 
    "humanitarian aid", "reconstruction",

    # Гуманітарні аспекти
    "civilian", "prisoner of war", "sanctions", "peace talks", "ceasefire", "neutrality", 
    "propaganda", "resistance",

    # Технології
    "surveillance", "electronic warfare", "cyberattack", "autonomous weapon", 
    "unmanned aerial vehicle", "anti-aircraft defense", "satellite imaging",

    # Політика та міжнародні відносини
    "ally", "enemy", "diplomacy", "sanctions", "NATO", "UN", "security council", 
    "military aid", "economic blockade", "geopolitics",

    # Інформаційний простір
    "media coverage", "propaganda", "disinformation", "fake news", "information warfare", 
    "public opinion", "war reporting", "journalism",

    # Логістика і забезпечення
    "supply chain", "military base", "logistics", "ammunition supply", 
    "field hospital", "evacuation", "resource management"
]

all_related_words = set(war_associated_words)

for base_word in war_associated_words:
    all_related_words.update(get_related_words(base_word))

print("Related Words:", all_related_words)

def translate_to_ukrainian(word_list):
    translated_words = set()
    for word in word_list:
        word = word.replace('_', ' ')
        try:
            translated_word = GoogleTranslator(source='en', target='uk').translate(word)
            translated_words.add(translated_word)
        except Exception as e:
            print(f"Error translating {word}: {e}")
    
    return translated_words

translated_words = translate_to_ukrainian(all_related_words)
print(translated_words)

with open("translated_words.json", "w", encoding="utf-8") as file:
    json.dump(list(translated_words), file, ensure_ascii=False, indent=4)

nlp = spacy.load("uk_core_news_trf")

lemmatized_words = []
for word in translated_words:
    doc = nlp(word)
    lemmatized_words.append(doc[0].lemma_ if doc else word)

with open("lemmatized_words.json", "w", encoding="utf-8") as file:
    json.dump(lemmatized_words, file, ensure_ascii=False, indent=4)

print("Лематизація завершена. Результат збережено у 'lemmatized_words.json'")