#!/bin/python

#This module provides functions to generate ("train") letters frequency tables and to evaluate analyzer accuracy

import tweepy, re, time #TODO: import module to convert python freqency dictionarie in csv tables

def gen_freq_dict():
    '''Generate a Python dictionary containing the frequency of each letter for each language (in percentage)'''
    pass

def gen_freq_csv(filename):
    '''Generate a csv file in which are encoded the frequency of each letter for each language (in percentage)
    :param str filename: name, with or without .csv extension, of the file containing frequency table
    '''
    pass

def main():
    """Test yout Twitter token and key"""
    auth = tweepy.OAuthHandler("kaa8NMKyhaYPmAK9mBWiEfU1k", "TiddL5O7d8FPy829GAleRRECgkHOMGJB0QeUbJCsKBQ0uA88kr")
    auth.set_access_token("1209924452760391682-FM8Xuy0gKWNZFNZqfx3o6AmXW57erO", "EYytb1yqADmI9Rpy90Z1QfwVFuXaV7ebcFOud0h53696N")
    api = tweepy.API(auth, wait_on_rate_limit=True)
    for tweet in tweepy.Cursor(api.search, q='#', count=100, lang='en').items():
        print(re.sub(r"(http.*)|(#.*)|(@.*? )|RT", "", tweet.text), tweet.lang) #removing links, hashtags, tags and various garbage
        #time.sleep(1)

if __name__ == "__main__":
    main()