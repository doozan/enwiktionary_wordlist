import itertools
import re
import sys

from .word import Word

verb_types = {
        "t": "transitive",
        "r": "reflexive",
        "i": "intransitive",
        "p": "pronominal",
        "x": "ambitransitive",
}

class Wordlist():
    def __init__(self, wordlist_data, cache_words=True):
        self.cache_words = cache_words
        self._cached = {}

        iter_list = iter(wordlist_data)
        first_line = next(iter_list)
        mbformat = not first_line.startswith("_____")
        iter_data = itertools.chain([first_line], iter_list)

        if mbformat:
            self.all_entries = {title: entry for title, entry in self._iter_entries_mbformat(iter_data)}
        else:
            self.all_entries = {title: entry for title, entry in self._iter_entries(iter_data)}

    @classmethod
    def from_file(cls, filename):
        with open(filename) as infile:
            return cls(infile)

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
                    word_obj = Word(title, word_items)
                    if (not pos or word_obj.pos == pos):
                        yield word_obj

                word_items = common + [ (key,value) ]

                word_pos = value

            else:
                word_items.append((key,value))

        if word_items:
            word_obj = Word(title, word_items)
            if (not pos or word_obj.pos == pos):
                yield word_obj

    def iter_all_words(self):
#        count = 0
        for word, entry in self.all_entries.items():
#            count += 1
#            if count > 10000:
#                break
            yield from self.get_words(word)

    def has_lemma(self, lemma, pos=None):
        """
        lemma is a string
        pos is a string
        Check if a given word, pos is a lemma
        """

        # only consider it a lemma if the first usage is as a lemma
        for word in self.get_words(lemma, pos):
            return word.is_lemma
        return False

    def has_entry(self, word):
        return word in self.all_entries

    def has_word(self, word, pos=None):
        return any(self.get_words(word, pos))

    def get_words(self, title, pos=None):
        if title not in self.all_entries:
            return

        if self.cache_words:
            if title not in self._cached:
                self._cached[title] = list(self._get_words(title))

                # Delete the source lines from all_entries
                if title in self.all_entries:
                    self.all_entries[title] = None

            for word in self._cached[title]:
                if not pos or pos == word.pos:
                    yield word

        else:
            yield from self._get_words(title, pos)

    def _get_words(self, word, pos=None):
        yield from self.get_entry_words(word, self.all_entries.get(word,[]), pos)

    def get_lemmas(self, word, max_depth=3):
        """
        word is a Word object
        Returns a dict: { lemma1: [formtypes], .. }
        """

        if word.is_lemma:
            return {word.word: [word.genders]}

        lemmas = {}
        for lemma, formtypes in word.form_of.items():
            if self.has_lemma(lemma, word.pos):
                lemmas[lemma] = formtypes
            elif max_depth>0:
                for redirect in self.get_words(lemma, word.pos):
                    lemmas.update(self.get_lemmas(redirect, max_depth-1))
                    break # Only look at the first word
            else:
                print(f"Lemma recursion exceeded: {word.word} {word.pos} -> {lemma}", file=sys.stderr)
                return {}

        return lemmas


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
