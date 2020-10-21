#!/usr/bin/python3

import os
import re
import sys

from wordlist import Wordlist

#ignore_notes = {
#    "archaic",
#    "dated",
#    "eye dialect",
#    "heraldry",
#    "heraldiccharge",
#    "historical",
#    "numismatics",
#    "obsolete",
#    "rare",
#}


class Meta():

    def __init__(self, word, common_pos, forms={}):
        self.word = word
        self.common_pos = common_pos
        self.forms = {**forms}

    @classmethod
    def from_word(cls, word):
        return cls(word.word, word.common_pos, word.forms)

    def add_form(self, formtype, form):
        if formtype not in self.forms:
            self.forms[formtype] = [form]
        elif form not in self.forms[formtype]:
            self.forms[formtype].append(form)

    def add_forms(self, formtype, all_forms):
        if not all_forms:
            return

        # use supplied formtype instead of the all_forms key
        for forms in all_forms.values():
            for form in forms:
                self.add_form(formtype, form)

    def __str__(self):
        line = [self.word, "{meta-" + self.common_pos + "}", "::"]

        forms = [ f"{k}={v}" for k, values in sorted(self.forms.items()) for v in values ]
        line.append("; ".join(forms))

        return(" ".join(line))

def make_verb_meta(word, paradigm):
    pattern,stems = paradigm
    line = [word.word, "{meta-verb}", "::"]

    params = []
    if pattern:
        params.append(f"pattern={pattern}")
    if stems:
        for stem in stems:
            params.append(f"stem={stem}")
    line.append("; ".join(params))
    return " ".join(line)

def make_sense_line(word, sense):
    line = [word.word, "{"+sense.pos+"}"]
    if sense.qualifier:
        line.append("["+sense.qualifier+"]")
    if sense.synonyms and len(sense.synonyms):
        line.append("|")
        line.append("; ".join(sense.synonyms))
    line.append("::")
    line.append(sense.gloss)
    return " ".join(line)

def process_data(data):
    wordlist = Wordlist(data)

    all_meta = get_all_word_forms(wordlist)
    get_lemma_forms(wordlist, all_meta)

    seen_meta = set()
    for word in [ word for words in wordlist.all_words.values() for word in words ]:

        # Skip words with no definitions
        if not word.senses:
            continue

        metakey = (word.word, word.common_pos)

        # FIXME: probabyl better to always stor metakey in seen_meta, adding a meta line to secondary words may be troublesome
        # also, should add handling for cases where first word is a sense of and second has a definition - as is, the first sense of doesn't get printed
        # this will require buffering

        # If this is the first word and it's not a lemma and has no nonform def, don't print anything
        if metakey not in seen_meta and word.form_of and not any(sense.formtype is None or sense.nonform for sense in word.senses):
            continue

        if word.common_pos == "verb" and word.paradigms:
            for paradigm in word.paradigms:
                yield make_verb_meta(word, paradigm)

        if metakey not in seen_meta:
            seen_meta.add(metakey)
            meta = all_meta.get(metakey)
            # Only print metadata forms for words that are lemmas
            if meta and not word.form_of:
                yield str(meta)

        for sense in word.senses:
            if sense.gloss:
                yield make_sense_line(word, sense)


def get_all_word_forms(wordlist):
    """
    Build meta for each unique (word, common_pos) with forms
    for word, common_pos pairs with multiple words, consolidate
    all forms into single entry
    """

    all_forms = {}
    for word in [ word for words in wordlist.all_words.values() for word in words ]:
        if not word.forms:
            continue

        key = (word.word, word.common_pos)
        if key not in all_forms:
            all_forms[key] = Meta.from_word(word)
        else:
            meta = all_forms[key]

            for formtype, forms in word.forms.items():
                # If the first word declaration is a feminine lemma, that is, if
                # it's not a "feminine of" noun and has no masculine definitions,
                # do *not* add masculine forms from following definitions
                # eg, hamburguesa is feminine only in the sense "hamburger" but is followed
                # by another usage "feminine of hamburgués, woman from Hamburg",
                if formtype in ["m", "mpl"] and formtype not in meta.forms:
                    continue
                for form in forms:
                    meta.add_form(formtype, form)

    return all_forms


def get_lemma_forms(wordlist, all_meta):

    # Build meta for non-lemmas with "form of" definitions and
    # add all forms of non-lemma words to their lemmas
    for word in [ word for words in wordlist.all_words.values() for word in words ]:

        if not word.form_of:
            continue

        # If the word is not a lemma, add it and all of its forms to the lemma
        for lemma, formtypes in word.form_of.items():
            key = (lemma, word.common_pos)
            meta = all_meta.get(key)
            # If this word references a lemma without a meta, we must create an empty meta for it first
            if meta is None:
                if lemma not in wordlist.all_words:
                    print(f"Unknown word '{lemma}' referenced by {word.word}", file=sys.stderr)
                if lemma not in wordlist.all_words \
                        and lemma.endswith(".") \
                        and lemma.rstrip(".") in wordlist.all_words:
                    print(f"stripping . from {lemma} for {word.word}", file=sys.stderr)
                    key = (lemma.rstrip("."), word.common_pos)
                all_meta[key] = Meta(lemma, word.common_pos)
                meta = all_meta.get(key)

            for formtype in formtypes:
                meta.add_form(formtype, word.word)
                if not word.forms:
                    continue

                # If this is the feminine of a masculine, add all plurals as "fpl"
                if formtype == "f":
                    for form in word.forms.get("pl",[]):
                        meta.add_form("fpl", form)
                    for form in word.forms.get("fpl",[]):
                        meta.add_form("fpl", form)

                # Otherwise, just add all forms with the detected "form of" form
                # (for misspellings/alt forms, etc where both singular and plural should be flagged)
                elif word.forms:
                    meta.add_forms(formtype, word.forms)


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description="Post process wiktionary export")
    parser.add_argument("infile", help="Input file")
    args = parser.parse_args()

    with open(args.infile) as infile:
        for line in process_data(infile):
            print(line)
