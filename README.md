# pet-project-nlp

[Suspilne](https://suspilne.media/latest/) (Суспільне)

## File 01_div_headline_url_scraper.py

> This code scrapes news from the Suspilne website and saves the data to a JSON file. First, a function is created to generate a unique ID for each article. Next, a list of URLs for 300 pages is generated using the site's base link. Each page is loaded via HTTP requests from the requests library. If the page is successfully retrieved (status 200), its HTML code is processed using BeautifulSoup. For each article, the title, link, and time of publication are extracted and stored in the all_data list along with a unique ID.

## File 02_lemmatizer_headline.py

> This code processes articles from a JSON file, adding a lemmatized version of its title to each article, and saves the result to a new file. First, the Ukrainian-language spaCy model “uk_core_news_trf” is loaded and used to tokenize and lemmatize texts in Ukrainian. Next, the file suspilne_articles.json containing the list of articles is opened, and its contents are loaded into the articles_data variable. Each article with updated information is added to the updated_articles list. After processing all the articles, this list is written to a new anal_suspilne_articles.json file in JSON format, where each article is presented in a convenient format with all its attributes, including the lemmatized headline. The result is saved in UTF-8 encoding and formatted for easy reading.

## File 03_wordnet_and_translate.py

> This script processes a set of war-related terms to create a comprehensive list of associated words, translates them into Ukrainian, lemmatizes them, and saves the results in JSON files for further use. The process begins with a predefined list of English words encompassing various aspects of war, such as military forces, strategies, consequences, humanitarian aspects, and technologies. Using the get_related_words() function, each word is expanded to include synonyms, hypernyms (broader concepts), hyponyms (narrower concepts), meronyms (component parts), and holonyms (the whole to which the concept belongs). This function relies on the WordNet library and iterates through each word to generate a set of related terms, ensuring no duplicates using a Python set. Next, the function translate_to_ukrainian() processes each word, replacing underscores in multi-word terms with spaces for better translation results. The translated words are added to a set, and any translation errors are logged into the console. The translated list is then saved as translated_words.json for later use. After translation, the script lemmatizes the Ukrainian words using spaCy's uk_core_news_trf language model. Lemmatization involves extracting the base form of each word, which provides a standardized representation for linguistic or computational analysis. The original form is retained if no lemma is found for a particular word. The lemmatized words are saved as lemmatized_words.json for the final output.

## File 04_classifier.py

> This script filters a collection of articles to identify those relevant to a predefined set of war-related keywords. It begins by loading a JSON file containing lemmatized keywords representing war-related concepts and another JSON file with article data, including metadata such as headlines and their lemmatized versions. The script processes each article, checking for keywords in the lemmatized headline. The article is added to a new list of filtered articles if a match is found. Finally, the filtered articles are saved to a new JSON file, ensuring the output is formatted for further analysis or application. This approach streamlines the identification of relevant content by leveraging keyword-based filtering on lemmatized text.

## File 05_div_content_scraper.py

> This script enhances the filtered articles dataset by scraping the main content of each article from its URL. It loads the filtered articles from a JSON file, iterates through each article, and sends an HTTP GET request to fetch the article's webpage. Using BeautifulSoup, it searches for the main content within specific HTML container classes. If the content is found, it is extracted as text and added to the corresponding article's data. If the content or page fails to load, appropriate messages are logged. Finally, the updated dataset, including the scraped content, is saved to a new JSON file for further use.

## File 06_cleaning_lemmatizing_content.py

> This script processes the content of filtered articles by lemmatizing and removing stopwords. It starts by loading a list of Ukrainian stopwords from a file and a pre-trained spaCy model for Ukrainian language processing. Then, it reads the filtered articles from a JSON file and iterates over each article. The script uses spaCy to lemmatize the content for each article, converting words to their base form. It also removes stopwords from the lemmatized content using a custom function that filters out words listed in the stopwords file. The lemmatized and cleaned content is added to each article's data. Finally, the updated articles are saved to a new JSON file, which now includes both the lemmatized and clean versions of the content.

## File 07_stemming_of_tone_vocab.py

> This script processes a CSV file containing words and their tone scores by stemming the words and creating a dictionary of unique stems and their corresponding tone scores. Each word from the file is then stemmed using the SnowballStemmer for Russian, and its tone score is extracted. The stemmed word is stored as the key, and its score is stored as the value in a dictionary. The final dictionary of stems and tone scores is saved into a JSON file for further use.

## File 08_stemming_content.py

> This script processes the content of articles by stemming the words in their clean content. It begins by loading a JSON file containing articles. For each article, it retrieves the "clean_content" field, splits the content into individual words, and stems each word using the SnowballStemmer for Russian. The stemmed words are then joined back together into a single string. This stemmed content is added to the article's data under the key "stem_content." Finally, the updated data, including the stemmed content for each article, is saved to a new JSON file for further use.

## File 09_sentiment_analysis.py

> This script analyzes the sentiment of the stemmed content in the articles. It starts by loading a custom tone dictionary from a JSON file, which is then integrated into the SentimentIntensityAnalyzer (SIA) from the nltk library. The script then loads a JSON file containing articles with their stemmed content. For each article, it calculates the sentiment using the polarity_scores() method from SIA, which provides the negative, neutral, positive, and compound sentiment scores. These scores are added to the article's data under the keys "neg_tone," "neu_tone," "pos_tone," and "compound_tone." Finally, the updated articles, including the sentiment analysis results, are saved to a new JSON file.
