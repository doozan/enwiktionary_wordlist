#!/usr/bin/python3

import argparse
import csv
import sys

from .wordlist import Wordlist

class AllForms:

    def __init__(self):
        self.all_forms = {}

    @classmethod
    def from_csv(cls, allforms_data):
        self = cls()

        cr = csv.reader(allforms_data)
        for form,pos,*lemmas in cr:
            for lemma in lemmas:
                self._add_form(form, pos, lemma)

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
#        for word in wordlist.get_words("de"):
#            self._process_word_forms(word, wordlist)
#        for word in wordlist.get_words("des"):
#            self._process_word_forms(word, wordlist)

    def _process_word_forms(self, word, wordlist):
        if not len(word.senses):
            return

        for lemma, formtypes in wordlist.get_lemmas(word).items():
            for lemma_formtype in formtypes:
                self._add_form(word.word, word.common_pos, lemma)

            for formtype, forms in word.forms.items():
                for form in forms:
                    if formtype in [ "m", "masculine", "masculine_counterpart" ]:
                        continue
                    if not word.is_lemma and lemma_formtype in ["f", "feminine", "feminine_counterpart"]:
                        if formtype in ["mpl", "masculine_plural"]:
                        #if formtype in ["m", "masculine", "masculine_counterpart", "mpl", "masculine_plural"]:
                            continue
                        if formtype in ["pl", "fpl", "plural", "feminine_plural"]:
                            formtype = "fpl"
                    self._add_form(form, word.common_pos, lemma)

    def _add_form(self, form, pos, lemma):

        if form == "-":
            return

        #value = f"{form}|{pos}|{lemma}"
        #self.all_forms.add(value)

        value = f"{pos}|{lemma}"
        if form not in self.all_forms:
            #self.all_forms[form] = {value}
            self.all_forms[form] = [value]
        elif value not in self.all_forms[form]:
            self.all_forms[form].append(value)
#        else:
#            self.all_forms[form].(value)
