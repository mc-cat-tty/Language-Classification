#!/bin/python

from Modules.analyzer import LettersFreq, FileLingua


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
