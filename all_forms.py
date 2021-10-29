#!/usr/bin/python3

import argparse
import collections
import csv
import mmap
import sys

from .wordlist import Wordlist

class AllForms:

    def __init__(self, resolve_true_lemmas=True):
        #self.count_formtype = collections.defaultdict(lambda: 0)
        self.all_forms = collections.defaultdict(list)
        self.resolve_true_lemmas = resolve_true_lemmas

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
    def from_wordlist(cls, wordlist, resolve_true_lemmas=True):
        self = cls(resolve_true_lemmas)
        self._load_wordlist_forms(wordlist)

#        for formtype, count in self.count_formtype.items():
#            print(formtype, count, file=sys.stderr)

        return self

    def _load_wordlist_forms(self, wordlist):
        for word in wordlist.iter_all_words():
            self._process_word_forms(word, wordlist)

    def _process_word_forms(self, word, wordlist):
        if not len(word.senses):
            return

        if self.resolve_true_lemmas:
            if word.is_lemma:
                self._add_word_forms(word, word.word)

            for lemma, formtypes in wordlist.get_lemmas(word).items():
                self._add_form(word.word, word.pos, lemma)
                self._add_word_forms(word, lemma)

        else:
            if word.is_lemma or (word.form_of and any(x for x in ["alt", "old", "rare", "spell"] for f in word.form_of.values() if x in f)):
                self._add_form(word.word, word.pos, word.word)
                self._add_word_forms(word, word.word)

    def _add_word_forms(self, word, lemma):
        """ Add all of a word's forms to the given lemma """

        for formtype, forms in word.forms.items():
            #self.count_formtype[formtype] += 1
            for form in forms:
                if formtype == "m":
                    continue

                if word.pos == "n" and  formtype == "mpl":
                    continue

                # ignore masculine/feminine counterparts of non binary words
                if word.genders == "m; f" and formtype in ["m", "f", "mpl", "fpl"]:
                    continue


                self._add_form(form, word.pos, lemma)

    def _add_form(self, form, pos, lemma):
        if form == "-":
            return

        value = f"{pos}|{lemma}"
        if value not in self.all_forms[form]:
            self.all_forms[form].append(value)
