#!/usr/bin/python3

import csv
import json
import re
import sys
from smart_open import open

from collections import defaultdict

class KaikkiToWordlist():

    # Ignore badly parsed formdata
    EXCLUDE_FORMS = {'', 'es-conj'}

    _form_terms = [
        "simple",
        "masculine",
        "feminine",
        "first",
        "second",
        "third",
        "person",
        "singular",
        "plural",
        "past",
        "present",
        "future",
        "tense",
        "infinitive",
        "imperfect",
        "conditional",
        "participle",
        "preterite",
        "gerund",
        "imperative",
        "indicative",
        "subjunctive",
        "female equivalent",
        "voseo",
        " ",
        "-",
        "/",
        "and",
        "form",
    ]
    RE_FORMTYPE = "(?:" + "|".join(_form_terms) +")+"

    def __init__(self, filename, include_self_declared_forms=False):
        self.all_forms = self.load_forms(filename, include_self_declared_forms)
        self.all_lemmas = self.load_lemmas(filename, self.all_forms)

    @classmethod
    def load_lemmas(cls, filename, all_forms):

        all_lemmas = defaultdict(lambda: defaultdict(list))
        with open(filename) as infile:
            for line in infile:
                data = json.loads(line)

                if cls.is_generated_form(data, all_forms):
                    continue

                cls.add_lemma(data, all_lemmas)

        return all_lemmas

    @classmethod
    def load_forms(cls, filename, include_self_declared=False):
        """ If include_self_declared is True, forms that declare themselves to be a form of a lemma will be included
        Otherwise, only forms that are declared by the lemma itself will be included
        """
        all_forms = defaultdict(set)
        with open(filename) as infile:
            for line in infile:
                if '"forms"' in line:
                    cls.add_lemma_forms(all_forms, json.loads(line))
                elif include_self_declared:
                    cls.add_self_declared_forms(all_forms, json.loads(line))

        return all_forms

    @classmethod
    def add_self_declared_forms(cls, all_forms, data):

        pos = data["pos"]
        form = data["word"]

        for sense in data["senses"]:
            sense_data = cls.parse_sense(sense)
            if not sense_data:
                continue
            gloss = sense_data["gloss"]

            formtype, lemma = cls.get_formtype(gloss)

            if not formtype or not lemma:
                continue

            cls.add_lemma_form(all_forms, lemma, pos, form, formtype)

    @staticmethod
    def add_lemma_form(all_forms, lemma, pos, form, formtype=None):
        # TODO: store formtype?
        all_forms[(lemma, pos)].add(form)

    @classmethod
    def add_lemma_forms(cls, all_forms, data):

        forms = data.get("forms")
        if not forms:
            return

        pos = data["pos"]
        lemma = data["word"]

        for form_data in forms:
            form = form_data.get("form")
            if form in cls.EXCLUDE_FORMS:
                continue
            cls.add_lemma_form(all_forms, lemma, pos, form)


    @staticmethod
    def is_known_form(form, pos, formtype, lemma, all_forms):
        if not formtype or not lemma:
            return False

        # TODO: verify formtype as well as the existence of the form
        return form in all_forms.get((lemma, pos), [])

    @classmethod
    def is_generated_form(cls, form_data, all_forms):
        form = form_data.get("word")
        pos = form_data.get("pos")
        senses = form_data.get("senses", [])

        return all(cls.is_generated_sense(s, form, pos, all_forms) for s in senses)

    @classmethod
    def is_generated_sense(cls, sense_data, form, pos, all_forms):

        glosses = sense_data.get("glosses", [])
        for gloss in glosses:
            formtype, lemma, = cls.get_formtype(gloss)
            if not cls.is_known_form(form, pos, formtype, lemma, all_forms):
                return False

        return True

    @classmethod
    def get_formtype(cls, gloss):

        # Check for combined
        match = re.match(f"({cls.RE_FORMTYPE}) of (.*?) combined with (.*)", gloss, re.IGNORECASE)
        if match:
            return f"{match.group(1)} combined with {match.group(3)}", match.group(2)

        # Check for expected form type
        match = re.match(f"({cls.RE_FORMTYPE})+ of (.*)", gloss, re.IGNORECASE)
        if match:
            return match.group(1), match.group(2)

        # Manual check for data generate by {{es-verb form of}}, which can only generate valid forms
        match = re.match("inflection of (.*?):\n##.*", gloss, re.IGNORECASE)
        if match:
            return "smart_inflection", match.group(1)

        return None, None

    @staticmethod
    def parse_sense(sense_data):
        glosses = sense_data.get("raw_glosses", [])
        if not glosses:
            return

        # In Spanish, only glosses following "{{rfdef}}" will have multiple entries
        # see 'rabiza'
        # # {{lb|es|nautical}} {{rfdef|es}}<!-- A [[snap end]]?-->
        #
        # The first gloss entry is the 'empty' entry, the following is the real entry
        if len(glosses) > 1:
            return

        gloss = glosses[0]
        res = {"gloss": gloss}

        syns = "; ".join(s['word'] for s in sense_data.get("synonyms", []))
        if syns:
            res["syn"] = syns

        senseid = "; ".join(sense_data.get("senseid", []))
        if senseid:
            res["senseid"] = senseid

        # TODO: get examples and other data

        return res

    @classmethod
    def add_lemma(cls, lemma_data, all_lemmas):

        senses = [cls.parse_sense(s) for s in lemma_data.get("senses", [])]
        senses = [s for s in senses if s]
        if not senses:
            return

        lemma = lemma_data.get("word")
        pos = lemma_data.get("pos")

        item = {}
        ety = lemma_data.get("etymology_text")
        if ety:
            item["etymology"] = ety
        item["senses"] = senses

        all_lemmas[lemma][pos].append(item)


    @staticmethod
    def print_value(depth, k, v):
        try:
            print('  '*depth + k + ": " + v.replace('\n', '\\n'))
        except BaseException as e:
            print("err", depth, k, v)
            raise e

    def dump_wordlist(self):

        for lemma, all_pos in sorted(self.all_lemmas.items()):
            print(f"_____\n{lemma}")
            for pos, items in all_pos.items():
                for item in items:
                    self.print_value(0, "pos", pos)
                    for k,v in sorted(item.items()):
                        if k != "senses":
                            self.print_value(1, k, v)
                    for sense in item["senses"]:
                        self.print_value(1, "gloss", sense["gloss"])
                        for k,v in sorted(sense.items()):
                            if k != "gloss":
                                self.print_value(2, k, v)

    def dump_allforms(self, filename):

        # build data[form,pos] = [lemmas]
        data = defaultdict(set)
        for lemma_pos, forms in self.all_forms.items():
            lemma, pos = lemma_pos
            data[(lemma, pos)].add(lemma)

            for form in forms:
                data[(form, pos)].add(lemma)

        with open(filename, "w") as outfile:
            csvwriter = csv.writer(outfile)
            for form_pos, lemmas in sorted(data.items()):
                form, pos = form_pos
                csvwriter.writerow([form, pos]+sorted(lemmas))

