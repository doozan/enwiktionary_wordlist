import re
from .sense import Sense

class Word():

    def __init__(self, word, data):

        self.word = word
        #self.forms = {}   # { formtype: [form1, ..] }
        self.form_of = {} # { lemma: [formtype1, formtype2 ..] }
        self._sense_data = None
        self._senses = None
        self._form_data = None
        self._forms = None
        self._form = None
        self.meta = None

        form = None
        common_pos = None

        for i, item in enumerate(data):
            key, value = item
            if key == "gloss":
                self._sense_data = data[i:]
                # Everything after the first gloss will be lazy-loaded as .senses
                break
            if key == "meta":
                self.meta = value
            elif key == "forms":
                self._form_data = value
                self.forms
            elif key == "pos":
                if value == "prop":
                    common_pos = "noun"
#                    form = "prop"
                elif value == "v":
                    common_pos = "verb"
                elif value == "n":
                    common_pos = "noun"
                else:
                    common_pos = value
            elif key == "form":
                if common_pos == "noun":
                    if value == "?":
                       value = None
                    elif value in [ "m-p", "m;p" ]:
                        value = "mp"
                    elif value == "f-p":
                        value = "fp"
                    elif value in ["m;f", "f;m"]:
                        value = "mf"
                    elif value == "mfbysense":
                        value = "mf"
                    elif value == "p":
                        value = "p"
                    form = value

        self._common_pos = common_pos
        self.form = form

        # force loading
        self.senses


    @property
    def form(self):
        return self._form

    @form.setter
    def form(self, value):
        self._form = value
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

    def add_form(self, formtype, form):
        if self._forms is None:
            self._forms = {}
        if formtype not in self._forms:
            self._forms[formtype] = [form]
        else:
            if form not in self._forms[formtype]:
                self._forms[formtype].append(form)

        # Feminine nouns are a "form of" their masculine counterpart
        if formtype == "m" and self.form == "f":
            self.add_lemma(form, "f")
        if formtype == "mpl" and self.form == "fp":
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
        if not self._common_pos and self.form:
            self._common_pos = self.get_common_pos(self.form)
        if self._common_pos == "n":
            self._common_pos = "noun"
        elif self._common_pos == "v":
            self._common_pos = "verb"
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


    @property
    def senses(self):
        if self._sense_data:
            self.parse_sense_data()
        if self._senses:
            return self._senses
        return []

    def parse_sense_data(self):
        sense = []
        for kv in self._sense_data:
            key, value = kv
            if key == "gloss":
                if sense:
                    self.add_sense(sense)
                sense = [(key, value)]
            else:
                sense.append(kv)
        if sense:
            self.add_sense(sense)

        self._sense_data = None

    def add_sense(self, data): # pos, qualifier, gloss, syndata):
        sense = Sense(data) # pos, qualifier, gloss, syndata)
        # Add "form of" if it's in the first sense
        if self._senses is None:
            self._senses = []
            if sense.lemma:
                self.add_lemma(sense.lemma, sense.formtype)
        self._senses.append(sense)

#    def add_sense(self, pos, qualifier, gloss, syndata):
#        sense = Sense(pos, qualifier, gloss, syndata)
#        # Add "form of" if it's in the first sense
#        if sense.lemma and not self.senses:
#            self.add_lemma(sense.lemma, sense.formtype)
#        self.senses.append(sense)


    @property
    def forms(self):
        if self._form_data:
            self.parse_forms(self._form_data)
            self._form_data = None

        if not self._forms:
            return {}

        return self._forms
