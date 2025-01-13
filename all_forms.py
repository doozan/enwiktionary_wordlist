#!/usr/bin/python3

import argparse
import collections
import csv
import io
import os
import sqlite3
import sys

from .wordlist import Wordlist

class AllForms:
    FEM_LEMMAS = ["cabra", "rata"]

    def __init__(self, dbfilename=None):

        if dbfilename:
            existing = os.path.exists(dbfilename)
            self.dbcon = sqlite3.connect(dbfilename)
            self.dbcon.execute('PRAGMA synchronous=OFF;')

            if not existing:
                self.dbcon.execute('''CREATE TABLE forms (form text, pos text, lemma text, UNIQUE(form,pos,lemma))''')
        else:
            self.dbcon = sqlite3.connect(":memory:")
            self.dbcon.execute('''CREATE TABLE forms (form text, pos text, lemma text, UNIQUE(form,pos,lemma))''')

    def get_lemmas(self, word, filter_pos=None):
        if filter_pos:
            if isinstance(filter_pos, list):
                in_clause = ",".join(["?"]*len(filter_pos))
                res = self.dbcon.execute(f"SELECT pos || '|' || lemma FROM forms WHERE form=? AND pos IN ({in_clause}) ORDER BY pos, lemma", (word, *filter_pos))
            else:
                res = self.dbcon.execute("SELECT pos || '|' || lemma FROM forms WHERE form=? AND pos=? ORDER BY pos, lemma", (word, filter_pos))
        else:
            res = self.dbcon.execute("SELECT pos || '|' || lemma FROM forms WHERE form=? ORDER BY pos, lemma", (word,))

        return [x[0] for x in res]

    def get_lemma_forms(self, lemma, filter_pos=None):
        if filter_pos:
            res = self.dbcon.execute(f"SELECT DISTINCT form FROM forms WHERE lemma=? AND pos=?", (lemma, filter_pos,))
        else:
            res = self.dbcon.execute(f"SELECT DISTINCT form FROM forms WHERE lemma=?", (lemma,))

        return [x[0] for x in res]

    def has_form(self, form, pos=None):
        if pos:
            res = self.dbcon.execute(f"SELECT form FROM forms WHERE form=? AND pos=? LIMIT 1", (form, pos,))
        else:
            res = self.dbcon.execute(f"SELECT form FROM forms WHERE form=? LIMIT 1", (form,))
        return bool(list(res))

    def has_lemma(self, lemma, pos=None):
        if pos:
            res = self.dbcon.execute(f"SELECT form FROM forms WHERE form=? and lemma=? AND pos=? LIMIT 1", (lemma, lemma, pos,))
        else:
            res = self.dbcon.execute(f"SELECT form FROM forms WHERE form=? and lemma=? LIMIT 1", (lemma,lemma))
        return bool(list(res))

    def get_form_pos(self, form):
        for x in self.dbcon.execute(f"SELECT DISTINCT pos FROM forms WHERE form=?", (form,)):
            yield x[0]

    @property
    def all_lemmas(self):
        for x in self.dbcon.execute("SELECT DISTINCT lemma FROM forms ORDER BY lemma"):
            yield x[0]

    @property
    def all_forms(self):
        for x in self.dbcon.execute("SELECT DISTINCT form FROM forms ORDER BY form"):
            yield x[0]

    @property
    def all(self):
        return self.dbcon.execute("SELECT form, pos, lemma  FROM forms ORDER BY form, pos, lemma")

    def get_all_forms(self, filter_pos):
        if filter_pos:
            if isinstance(filter_pos, list):
                in_clause = ",".join(["?"]*len(filter_pos))
                res = self.dbcon.execute(f"SELECT DISTINCT form FROM forms WHERE pos IN ({in_clause})")
            else:
                res = self.dbcon.execute(f"SELECT DISTINCT form FROM forms WHERE pos=?", (filter_pos,))

        return [x[0] for x in res]

    @classmethod
    def from_data(cls, allforms_data, dbfilename=None):
        self = cls(dbfilename)

        self.dbcon.execute("BEGIN TRANSACTION;")

        cr = csv.reader(allforms_data)
        for form,pos,*lemmas in cr:
            for lemma in lemmas:
                self._add_form(form, pos, lemma)

        self.dbcon.execute('''CREATE INDEX idx_form_pos ON forms (form, pos)''')
        self.dbcon.execute('''CREATE INDEX idx_lemma ON forms (lemma)''')
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
    def from_wordlist(cls, wordlist):
        self = cls()

        self.dbcon.execute("BEGIN TRANSACTION;")
        self._load_wordlist_forms(wordlist)
        self.dbcon.execute('''CREATE INDEX idx_form_pos ON forms (form, pos)''')
        self.dbcon.execute("COMMIT;")

        return self

    def _load_wordlist_forms(self, wordlist):

        prev_pos = None
        prev_word = None
        primary_lemma = True
        for word in wordlist.iter_all_words():

            if self.is_lemma(word):
                self._add_form(word.word, word.pos, word.word)
                self._add_word_forms(word, word.word, wordlist)
                self._add_female_equivalent(word, wordlist)
                self._add_reflexive_infinitive(word, wordlist)
            else:
                for lemma, formtypes in word.form_of.items():
                    self._add_form(word.word, word.pos, lemma)
                    self._add_word_forms(word, lemma, wordlist)

    @staticmethod
    def is_lemma(word):

        """
        This is based on wiktionary's concept of a lemma, which is that it doesn't declare a form of in header:
           + " form" not in meta

        This is different from the implementation in dump_lemmas, which is more strict
        """

        if not word.senses:
            return False

        if word.meta and (
                (" form" in word.meta and "apocopate" not in word.meta and " form" not in word.word)
                or "misspelling" in word.meta
                or "es-past participle" in word.meta
                ):
            return False

        return True


    def _add_reflexive_infinitive(self, word, wordlist):
        if word.pos != "v":
            return

        if word.word.endswith("rse"):
            self._add_form(word.word[:-2], word.pos, word.word)

    def _add_female_equivalent(self, word, wordlist):
        if word.genders != "m":
            return

        if word.pos not in ["n", "prop", "suffix"]:
            return

        fems = word.forms.get("f", [])
        fpl = word.forms.get("fpl", [])

        for i,form in enumerate(fems):
            if not form:
                continue

            if not wordlist.has_word(form, word.pos):
                self._add_form(form, word.pos, form)

            if len(fems) == len(fpl):
                self._add_form(fpl[i], word.pos, form)
            else:
                # If there are multiple female lemmas and nota a 1-to-1 mapping of lemmas to plurals,
                # it will be impossible to guess which plural(s) match to which lemmas
                # Luckily, there's nothing like that in the dataset. Yet.
                if len(fems) > 1:
                    raise ValueError("multiple female lemmas with multiple plurals",
                            word.word, word.pos, fems, fpl, file=sys.stderr)
                for pl in fpl:
                    self._add_form(pl, word.pos, form)


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

                if word.genders == "f" and word.form_of and formtype in ["m", "mpl"] and word.word not in self.FEM_LEMMAS:
                    continue

                if non_binary and formtype in ["m", "f", "mpl", "fpl"]:
                    continue

                self._add_form(form, word.pos, lemma)

    def _add_form(self, form, pos, lemma):
        if form == "-":
            return

        for f in form.split("|"):
            self.dbcon.execute("INSERT OR IGNORE INTO forms VALUES (?, ?, ?)", [f, pos, lemma])


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
