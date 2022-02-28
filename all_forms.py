#!/usr/bin/python3

import argparse
import collections
import csv
import os
import pickle
import sqlite3
import sys

from .wordlist import Wordlist

class AllForms:

    def __init__(self, db=None):

        if db:
            existing = os.path.exists(db)
            # TODO check if file exists
            self.dbcon = sqlite3.connect(db)
            self.dbcon.execute('PRAGMA synchronous = OFF')
            if not existing:
                self.dbcon.execute('''CREATE TABLE forms (form text, pos text, lemma text, UNIQUE(form,pos,lemma))''')
        else:
            self.dbcon = sqlite3.connect(":memory:")
            self.dbcon.execute('''CREATE TABLE forms (form text, pos text, lemma text, UNIQUE(form,pos,lemma))''')

    def get_lemmas(self, word, filter_pos=None):
        if filter_pos:
            res = self.dbcon.execute("SELECT pos || '|' || lemma FROM forms WHERE form=? AND pos=? ORDER BY pos, lemma", (word, filter_pos))
        else:
            res = self.dbcon.execute("SELECT pos || '|' || lemma FROM forms WHERE form=? ORDER BY pos, lemma", (word,))

        return [x[0] for x in res]

    @property
    def all_forms(self):
        for x in self.dbcon.execute("SELECT DISTINCT form FROM forms ORDER BY form"):
            yield x[0]

    @property
    def all(self):
        return self.dbcon.execute("SELECT form, pos, lemma  FROM forms ORDER BY form, pos, lemma")

    @classmethod
    def from_data(cls, allforms_data, db=None):
        self = cls(db)

        self.dbcon.execute("BEGIN TRANSACTION;")

        cr = csv.reader(allforms_data)
        for form,pos,*lemmas in cr:
            for lemma in lemmas:
                self._add_form(form, pos, lemma)

        self.dbcon.execute('''CREATE INDEX idx_form_pos ON forms (form, pos)''')
        self.dbcon.execute("COMMIT;")
        return self

    @classmethod
    def from_file(cls, filename, cache_words=True):
        # check for cached version
        cached = filename + ".sqlite"
        if os.path.exists(cached) and os.path.getctime(cached) > os.path.getctime(filename):
            self = cls(cached)
            return self

        with open(filename) as infile:
            print("compiling", cached, file=sys.stderr)
            return cls.from_data(infile, cached)

    @classmethod
    def from_wordlist(cls, wordlist, resolve_lemmas=True):
        self = cls()

        self.dbcon.execute("BEGIN TRANSACTION;")
        self._load_wordlist_forms(wordlist, resolve_lemmas)
        self.dbcon.execute('''CREATE INDEX idx_form_pos ON forms (form, pos)''')
        self.dbcon.execute("COMMIT;")

#        for formtype, count in self.count_formtype.items():
#            print(formtype, count, file=sys.stderr)

        return self

    def _load_wordlist_forms(self, wordlist, resolve_lemmas):
        for word in wordlist.iter_all_words():
            self._process_word_forms(word, wordlist, resolve_lemmas)

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

            w = next(wordlist.get_words(lemma, word.pos), None)
            if w and self.is_lemma(w):
                lemmas[lemma] = formtypes

#            if any(self.is_lemma(w) for w in wordlist.get_words(lemma, word.pos)):
#                lemmas[lemma] = formtypes

            elif max_depth>0:
                for redirect in wordlist.get_words(lemma, word.pos):
                    lemmas.update(self._resolve_lemmas(wordlist, redirect, max_depth-1))
                    break # Only look at the first word

            else:
                print(f"Lemma recursion exceeded: {word.word} {word.pos} -> {lemma}", file=sys.stderr)
                return {}

        return lemmas

    def _process_word_forms(self, word, wordlist, resolve_lemmas):

        if not len(word.senses):
            return

        if resolve_lemmas:
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

        self.dbcon.execute("INSERT OR IGNORE INTO forms VALUES (?, ?, ?)", [form, pos, lemma])

#        value = f"{pos}|{lemma}"
#        if value not in self.all_forms[form]:
#            self.all_forms[form].append(value)
