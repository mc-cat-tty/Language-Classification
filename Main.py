#!/bin/python

import string, csv
from typing import Dict, Any


class Alphabet:
    charset = list(string.ascii_lowercase)

class LettersFreq:
    letters_freq = {}
    filename = ''

    def set_file(file_name):
        LettersFreq.filename = file_name
        LettersFreq._import_letters_freq()

    @staticmethod
    def _import_letters_freq():
        with open(LettersFreq.filename, "r") as file:
            csv_file = csv.DictReader(file, delimiter=',')
            for row in csv_file:
                row = dict(row) #Convert row to dict
                lang = row['Language']
                del row['Language'] #Remove 'Language' fields
                for letter, freq in row.items():
                    row[letter] = float(freq.strip("%")) #Convert form num% to float
                #print(row)
                LettersFreq.letters_freq[lang] = row #Remain only a dict of letter:frequency
            #print(LettersFreq.letters_freq)

class FileLingua(Alphabet, LettersFreq):
    def __init__(self, filename):
        self.filename = filename
        file = open(filename, "rt")
        self.txt = file.read()
        self.rows = len(self.txt.split('\n')) - 1
        self.words = len(self.txt.split())
        self.chars = len(self.txt)
        self.chars_freq = {} #Frequency of each alphabet char
        self.lang = '' #Language
        self.distances = {} #Distance between file chars freq and refernce chars freq
        file.close()
        self._extract_chars_freq()
        self._find_lang()

    def __repr__(self):  # Overriding object method
        return "\"%s\" have %d chars, %d words, %d rows. Written in %s language." % (
        self.filename, self.chars, self.words, self.rows, self.lang)

    def __str__(self):
        return "\"%s\" [chars=%d, words=%d, rows=%d, language=%s]" % (
        self.filename, self.chars, self.words, self.rows, self.lang)

    def file_format(self):
        chars_freq_scheme = ''
        for letter, freq in self.chars_freq.items():
            chars_freq_scheme += "{:>20} : {}\n".format(letter, freq)
        return """\
Filename: {}
Chars number: {}
Words number: {}
Rows number: {}
Chars frequency:
{}
Language: {}
        """.format(self.filename, self.chars, self.words, self.rows, chars_freq_scheme, self.lang)

    def _extract_chars_freq(self):  # Private method
        if (not self.chars_freq):  # Check if chars_freq dict already exists
            for letter in FileLingua.charset:  # if not pupulate it
                self.chars_freq[letter] = (self.txt.count(letter) *100 / self.chars)

    def _find_lang(self):
        distances = {}
        for lang, freq_dict in LettersFreq.letters_freq.items():
            dist = 0
            for (letter, freq1), (letter, freq2) in zip(freq_dict.items(), self.chars_freq.items()):
                dist += abs(freq1-freq2)
            distances[dist] = lang
        #print(distances) #Debug
        self.lang = distances[min(distances.keys())]

    def save_stat_file(self):
        filename = self.filename.split('.')[0] + ".stat"
        file = open(filename, "wt")
        file.write(self.file_format())
        file.close()

    def save_csv_file(self):
        pass

    def save_json_file(self):
        pass

    def evaluate_quality(self):
        '''implements Twitter API to estimate a quality of reconaissance'''
        pass

def main():
    LettersFreq.set_file("Frequency_Tables/letters_frequency.csv")
    ita = FileLingua("Test_Files/ita.txt")
    print(ita)
    ita.save_stat_file()

    fr = FileLingua("Test_Files/fr.txt")
    print(fr)
    fr.save_stat_file()



if __name__ == "__main__":
    main()
