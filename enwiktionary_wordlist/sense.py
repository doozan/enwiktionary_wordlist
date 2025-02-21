import re
import sys

from .example import Example

class Sense():
    def __init__(self, data, depth=1): # pos, qualifier, gloss, syndata):

        assert depth > 0
        self.depth = depth
        self.gloss = None
        self.qualifier = None
        self.usage = []
        self.id = None
        self._regiondata = None
        self._regions = None
        self._nymdata = []
        self._nyms = []
        self.examples = []
        self.subsenses = []

        gloss = "_" * (depth-1) + "gloss"
        subsense = "_" + gloss
        prev = ["_" * p + "gloss"  for p in range(depth-1)]

        while(data):
            item = data.pop(0)
            key, value = item
            if key == gloss:
                if depth == 1:
                    assert self.gloss == None
                    self.gloss = value
                else:
                    if self.gloss == None:
                        self.gloss = value
                    # Start of a new subsense, repair the stack and return
                    else:
                        data.insert(0, item)
                        break
            elif key == subsense:
                # new subsense, repair the stack
                data.insert(0, item)
                self.subsenses.append(Sense(data, depth+1))
            elif key in prev: # start of a new sense, repair the stack and return
                data.insert(0, item)
                break
            elif key == "ex":
                data.insert(0, item)
                self.parse_examples(data)
            elif key == "id":
                self.id = value
            elif key == "usage":
                self.usage.append(value)
            elif key in ["syn", "ant"]:
                self._nymdata.append((key, value))
            elif key == "q":
                # "q" before nymdata applies to the gloss
                # "q" after nymdata applies to the nyms
                if self._nymdata:
                    self._nymdata.append((key, value))
                else:
                    self.qualifier = value
            elif key == "regional":
                self._regiondata = value
            else:
                raise ValueError(f"Unexpected data: {key}, {value}")

        self.formtype, self.lemma, self.nonform = self.parse_form_of(self.gloss)
        if self.lemma:
            self.lemma = self.lemma.strip()

    def parse_examples(self, data):
        ex_data = []
        while data:
            item = data.pop(0)
            key, value = item
            if key == "ex":
                if ex_data:
                    self.add_example(ex_data)
                ex_data = [item]
            elif key in ["eng", "src"]:
                ex_data.append(kv)
            else:
                data.insert(0, item)
                break
        if ex_data:
            self.add_example(ex_data)

    def add_example(self, ex_data):
        self.examples.append(Example(ex_data))

    @property
    def nyms(self):
        if self._nymdata:
            nymtype = None
            qualifier = None
            nyms = []

            for k, v in self._nymdata:
                if k in ["syn", "ant"]:
                    if nyms:
                        self._nyms.append((nymtype, qualifier, nyms))
                    nymtype = k
                    qualifier = None
                    nyms = self.parse_list(v)
                elif k == "q":
                    qualifier = v
                else:
                    raise ValueError("Unhandled nymdata", (k,v), self._nymdata)

            if nyms:
                self._nyms.append((nymtype, qualifier, nyms))

            self._nymdata = None
        return self._nyms

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
        "misspelling": "alt",
        "neuter singular": "form",
        "nonstandard form": "alt",
        "nonstandard spelling": "alt",
        "obsolete form": "old",
        "obsolete spelling": "old",
        "only used": "onlyin", # forms may differ in POS from the target
        "plural": "pl",
        "pronunciation spelling": "alt",
        "rare form": "rare",
        "rare spelling": "rare",
        "reflexive": "reflexive",
        "singular": "form",
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
        "smart inflection": "smart_inflection",
        r"(?:gerund|pp|cond|fut|infinitive|imp|impf|neg_imp|pres|pret)_\w+": "1", # patern matches will always be themselves
    }

    alt_form_pattern = r"(?:^|A |An |\(|[,;:\)] )(" + "|".join(form_of_prefix.keys()) + r") (?:of|in) ([^,;:()]*)[,;:()]?"

    # Add "form" after the alt form pattern is generated so it doesn't warn on every literal string with the phrase "form of xxx"
    form_of_prefix["form"] = "alt"
    form_pattern = r"(?:^|A |An |\(|[,;:\)] )(" + "|".join(form_of_prefix.keys()) + r') (?:of|in) "([^"]*)"'
