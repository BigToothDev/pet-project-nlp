import json
from nltk.corpus import wordnet
from deep_translator import GoogleTranslator

#syns = wordnet.synsets("war") 
#print(syns)

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
    "war", "combat", "battle", "weapon", "shell", "tank", "drone", "bomb", "missile", "nuclear weapon", "artillery", 
    "attack", "bombardment", "air raid", "invasion", "occupation", "enemy", "ally", "infantry", "prisoner of war",
    "mercenary", "veteran", "civilian", "migration", "famine", "strategy", "tactic", "fortification", "espionage",
    "mobilization", "reconnaissance", "siren", "sanctions", "ceasefire", "peace talks",
    "occupation", "neutrality", "propaganda", "resistance", "terrorism"
]

all_related_words = set()
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