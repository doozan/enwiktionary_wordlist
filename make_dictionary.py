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
This will build a dictionary from an english wiktionary dump
"""

import os
os.environ["PYWIKIBOT_NO_USER_CONFIG"]="2"
from pywikibot import xmlreader
from enwiktionary_templates import expand_templates
import re
import sys

import enwiktionary_parser as wtparser


class DictionaryBuilder:
    def __init__(self, lang_name, lang_id):
        self.LANG_SECTION = lang_name
        self.LANG_ID = lang_id
        self._problems = {}
        self._stats = {}
        self.fixes = set()
        self.title = None

    def flag_problem(self, problem, *data, from_child=False):
        """
        Add *problem* to the internal list of problems
        """
        self._problems[problem] = self._problems.get(problem, []) + [data]
        # TODO: do something with the errors raised

    def get_language_entry(self, text):
        """
        Return the body text of the language entry
        """
        start = fr"(^|\n)==\s*{self.LANG_SECTION}\s*==\s*\n"
        re_endings = [ r"\[\[\s*Category\s*:", r"==[^=]+==", r"----" ]
        #template_endings = [ "c", "C", "top", "topics", "categorize", "catlangname", "catlangcode", "cln", "DEFAULTSORT" ]
        template_endings = [ "top", "topics", "categorize", "catlangname", "catlangcode", "DEFAULTSORT" ]
        re_endings += [ r"\{\{\s*"+item+r"\s*\|" for item in template_endings ]
        endings = "|".join(re_endings)
        newlines = r"(\n\s*){1,2}"
        pattern = fr"{start}.*?(?={newlines}({endings})|$)"

        res = re.search(pattern, text, re.DOTALL)
        if res:
            return res.group(0)

    def exclude_word(self, word):
        if not hasattr(word, "headword") or not word.headword:
            return False

        headword = word.headword
        # Ignore forms
        # FIXME: put language specific stuff someplace else?
        if str(headword.name) in { "es-adj-form", "es-verb-form", "es-past participle" }:
            return True

        # Ignore feminine forms
        # FIXME: put language specific stuff someplace else?
        if str(headword.name) == "es-adj" and headword.has("m") or headword.has("masculine"):
            return True

        if str(headword.name) == "head" and headword.has(2) and " form" in str(headword.get(2)):
            return True

        return False

    def build_meta(self, title, metatype, data):
        if not data or not data.strip():
            return None
        return title + " {meta-" + metatype + "} :: " + data

    def forms_to_meta(self, forms):
        if not forms:
            return None

        res = []
        for k,values in sorted(forms.items()):
            for v in values:
                if re.search(r"[\<\{\[]", v):
                    v = self.wiki_to_text(v)

                if ";" in v:
                    raise ValueError(f"ERROR: ; found in value ({v})")

                res.append(f"{k}={v}")

        return "; ".join(res)

    def get_meta(self, title, word):
        """ Returns a list of meta entries or None if word has no form data"""
        if word.shortpos in ["n", "prop", "num"]:
            metatype = "noun"

        elif word.shortpos in ["adj"]:
            metatype = "adj"

        elif word.shortpos.startswith("v"):
            metatype = "verb"

        else:
            return []

        meta = self.build_meta(title, metatype, self.forms_to_meta(word.forms))
        if meta:
            return [meta]
        return []


    def parse_entry(self, text, title):
        self.title = title
        wikt = wtparser.parse_page(text, title, parent=self)

        entry = []

        for word in wikt.ifilter_words():
            all_meta = self.get_meta(title, word)
            for meta in all_meta:
                entry.append(meta)

            if self.exclude_word(word):
                continue

            for sense in word.ifilter_wordsenses():
                # Skip senses that are just a request for a definition
                if "{{rfdef" in sense.gloss:
                    continue
                if "{{defn" in sense.gloss:
                    continue

                gloss_text = self.gloss_to_text(sense.gloss)
                if gloss_text == "":
                    continue

                synonyms = []
                for nymline in sense.ifilter_nymlines(matches = lambda x: x.type == "Synonyms"):
                    synonyms += self.items_to_synonyms(nymline.items)

                all_qualifiers = word.qualifiers + sense.gloss.qualifiers
                pos = self.make_pos_tag(word, all_qualifiers)
                qualification = self.make_qualification(all_qualifiers, title)

                items = [title, pos]
                if qualification:
                    items.append(qualification)
                if synonyms:
                    items.append("|")
                    items.append("; ".join(synonyms))

                items.append("::")
                items.append(gloss_text)

                line = " ".join(items)
                entry.append(line)

        return entry

    def wiki_to_text(self, wikitext):
        wikt = wtparser.parse(wikitext)

        expand_templates(wikt, self.title)

        # Reparse and expand links
        wikt = wtparser.parse(str(wikt))
        for wikilink in wikt.filter_wikilinks():
            display = wikilink.text if wikilink.text else wikilink.title
            wikt.replace(wikilink, display)


        # Remove comments
        for comment in wikt.filter_comments():
            wikt.remove(comment)
        # Also remove any unterminated comments
        res = re.sub(r"<!--.*", "", str(wikt))

        res = re.sub("''+", "", res)
        res = re.sub(r"<sup>(.*?)</sup>", r"^\1", res)
        res = re.sub(r"<sub>(.*?)</sub>", r"\1", res)
        res = re.sub(r"<ref(.*?)</ref>", "", res)
        res = re.sub(r"<ref [^>]*/>", "", res)
        res = re.sub(r"<ref>.*", "", res)
        res = re.sub(r"&nbsp;", " ", res)
        res = re.sub(r"&ndash;", "-", res)
        return res

    def gloss_to_text(self, gloss):
        return re.sub(r"\s\s+", " ", self.wiki_to_text(gloss.data.rstrip("\r\n\t .")).strip())

    def items_to_synonyms(self, items):
        synonyms = []
        for item in items:
            synonym = None
            if "alt" in item:
                synonym = self.wiki_to_text(item["alt"]).strip()
            if not synonym:
                synonym = self.wiki_to_text(item["target"]).strip()
            if synonym:
                synonyms.append(synonym)
#           [ { "target": "word", "q": "qual" }, { "target": "word2", "tr": "tr" } ]

        return synonyms

    q_verbs = {
        "transitive": "t",
        "reflexive": "r",
        "intransitive": "i",
        "pronominal": "p",
        "ambitransitive": "it",
    }

    def make_gendertag(self, all_genders):
        genders = []
        for gender in all_genders:
            gender = gender.replace("-", "")
            if gender not in genders:
                genders.append(gender)
        return "".join(genders)

    def make_pos_tag(self, word, qualifiers):
        pos = word.shortpos
        gendertag = self.make_gendertag(word.genders)

        if pos in ["n","prop"] and gendertag:
            return "{" + gendertag + "}"
        if pos == "v":
            for q in qualifiers:
                if q in self.q_verbs:
                    pos += self.q_verbs[q]

        return "{" + pos + "}"

    def make_qualification(self, all_qualifiers, title):
        """ Remove verb qualifiers and process remaining as if it were a label """

        qualifiers = [q for q in all_qualifiers if not q in self.q_verbs]
        # FIXME: hardcoded language key
        template_str = "{{lb|es|" + "|".join(qualifiers) + "}}"
        qualified = self.wiki_to_text(template_str)
        if not qualified:
            return ""

        # Change () to []
        return "[" + qualified[1:-1] + "]"

def main():

    import argparse

    parser = argparse.ArgumentParser(description="Convert *nym sections to tags.")
    parser.add_argument("--xml", help="XML file to load", required=True)
    parser.add_argument("--lang-id", help="Language id", required=True)
    parser.add_argument("--lang-section", help="Language name", required=True)
    args = parser.parse_args()

    if not os.path.isfile(args.xml):
        raise FileNotFoundError(f"Cannot open: {args.xml}")

    # TODO: get lang-section from lang-id
    # or, use --lang param and take either lang-id or language name

    dump = xmlreader.XmlDump(args.xml)
    parser = dump.parse()

    builder = DictionaryBuilder(args.lang_section, args.lang_id)

    count = 0
    lang_count = 0

    for entry in parser:
        count += 1

        if ":" in entry.title:
            continue

        lang_entry = builder.get_language_entry(entry.text)

        if not lang_entry:
            continue

        lang_count += 1

        entry = builder.parse_entry(lang_entry, entry.title)
        for line in entry:
            if line.strip() != "":
                print(line)

if __name__ == "__main__":
    main()
