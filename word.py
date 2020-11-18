import re
from .sense import Sense

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
        "m/f",  # masculine/feminine have same meaning
        "m-f",  # masculine/feminine have different meanings
    }
