#!/usr/bin/python3
#
# Copyright (c) 2020 Jeff Doozan
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Convert a wiktionary entries into wordlist entries
"""

from collections import defaultdict
import os
import re
import sys

import enwiktionary_parser as wtparser
from enwiktionary_parser.sections.usage import UsageSection
from enwiktionary_parser.sections.etymology import EtymologySection

from enwiktionary_wordlist.utils import wiki_to_text, make_qualification, make_pos_tag

class WordlistBuilder:
    def __init__(self, lang_name, lang_id):
        self.LANG_SECTION = lang_name
        self.LANG_ID = lang_id

        start = fr"(^|\n)==\s*{self.LANG_SECTION}\s*==\s*\n"
        re_endings = [ r"\[\[\s*Category\s*:", r"==[^=]+==", r"----" ]
        #template_endings = [ "c", "C", "top", "topics", "categorize", "catlangname", "catlangcode", "cln", "DEFAULTSORT" ]
        template_endings = [ "top", "topics", "categorize", "catlangname", "catlangcode", "DEFAULTSORT" ]
        re_endings += [ r"\{\{\s*"+item+r"\s*\|" for item in template_endings ]
        endings = "|".join(re_endings)
        newlines = r"(\n\s*){1,2}"
        pattern = fr"{start}.*?(?={newlines}({endings})|$)"
        self._re_pattern = re.compile(pattern, re.DOTALL)

    def get_language_entry(self, text):
        """
        Return the body text of the language entry
        """

        res = re.search(self._re_pattern, text)
        if res:
            return res.group(0)

    def forms_to_string(self, forms, title):
        if not forms:
            return None

        res = []
        for k,values in sorted(forms.items()):
            for v in sorted(values):
                if re.search(r"[\<\{\[]", v):
                    v = wiki_to_text(v, title)

                if ";" in v:
                    raise ValueError(f"ERROR: ; found in value ({v})")

                k = re.sub("[.,/:;]+", "", k)
                k = re.sub(" +", "_", k)
                res.append(f"{k}={v}")

        return "; ".join(res)


    def get_meta(self, title, word):
        """ Returns a formatted form line with the template(s) defining the forms """

        pos = word.shortpos
        return title + " {" + pos + "-meta} :: " + " ".join(map(str,word.form_sources)).replace("\n","")


    def get_etymology(self, word):
        # Ideally, the word is inside an Etymology section
        res = word.get_ancestor(EtymologySection)
        if res:
            return [res]

        # But sometimes etymology is L3 and POS is also L3, find the nearest preceeding etymology section
        for sibling in word._parent._parent.ifilter(recursive=False):
            if isinstance(sibling,  EtymologySection):
                res = sibling
            if sibling == word._parent:
                break
        if res:
            return [res]
        return []

    def get_usage(self, word):
        """ Returns a list of Usage sections that match the given word """

        res = None
        # First, look for Usage as a child of the word
        after = False
        res = word._parent.filter_usagenotes(recursive=True)
        if res:
            return res

        # Next, look for usage notes that come after the word at the same level
        after = False
        for sibling in word._parent._parent.ifilter(recursive=False):
            if sibling == word._parent:
                after = True
            if not after:
                continue
            if isinstance(sibling, UsageSection):
                return sibling.filter_usagenotes(recursive=True)

        return []

    def entry_to_text(self, text, title):
        wikt = wtparser.parse_page(text, title, parent=self)

        words = wikt.filter_words()
        if not words:
            return []

        entry = []

        for word in wikt.ifilter_words():
            senses = []
            for sense in word.ifilter_wordsenses():
                # Skip senses that are just a request for a definition
                if "{{rfdef" in sense.gloss:
                    continue
                if "{{defn" in sense.gloss:
                    continue

                gloss_text = self.gloss_to_text(sense.gloss, title)
                if gloss_text == "":
                    continue

                sense_data = {}
                sense_data["gloss"] = gloss_text

                if sense.gloss.qualifiers:
                    qualifiers = make_qualification(self.LANG_ID, title, sense.gloss.qualifiers)
                    if qualifiers:
                        qualifiers = qualifiers.rstrip(", ")
                        sense_data["q"] = qualifiers

                synonyms = []
                for nymline in sense.ifilter_nymlines(matches = lambda x: x.type == "Synonyms"):
                    synonyms += self.items_to_synonyms(nymline.items, title)
                if synonyms:
                    sense_data["syn"] = '; '.join(synonyms)

                if sense_data not in senses:
                    senses.append(sense_data)

            usages = []
            for usage in self.get_usage(word):
                usage_text = self.usage_to_text(usage, title)
                if usage_text:
                    usages.append(usage_text)

            etys = []
            for ety in self.get_etymology(word):
                for node in ety.ifilter_etymologies():
                    ety_text = self.etymology_to_text(node, title)
                    if ety_text:
                        etys.append(ety_text)
                word.ifilter_wordsenses()

            entry += self.make_word_entry(
                pos = word.shortpos,
                meta = " ".join(map(str,word.form_sources)).replace("\n", ""),
                genders = "; ".join(word.genders) if word.genders else None,
                qualifier = make_qualification(self.LANG_ID, title, word.qualifiers),
                usages = usages,
                etys =  etys,
                senses = senses,
            )

        return entry

    @staticmethod
    def make_word_entry(pos, meta, qualifier, genders, usages, etys, senses):
        word_entry = []
        word_entry.append(f"pos: {pos}")
        if meta:
            word_entry.append(f"  meta: {meta}")

        if genders:
            word_entry.append(f"  g: {genders}")

        if qualifier:
            word_entry.append(f"  q: {qualifier}")

        for usage in usages:
            if usage:
                word_entry.append(f"  usage: {usage}")

        for ety in etys:
            if ety:
                word_entry.append(f"  etymology: {ety}")

        for sense_data in senses:
            for k,v in sense_data.items():
                if not v:
                    continue
                if k == "gloss":
                    word_entry.append(f"  {k}: {v}")
                else:
                    word_entry.append(f"    {k}: {v}")

        return word_entry

    def gloss_to_text(self, gloss, title):
        return re.sub(r"\s\s+", " ", wiki_to_text(gloss.data.rstrip("\r\n\t ."), title).strip())

    def usage_to_text(self, usage, title):
        text = wiki_to_text(usage, title).strip()
        # Strip leading * if there are no newlines
        if "\n" not in text:
            text = re.sub("^[ *#]+", "", text)
        else:
            text = re.sub("\n", r"\\n", text)
        return text

    def etymology_to_text(self, etymology, title):
        return re.sub("\n", r"\\n", wiki_to_text(etymology, title).strip())

    def items_to_synonyms(self, items, title):
        synonyms = []
        for item in items:
            synonym = None
            if "alt" in item:
                synonym = wiki_to_text(item["alt"], title).strip()
            if not synonym:
                synonym = wiki_to_text(item["target"], title).strip()
            if synonym:
                synonyms.append(synonym)
#           [ { "target": "word", "q": "qual" }, { "target": "word2", "tr": "tr" } ]

        return synonyms

    @classmethod
    def word_to_text(cls, word):

        senses = []
        non_verbform_sense = False
        for sense in word.senses:
            if not sense.gloss:
                continue

            s = {}
            s["gloss"] = sense.gloss
            s["q"] = sense.qualifier.rstrip(", ") if sense.qualifier else None
            s["syn"] = "; ".join(sense.synonyms) if sense.synonyms else None
            s["regional"] = "; ".join(sense.regions) if sense.regions else None
            senses.append(s)

        word_lines = WordlistBuilder.make_word_entry(
            pos = word.pos,
            meta = word.meta,
            qualifier = word.qualifier,
            genders = word.genders,
            usages = [word.use_notes],
            etys = [word.etymology],
            senses = senses
            )

        return word_lines

    @staticmethod
    def has_extra_info(word):
        """ Returns true if a word has data beyond what can be auto generated """
        return word.qualifier or word.use_notes or word.etymology


    @staticmethod
    # word must be the pp_ms form
    def get_part_lemma(word, wordlist):
        for word in wordlist.get_words(word, "part"):
            for sense in word.senses:
                if sense.lemma:
                    return sense.lemma

    @staticmethod
    def get_part_formtype(formtype):
        return {"pp_ms": "pp_ms", "f": "pp_fs", "mpl": "pp_mp", "fpl": "pp_fp"}.get(formtype, formtype)

    @classmethod
    def is_generated(cls, word, wordlist):
        """ Returns true if a word is a simple form that can be generated by the given wordlist """

        def has_reflexive(lemma):
            return any(s.qualifier and re.search("(reflexive|pronominal)", s.qualifier) for s in lemma.senses)

        for sense in word.senses:
            if not sense.formtype or sense.nonform:
                return False

            formtype = "pl" if word.pos == "adj" and sense.formtype == "mpl" else sense.formtype

            if formtype == "smart_inflection":
                continue

            lemmas = wordlist.get_words(sense.lemma, word.pos)
            if formtype == "reflexive" and any(has_reflexive(lemma) for lemma in lemmas):
                continue

            # -r verbs are infinitive of -rse verbs, but -rse verbs list themselves at their infinitive formtype
            if formtype == "infinitive" and sense.lemma.endswith("rse") and any(wordlist.get_words(sense.lemma[:-2])):
                continue

            # participles should be considered generated if they match the pp_XX forms of the verb
            # only pp_ms will list the verb, the others will list the pp_ms form and will need
            # to do a lookup to find the verb
            if word.pos == "part":
                formtype = cls.get_part_formtype(formtype)
                lemma = sense.lemma if formtype == "pp_ms" else cls.get_part_lemma(sense.lemma, wordlist)
                if not lemma or not any(word.word in l.forms.get(formtype, []) for l in wordlist.get_words(lemma, "v")):
                    return False
                continue

            if not any(word.word in l.forms.get(formtype, []) for l in lemmas):
                # infinitive_comb will refer to the -r form of -rse verbs, so manually check the -rse lemma
                if (formtype.startswith("infinitive_comb_") or formtype.startswith("gerund_comb_")) \
                    and sense.lemma.endswith("r") \
                    and any(word.word in l.forms.get(formtype, []) for l in wordlist.get_words(sense.lemma + "se", "v")):
                    continue
                return False

        return True


    @staticmethod
    def from_wordlist(wordlist, exclude_generated, exclude_empty):
        entry = []
        for word in sorted(wordlist.all_entries.keys()):
            skipped = defaultdict(list)
            header = False
            for word_obj in wordlist.get_words(word):

                if exclude_empty and not word_obj.senses:
                    continue

                # Words with forms before lemmas are forms
                # eg, piernas is usually a form of pierna, not the less-frequenly used piernas
                # because its words are listed in the order (piernas, form of pierna), (piernas, lemma)
                # For these rare cases, it's important to preserve the "form of", even if it's a
                # generated form of

                if exclude_generated and WordlistBuilder.is_generated(word_obj, wordlist):
                    skipped[word_obj.pos].append(word_obj)
                    continue

                queue = skipped[word_obj.pos] + [word_obj]
                skipped[word_obj.pos] = []
                for word_obj in queue:
                    word_lines = WordlistBuilder.word_to_text(word_obj)
                    if not word_lines:
                        continue
                    if not header:
                        if entry:
                            yield "\n".join(entry)
                            entry = []
                        header = True
                        entry = ["_____", word]
                    entry += word_lines

        if entry:
            yield "\n".join(entry)
