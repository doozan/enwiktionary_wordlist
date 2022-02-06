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
from .wordlist import Wordlist

class WordlistBuilder:
    def __init__(self, lang_name, lang_id):
        self.LANG_SECTION = lang_name
        self.LANG_ID = lang_id
        self._problems = {}
        self._stats = {}
        self.fixes = set()

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

            if not senses:
                continue

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
    def word_to_text(cls, word, exclude_verb_forms):

        senses = []
        non_verbform_sense = False
        for sense in word.senses:
            if not sense.gloss:
                continue

            if exclude_verb_forms:
                if sense.nonform or not sense.formtype:
                    non_verbform_sense = True

                elif "_" not in sense.formtype and sense.formtype not in ["gerund", "infinitive", "reflexive"]:
                    non_verbform_sense = True

            s = {}
            s["gloss"] = sense.gloss
            s["q"] = sense.qualifier.rstrip(", ") if sense.qualifier else None
            s["syn"] = "; ".join(sense.synonyms) if sense.synonyms else None
            s["regional"] = "; ".join(sense.regions) if sense.regions else None
            senses.append(s)

        if not senses or exclude_verb_forms and not non_verbform_sense:
            return

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

    @classmethod
    def is_generated(cls, word, wordlist):
        """ Returns true if a word is a simple form that can be generated by the given wordlist """

        if cls.has_extra_info(word):
            return False

        for sense in word.senses:
            if not sense.formtype or sense.nonform:
                return False

            lemmas = wordlist.get_words(sense.lemma, word.pos)

            formtype = "pl" if word.pos == "adj" and sense.formtype == "mpl" else sense.formtype
            if not any(l for l in lemmas if word.word in l.forms.get(formtype, [])):
                return False

        return True


def iter_langdata(datafile):

    if not os.path.isfile(datafile):
        raise FileNotFoundError(f"Cannot open: {datafile}")

    yield from LanguageFile.iter_articles(datafile)

def iter_xml(datafile, lang_section):

    if not os.path.isfile(datafile):
        raise FileNotFoundError(f"Cannot open: {datafile}")

    dump = xmlreader.XmlDump(datafile)
    parser = dump.parse()

    langparser = LanguageFile(lang_section)

    for entry in parser:

        if ":" in entry.title or "/" in entry.title:
            continue

        lang_entry = langparser.get_language_entry(entry.text)

        if not lang_entry:
            continue

        yield entry.title, lang_entry

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Convert *nym sections to tags.")
    parser.add_argument("--xml", help="Read entries from specified wiktionary XML dump")
    parser.add_argument("--langdata", help="Read articles from specified language data file")
    parser.add_argument("--wordlist", help="Read articles from existing wordlist")
    parser.add_argument("--lang-id", help="Language id")
    parser.add_argument("--limit", help="Limit to n entries", type=int, default=0)
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--exclude-verb-forms', action='store_true', help="Exclude all verb forms")
    parser.add_argument('--exclude-generated-forms', action='store_true', help="Exclude forms entries that can be generate automatically")
    args = parser.parse_args()

    count = 0
    entries = {}

    if args.langdata or args.xml:
        if not args.lang_id:
            raise ValueError("--lang-id is required when using --xml or --langdata")

        elif args.lang_id not in lang_ids:
            raise ValueError(f"Unknown language id: {args.lang_id}")

        lang_section = lang_ids[args.lang_id]
        builder = WordlistBuilder(lang_section, args.lang_id)

        if args.langdata:
            iter_entry = iter_langdata(args.langdata)
        else:
            iter_entry = iter_xml(args.xml, lang_section)

        def _iter_entries():
            for title, entry in iter_entry:
                entry = builder.entry_to_text(entry, title)
                if not entry:
                    continue
                yield title, entry

        iter_entries = _iter_entries()

    elif args.wordlist:
        infile = open(args.wordlist)
        iter_entries = Wordlist._iter_entries(infile)

    else:
        raise ValueError("No input file specified, use --xml or --lang-data or --wordlist")

    # Build a Wordlist manually so later it can be used to validate entries
    wordlist = Wordlist()
    count = 0
    for title, entry in iter_entries:
        count += 1
        if count % 1000 == 0 and args.verbose:
            print(count, file=sys.stderr, end="\r")
        if args.limit and count >= args.limit:
            break
        wordlist.all_entries[title] = map(str.lstrip, entry)

    for word in sorted(wordlist.all_entries.keys()):
        skipped = []
        skipped_pos = None
        header = False
        for word_obj in wordlist.get_words(word):

            # Words with forms before lemmas are forms
            # eg, piernas is usually a form of pierna, not the less-frequenly used piernas
            # because its words are listed in the order (piernas, form of pierna), (piernas, lemma)
            # For these rare cases, it's important to preserve the "form of", even if it's a
            # generated form of

            if word_obj.pos != skipped_pos:
                skipped = []
                skipped_pos = word_obj.pos

            if args.exclude_generated_forms and WordlistBuilder.is_generated(word_obj, wordlist):
                skipped.append(word_obj)
                continue

            queue = skipped + [word_obj]
            skipped = []
            for word_obj in queue:
                word_lines = WordlistBuilder.word_to_text(word_obj, args.exclude_verb_forms)
                if not word_lines:
                    continue
                if not header:
                    header = True
                    print("_____")
                    print(word)
                print("\n".join(word_lines))

    print(count, "entries processed", file=sys.stderr)

if __name__ == "__main__":
    main()

