#!/usr/bin/python3
# -*- python-mode -*-

import os
import re
import sys

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

def get_common_pos(pos):
    pos = pos.lower().strip()
    if pos.startswith("v"):
        return "verb"
    elif pos in noun_tags:
        return "noun"
    return pos

noun_tags = {
    "prop", # proper noun with no gender
    "n",    # noun with no gender (very few cases, mainly just cruft in wiktionary)
    "f",    # feminine (casa)
    "fp",   # feminine always plural (uncommon) (las esposas - handcuffs)
    "m",    # masculine (frijole)
    "mf",   # uses el/la to indicate gender of person (el/la dentista)
    "mp",   # masculine plural, nouns that are always plural (lentes)
}

class Meta():

    def __init__(self, line=None):
        self.forms = {}
        self.word = None
        self.common_pos = None

        if line:
            res = re.match(r"(.*?) {meta-(.*?)} :: (.*)", line)
            self.word = res.group(1)
            self.common_pos = res.group(2)
            for match in re.finditer(r"\s*(.*?)=(.*?)(; |$)", res.group(3)):
                self.add_form(match.group(1), match.group(2))

    def add_form(self, formtype, value):
        if formtype not in self.forms:
            self.forms[formtype] = [value]
        elif value not in self.forms[formtype]:
            self.forms[formtype].append(value)

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

class Word():
    def __init__(self, line):
        self.word = None
        self.pos = None
        self.lines = []
        self.lemmas = {}
        self.has_nonform_def = False
        self.meta = None

        self.add_line(line)

    @property
    def common_pos(self):
        # TODO: FIXME sloppy, calls global function
        return get_common_pos(self.pos)

    def add_line(self, line):
        word, pos, note, syn, definition = self.parse_line(line)

        if not self.word:
            self.word = word

        if pos.startswith("meta"):
            self.add_meta(line)
            return

        if not self.pos:
            self.pos = pos

        self.lines.append(line)
        form, lemma, remainder = self.get_form(definition)
        if form:
            # TODO: alert if pos=f and lemma is not in meta m
            self.add_lemma(lemma, form)
            if remainder.strip():
                self.has_nonform_def = True
        else:
            self.has_nonform_def = True

    def add_meta(self, line):
        if self.meta:
            raise ValueError("meta is already set", str(self.meta), line)
        self.meta = Meta(line)

        # Non-binary words are their own lemmas
        if "m" in self.meta.forms and "f" in self.meta.forms:
            return

        # If this defines masculine, assume the masculine is the lemma
        if "m" in self.meta.forms:
            for lemma in self.meta.forms["m"]:
                self.add_lemma(lemma, "f")

    @staticmethod
    def parse_line(line):

        pattern = r"""(?x)
             (?P<word>[^{:]+)             # The word (anything not an opening brace)

             ([ ]{                        # (optional) a space
               (?P<pos>[^}]*)             #    and then the the part of speech, enclosed in curly braces
             \})*                         #    (this may be specified more than once, the last one wins)

             ([ ]\[                       # (optional) a space
               (?P<note>[^\]]*)           #    and then the note, enclosed in square brackets
             \])?

             (?:[ ][|][ ]                    # (optional) a space and then a pipe | and a space
               (?P<syn>.*?)                #    and then a list of synonyms
             )?

             (                            # this whole bit can be optional
               [ ]*::[ ]                  #   :: optionally preceded by whitespace and followed by a mandatory space

               (?P<def>.*)                #   the definition
             )?
             \n?$                         # an optional newline at the end
        """
        res = re.match(pattern, line)
        if not res:
            raise ValueError("Cannot parse", line)

        word = res.group('word').strip()
        pos = res.group('pos') if res.group('pos') else ''
        note = res.group('note') if res.group('note') else ''
        syn = res.group('syn') if res.group('syn') else ''
        definition = res.group('def') if res.group('def') else ''

        return (word, pos, note, syn, definition)

    def add_lemma(self, lemma, form):
        if lemma not in self.lemmas:
            self.lemmas[lemma] = [form]
        else:
            self.lemmas[lemma].append(form)

    @classmethod
    def get_form(cls, definition):
        """
        Detect "form of" variations in the definition

        returns tuple (form, lemma, remaining_definition)
        """
        res = re.search(cls.form_pattern, definition)

        if res:
            form = cls.form_of[res.group(1)]
            lemma = res.group(2)
            remainder = re.sub(re.escape(res.group(0)), "", definition).strip()
            return (form, lemma, remainder)

        return (None,None,None)

    form_of = {
        "alternate form": "alt",
        "alternate spelling": "alt",
        "alternative form": "alt",
        "alternative form": "alt",
        "alternative spelling": "alt",
        "alternative typography": "alt",
        "archaic spelling": "old",
        "common misspelling": "spell",
        "dated form": "old",
        "dated spelling": "old",
        "euphemistic form": "spell",
        "euphemistic spelling": "spell",
        "eye dialect": "alt",
        "feminine": "f",
        "feminine equivalent": "f",
        "feminine singular": "f",
        "feminine plural": "fpl",
        "feminine noun": "f",
        "informal form": "spell",
        "informal spelling": "spell",
        "masculine": "m",
        "masculine singular": "m",
        "masculine plural": "mpl",
        "misspelling": "spell",
        "nonstandard form": "spell",
        "nonstandard spelling": "spell",
        "obsolete form": "old",
        "obsolete spelling": "old",
        "plural": "pl",
        "pronunciation spelling": "spell",
        "rare form": "old",
        "rare spelling": "old",
        "superseded form": "old",
        "superseded spelling": "old",
    }
    form_pattern = "(" + "|".join(form_of.keys()) + r") of ([^.,;:()]*)[.,;:()]?"


def process_data(data):
    all_words = load_all_words(data)
    all_meta = process_meta(all_words)
    seen_meta = set()

    for word in all_words:
        metakey = (word.word, word.common_pos)

        # If this is the first word and it's not a lemma and has no nonform def, don't print anything
        if metakey not in seen_meta and word.lemmas and not word.has_nonform_def:
            continue

        if metakey not in seen_meta:
            seen_meta.add(metakey)
            meta = all_meta.get(metakey)
            if meta:
                yield str(meta)

        yield from word.lines

def load_all_words(data):
    all_words = []
    prev_word = None
    prev_common_pos = None
    word_item = None
    for line in data:
        line = line.strip()
        word, pos, note, syn, definition = Word.parse_line(line)
        if pos.startswith("meta-"):
            # Remove the previous item from the list if it didn't contain anything
            if word_item and not word_item.lines:
                all_words.pop()
            prev_common_pos = pos[5:]
            prev_word = word
            word_item = Word(line)
            all_words.append(word_item)

        else:
            common_pos = get_common_pos(pos)
            if word != prev_word or common_pos != prev_common_pos:
                # Remove the previous item from the list if it didn't contain anything
                if word_item and not word_item.lines:
                    all_words.pop()
                prev_common_pos = get_common_pos(pos)
                prev_word = word
                word_item = Word(line)
                all_words.append(word_item)

            else:
                word_item.add_line(line)

    return all_words

def process_meta(words):

    all_meta = {}

    # Build the meta for each word, common_pos
    # For words with multiple meta declarations, consolidate into a single meta line,
    for word in words:
        if not word.meta:
            continue

        key = (word.word, word.common_pos)
        if key not in all_meta:
            all_meta[key] = word.meta
        else:
            meta = all_meta[key]

            # If the original meta has no masculine definitions (eg, it's a feminine lemma)
            # do *not* add masculine forms from following definitions
            # (eg, hamburguesa is feminine only in the sense "hamburger" but is followed
            # by another usage "feminine of hamburgués, woman from Hamburg")
            is_lemma = "m" in meta.forms
            for formtype, forms in word.meta.forms.items():
                if not is_lemma and formtype in ["m", "mpl"]:
                    continue
                for form in forms:
                    meta.add_form(formtype, form)

    # Build meta for non-lemmas with definitions and
    # add all forms of non-lemma words to their lemmas
    for word in words:
        if not word.lemmas:
            continue

        # If the word is not a lemma, add it and all of its forms to its lemma
        for lemma, formtypes in word.lemmas.items():
            key = (lemma, word.common_pos)
            meta = all_meta.get(key)
            # If this word references a lemma without a meta, we must create an empty meta for it first
            if meta is None:
                meta = Meta()
                meta.word = lemma
                meta.common_pos = word.common_pos
                all_meta[key] = meta

            for formtype in formtypes:
                meta.add_form(formtype, word.word)
                if not word.meta:
                    continue

                # If this is the feminine of a masculine, add all plurals as "fpl"
                if formtype == "f":
                    for form in word.meta.forms.get("pl",[]):
                        meta.add_form("fpl", form)
                    for form in word.meta.forms.get("fpl",[]):
                        meta.add_form("fpl", form)

                # Otherwise, just add all forms with the detected "form of" form
                # (for misspellings/alt forms, etc where both singular and plural should be flagged)
                elif word.meta:
                    meta.add_forms(formtype, word.meta.forms)

    return all_meta


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description="Post process wiktionary export")
    parser.add_argument("infile", help="Input file")
    args = parser.parse_args()

    with open(args.infile) as infile:
        for line in process_data(infile):
            print(line)
