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

    def get_lemmas(self, word, filter_pos=[]):
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
                if filter_pos and pos not in filter_pos:
                    continue

                for lemma in lemmas:
                    value = f"{pos}|{lemma}"
                    if value not in results:
                        results.append(f"{pos}|{lemma}")

            return results
        else:
            if not filter_pos:
                return self.all_forms.get(word, [])
            return [x for x in self.all_forms.get(word, []) if x.split("|")[0] in filter_pos]

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

    def is_lemma(self, word):

        """
        Returns True if
           + " form" not in meta
           + the first gloss is not a "form of"
        else False

        Note, there's a similar implementation in dump_lemmas,
        any major improvements should be ported there
        """

        if not word.senses:
            return False

        if word.meta and " form" in word.meta and " form" not in word.word:
            return False

        # If the first sense is a form-of, it's not a lemma
        for sense in word.senses:
            if sense.formtype:
                return False
            break # Only look at the first sense

        return True


    def _resolve_lemmas(self, wordlist, word, max_depth=3):
        """
        follows a wordform to its final lemma
        word is a Word object
        Returns a dict: { lemma1: [formtypes], .. }
        """

        if self.is_lemma(word):
            return {word.word: [word.genders]}

        lemmas = {}
        for lemma, formtypes in word.form_of.items():

            if any(self.is_lemma(w) for w in wordlist.get_words(lemma, word.pos)):
                lemmas[lemma] = formtypes

            elif max_depth>0:
                for redirect in wordlist.get_words(lemma, word.pos):
                    lemmas.update(self._resolve_lemmas(wordlist, redirect, max_depth-1))
                    break # Only look at the first word

            else:
                print(f"Lemma recursion exceeded: {word.word} {word.pos} -> {lemma}", file=sys.stderr)
                return {}

        return lemmas

    def _process_word_forms(self, word, wordlist):

        if not len(word.senses):
            return

        if self.resolve_true_lemmas:
            if self.is_lemma(word):
                self._add_form(word.word, word.pos, word.word)
                self._add_word_forms(word, word.word, wordlist)

            for lemma, formtypes in self._resolve_lemmas(wordlist, word).items():
                self._add_form(word.word, word.pos, lemma)
                self._add_word_forms(word, lemma, wordlist)

        else:
#            if not (word.pos == "v" and not word.is_lemma):
            self._add_form(word.word, word.pos, word.word)
            self._add_word_forms(word, word.word, wordlist)

            for lemma, formtypes in word.form_of.items():
                self._add_form(word.word, word.pos, lemma)
                self._add_word_forms(word, lemma, wordlist)

    opposite_genders = {"m": "f", "f": "m", "m-p": "fpl", "f-p": "mpl"}
    def _add_word_forms(self, word, lemma, wordlist):
        """ Add all of a word's forms to the given lemma """

        non_binary = "m" in word.forms and "f" in word.forms

        if word.genders in self.opposite_genders:
            opposite =  self.opposite_genders[word.genders]
            opposite_forms = word.forms.get(opposite, [])
            opposite_words = [ w for x in opposite_forms for w in wordlist.get_words(x, word.pos) ]

            # If this is a lemma, restrict overrides to opposite lemmas
            # Conversely, if this is a form, allow opposite gendered forms to override it
            if self.is_lemma(word):
                opposite_words = [ w for w in opposite_words if self.is_lemma(w) ]
        else:
            opposite_words=[]

        for formtype, forms in word.forms.items():
            #self.count_formtype[formtype] += 1
            for form in forms:

                # If this a gendered noun adding a form of the opposite gender, verify the form isn't already declared
                # by the opposite lemma
                if opposite_words and word.word != form and formtype in ["m", "mpl", "fpl"] and formtype[0] != word.genders \
                   and any(x for x in opposite_words if form == x.word or any(y for y in x.forms.values() if form in y)):
                    continue

                if word.genders == "f" and word.form_of and formtype in ["m", "mpl"]:
                    continue

                if non_binary and formtype in ["m", "f", "mpl", "fpl"]:
                    continue


                self._add_form(form, word.pos, lemma)

    def _add_form(self, form, pos, lemma):
        if form == "-":
            return

        value = f"{pos}|{lemma}"
        if value not in self.all_forms[form]:
            self.all_forms[form].append(value)
