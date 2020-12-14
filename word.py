import enwiktionary_templates as templates
import re
from .sense import Sense
from .wiki_to_text import wiki_to_text

class Word():

    def __init__(self, word, data):

        self.word = word
        self._forms = None # { formtype: [form1, ..] }
        self.form_of = {} # { lemma: [formtype1, formtype2 ..] }
        self._sense_data = None
        self._senses = None
        self.meta = None
        self.genders = None

        for i, item in enumerate(data):
            key, value = item
            if key == "gloss":
                self._sense_data = data[i:]
                # Everything after the first gloss will be lazy-loaded as .senses
                break
            elif key == "meta":
                self.meta = value
            elif key == "pos":
                if value == "prop":
                    value = "n"
                self._pos = value
            elif key == "g":
                if self._pos == "n":
                    self.genders = value

    @property
    def is_lemma(self):
        return not ("m" in self.forms and "f" in self.forms) and\
            self.senses and not self.form_of

    def add_form(self, formtype, form):
        if self._forms is None:
            self._forms = {}

        if "[[" in form or "</" in form:
            form = wiki_to_text(form, self.word)

        if formtype not in self._forms:
            self._forms[formtype] = [form]
        else:
            if form not in self._forms[formtype]:
                self._forms[formtype].append(form)

        # Feminine nouns are a "form of" their masculine counterpart
        if formtype == "m" and self.genders == "f":
            self.add_lemma(form, "f")
        if formtype == "mpl" and self.genders == "fp":
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
    def pos(self):
        return self._pos

    @classmethod
    def get_common_pos(cls, pos):
        pos = pos.lower().strip()
        if pos.startswith("v"):
            return "v"
        elif pos in cls.noun_tags:
            return "n"
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
        if not self._forms and self.meta:
            self.get_forms_from_meta()
            self.meta = None
            if not self._forms:
                return {}

            if self.genders == "f":
                for form in self._forms.get("m", []):
                    self.add_lemma(form, "f")
            elif self.genders == "fp":
                for form in self._forms.get("mpl", []):
                    self.add_lemma(form, "fpl")

        if not self._forms:
            return {}

        return self._forms

    def get_forms_from_meta(self):
        for template in templates.iter_templates(self.meta):
            if template.name == "head":
                data = self.get_head_forms(template)
            else:
                data = templates.expand_template(template, self.word)
            self.add_forms(self.parse_list(data))


    @staticmethod
    def get_head_forms(template):
        if template is None:
            return {}

        params = templates.get_template_params(template)

        res = {}
        offset=3
        while str(offset+1) in params:
            formtype = params[str(offset)]
            formtype = re.sub("[^a-zA-Z0-9]", "_", formtype)
            form = params[str(offset+1)]
            offset += 2

            if not form.strip():
                continue

            if formtype not in res:
                res[formtype] = [form]
            else:
                res[formtype].append(form)

        return "; ".join([f"{k}={v}" for k,vs in sorted(res.items()) for v in vs])
