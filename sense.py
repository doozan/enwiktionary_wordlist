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
