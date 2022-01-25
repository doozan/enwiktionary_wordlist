import re
import sys

class Sense():
    def __init__(self, data): # pos, qualifier, gloss, syndata):

        self.gloss = None
        self.qualifier = None
        self._regiondata = None
        self._regions = None
        self._syndata = None
        self._synonyms = None

        for key, value in data:
            if key == "gloss":
                self.gloss = value
            elif key == "q":
                self.qualifier = value
            elif key == "syn":
                self._syndata = value
            elif key == "regional":
                self._regiondata = value
            else:
                raise ValueError(f"Unexpected data: {key}, {value}")

        self.formtype, self.lemma, self.nonform = self.parse_form_of(self.gloss)
        if self.lemma:
            self.lemma = self.lemma.strip()

    @property
    def synonyms(self):
        if self._syndata:
            self._synonyms = self.parse_list(self._syndata)
            self._syndata = None
        return self._synonyms

    @property
    def regions(self):
        if self._regiondata:
            self._regions = self.parse_list(self._regiondata)
            self._regiondata = None
        return self._regions

    @classmethod
    def parse_list(cls, syndata):
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
            formtype = cls.form_of_prefix.get(res.group(1), res.group(1))
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
        "adjective form": "form",
        "alternate form": "alt",
        "alternate spelling": "alt",
        "alternative letter-case form": "alt",
        "alternative case form": "alt",
        "alternative form": "alt",
        "alternative spelling": "alt",
        "alternative typography": "alt",
        "apocopic form": "alt",
        "archaic spelling": "old",
        "common misspelling": "alt",
        "compound form": "form",
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
        "infinitive": "infinitive",
        "inflection": "form",
        "informal form": "alt",
        "informal spelling": "alt",
        "masculine": "m",
        "masculine singular": "m",
        "masculine plural": "mpl",
        "misspelling": "spell",
        "neuter singular": "form",
        "nonstandard form": "alt",
        "nonstandard spelling": "alt",
        "obsolete form": "old",
        "obsolete spelling": "old",
        "only used": "alt",
        "plural": "pl",
        "pronunciation spelling": "alt",
        "rare form": "rare",
        "rare spelling": "rare",
        "reflexive": "reflexive",
        "superseded form": "old",
        "superseded spelling": "old",
        "present participle": "gerund",
        "past participle": "pp_ms",
        "masculine singular past participle": "pp_ms",
        "masculine plural past participle": "pp_mp",
        "feminine singular past participle": "pp_fs",
        "feminine plural past participle": "pp_fp",
        "gerund": "gerund",
        "infinitive": "infinitive",
        r"(?:gerund|pp|cond|fut|infinitive|imp|impf|neg_imp|pres|pret)_\w+": "1", # patern matches will always be themselves
    }

    alt_form_pattern = r"(?:^|A |An |\(|[,;:\)] )(" + "|".join(form_of_prefix.keys()) + r") (?:of|in) ([^,;:()]*)[,;:()]?"

    # Add "form" after the alt form pattern is generated so it doesn't warn on every literal string with the phrase "form of xxx"
    form_of_prefix["form"] = "alt"
    form_pattern = r"(?:^|A |An |\(|[,;:\)] )(" + "|".join(form_of_prefix.keys()) + r') (?:of|in) "([^"]*)"'
