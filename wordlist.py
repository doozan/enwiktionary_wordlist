import re

class Sense():
    def __init__(self, pos, qualifier, gloss, syndata):
        self.pos = pos
        self.qualifier = qualifier
        self.gloss = gloss
        self._syndata = syndata
        self._synonyms = None

        self.formtype, self.lemma, self.nonform = self.parse_form_of(gloss)
#        if self.formtype and not self.nonform:
#            self.gloss = ""

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
        "neuter singular": "alt",
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
    form_pattern = "(" + "|".join(form_of_prefix.keys()) + r") of ([^.,;:()]*)[.,;:()]?"

class Word():
    def __init__(self, word, pos=None, common_pos=None):
        self.word = word
        self.pos = pos
        self._common_pos = common_pos
        self.senses = []
        self._forms = {}   # { formtype: [form1, ..] }
        self.form_of = {} # { lemma: [formtype1, formtype2 ..] }
        self._meta = []

    @property
    def forms(self):
        if self._meta:
            self.process_meta()
        return self._forms

    def add_sense(self, pos, qualifier, gloss, syndata):
        sense = Sense(pos, qualifier, gloss, syndata)
        self.senses.append(sense)
        if sense.lemma:
            self.add_lemma(sense.lemma, sense.formtype)

    def add_form(self, formtype, form):
        if formtype not in self._forms:
            self._forms[formtype] = [form]
        else:
            if form not in self._forms[formtype]:
                self._forms[formtype].append(form)

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
        self._meta.append(data)

    def process_meta(self):
        for line in self._meta:
            self.add_forms(self.parse_list(line))
        self._meta = []

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

class Verb(Word):
    def __init__(self, word):
        self._paradigms = []
        super().__init__(word, pos=None, common_pos="verb")

    @property
    def paradigms(self):
        if self._meta:
            self.process_meta()
        return self._paradigms

    def process_meta(self):
        while self._meta:
            line = self._meta.pop(0)
            items = self.parse_list(line)
            if "pattern" in items or "stem" in items:
                pattern = items.get("pattern", [None])[0]
                stems = items.get("stem", None)
                self.add_paradigm(pattern, stems)
            else:
                self.add_forms(items)

    def add_paradigm(self, pattern, stems):
        self._paradigms.append((pattern, stems))


class Wordlist():
    def __init__(self, data):
        self.all_words = []

        prev_word = None
        prev_pos = None
        prev_common_pos = None
        word_item = None

        for line in data:
            word, pos, note, syn, definition = self.parse_line(line)
            common_pos = None

            if pos.startswith("meta-"):
                common_pos = pos[len("meta-"):]
                # A meta line starts a new word unless it was preceeded by an identical meta line
                if prev_word != word or prev_pos != pos:
                    word_item = self.add_word(word,None,common_pos)
                word_item.add_meta(definition)

            else:
                common_pos = Word.get_common_pos(pos)
                if word != prev_word or common_pos != prev_common_pos: # or (pos != prev_pos and "meta-" not in prev_pos):
                    word_item = self.add_word(word,pos,common_pos)

                if not word_item.pos:
                    word_item.pos = pos
                word_item.add_sense(pos, note, definition, syn)

            prev_word = word
            prev_pos = pos
            prev_common_pos = common_pos

    def add_word(self, word, pos=None, common_pos=None):
        if common_pos and common_pos == "verb":
            word_item = Verb(word)
        else:
            word_item = Word(word, pos, common_pos)

        self.all_words.append(word_item)
        return word_item

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


