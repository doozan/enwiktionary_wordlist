#!/usr/bin/python3

import argparse
import collections
import csv
import io
import os
import pickle
import sqlite3
import sys

from .wordlist import Wordlist

class AllForms:

    def __init__(self, dbfilename=None):

        if dbfilename:
            existing = os.path.exists(dbfilename)
            self.dbcon = sqlite3.connect(dbfilename)
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
    def from_data(cls, allforms_data, dbfilename=None):
        self = cls(dbfilename)

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
        if os.path.exists(cached):
            if os.path.getctime(cached) > os.path.getctime(filename):
                return cls(cached)

            # delete the old cache
            os.remove(cached)

        with open(filename) as infile:
            return cls.from_data(infile, cached)

    @classmethod
    def from_wordlist(cls, wordlist, resolve_lemmas=True):
        self = cls()

        self.dbcon.execute("BEGIN TRANSACTION;")
        self._load_wordlist_forms(wordlist, resolve_lemmas)
        self.dbcon.execute('''CREATE INDEX idx_form_pos ON forms (form, pos)''')
        self.dbcon.execute("COMMIT;")

        return self

    def _load_wordlist_forms(self, wordlist, resolve_lemmas):

        prev_pos = None
        prev_word = None
        primary_lemma = True
        for word in wordlist.iter_all_words():

            if self.is_lemma(word):
                self._add_form(word.word, word.pos, word.word)
                self._add_word_forms(word, word.word, wordlist)
            else:
                for lemma, formtypes in word.form_of.items():
                    self._add_form(word.word, word.pos, lemma)
                    self._add_word_forms(word, lemma, wordlist)


            old = """

            secondary = bool(word.word == prev_word and word.pos == prev_pos)
            prev_word = word.word
            prev_pos = word.pos
            if not secondary:
                primary_lemma = True
            is_lemma = self.is_lemma(word)
            print(word.word, "is_lemma:", is_lemma)
            primary_lemma = primary_lemma and is_lemma

            if not len(word.senses):
                continue

            if False: #resolve_lemmas:
                # Only add forms for primary lemmas (lemmas that occur before a nonlemma)
                if primary_lemma:
                    print("primary lemma", word.word, word.pos, word.genders)
                    self._add_form(word.word, word.pos, word.word)
                    self._add_word_forms(word, word.word, wordlist)
                else:
                    print("non-primary lemma", word.word)

                    # Don't try to resolve secondary lemmas
#                    if is_lemma:
#                        continue

                    for lemma, formtypes in self._resolve_lemmas(wordlist, word).items():
                        print("  adding", lemma, formtypes)
                        self._add_form(word.word, word.pos, lemma)
                        self._add_word_forms(word, lemma, wordlist)

            else:
#                if not (word.pos == "v" and not word.is_lemma):
                self._add_form(word.word, word.pos, word.word)
                self._add_word_forms(word, word.word, wordlist)

                for lemma, formtypes in word.form_of.items():
                    self._add_form(word.word, word.pos, lemma)
                    self._add_word_forms(word, lemma, wordlist)
"""

    @staticmethod
    def is_lemma(word):

        """
        This is based on wiktionary's concept of a lemma, which is that it doesn't declare a form of in header:
           + " form" not in meta

        This is different from the implementation in dump_lemmas, which is more strict
        """

        if not word.senses:
            return False

        if word.meta and " form" in word.meta and " form" not in word.word:
            return False

#        if word.pos == "n" and word.genders == "f" and "m" in word.forms and word.word not in FEM_LEMMAS:
#            return False

        # If the first sense is a form-of, it's not a lemma
#        for sense in word.senses:
#            if sense.formtype:
#                return False
#            break # Only look at the first sense

        return True


#    @classmethod
#    def _resolve_lemmas(cls, wordlist, word, max_depth=3):
        """
        follows a wordform to its final lemma
        word is a Word object
        Returns a dict: { lemma1: [formtypes], .. }

        if cls.is_lemma(word):
            return {word.word: [word.genders]}

        lemmas = {}
        for lemma, formtypes in word.form_of.items():

            w = next(wordlist.get_words(lemma, word.pos), None)
            if cls.is_lemma(w):
                lemmas[lemma] = formtypes

#            if any(cls.is_lemma(w) for w in wordlist.get_words(lemma, word.pos)):
#                lemmas[lemma] = formtypes

            elif max_depth>0:
                for redirect in wordlist.get_words(lemma, word.pos):
                    lemmas.update(cls._resolve_lemmas(wordlist, redirect, max_depth-1))
                    break # Only look at the first word

            else:
                print(f"Lemma recursion exceeded: {word.word} {word.pos} -> {lemma}", file=sys.stderr)
                return {}

        return lemmas
"""

    #opposite_genders = {"m": "f", "f": "m", "m-p": "fpl", "f-p": "mpl"}
    opposite_genders = {"f": "m", "f-p": "mpl"}
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


    @property
    def all_csv(self):
        lemmas = []
        prev_pos = None
        prev_form = None
        for form, pos, lemma in self.all:
            if form != prev_form or pos != prev_pos:
                if lemmas:
                    yield self.make_csv(prev_form, prev_pos, lemmas)
                lemmas = []
            lemmas.append(lemma)
            prev_form = form
            prev_pos = pos
        yield self.make_csv(prev_form, prev_pos, lemmas)

    @staticmethod
    def make_csv(form, pos, lemmas):
        si = io.StringIO()
        cw = csv.writer(si)
        cw.writerow([form,pos]+sorted(lemmas))
        return si.getvalue().strip()


#        value = f"{pos}|{lemma}"
#        if value not in self.all_forms[form]:
#            self.all_forms[form].append(value)
