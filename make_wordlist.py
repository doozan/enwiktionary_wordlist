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
from .language_extract import LanguageFile
import re
import sys
from .utils import wiki_to_text, make_qualification, make_pos_tag

import enwiktionary_parser as wtparser
from enwiktionary_parser.languages.all_ids import languages as lang_ids
from enwiktionary_parser.sections.usage import UsageSection
from enwiktionary_parser.sections.etymology import EtymologySection

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
                    v = wiki_to_text(v, self.title)

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
        self.title = title
        wikt = wtparser.parse_page(text, title, parent=self)

        words = wikt.filter_words()
        if not words:
            return []

        entry = ["_____", title]

        for word in wikt.ifilter_words():
            #if self.exclude_word(word):
            #    continue

            entry.append(f"pos: {word.shortpos}")
            meta = " ".join(map(str,word.form_sources)).replace("\n", "")
            entry.append(f"  meta: {meta}")

            if word.genders:
                entry.append(f"  g: {'; '.join(word.genders)}")

            if word.qualifiers:
                qualifiers = make_qualification(self.LANG_ID, word.title, word.qualifiers)
                if qualifiers:
                    entry.append(f"  q: {qualifiers}")

            for usage in self.get_usage(word):
                entry.append(f"  usage: " + self.usage_to_text(usage))

            for ety in self.get_etymology(word):
                for node in ety.ifilter_etymologies():
                    ety_text = self.etymology_to_text(node)
                    if ety_text:
                        entry.append(f"  etymology: " + self.etymology_to_text(node))

            seen_senses = []
            for sense in word.ifilter_wordsenses():
                # Skip senses that are just a request for a definition
                if "{{rfdef" in sense.gloss:
                    continue
                if "{{defn" in sense.gloss:
                    continue

                gloss_text = self.gloss_to_text(sense.gloss)
                if gloss_text == "":
                    continue

                sense_data = []

                sense_data.append(f"  gloss: {gloss_text}")
                if sense.gloss.qualifiers:
                    qualifiers = make_qualification(self.LANG_ID, word.title, sense.gloss.qualifiers)
                    if qualifiers:
                        sense_data.append(f"    q: {qualifiers}")
                synonyms = []
                for nymline in sense.ifilter_nymlines(matches = lambda x: x.type == "Synonyms"):
                    synonyms += self.items_to_synonyms(nymline.items)
                if synonyms:
                    sense_data.append(f"    syn: {'; '.join(synonyms)}")

                sense_alldata = "|".join(sense_data)
                if sense_alldata in seen_senses:
                    continue
                else:
                    seen_senses.append(sense_alldata)
                    entry += sense_data

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
                pos = make_pos_tag(word, all_qualifiers)
                qualification = make_qualification(self.LANG_ID, self.title, all_qualifiers, True)

                items = [title, pos]
                if qualification:
                    items.append("["+qualification+"]")
                if synonyms:
                    items.append("|")
                    items.append("; ".join(synonyms))

                items.append("::")
                items.append(gloss_text)

                line = " ".join(items)
                entry.append(line)

        return entry

    def gloss_to_text(self, gloss):
        return re.sub(r"\s\s+", " ", wiki_to_text(gloss.data.rstrip("\r\n\t ."), self.title).strip())

    def usage_to_text(self, usage):
        text = wiki_to_text(usage, self.title).strip()
        # Strip leading * if there are no newlines
        if "\n" not in text:
            text = re.sub("^[ *#]+", "", text)
        else:
            text = re.sub("\n", r"\\n", text)
        return text

    def etymology_to_text(self, etymology):
        return re.sub("\n", r"\\n", wiki_to_text(etymology, self.title).strip())

    def items_to_synonyms(self, items):
        synonyms = []
        for item in items:
            synonym = None
            if "alt" in item:
                synonym = wiki_to_text(item["alt"], self.title).strip()
            if not synonym:
                synonym = wiki_to_text(item["target"], self.title).strip()
            if synonym:
                synonyms.append(synonym)
#           [ { "target": "word", "q": "qual" }, { "target": "word2", "tr": "tr" } ]

        return synonyms


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
    parser.add_argument('--verbose', action='store_true')
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
                        qualifiers = make_qualification(self.LANG_ID, self.title, sense.qualifier.split("; "))
                        if qualifiers:
                            print(f"    q: {qualifiers}")
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
        if count % 1000 == 0 and args.verbose:
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
