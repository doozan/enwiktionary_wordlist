#!/usr/bin/python3
#
# Copyright (c) 2020-2025 Jeff Doozan
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
import copy
import os
import re
import sys

import enwiktionary_sectionparser as sectionparser
from autodooz.sections import ALL_POS, COUNTABLE_SECTIONS, ALL_LANGS

import mwparserfromhell as mwparser

from enwiktionary_wordlist.utils import wiki_to_text, make_pos_tag

class WordlistBuilder:
    def __init__(self, lang_name, lang_id, transcludes_filename=None, expand_templates=False, generate_meta=False):
        self.LANG_SECTION = lang_name
        self.LANG_ID = lang_id
        self._expand_templates = expand_templates
        self._generate_meta = generate_meta

        self._transclude_senses = {}
        if transcludes_filename:
            with open(transcludes_filename) as infile:
                for l in infile:
                    word, senseid, _, sense = l.split(":", 3)
                    self._transclude_senses[(word,senseid)] = sense.strip()

        start = fr"(^|\n)==\s*{self.LANG_SECTION}\s*==\s*\n"
        re_endings = [ r"\[\[\s*Category\s*:", r"==[^=]+==", r"----" ]
        #template_endings = [ "c", "C", "top", "topics", "categorize", "catlangname", "catlangcode", "cln", "DEFAULTSORT" ]
        template_endings = [ "top", "topics", "categorize", "catlangname", "catlangcode", "DEFAULTSORT" ]
        re_endings += [ r"\{\{\s*"+item+r"\s*\|" for item in template_endings ]
        endings = "|".join(re_endings)
        newlines = r"(\n\s*){1,2}"
        pattern = fr"{start}.*?(?={newlines}({endings})|$)"
        self._re_pattern = re.compile(pattern, re.DOTALL)

    @staticmethod
    def get_child_or_later_peer(section, title):
        child = next(section.ifilter_sections(matches=lambda x: x.title == title), None)
        if child:
            return child

        after = False
        for peer in section.parent.ifilter_sections(recursive=False):
            if after:
                if peer.title == title:
                    return peer
            elif peer == section:
                after = True


    @staticmethod
    def get_ancestor_or_preceeding_peer(section, title):
        ancestor = section
        while hasattr(ancestor, "parent"):
            ancestor = ancestor.parent
            if ancestor.title == title:
                return ancestor

        matched = None
        for peer in section.parent.ifilter_sections(recursive=False):
            if peer.title == title:
                matched = peer
            if peer == section:
                return matched

        raise ValueError("this should never happen", title, section.path)



    @staticmethod
    def get_indtr_qualifiers(t):
        types = {
            "intr": "intransitive",
            "ditr": "ditransitive",
            "cop": "copulative",
            "aux": "auxiliary",
        }
        q = [ str(v) for k,v in types.items() if t.has(k) ]
        if not q:
            q = [ "transitive" ]

        return q

    _sense_ids = { "senseid", "sid" }
    _anchors = { "anchor", "s", "senseid" }
    _labels = { "label", "lb", "lbl", "term-label" }
    _indtr = { "indtr" }
    _categories = { "c", "C", "cat", "top", "topic", "topics", "categorize", "catlangname", "catlangcode", "cln", "DEFAULTSORT" }
    _all_leading_templates = _anchors | _labels | _indtr | _categories
    _re_templates = "|".join(map(re.escape, _all_leading_templates))
    _leading_template_pattern = r'\s*{{\s*(' + _re_templates + r')\s*\|'

    @staticmethod
    def get_label_qualifiers(t):
        return [ str(p) for p in t.params if p.name != "1" and str(p.name).isdigit() ]

    def extract_qualifiers(self, text):
        """Process leading anchor and label templates

        Returns [[qualifiers]], remainder of line"""

        if not text.lstrip().startswith("{{"):
            return [], text

        qualifiers = []

        wiki = mwparser.parse(text)
        templates = wiki.ifilter_templates()

        to_remove = []
        t = next(templates)
        # while the gloss line starts with known qualifier templates, extract them one-by-one
        while t and str(wiki).lstrip(": ").startswith(str(t)):
            t_name = t.name.strip()

            if t_name in self._labels:
                qualifiers += self.get_label_qualifiers(t)

            # Scrape basic verb qualifiers from indtr, but don't parse/strip them
            elif t_name in self._indtr:
                qualifiers += self.get_indtr_qualifiers(t)

            elif t_name in self._all_leading_templates:
                test = True

            else:
                break

            wiki.remove(t)
            t = next(templates, None)

        return qualifiers, str(wiki).lstrip(": ")

    def get_term_qualifiers(self, pos):
        wiki = mwparser.parse("\n".join(pos.headlines))
        qualifiers = []
        for t in wiki.filter_templates(recursive=False, matches=lambda x: x.name.strip() in ["tlb", "term label", "term-label"]):
             qualifiers += self.get_label_qualifiers(t)
        return qualifiers

    def gloss_to_text(self, wikitext, title):
        text = self.expand_templates(wikitext, title)
        text = text.strip().rstrip(".")
        text = re.sub(r"\s\s+", " ", text)
        text = re.sub("\n", r"\\n", text)
        return text

    def get_sense_id(self, text):
        ids = []
        if any(x in text for x in ["{{senseid|", "{{sid|"]):
            wikt = mwparser.parse(text)
            for t in wikt.ifilter_templates(matches=lambda x: x.name in ["senseid", "sid"]):
                ids.append(str(t.get(2).value))
        return "; ".join(ids)

    def get_sense_data(self, sense, title):
        sense_data = {}

        qualifiers, gloss_wikitext = self.extract_qualifiers(sense.data)
        sense_data["gloss"] = self.gloss_to_text(gloss_wikitext, title)
        sense_id = self.get_sense_id(sense.data)
        if sense_id:
            sense_data["id"] = sense_id

        if qualifiers:
            qualifier = self.get_qualifier(title, qualifiers)
            if qualifier:
                qualifier = qualifier.rstrip(", ")
                sense_data["q"] = qualifier

        for nymtype in ["syn"]:
            nyms = "; ".join(self.expand_templates(c.data, title) for c in sense._children if c._type == nymtype or (c._type == "unknown" and "{{" + nymtype in c.data))
            if nyms:
                sense_data[nymtype] = nyms

        subsenses = [self.get_sense_data(c, title) for c in sense._children if c._type == "sense" or (c._type == "unknown" and c.prefix == "##")]
        if subsenses:
            sense_data["subsenses"] = subsenses

        return sense_data


    def entry_to_text(self, text, title):
        parsed = sectionparser.parse(text, title)
        if not parsed:
            print("unparsable page:", title, file=sys.stderr)
            log = []
            parsed = sectionparser.parse(text, title, log)
            print(log, file=sys.stderr)
            print(parsed._state, file=sys.stderr)
            return

        entry = []

        for section in parsed.ifilter_sections(matches=lambda x: x.title in ALL_POS):
            pos = sectionparser.parse_pos(section)
            if not pos:
                print("unparsable section:", section.path, file=sys.stderr)
                continue

            # TODO: get qualifiers from tlb
            # {{tlb|es|siglum}}
            term_qualifiers = self.get_qualifier(title, self.get_term_qualifiers(pos))

            senses = []
            for sense in pos.senses:

                # Skip senses that are just a request for a definition
                if "{{rfdef" in sense.data:
                    continue
                if "{{defn" in sense.data:
                    continue

                sense_data = self.get_sense_data(sense, title)
                if sense_data and sense_data.get("gloss") and sense_data not in senses:
                    senses.append(sense_data)


            usages = []
            usage = self.get_child_or_later_peer(section, "Usage notes")
            if usage:
                usage_text = self.usage_to_text(usage, title)
                if usage_text:
                    usages.append(usage_text)


            etys = []
            ety = self.get_ancestor_or_preceeding_peer(section, "Etymology")
            if ety:
                ety_text = self.etymology_to_text(ety, title)
                if ety_text:
                    etys.append(ety_text)

            meta = self.get_meta(pos)
            genders = self.get_genders(pos)
            short_pos = self.get_shortpos(pos)

            #qualifier = self.get_qualifier(title, word.qualifiers)
            entry += self.make_word_entry(
                pos = short_pos,
                meta = meta,
                genders = "; ".join(genders) if genders else None,
                qualifier = term_qualifiers,
                usages = usages,
                etys =  etys,
                senses = senses,
            )

        return entry

    def get_qualifier(self, title, qualifiers, strip_verb_qualifiers=False):
        """ Convert a list of qualifiers to label """

        if not qualifiers:
            return ""
        if not self._expand_templates:
            return ", ".join(qualifiers)


        if strip_verb_qualifiers:
            pos, qualifiers = extract_verb_qualifiers(qualifiers)

        template_str = "{{label|" + self.LANG_ID + "|" + "|".join(qualifiers) + "}}"
        qualified = wiki_to_text(template_str, title)
        if not qualified:
            return ""

        # Strip ()
        return qualified[1:-1]


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

        def add_sense_data(sense_data, depth=1):
            padding = "  " * depth
            prefix = "_" * (depth-1)
            for k,v in sense_data.items():
                if not v:
                    continue
                if k == "subsenses":
                    for subsense in v:
                        add_sense_data(subsense, depth+1)
                elif k.lstrip("_") == "gloss":
                    word_entry.append(f"{padding}{prefix}gloss: {v}")
                else:
                    word_entry.append(f"{padding}  {k}: {v}")

        for sense_data in senses:
            add_sense_data(sense_data)

        return word_entry

    def expand_templates(self, text, title):
        if not self._expand_templates:
            return text.strip()
        return wiki_to_text(text, title, transclude_senses=self._transclude_senses).strip()

    def usage_to_text(self, usage, title):
        text = self.expand_templates(usage.content_text, title)
        # Strip leading * if there are no newlines
        if "\n" not in text:
            text = re.sub("^[ *#]+", "", text)
        else:
            text = re.sub("\n", r"\\n", text)
        return text

    def etymology_to_text(self, etymology, title):
        text = self.expand_templates(etymology.content_text, title).strip()
        text = re.sub("\n", r"\\n", text)
        if text == ".":
            return ""
        return text


    @classmethod
    def word_to_text(cls, word):

        non_verbform_sense = False

        word_entry = {}

        def make_sense_data(sense):

            if not sense.gloss:
                raise ValueError("Bad gloss")

            s = {}
            s["gloss"] = sense.gloss
            s["id"] = sense.id
            s["q"] = sense.qualifier.rstrip(", ") if sense.qualifier else None
            # TODO
            #s["usage"] = sense.usage
            #s["ex"] = sense.ex
            for nym in ["ant", "syn"]:
                nyms = []
                for n in sense.nyms:
                    if n[0] == nym:
                        nyms += n[2]
                # TODO: add qualifier, or just skip this if not used by make_word_entry?
                s[nym] = "; ".join(nyms) if nyms else None
            s["regional"] = "; ".join(sense.regions) if sense.regions else None

            subsenses = []
            for subsense in sense.subsenses:
                subsenses.append(make_sense_data(subsense))
            s["subsenses"] = subsenses if subsenses else None

            return s

        senses = []
        for sense in word.senses:
            senses.append(make_sense_data(sense))

        word_lines = cls.make_word_entry(
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


    #### Language-specific stuff than should be abstracted/overridden

    @staticmethod
    def get_headline_templates(pos):
        wiki = mwparser.parse("\n".join(pos.headlines))
        return wiki.filter_templates(recursive=False, matches=lambda x: x.name not in ["es-card", "es-suffix form"] and (x.name.startswith("es-") or x.name in ["head", "head-lite"]))


    def get_meta(self, pos):
        templates = self.get_headline_templates(pos)

        extra = []
        if any("es-verb" in t.name for t in templates):
            for child in pos.section.ifilter_sections(recursive=True, matches=lambda x: x.title == "Conjugation"):
                extra += re.findall("{{es-conj.*?}}", child.content_text)

            # If the word doesn't explicitly include a call to es-conj, generate one from the es-verb
            if not extra and self._generate_meta:
                for t in templates:
                    if "es-verb" in t.name and all(p.name in [1, "1", "head"] for p in t.params):
                        new_t = copy.deepcopy(t)
                        new_t.name = "es-conj"
                        extra.append(str(new_t))

        res = []
        for item in templates + extra:
            item = str(item)
            if item not in res:
                res.append(item)

        return " ".join(res)

    @classmethod
    def get_verb_form_sources(cls, word):
        if not word or not word.headword:
            return []
        conj_templates = list(cls.get_conjugation_templates(word))

        # If the word doesn't explicitly include a call to es-conj, generate one from the es-verb
        if not conj_templates and word.headword.name == "es-verb":
            if not all(p.name in ["1"] for p in word.headword.params):
                print(word.headword, file=sys.stderr)
                print(word.headword.params, file=sys.stderr)
                print([p.name for p in word.headword.params], file=sys.stderr)
            else:
                conj_template = copy.deepcopy(word.headword)
                conj_template.name = "es-conj"
                conj_templates = [conj_template]
        return [word.headword] + conj_templates

    @classmethod
    def get_conjugation_templates(cls, word):
        """ Find all conjugation templates for word """

        # Find the nearest ancestor with a Conjugation section
        matcher = lambda x: callable(getattr(x, "filter_sections", None)) and \
                any(x.filter_sections(matches=lambda y: y.name.strip().startswith("Conjugation")))
        ancestor = word.get_matching_ancestor(matcher)
        if not ancestor:
            if " " not in word.page_title and not word.page_title.endswith("se"):
                print("No conjugations", word.page_title, file=sys.stderr)
            return []

        for conjugation in ancestor.ifilter_sections(matches=lambda x: x.name.strip().startswith("Conjugation")):
            for t in conjugation.ifilter_templates(matches=lambda x: x.name.strip().startswith("es-conj")):
                yield t

                #meta = " ".join(map(str,word.form_sources)).replace("\n", ""),
        return

    def get_shortpos(self, pos):
        # TODO: separate to manual overrides
        if pos.section.title == "Participle":
            return "part"
        return ALL_POS.get(pos.section.title, pos.section.title)

    # TODO: make this generic / overrideable
    def get_genders(self, section):
        return self.spanish_get_genders(section)


    spanish_gender_sources = {
        "head": {
            "g": ["g", "gen", "g1"],
            "g2": ["g2"],
            "g3": ["g3"],
        },
        "es-noun": {
            "g": ["1", "g", "gen", "g1"],
            "g2": ["g2"],
            "g3": ["g3"],
        },
        "es-proper noun": {
            "g": ["1", "g", "gen", "g1"],
            "g2": ["g2"],
            "g3": ["g3"],
        },
        "es-proper-noun": {
            "g": ["1", "g", "gen", "g1"],
            "g2": ["g2"],
            "g3": ["g3"],
        },
    }

    def spanish_get_genders(self, pos):
        templates = self.get_headline_templates(pos)
        res = {}
        for template in templates:
            sources = self.spanish_gender_sources.get(str(template.name))
            if not sources:
                continue

            for k,params in sources.items():
                for param in params:
                    if template.has(param):
                        res[k] = res.get(k, []) + [str(template.get(param).value)]

        return [ v[0] for v in res.values() ]
