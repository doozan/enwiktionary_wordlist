#!/usr/bin/python3

import argparse
import csv
import mmap
import sys

from .wordlist import Wordlist

class AllForms:

    def __init__(self):
        self.all_forms = {}

    def get_lemmas(self, word):
        if hasattr(self, 'mmap_obj'):
            if word not in self.all_forms:
                return []
            offset = self.all_forms[word]
            self.mmap_obj.seek(offset)

            results = []
            for line in iter(self.mmap_obj.readline, b''):

                line = line.decode('utf-8').strip()
                row = next(csv.reader([line]), None)
                form,pos,*lemmas = row
                if form != word:
                    break

                for lemma in lemmas:
                    value = f"{pos}|{lemma}"
                    if value not in results:
                        results.append(f"{pos}|{lemma}")

            return results
        else:
            return self.all_forms.get(word, [])

    @classmethod
    def from_data(cls, allforms_data):
        self = cls()

        cr = csv.reader(allforms_data)
        for form,pos,*lemmas in cr:
            for lemma in lemmas:
                self._add_form(form, pos, lemma)

        return self

    @classmethod
    def from_file(cls, filename):
        self = cls()

        self.file_obj = open(filename, mode="rb")
        self.mmap_obj = mmap.mmap(self.file_obj.fileno(), length=0, access=mmap.ACCESS_READ)

        offset = self.mmap_obj.tell()
        for line in iter(self.mmap_obj.readline, b''):

            line = line.decode('utf-8').strip()
            row = next(csv.reader([line]), None)
            if not row:
                continue
            form,pos,*lemmas = row
            if form not in self.all_forms:
                self.all_forms[form] = offset
            offset = self.mmap_obj.tell()

        return self

    @classmethod
    def from_wordlist(cls, wordlist):
        self = cls()
        self._load_wordlist_forms(wordlist)
        return self

    def _load_wordlist_forms(self, wordlist):
        """
        Return a list of all known word form/lemma combinations
        [ "form|pos|lemma", ... ]
        """

        for word in wordlist.iter_all_words():
            self._process_word_forms(word, wordlist)

    def _process_word_forms(self, word, wordlist):
        if not len(word.senses):
            return

        if word.is_lemma:
            self._add_word_forms(word, word.word)

        for lemma, formtypes in wordlist.get_lemmas(word).items():
            for lemma_formtype in formtypes:
                self._add_form(word.word, word.pos, lemma)
            self._add_word_forms(word, lemma)

    def _add_word_forms(self, word, lemma):
        """ Add all of a word's forms to the given lemma """
        for formtype, forms in word.forms.items():
            for form in forms:
                if formtype in [ "m", "masculine", "masculine_counterpart" ]:
                    continue
                if not word.is_lemma and formtype in ["f", "feminine", "feminine_counterpart"]:
                    if formtype in ["mpl", "masculine_plural"]:
                    #if formtype in ["m", "masculine", "masculine_counterpart", "mpl", "masculine_plural"]:
                        continue
                    if formtype in ["pl", "fpl", "plural", "feminine_plural"]:
                        formtype = "fpl"
                self._add_form(form, word.pos, lemma)

    def _add_form(self, form, pos, lemma):

        if form == "-":
            return

        value = f"{pos}|{lemma}"
        if form not in self.all_forms:
            self.all_forms[form] = [value]
        elif value not in self.all_forms[form]:
            self.all_forms[form].append(value)
