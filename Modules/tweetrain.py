#/usr/bin/env python

"""
This module provides functions to generate ("train") letters frequency tables and to evaluate analyzer accuracy
"""

import tweepy, re, csv
from Modules.analyzer import extract_chars_freq, charset, LettersFreq
import logging

CONSUMER_TOKEN = ""  # Substitute with your own values
CONSUMER_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""

langs = {  # Languages
    "English": "en",
    # "Arabic": "ar",  # Languages with non-latin alphabet have been commented
    # "Bengali": "bn",
    "Czech": "cs",
    "Danish": "da",
    "German": "de",
    # "Greek": "el",
    "Spanish": "es",
    #"Persian": "fa",
    "Finnish": "fi",
    "Filipino": "fil",
    "French": "fr",
    # "Hebrew": "he",
    # "Hindi": "hi",
    "Hungarian": "hu",
    "Indonesian": "id",
    "Italian": "it",
    # "Japanese": "ja",
    # "Korean": "ko",
    #"Malay": "msa",
    "Dutch": "nl",
    "Norwegian": "no",
    "Polish": "pl",
    "Portuguese": "pt",
    "Romanian": "ro",
    # "Russian": "ru",
    "Swedish": "sv",
    # "Thai": "th",
    #"Turkish": "tr",
    # "Ukrainian": "uk",
    # "Urdu": "ur",
    "Vietnamese": "vi"
    }

langs_R = {v:k for k, v in langs.items()} # Reversed langs


def gen_freq_dict(max_count=100):  # Generate Frequency Dictionary
    """
    Generate a Python dictionary containing the frequency of each letter for each language (in percentage)
    :param max_count: Maximum number of messages analyzed for each language
    :return: Python dictionary that contains letters frequencies
    """

    auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN,
                          ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    freq = {}
    for n, c in langs.items():  # Name, language Code
        buf = ''
        for tweet in tweepy.Cursor(api.search, q='#', lang=c).items(max_count):
            buf += re.sub(r"(http.*)|(#.*)|(@.*? )|RT", "",
                          tweet.text).lower()  # removing links, hashtags, tags and various garbage, then count letters
            #print(buf)  # Debug
        freq[n] = extract_chars_freq(buf)
    return freq


def gen_freq_csv(filename="letters_frequency_twitter.csv", max_count=100):  # Generate Frequency Dictionary
    """
    Generate a csv file in which are encoded the frequency of each letter for each language (in percentage)
    :param filename: Name, with or without .csv extension, of the file containing frequency table
    :param max_count: Maximum number of messages analyzed for each language
    :return: True if succeed or False if failed
    """
    try:
        with open(filename, "w") as file:
            csv_file = csv.writer(file)
            csv_file.writerow(['Language']+charset)
            d = gen_freq_dict(max_count)
            for lang, freq in d.items():
                vals = list(freq.values())
                csv_file.writerow([lang]+list(map(lambda x: str(x)+"%", vals)))  # lamba function to add '%' sign
        return True
    except:
        logging.warning("Error while opening ")
        return False


def main():
    """Test yout Twitter token and key"""
    auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN,
                          ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    for tweet in tweepy.Cursor(api.search, q='#', count=100, lang='en').items():
        print(re.sub(r"(http.*)|(#.*)|(@.*? )|RT", "", tweet.text),
              tweet.lang)  # removing links, hashtags, tags and various garbage
        # time.sleep(1)


def train():
    print(gen_freq_csv("../Frequency_Tables/letters_frequency_twitter.csv", 500))


if __name__ == "__main__":
    main()
    #train()
