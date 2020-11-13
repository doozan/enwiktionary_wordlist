import re
import sys

class Sense():
    def __init__(self, pos, qualifier, gloss, syndata):
        self.pos = pos
        self.qualifier = qualifier
        self.gloss = gloss
        self._syndata = syndata
        self._synonyms = []

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
        "female equivalent": "f",
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
        self._pos = pos
        self._common_pos = common_pos
        self.senses = []
        self.forms = {}   # { formtype: [form1, ..] }
        self.form_of = {} # { lemma: [formtype1, formtype2 ..] }

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value
        if value == "f":
            for form in self.forms.get("m", []):
                self.add_lemma(form, "f")
        elif value == "fp":
            for form in self.forms.get("mpl", []):
                self.add_lemma(form, "fpl")

    @property
    def is_lemma(self):
        return self.senses and not self.form_of \
                and not ("m" in self.forms and "f" in self.forms)

    def add_sense(self, pos, qualifier, gloss, syndata):
        sense = Sense(pos, qualifier, gloss, syndata)
        # Add "form of" if it's in the first sense
        if sense.lemma and not self.senses:
            self.add_lemma(sense.lemma, sense.formtype)
        self.senses.append(sense)

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
            if formtype not in self.form_of[lemma]:
                self.form_of[lemma].append(formtype)

    def parse_forms(self, data):
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

        prev_word = None
        prev_pos = None
        prev_common_pos = None
        word_item = None

        for line in data:
            word, pos, note, syn, data = self.parse_line(line)
            common_pos = None

            if pos.endswith("-forms"):
                common_pos = pos[:-len("-forms")]
                word_item = self.add_word(word,None,common_pos)
                word_item.parse_forms(data)

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
