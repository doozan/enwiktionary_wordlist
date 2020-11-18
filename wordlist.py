import re
import sys

from .word import Word

class Wordlist():
    def __init__(self, data):
        self.all_words = {}     # { word: {  pos: [ Word1, .. ] }}
        self._all_forms = None  # { form: {  pos: { formtype:[lemma1, ..] }}}

        word_item = None

        for line in data:
            word, pos, note, syn, data = self.parse_line(line)

            if pos.endswith("-meta"):
                common_pos = pos[:-len("-meta")]
                word_item = self.add_word(word,None,common_pos)

            elif pos.endswith("-forms"):
                word_item.parse_forms(data)

            else:
                if not word_item.pos:
                    word_item.pos = pos

                word_item.add_sense(pos, note, data, syn)

    @classmethod
    def from_file(cls, filename):
        with open(filename) as infile:
            return cls(infile)

    def add_word(self, word, pos=None, common_pos=None):
        word_item = Word(word, pos, common_pos)

        if word not in self.all_words:
            self.all_words[word] = {common_pos: [word_item]}
        elif common_pos not in self.all_words[word]:
            self.all_words[word][common_pos] = [word_item]
        else:
            self.all_words[word][common_pos].append(word_item)

        return word_item

    def has_lemma(self, lemma, common_pos):
        """
        lemma is a string
        common_pos is a string
        Check if a given word, pos is a lemma
        """

        # only consider it a lemma if the first usage is as a lemma
        words = self.get_words(lemma, common_pos)
        return len(words) and words[0].is_lemma

    def has_word(self, word, common_pos):
        return bool(self.all_words.get(word,{}).get(common_pos,[]))

    def get_words(self, word, common_pos):
        return self.all_words.get(word,{}).get(common_pos,[])

    def get_lemmas(self, word, max_depth=3):
        """
        word is a Word object
        Returns a dict: { lemma1: [formtypes], .. }
        """

        if word.is_lemma:
            return {word.word: [word.pos]}

        lemmas = {}
        for lemma, formtypes in word.form_of.items():
            if self.has_lemma(lemma, word.common_pos):
                lemmas[lemma] = formtypes
            elif max_depth>0:
                for redirect in self.get_words(lemma, word.common_pos):
                    lemmas.update(self.get_lemmas(redirect, max_depth-1))
                    break # Only look at the first word
            else:
                print(f"Lemma recursion exceeded: {word.word} {word.common_pos} -> {lemma}", file=sys.stderr)
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


    @classmethod
    def add_form(cls, dest, form, pos, formtype, lemma):
        if form == "-":
#            print(f"Bad form '-' referenced by {lemma} {formtype} {pos}", file=sys.stderr)
            return


        target = f"{pos}:{lemma}:{formtype}"
        if form not in dest:
            dest[form] = [target]
        else:
            if target not in dest[form]:
                dest[form].append(target)


#        if form not in dest:
#            dest[form] = {(pos,formtype,lemma)}
#        else:
#            dest[form].add((pos,formtype,lemma))

#        if form not in dest:
#            dest[form] = {pos: {formtype: [lemma]}}
#        elif pos not in dest[form]:
#            dest[form][pos] = {formtype: [lemma]}
#        elif formtype not in dest[form][pos]:
#            dest[form][pos][formtype] = [lemma]
#        else:
#            if lemma not in dest[form][pos][formtype]:
#                dest[form][pos][formtype].append(lemma)

    def get_all_forms(self):
        """
        Return a dictionary of all known lemmas and all of their forms
        lemma: {pos: { formtype:[form1, ..], .. }}
        if reverse is True, builds a dictionary all known forms and their lemmas
        form: {pos: { formtype:[lemma1, ..], .. }}
        """
        all_items = {}

        prev_word = None
        prev_common_pos = None
        for pos_list in self.all_words.values():
            for words in pos_list.values():
                for word in words:
                    if not len(word.senses):
                        continue

                    for lemma, formtypes in self.get_lemmas(word).items():
                        for lemma_formtype in formtypes:
                            self.add_form(all_items, word.word, word.common_pos, lemma_formtype, lemma)

                            for formtype, forms in word.forms.items():
                                for form in forms:
                                    if lemma_formtype == "f" and not word.is_lemma:
                                        if formtype in ["m", "mpl"]:
                                            continue
                                        elif formtype in ["pl", "fpl"]:
                                            formtype = "fpl"

                                    self.add_form(all_items, form, word.common_pos, formtype, lemma)

        return all_items

    @property
    def all_forms(self):
        """ Returns a dictionary of all forms and their lemmas
        form: {pos: { formtype:[lemma1, ..], .. }}
        """
        if not self._all_forms:
            self._all_forms = self.get_all_forms()
        return self._all_forms
