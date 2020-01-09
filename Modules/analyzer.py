#!/bin/python

# This module provides classes and constants to analyze the language of a text given as input (also form a file)

import csv
import math
import string
from re import sub

charset = list(string.ascii_lowercase)

def extract_chars_freq(text):
    if not text:
        return {l: 0.0 for l in charset}
    text = text.lower()
    text_len = len(sub('[^a-z]', '', text))  # Count only lowercase characters in text
    return {l: (text.count(l) * 100 / text_len) for l in charset}

def find_lang(text):
    distances = {}
    chars_freq = extract_chars_freq(text)
    for lang, freq_dict in LettersFreq.letters_freq.items():
        dist = 0
        for (letter1, freq1), (letter2, freq2) in zip(freq_dict.items(), chars_freq.items()):
            dist += (freq1 - freq2) ** 2
        distances[math.sqrt(dist)] = lang
    return distances[min(distances.keys())]


class LettersFreq:
    letters_freq = {}
    filename = ''

    @staticmethod
    def set_file(file_name): # TODO : docstring = class to initialize with the .csv file containing the reference table
        LettersFreq.filename = file_name
        LettersFreq._import_letters_freq()

    @staticmethod
    def _import_letters_freq():
        with open(LettersFreq.filename, "r") as file:
            csv_file = csv.DictReader(file, delimiter=',')
            for row in csv_file:
                row = dict(row)  # Convert row to dict
                lang = row['Language']
                del row['Language']  # Remove 'Language' fields
                for letter, freq in row.items():
                    row[letter] = float(freq.strip("%"))  # Convert form num% to float
                # print(row)
                LettersFreq.letters_freq[lang] = row  # Remain only a dict of letter:frequency
            # print(LettersFreq.letters_freq)


class TestoLingua(LettersFreq):
    def __init__(self, text):
        self.text = text
        self.rows = len(self.text.split('\n'))
        self.words = len(self.text.split())
        self.chars = len(self.text)
        self.chars_freq = {}  # Frequency of each alphabet char
        self.lang = ''  # Language
        self.distances = {}  # Distance between file chars freq and reference chars freq
        self._extract_chars_freq()
        self._find_lang()

    def __repr__(self):  # Overriding object method
        return "This text have {} chars, {} words, {} rows. Written in {} language." .format(
            self.chars, self.words, self.rows, self.lang)

    def __str__(self):
        return "\"{:.10}...\" [chars={}, words={}, rows={}, language={}]".format(
            self.text, self.chars, self.words, self.rows, self.lang)

    def stat_format(self):
        chars_freq_scheme = ''
        for letter, freq in self.chars_freq.items():
            chars_freq_scheme += "{:>20} : {}\n".format(letter, freq)
        return """\
Text: {:.10}...
Chars number: {}
Words number: {}
Rows number: {}
Chars frequency:
{}
Language: {}
            """.format(self.text, self.chars, self.words, self.rows, chars_freq_scheme, self.lang)

    def stat(self):  # statistics
        return {"Chars number": self.chars, "Words number": self.words, "Rows number": self.rows,
                "Language": self.lang, "Chars frequency": {l:'{}%'.format(round(f, 2)) for l, f in self.chars_freq.items()}}

    def _extract_chars_freq(self):  # Private method
        if not self.chars_freq:  # Check if chars_freq dict already exists
            self.chars_freq = extract_chars_freq(self.text)

    def _find_lang(self):
        self.lang = find_lang(self.text)

class FileLingua(TestoLingua):
    def __init__(self, filename):
        self.filename = filename
        file = open(filename, "rt")
        super().__init__(file.read())
        file.close()
        self.rows -= 1 # len() counts also the last void line

    def __repr__(self):  # Overriding object method
        return '"{}" '.format(self.filename) + super().__repr__()

    def __str__(self):
        return '"{}" '.format(self.filename) + super().__str__()

    def stat_format(self):
        return "Filename: {}\n".format(self.filename) + super().stat_format()

    def stat_file(self):
        filename = self.filename.rsplit('.', 1)[0] + ".stat"  # split starting from the right
        file = open(filename, "wt")
        file.write(self.stat_format())
        file.close()
    
    # def stat(self):
    #     d =  super().stat()
    #     d.setdefault("Filename", self.filename)
    #     return d.update({"Filename": self.filename})

    def csv_file(self):  # TODO
        pass

    def json_file(self):  # TODO
        pass


def main():
    LettersFreq.set_file("../Frequency_Tables/letters_frequency_twitter.csv")
    ita = FileLingua("../Test_Files/ita.txt")
    print(ita)
    ita.stat_file()

    fr = FileLingua("../Test_Files/fr.txt")
    print(fr)
    fr.stat_file()

    en = FileLingua("../Test_Files/en.txt")
    print(en)
    en.stat_file()

    es = FileLingua("../Test_Files/es.txt")
    print(es)
    es.stat_file()


if __name__ == "__main__":
    main()
