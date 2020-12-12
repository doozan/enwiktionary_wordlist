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
from enwiktionary_extract import LanguageFile
import re
import sys

import enwiktionary_parser as wtparser
from enwiktionary_parser.languages.all_ids import languages as lang_ids

class WordlistBuilder:
    def __init__(self, lang_name, lang_id):
        self.LANG_SECTION = lang_name
        self.LANG_ID = lang_id
        self._problems = {}
        self._stats = {}
        self.fixes = set()
        self.title = None

        start = fr"(^|\n)==\s*{self.LANG_SECTION}\s*==\s*\n"
        re_endings = [ r"\[\[\s*Category\s*:", r"==[^=]+==", r"----" ]
        #template_endings = [ "c", "C", "top", "topics", "categorize", "catlangname", "catlangcode", "cln", "DEFAULTSORT" ]
        template_endings = [ "top", "topics", "categorize", "catlangname", "catlangcode", "DEFAULTSORT" ]
        re_endings += [ r"\{\{\s*"+item+r"\s*\|" for item in template_endings ]
        endings = "|".join(re_endings)
        newlines = r"(\n\s*){1,2}"
        pattern = fr"{start}.*?(?={newlines}({endings})|$)"
        self._re_pattern = re.compile(pattern, re.DOTALL)

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

        res = re.search(self._re_pattern, text)
        if res:
            return res.group(0)

    def forms_to_string(self, forms):
        if not forms:
            return None

        res = []
        for k,values in sorted(forms.items()):
            for v in sorted(values):
                if re.search(r"[\<\{\[]", v):
                    v = self.wiki_to_text(v, self.title)

                if ";" in v:
                    raise ValueError(f"ERROR: ; found in value ({v})")

                k = re.sub("[.,/:;]+", "", k)
                k = re.sub(" +", "_", k)
                res.append(f"{k}={v}")

        return "; ".join(res)

    def get_forms(self, title, word):
        """ Returns a formatted form line containing the word forms """
        if not word.forms:
            return None

        if word.shortpos == "prop":
            pos = "n"
        else:
            pos = word.shortpos

        return title + " {" + pos + "-forms} :: " + self.forms_to_string(word.forms)


    def get_meta(self, title, word):
        """ Returns a formatted form line with the template(s) defining the forms """

        if word.shortpos == "prop":
            pos = "n"
        else:
            pos = word.shortpos

        return title + " {" + pos + "-meta} :: " + " ".join(map(str,word.form_sources)).replace("\n","")


    def entry_to_text(self, text, title):
        self.title = title
        wikt = wtparser.parse_page(text, title, parent=self)

        words = wikt.filter_words()
        if not words:
            return []

        entry = ["_____", title]

        # TODO: Check for usage note outside word entries and append it here
        # TODO: "" synonym section

        for word in wikt.ifilter_words():
            #if self.exclude_word(word):
            #    continue

            entry.append(f"pos: {word.shortpos}")
            meta = " ".join(map(str,word.form_sources)).replace("\n", "")
            entry.append(f"  meta: {meta}")

            if word.forms:
                forms =  self.forms_to_string(word.forms)
                entry.append(f"  forms: {forms}")
            if word.genders:
                entry.append(f"  g: {'; '.join(word.genders)}")

            if word.qualifiers:
                qualifiers = self.make_qualification(word.qualifiers)[1:-1]
                entry.append(f"  q: {qualifiers}")

            # TODO: Check for usage notes

            for sense in word.ifilter_wordsenses():
                # Skip senses that are just a request for a definition
                if "{{rfdef" in sense.gloss:
                    continue
                if "{{defn" in sense.gloss:
                    continue

                gloss_text = self.gloss_to_text(sense.gloss)
                if gloss_text == "":
                    continue

                entry.append(f"  gloss: {gloss_text}")
                if sense.gloss.qualifiers:
                    qualifiers = self.make_qualification(sense.gloss.qualifiers)[1:-1]
                    entry.append(f"    q: {qualifiers}")
                synonyms = []
                for nymline in sense.ifilter_nymlines(matches = lambda x: x.type == "Synonyms"):
                    synonyms += self.items_to_synonyms(nymline.items)
                if synonyms:
                    entry.append(f"    syn: {'; '.join(synonyms)}")

                # TODO: Get usage examples?

        return entry

    def entry_to_mbformat(self, text, title):
        self.title = title
        wikt = wtparser.parse_page(text, title, parent=self)

        entry = []

        for word in wikt.ifilter_words():
            #if self.exclude_word(word):
            #    continue

            meta = self.get_meta(title, word)
            if meta:
                entry.append(meta)
            forms = self.get_forms(title, word)
            if forms:
                entry.append(forms)

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
                qualification = self.make_qualification(all_qualifiers)

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

    @staticmethod
    def wiki_to_text( wikitext, title):
        wikt = wtparser.parse(wikitext)

        expand_templates(wikt, title)

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
        return re.sub(r"\s\s+", " ", self.wiki_to_text(gloss.data.rstrip("\r\n\t ."), self.title).strip())

    def items_to_synonyms(self, items):
        synonyms = []
        for item in items:
            synonym = None
            if "alt" in item:
                synonym = self.wiki_to_text(item["alt"], self.title).strip()
            if not synonym:
                synonym = self.wiki_to_text(item["target"], self.title).strip()
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

    def make_qualification(self, all_qualifiers):
        """ Remove verb qualifiers and process remaining as if it were a label """

        qualifiers = [q for q in all_qualifiers if not q in self.q_verbs]
        template_str = "{{lb|" + self.LANG_ID + "|" + "|".join(qualifiers) + "}}"
        qualified = self.wiki_to_text(template_str, self.title)
        if not qualified:
            return ""

        # Change () to []
        return "[" + qualified[1:-1] + "]"



def iter_langdata(datafile):

    if not os.path.isfile(datafile):
        raise FileNotFoundError(f"Cannot open: {datafile}")

    yield from LanguageFile.iter_articles(datafile)

def iter_xml(datafile, lang_section, lang_id):

    if not os.path.isfile(datafile):
        raise FileNotFoundError(f"Cannot open: {datafile}")

    dump = xmlreader.XmlDump(datafile)
    parser = dump.parse()

    langparser = LanguageFile(lang_section)
    #builder = WordlistBuilder(lang_section, lang_id)

    for entry in parser:

        if ":" in entry.title:
            continue

        lang_entry = langparser.get_language_entry(entry.text)
#        lang_entry = builder.get_language_entry(entry.text)

        if not lang_entry:
            continue

        yield entry.title, lang_entry

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Convert *nym sections to tags.")
    parser.add_argument("--xml", help="Read entries from specified wiktionary XML dump")
    parser.add_argument("--langdata", help="Read articles from specified language data file")
    parser.add_argument("--wordlist", help="Read articles from existing wordlist")
    parser.add_argument("--lang-id", help="Language id", required=True)
    parser.add_argument("--limit", help="Limit to n entries", type=int, default=0)
    parser.add_argument("--mbformat", help="Output mb-compatible file format", action='store_true')
    args = parser.parse_args()

    count = 0
    entries = {}

    # Dump an existing wordlist
    if args.wordlist:
        from enwiktionary_wordlist.wordlist import Wordlist

        with open(args.wordlist) as data:
            wordlist = Wordlist(data)
            prev_word = None
            pos = None
            for word in wordlist.iter_all_words():
                if word.word != prev_word:
                    print("_____")
                    print(word.word)
                pos = word.pos
                print(f"pos: {word.pos}")
                print(f"  meta: {word.meta}")
                if word.forms:
                    form_str = []
                    for formtype, forms in word.forms.items():
                        for form in forms:
                            form_str.append(f"{formtype}={form}")
                    print(f"  forms: {'; '.join(form_str)}")
                if word.genders:
                    print(f"  g: {word.genders}")
                for sense in word.senses:
                    print(f"  gloss: {sense.gloss}")
                    if sense.qualifier:
                        quals = sense.qualifier.split("; ")
                        template_str = "{{lb|es|" + "|".join(quals) + "}}"
                        qual = WordlistBuilder.wiki_to_text(template_str, word.word)[1:-1]
                        print(f"    q: {qual}")
                    if sense.synonyms:
                        print(f"    syn: {'; '.join(sense.synonyms)}")

                prev_word = word.word


    if args.lang_id not in lang_ids:
        raise ValueError(f"Unknown language id: {args.lang_id}")
    lang_section = lang_ids[args.lang_id]

    if args.langdata:
        iter_data = iter_langdata(args.langdata)
    elif args.xml:
        iter_data = iter_xml(args.xml, lang_section, args.lang_id)
    else:
        print("No input file specified, use --xml or --lang-data")

    builder = WordlistBuilder(lang_section, args.lang_id)

    to_text = builder.entry_to_mbformat if args.mbformat else builder.entry_to_text

    for entry_title, lang_entry in iter_data:
        count += 1
        if count % 1000 == 0:
            print(count, file=sys.stderr, end="\r")
        if args.limit and count % args.limit == 0:
            break

        try:
            entry = to_text(lang_entry, entry_title)

        except ValueError as ex:
            print(f"{entry_title} generated an error {ex}", file=sys.stderr)
        if entry:
            entries[entry_title] = entry
        else:
            print(f"{entry_title} generated no data", file=sys.stderr)

    for title, entry in sorted(entries.items()):
        print("\n".join(entry))

    print(count, "entries processed", file=sys.stderr)

if __name__ == "__main__":
    main()
