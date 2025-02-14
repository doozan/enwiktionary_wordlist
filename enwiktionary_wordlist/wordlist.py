import itertools
import os
import pickle
import re
import sys

from .word import Word

from enwiktionary_wordlist.utils import wiki_to_text

verb_types = {
        "t": "transitive",
        "r": "reflexive",
        "i": "intransitive",
        "p": "pronominal",
        "x": "ambitransitive",
}

class Wordlist():
    def __init__(self, wordlist_data=None, cache_words=True, template_cachedb=None, redirects={}):
        # cache here refers to the database used to cache mediawiki queries used to expand templates
        self.template_cachedb = template_cachedb
        self.redirects = redirects

        # cache here refers to caching word objects in memory to speed up repeat access
        self.cache_words = cache_words
        self._cached = {}
        if not wordlist_data:
            self.all_entries = {}
            return

        iter_list = iter(wordlist_data)
        first_line = next(iter_list)
        mbformat = not first_line.startswith("_____")
        iter_data = itertools.chain([first_line], iter_list)

        if mbformat:
            self.all_entries = {title: entry for title, entry in self._iter_entries_mbformat(iter_data)}
        else:
            self.all_entries = {title: entry for title, entry in self._iter_entries(iter_data)}

    @classmethod
    def from_file(cls, filename, cache_words=True, template_cachedb=None):
        # check for cached version
        cached = filename + ".~db"
        if os.path.exists(cached) and os.path.getctime(cached) > os.path.getctime(filename):
            with open(cached, "rb") as infile:
                res = pickle.load(infile)
            return res

        with open(filename) as infile:
            res = cls(infile, cache_words, template_cachedb=template_cachedb)
            with open(cached, "wb") as outfile:
                pickle.dump(res, outfile)
            return res

    @staticmethod
    def _iter_entries(data):

        entry = None
        title = None
        for line in data:
            line = line.strip()
            #line = line.rstrip()
            if line.startswith("#") or line == "":
                continue
            if line == "_____":
                if entry:
                    yield(title, entry)
                entry = []
                title = None
            else:
                if entry is None:
                    raise ValueError("Invalid file format", line)
                if title is None:
                    title = line
                else:
                    entry.append(line)
        if entry:
            yield(title, entry)

    @classmethod
    def _iter_entries_mbformat(cls, data):

        entry = []
        prev_word = None
        first = True
        for line in data:
            word, pos, note, syn, definition = cls.parse_line(line)
            if word != prev_word:
                if prev_word:
                    yield(prev_word, entry)

                if not pos.endswith("-meta"):
                    #raise ValueError("Expected meta line", prev_word, line)
                    print("Expected meta line", prev_word, line, file=sys.stderr)
                    continue
                entry = []

            if pos.endswith("-meta"):
                pos = pos[:-len("-meta")]
                entry += [f"pos: {pos}", f"meta: {definition}"]
                first = True

            elif pos.endswith("-forms"):
                entry.append(f"forms: {definition}")
            else:
                if first:
                    if pos in ["m","f","mf","m-f","mp","fp","mfp"]:
                        entry.append(f"g: {pos}")
                    first = False
                if definition:
                    entry.append(f"gloss: {definition}")
                    if pos.startswith("v"):
                        note = cls.add_verb_forms_to_note(note, pos)
                    if note:
                        entry.append(f"q: {note}")
                    if syn:
                        entry.append(f"syn: {syn}")
            prev_word = word

        if entry:
            yield(prev_word, entry)


    @staticmethod
    def add_verb_forms_to_note(note, pos):
        """ Adds verb types to the note usage """
        if not pos.startswith("v") or pos == "v":
            return note

        notes = []
        types = pos[1:].replace("it", "x")
        for verbtype in types:
            notes.append(verb_types[verbtype])
        if note:
            notes.append(note)
        return "; ".join(notes)

    def get_entry_words(self, title, lines, pos=None):

        common = []
        word_items = []
        word_pos = None

        first = False
        for line in lines:
            key, _junk, value = line.partition(": ")

            if first:
                if key != "pos":
                    common.append((key, value))
                else:
                    first = False

            elif key == "pos":
                if word_items:
                    word_obj = Word(self, title, word_items)
                    if (not pos or word_obj.pos == pos):
                        yield word_obj

                word_items = common + [ (key,value) ]

                word_pos = value

            else:
                word_items.append((key,value))

        if word_items:
            word_obj = Word(self, title, word_items)
            if (not pos or word_obj.pos == pos):
                yield word_obj

    def iter_all_words(self):
        for word, entry in self.all_entries.items():
            yield from self.get_iwords(word)

    def has_entry(self, word):
        return word in self.all_entries

    def has_word(self, word, pos=None):
        return any(self.get_iwords(word, pos))

    def get_words(self, title, pos=None):
        return list(self.get_iwords(title, pos))

    def get_iwords(self, title, pos=None):
        if title not in self.all_entries:
            return []

        if self.cache_words:
            if title not in self._cached:
                self._cached[title] = tuple(self._get_iwords(title))

                # Delete the source lines from all_entries
                if title in self.all_entries:
                    self.all_entries[title] = None
                    # don't delete the entry, it breaks iteration in allforms

            for word in self._cached[title]:
                if not pos or pos == word.pos:
                    yield word

        else:
            yield from self._get_iwords(title, pos)

    def _get_iwords(self, word, pos=None):
        return self.get_entry_words(word, self.all_entries.get(word,[]), pos)

    def get_formtypes(self, lemma, pos, form):
        """ Returns the possible formtypes of a given form in lemma,pos """
        for word in self.get_iwords(lemma, pos):
            yield from word.get_formtypes(form)

    def expand_templates(self, text, title):
        return wiki_to_text(text, title, template_cachedb=self.template_cachedb, redirects=self.redirects).strip()

    @staticmethod
    def parse_line(line):
        """ Parse dictionary lines:
        word {pos-forms} :: formtype=form; formtype2=form2
        word {pos} | syn1; syn2 :: [qualifiers] gloss
        absolver {verb-forms} :: pattern=-olver; stem=abs
        """

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
