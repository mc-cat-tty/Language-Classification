#/usr/bin/env python

import csv, string


# This script converts "letters_frequency_vertical.csv" in a more usable and useful .csv file reversing rows and columns

def main():
    dict_f = {}
    with open("../Frequency_Tables/letters_frequency.csv", "wt") as file_out:
        csv_file_out = csv.writer(file_out)
        with open("../Frequency_Tables/letters_frequency_vertical.csv", "r") as file:
            csv_file = csv.DictReader(file, delimiter=';')
            for line in csv_file:
                print(line, '\n')
                for lang, freq in line.items():
                    if lang == 'Letter':
                        letter = freq
                    else:
                        try:
                            dict_f[lang][letter] = freq
                        except KeyError:
                            dict_f[lang] = {}
                            dict_f[lang][letter] = freq
        print(dict_f)
        buf = ["Language"]
        buf += list(string.ascii_lowercase)
        csv_file_out.writerow(buf)
        for lang, freq in dict_f.items():
            buf = [lang]
            buf += list(freq.values())
            csv_file_out.writerow(buf)
    # with open("letters_frequency.csv", "wt") as file:
    #     csv_file = csv.DictWriter(file, fieldnames=list(string.ascii_lowercase))
    #     csv_file.writeheader()
    #     csv_file.writerows(list(dict_f.items()))


if __name__ == '__main__':
    main()
