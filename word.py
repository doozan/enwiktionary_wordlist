from collections import defaultdict
import enwiktionary_templates as templates
import re
from .sense import Sense
from .utils import wiki_to_text

shorten_formtype = {
    "feminine": "f",
    "feminine_singular": "f",
    "feminine_counterpart": "f",
    "masculine": "m",
    "masculine_singular": "m",
    "masculine_counterpart": "m",
    "feminine_plural": "fpl",
    "of_plural": "pl",
    "plural": "pl",
    "masculine_plural": "mpl",
}


class Word():

    def __init__(self, word, data):

        self.word = word
        self._pos = None
        # accessed as .forms
        self._forms = defaultdict(list) # { formtype: [form1, ..] }
        # accessed as .form_of
        self._form_of = defaultdict(list) # { lemma: [formtype1, formtype2 ..] }
        self._sense_data = None
        self._senses = None
        self.meta = None
        self._meta_parsed = False
        self.genders = None
        self.qualifier = None
        self.etymology = None
        self.use_notes = None

        for i, item in enumerate(data):
            key, value = item
            if key == "gloss":
                self._sense_data = data[i:]
                # Everything after the first gloss will be lazy-loaded as .senses
                break
            elif key == "meta":
                self.meta = value
            elif key == "usage":
                self.use_notes = value
            elif key == "etymology":
                self.etymology = value
            elif key == "pos":
                self._pos = value
            elif key == "g":
#                if self._pos in ["n", "prop"]:
                self.genders = value
            # Term labels
            elif key == "q":
                self.qualifier = value

    def add_form(self, formtype, form):

        if formtype == "infinitive_linked":
            return

        if "[[" in form or "</" in form:
            form = wiki_to_text(form, self.word)

        # strip "no" and direct objects that preceed the verb conjugation
        # "no te metes" -> "metes"
        if self.pos == "v" and " " in form:
            form = re.sub(f"^(?:no )?(?:(?:me|te|se|nos|os) )?(.*)", r'\1', form)

        if form not in self._forms[formtype]:
            self._forms[formtype].append(form)

        # Feminine nouns are a "form of" their masculine counterpart
#        if formtype == "m" and self.genders == "f":
#            self.add_lemma(form, "f")
        if formtype == "mpl" and self.genders == "fp":
            self.add_lemma(form, "fpl")

    def get_formtypes(self, word):
       for formtype, forms in self.forms.items():
           if word in forms:
               yield formtype

    def add_lemma(self, lemma, formtype):
        if formtype not in self.form_of[lemma]:
            self.form_of[lemma].append(formtype)

    @staticmethod
    def parse_list(line):
        items = {}
        for match in re.finditer(r"\s*(.*?)=(.*?)(; |$)", line):
            k = match.group(1)
            v = match.group(2)
            yield k,v

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
        self._parse_sense_data()
        if self._senses:
            return self._senses
        return []

    def _parse_sense_data(self):
        if not self._sense_data:
            return

        # Unset sense_data quickly so it doesn't get called recursively if
        # something reads .forms or .form_of
        data = self._sense_data
        self._sense_data = None

        sense = []
        for kv in data:
            key, value = kv
            if key == "gloss":
                if sense:
                    self.add_sense(sense)
                sense = [(key, value)]
            else:
                sense.append(kv)
        if sense:
            self.add_sense(sense)


    def add_sense(self, data): # pos, qualifier, gloss, syndata):
        sense = Sense(data) # pos, qualifier, gloss, syndata)
        # Add "form of" if it's in the first sense
        if self._senses is None:
            self._senses = []
            if sense.lemma:
                self.add_lemma(sense.lemma, sense.formtype)

        if sense not in self._senses:
            self._senses.append(sense)

#    def add_sense(self, pos, qualifier, gloss, syndata):
#        sense = Sense(pos, qualifier, gloss, syndata)
#        # Add "form of" if it's in the first sense
#        if sense.lemma and not self.senses:
#            self.add_lemma(sense.lemma, sense.formtype)
#        self.senses.append(sense)

    def _parse_meta(self):
        if not self._meta_parsed and self.meta:
            self._meta_parsed = True
            self.add_forms_from_meta()

            if self.genders == "fp":
                for form in self._forms.get("mpl", []):
                    self.add_lemma(form, "fpl")

    @property
    def form_of(self):
        self._parse_meta()
        self._parse_sense_data()
        return self._form_of

    @property
    def forms(self):
        self._parse_meta()
        return self._forms

    def has_form(self, form, formtype=None):
        if formtype:
            return form in self.forms.get(formtype,[])
        return any(form in f for f in self.forms.values())

    def add_forms_from_meta(self):
        for template in templates.iter_templates(self.meta):
            if template.name == "head":
                data = self.get_head_forms(template)
            else:
                data = templates.expand_template(template, self.word)

            for formtype, form in self.parse_list(data):
                self.add_form(formtype, form)

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

            formtype = shorten_formtype.get(formtype, formtype)

            if formtype not in res:
                res[formtype] = [form]
            else:
                res[formtype].append(form)

        return "; ".join([f"{k}={v}" for k,vs in sorted(res.items()) for v in vs])
