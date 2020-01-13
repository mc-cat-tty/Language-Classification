#!/bin/python

from wikipediaapi import Wikipedia
import requests
from Modules.analyzer import find_lang, LettersFreq
from Modules.tweetrain import langs


class Dataset:
    def __init__(self, dataset_len):
        self.dataset_len = dataset_len

    def _remove_unknown_langs(self, pages):
        return {lang: page for lang, page in pages.items() if lang in langs.values()}

    def _get_random_page(
            self):  # This function use web API because in wikipediaapi isn't implemented any function to get a random page
        while True:
            page = requests.get("https://en.wikipedia.org/api/rest_v1/page/random/summary").json()
            if page['lang'] in langs.values():
                return page

    def get_dataset(self):
        data = []
        while len(data) < self.dataset_len:
            rand_page = self._get_random_page()
            lang = rand_page['lang']
            wiki = Wikipedia(lang)
            page = wiki.page(rand_page['title'])
            data.append({'lang': lang, 'text': page.text})
            langlinks = self._remove_unknown_langs(page.langlinks)
            for lang, page in langlinks.items():
                data.append({'lang': lang, 'text': page.text})
        return data


class QualityEvaluator:
    def __init__(self, dataset_len):
        self.dataset = Dataset(dataset_len).get_dataset()
        self._confusion_dict = {'true_pos': {}, 'false_neg': {}, 'false_pos': {}, 'true_neg': {}, 'total': {}}
        self._compile_confusion()

    def _compile_confusion(self):
        def catalogue(p, l):
            predicted_lang = langs[find_lang(p['text'])]
            if p['lang'] == l:
                if predicted_lang == l:
                    self._confusion_dict['true_pos'][l] += 1
                else:
                    self._confusion_dict['false_neg'][l] += 1
                self._confusion_dict['total'][l] += 1
            else:
                if predicted_lang == l:
                    self._confusion_dict['false_pos'][l] += 1
                else:
                    self._confusion_dict['true_neg'][l] += 1

        for lang in langs.values():
            for key in self._confusion_dict.keys():
                self._confusion_dict[key].setdefault(lang, 0)
            for page in self.dataset:
                catalogue(page, lang)
        #  TODO : remove void elements

    def sensitivity(self):  # Proportion of actual positives that are correctly identified
        true_pos = sum(self._confusion_dict['true_pos'].values())
        false_neg = sum(self._confusion_dict['false_neg'].values())
        return true_pos / (true_pos + false_neg)

    def specificity(self):  # Proportion of actual negatives that are correctly identified
        true_neg = sum(self._confusion_dict['true_neg'].values())
        false_pos = sum(self._confusion_dict['false_pos'].values())
        return true_neg / (true_neg + false_pos)

    def quality_parameters(self):
        confusion_dict = self._confusion_dict
        confusion_dict.update({'sensitivity': self.sensitivity(), 'sensibility': self.specificity()})
        return confusion_dict


def main():
    # wiki = Wikipedia("en")
    # page = wiki.page("ab")
    # print(page.exists(), page.text)
    # print(Dataset(10).get_dataset())
    LettersFreq.set_file("../Frequency_Tables/letters_frequency_twitter.csv")
    q = QualityEvaluator(10)
    print(q.sensitivity())
    print(q.specificity())
    print(q.quality_parameters())


if __name__ == "__main__":
    main()
