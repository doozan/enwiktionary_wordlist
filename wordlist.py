import re
import sys

class Sense():
    def __init__(self, pos, qualifier, gloss, syndata):
        self.pos = pos
        self.qualifier = qualifier
        self.gloss = gloss
        self._syndata = syndata
        self._synonyms = None

        if " of " in gloss:
            self.formtype, self.lemma, self.nonform = self.parse_form_of(gloss)
            if self.lemma:
                self.lemma = self.lemma.strip()
        else:
            self.formtype = None
            self.lemma = None
            self.nonform = None

    @property
    def synonyms(self):
        if not self._synonyms and self._syndata:
            self._synonyms = self.parse_syndata(self._syndata)
        return self._synonyms

    @classmethod
    def parse_syndata(cls, syndata):
        if syndata == "":
            return []
        return syndata.split("; ")

    @classmethod
    def parse_form_of(cls, definition):
        """
        Detect "form of" variations in the definition

        returns tuple (formtype, lemma, remaining_definition)
        """
        res = re.search(cls.form_pattern, definition)

        if res:
            formtype = cls.form_of_prefix[res.group(1)]
            lemma = res.group(2)
            nonform = re.sub(re.escape(res.group(0)), "", definition).strip()
            return (formtype, lemma, nonform)

        res = re.search(cls.alt_form_pattern, definition)
        if res:
            print(f"Found non-template form of: {definition}", file=sys.stderr)
            formtype = cls.form_of_prefix[res.group(1)]
            lemma = res.group(2)
            nonform = re.sub(re.escape(res.group(0)), "", definition).strip()
            return (formtype, lemma, nonform)

        return (None,None,None)

    form_of_prefix = {
        "alternate form": "alt",
        "alternate spelling": "alt",
        "alternative form": "alt",
        "alternative spelling": "alt",
        "alternative typography": "alt",
        "archaic spelling": "old",
        "common misspelling": "spell",
        "dated form": "old",
        "dated spelling": "old",
        "euphemistic form": "alt",
        "euphemistic spelling": "alt",
        "eye dialect": "alt",
        "feminine": "f",
        "feminine equivalent": "f",
        "feminine singular": "f",
        "feminine plural": "fpl",
        "feminine noun": "f",
        "informal form": "alt",
        "informal spelling": "alt",
        "masculine": "m",
        "masculine singular": "m",
        "masculine plural": "mpl",
        "misspelling": "spell",
        "neuter singular": "alt",
        "nonstandard form": "alt",
        "nonstandard spelling": "alt",
        "obsolete form": "old",
        "obsolete spelling": "old",
        "plural": "pl",
        "pronunciation spelling": "alt",
        "rare form": "rare",
        "rare spelling": "rare",
        "superseded form": "old",
        "superseded spelling": "old",
    }
    form_pattern = r"(?:^|A |An |\(|[,;:\)] )(" + "|".join(form_of_prefix.keys()) + r') of "([^"]*)"'
    alt_form_pattern = r"(?:^|A |An |\(|[,;:\)] )(" + "|".join(form_of_prefix.keys()) + r") of ([^,;:()]*)[,;:()]?"

class Word():
    def __init__(self, word, pos=None, common_pos=None):
        self.word = word
        self.pos = pos
        self._common_pos = common_pos
        self.senses = []
        self.forms = {}   # { formtype: [form1, ..] }
        self.form_of = {} # { lemma: [formtype1, formtype2 ..] }

    @property
    def is_lemma(self):
        return self.senses and not self.form_of

    def add_sense(self, pos, qualifier, gloss, syndata):
        sense = Sense(pos, qualifier, gloss, syndata)
        self.senses.append(sense)
        if sense.lemma:
            self.add_lemma(sense.lemma, sense.formtype)

    def add_form(self, formtype, form):
        if formtype not in self.forms:
            self.forms[formtype] = [form]
        else:
            if form not in self.forms[formtype]:
                self.forms[formtype].append(form)

        # Feminine nouns are a "form of" their masculine counterpart
        if formtype == "m" and self.pos == "f":
            self.add_lemma(form, "f")
        if formtype == "mpl" and self.pos == "fp":
            self.add_lemma(form, "fpl")

    def add_forms(self, data):
        """ Add forms from a dictionary object
        { formtype: [ form1, form2, ..] }
        """
        for formtype,forms in data.items():
            for form in forms:
                self.add_form(formtype, form)

    def add_lemma(self, lemma, formtype):
        if lemma not in self.form_of:
            self.form_of[lemma] = [formtype]
        else:
            self.form_of[lemma].append(formtype)

    def add_meta(self, data):
        self.add_forms(self.parse_list(data))

    @staticmethod
    def parse_list(line):
        items = {}
        for match in re.finditer(r"\s*(.*?)=(.*?)(; |$)", line):
            k = match.group(1)
            v = match.group(2)
            if k not in items:
                items[k] = [v]
            else:
                items[k].append(v)

        return items

    @property
    def common_pos(self):
        if not self._common_pos and self.pos:
            self._common_pos = self.get_common_pos(self.pos)
        return self._common_pos

    @classmethod
    def get_common_pos(cls, pos):
        pos = pos.lower().strip()
        if pos.startswith("v"):
            return "verb"
        elif pos in cls.noun_tags:
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

class Wordlist():
    def __init__(self, data):
        self.all_words = {}     # { word: {  pos: [ Word1, .. ] }}
        self._all_forms = None  # { form: {  pos: { formtype:[lemma1, ..] }}}
        self._all_lemmas = None # { lemma: { pos: { formtype:[form1, ..] }}}

        prev_word = None
        prev_pos = None
        prev_common_pos = None
        word_item = None

        for line in data:
            word, pos, note, syn, data = self.parse_line(line)
            common_pos = None

            if pos.startswith("meta-"):
                common_pos = pos[len("meta-"):]
                word_item = self.add_word(word,None,common_pos)
                word_item.add_meta(data)

            else:
                common_pos = Word.get_common_pos(pos)
                if word != prev_word or common_pos != prev_common_pos:
                    word_item = self.add_word(word,pos,common_pos)

                if not word_item.pos:
                    word_item.pos = pos
                word_item.add_sense(pos, note, data, syn)

            prev_word = word
            prev_pos = pos
            prev_common_pos = common_pos

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

        return any(word.is_lemma for word in self.get_words(lemma, common_pos))

    def get_words(self, word, common_pos):
        return self.all_words.get(word,{}).get(common_pos,[])

    def get_lemmas(self, word, max_depth=3):
        """
        word is a Word object
        Returns the lemmas for a given word as a list of (word, formtype) tuples
        """

        if word.is_lemma:
            return {word.word: [word.pos]}

        lemmas = {}
        for lemma, formtypes in word.form_of.items():
            if self.has_lemma(lemma, word.common_pos):
                lemmas[lemma] = formtypes
            elif max_depth>0:
                subwords = self.get_words(lemma, word.common_pos)
                for subword in subwords:
                    lemmas.update(self.get_lemmas(subword, max_depth-1))
            else:
                print(f"Lemma recursion exceeded: {word.word} {word.common_pos} -> {lemma}", file=sys.stderr)
                return {}

        return lemmas

    @staticmethod
    def parse_line(line):
        """ Parse dictionary lines:
        word {meta-pos} :: formtype=form; formtype2=form2
        word {pos} | syn1; syn2 :: [qualifiers] gloss
        absolver {meta-verb} :: pattern=-olver; stem=abs
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
    def add_form(cls, dest, lemma, pos, formtype, form, reverse=False):
        if form == "-":
            print(f"Bad form '-' referenced by {lemma} {pos}", file=sys.stderr)
            return

        if reverse:
            lemma, form = form, lemma
        key = (lemma, pos)

        if lemma not in dest:
            dest[lemma] = {}
        if pos not in dest[lemma]:
            dest[lemma][pos] = {}
        if formtype not in dest[lemma][pos]:
            dest[lemma][pos][formtype] = [form]
        else:
            if form not in dest[lemma][pos][formtype]:
                dest[lemma][pos][formtype].append(form)

    @classmethod
    def add_forms(cls, dest, lemma, pos, forms, forced_formtype=None, reverse=False):
        for formtype, forms in forms.items():
            if forced_formtype:
                formtype = forced_formtype
            for form in forms:
                cls.add_form(dest, lemma, pos, formtype, form, reverse=reverse)

    @classmethod
    def add_feminine_forms(cls, dest, lemma, pos, forms, reverse=False):
        for formtype, forms in forms.items():
            for form in forms:
                if formtype in ["m", "mpl"]:
                    continue
                if formtype in ["pl", "fpl"]:
                    cls.add_form(dest, lemma, pos, "fpl", form, reverse=reverse)
                else:
                    cls.add_form(dest, lemma, pos, formtype, form, reverse=reverse)

    def get_all_lemmas(self, reverse=False):
        """
        Return a dictionary of all known lemmas and all of their forms
        lemma: {pos: { formtype:[form1, ..], .. }}
        if reverse is True, builds a dictionary all known forms and their lemmas
        form: {pos: { formtype:[lemma1, ..], .. }}
        """
        all_items = {}

        for pos_list in self.all_words.values():
            for words in pos_list.values():
                for word in words:

                    if not len(word.senses):
                        continue

                    # Word is a lemma, add it and all its forms
                    if word.is_lemma:
                        self.add_form(all_items, word.word, word.common_pos, word.pos, word.word, reverse=reverse)
                        self.add_forms(all_items, word.word, word.common_pos, word.forms, reverse=reverse)
                        continue

                    # Word is form of another lemma, add its forms to the lemma
                    for lemma, formtypes in self.get_lemmas(word).items():
                        for formtype in formtypes:
                            self.add_form(all_items, lemma, word.common_pos, formtype, word.word, reverse=reverse)
                            if formtype == "f":
                                # If this is the feminine of a masculine, add all plurals as "fpl"
                                self.add_feminine_forms(all_items, lemma, word.common_pos, word.forms, reverse=reverse)
                            else:
                                self.add_forms(all_items, lemma, word.common_pos, word.forms, formtype, reverse=reverse)

        return all_items

    @property
    def all_lemmas(self):
        """ Returns a dictionary of all lemmas and their forms
        lemma: {pos: { formtype:[form1, ..], .. }}
        """
        if not self._all_lemmas:
            self._all_lemmas = self.get_all_lemmas()
        return self._all_lemmas

    @property
    def all_forms(self):
        """ Returns a dictionary of all forms and their lemmas
        form: {pos: { formtype:[lemma1, ..], .. }}
        """
        if not self._all_forms:
            self._all_forms = self.get_all_lemmas(reverse=True)
        return self._all_forms
