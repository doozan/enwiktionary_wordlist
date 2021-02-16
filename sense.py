import re
import sys

class Sense():
    def __init__(self, data): # pos, qualifier, gloss, syndata):

        self.gloss = None
        self.qualifier = None
        self._syndata = None
        self._synonyms = None

        for key, value in data:
            if key == "gloss":
                self.gloss = value
            elif key == "q":
                self.qualifier = value
            elif key == "syn":
                self._syndata = value

        if " of " in self.gloss:
            self.formtype, self.lemma, self.nonform = self.parse_form_of(self.gloss)
            if self.lemma:
                self.lemma = self.lemma.strip()
        else:
            self.formtype = None
            self.lemma = None
            self.nonform = None

    @property
    def synonyms(self):
        if self._syndata:
            self._synonyms = self.parse_syndata(self._syndata)
        if not self._synonyms:
            return []
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
            if res.group(1) == "compound form":
                nonform = re.sub(r'^([+]".*?")*', "", nonform)
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
        "adjective form": "alt", # form
        "alternative case form": "alt",
        "alternate form": "alt",
        "alternate spelling": "alt",
        "alternative form": "alt",
        "alternative spelling": "alt",
        "alternative typography": "alt",
        "apocopic form": "alt",
        "archaic spelling": "old",
        "common misspelling": "spell",
        "compound form": "alt", # form
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
        "inflection": "alt", # form
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
        "only used in": "alt",
        "plural": "pl",
        "pronunciation spelling": "alt",
        "rare form": "rare",
        "rare spelling": "rare",
        "superseded form": "old",
        "superseded spelling": "old",
    }
    alt_form_pattern = r"(?:^|A |An |\(|[,;:\)] )(" + "|".join(form_of_prefix.keys()) + r") of ([^,;:()]*)[,;:()]?"

    # Add "form" after the alt form pattern is generated so we don't match every "form of xxx"
    form_of_prefix["form"] = "alt"
    form_pattern = r"(?:^|A |An |\(|[,;:\)] )(" + "|".join(form_of_prefix.keys()) + r') of "([^"]*)"'
