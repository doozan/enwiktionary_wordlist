#!/usr/bin/python3

import csv
import collections
import html
import os
import re
import sys

from enwiktionary_wordlist.wordlist import Wordlist
from enwiktionary_wordlist.all_forms import AllForms

class WordlistToDictunformat():

    def __init__(self, wordlist, allforms=None):
        self.wordlist = wordlist
        self.allforms = allforms if allforms else AllForms.from_wordlist(wordlist)

    formtypes = {
        "pl": "pl",
        "m": "m",
        "mpl": "m pl",
        "f": "f",
        "fpl": "f pl",
    }

    display_gender = {
        'm': 'm',
        'f': 'f',
        'm-s': 'm',
        'f-s': 'f',
        'p': 'pl',
        'f; m': 'f or m',
        'm; f': 'm or f',
        'm; p': 'm or pl',
        'mf': 'm or f',
        'm-f': 'm or f',
        'mfbysense': 'm or f',
        'm-p': 'm pl',
        'f-p': 'f pl',
        'm-p; f-p': 'm pl or f pl',
        'f-p; m-p': 'f pl or m pl',
        '?': '?',
    }

    #'adj', 'adv', 'affix', 'art', 'conj', 'contraction', 'determiner', 'diacrit', 'interj', 'letter', 'n', 'num', 'particle', 'phrase', 'prefix', 'prep', 'pron', 'prop', 'proverb', 'punct', 'suffix', 'symbol', 'v']
    display_pos = {
        'v': 'verb',
        'n': 'noun'
    }

    def is_lemma(self, word):
        if word.meta and " form" in word.meta:
            return False
        return True

    def get_primary_word(self, words):
        """ Returns the first item in a list that is a lemma
        If nothing found, returns the first word in the list
        """
        for word in words:
            if any(self.is_lemma(w) for w in self.wordlist.get_words(word)):
                return word

        words.sort()
        return words[0]

    def format_word(self, word_obj):
        items = []
        items += self.format_header(word_obj)

        items.append('<ol style="padding:0; margin-left: 1em; margin-top: .2em; margin-bottom: 1em">\n')
        for i,sense in enumerate(word_obj.senses, 1):
            items += self.format_sense_data(i, sense)
        items.append('</ol>\n')

        if word_obj.use_notes:
            items += self.format_use_notes(word_obj.use_notes)
        items.append("")

    #    if word_obj.etymology:
    #        items.append(format_etymology(word_obj.etymology))

        return items

    def format_header(self, word_obj):
        line = [f"<b>{word_obj.word}</b>"]

        line.append(" <i>")
        line.append(self.display_pos.get(word_obj.pos, word_obj.pos))
        if word_obj.genders:
            if word_obj.genders not in self.display_gender:
                print(f"Unknown gender {word_obj.word}: '{word_obj.genders}'", file=sys.stderr)
            line.append(f", {self.display_gender.get(word_obj.genders, word_obj.genders)}")
        line.append("</i>")

        if word_obj.pos != "v" and word_obj.forms:
            form_items = []
            for formtype in self.formtypes.keys():
                forms = word_obj.forms.get(formtype)
                if forms:
                    if formtype not in self.formtypes:
                        print(f"Unknown formtype {word_obj.word}: '{formtype}'", file=sys.stderr)
                    else:
                        form_items.append(f'<i>{self.formtypes[formtype]}</i> {" <i>or</i> ".join(forms)}')

            if form_items:
                line.append(" (")
                line.append(", ".join(form_items))
                line.append(")")

        line.append("\n")

        return line

    @staticmethod
    def format_sense_data(idx, sense):

        line = [f"<li>"]
        if sense.qualifier:
            line.append(f"[<i>{sense.qualifier}</i>] ")

        line.append(html.escape(sense.gloss))

        if sense.synonyms:
            line.append('<div style="font-size: 80%">')
            line.append("Synonyms: " + "; ".join(sense.synonyms))
            line.append('</div>')
        line.append('</li>\n')

        return line

    @staticmethod
    def format_etymology(ety):
        # TODO: better formatting
        return '<p style="margin-top: 1em"><i>Etymology:</i> ' + html.escape(ety.encode('latin-1', 'backslashreplace').decode('unicode-escape')) + "</p>\n"

    @staticmethod
    def format_use_notes(usage):

        if r"\n" not in usage:
            return [f'<p style="margin-top: 1em"><i>Note:</i> {usage}</p>']

        item = [f'<p style="margin-top: 1em"><i>Note:</i> ']
        first = True
        for line in re.split(r"\\n", usage):
            if first:
                first = False
            else:
                item.append("<p>")
            item.append(f'{line.lstrip(" *#:")}</p>\n')
        return item

    def format_forms_text(self, formtype, forms):
        return self.formtypes[formtype] + ' "' + \
                '" or "'.join(forms) \
                + '"'

    @staticmethod
    def format_etymology_text(ety):
        return ety.encode('latin-1', 'backslashreplace').decode('unicode-escape')

    @staticmethod
    def format_use_notes_text(usage):
        if r"\n" not in usage:
            return "Note: " + re.sub(r"\*\s+]*","", usage)
        else:
            return "Note:\n" + re.sub(r"\\n", "\n", usage)


    @staticmethod
    def format_header_text(word_obj):
        line = [f"{word_obj.word}"]
        if word_obj.genders:
            # TODO: pretty format genders
            line.append(f" ({word_obj.pos}, {self.display_gender[word_obj.genders]})")
        else:
            line.append(f" ({word_obj.pos})")

        if word_obj.pos != "v" and word_obj.forms:
            form_items = []
            for formtype in self.formtypes.keys():
                forms = word_obj.forms.get(formtype)
                if forms:
                    form_items.append(format_forms_text(formtype, forms))

            if form_items:
                line.append(", ")
                line.append(", ".join(form_items))

        return "".join(line).strip()

    @staticmethod
    def format_sense_data_text(idx, sense):
        lines = []

        line = [f"{idx}."]
        if sense.qualifier:
            line.append("("+sense.qualifier+")")

        line.append(sense.gloss)
        lines.append(" ".join(line))

        if sense.synonyms:
            lines.append("      Synonyms: " + "; ".join(sense.synonyms))

        return "\n".join(lines)


    def format_word_text(self, word_obj):
        items = []
        items.append(self.format_header_text(word_obj))
        if word_obj.etymology:
            items.append(self.format_etymology_text(word_obj.etymology))
        for i,sense in enumerate(word_obj.senses, 1):
            items.append(self.format_sense_data_text(i, sense))
        if word_obj.use_notes:
            items.append(self.format_use_notes_text(word_obj.use_notes))
        items.append("")

        return items


    def get_word_page(self, word_obj, seen, follow_lemmas=True):

        items = []
        if not word_obj.senses:
            return []

        items += self.format_word(word_obj)

        if follow_lemmas:
            for lemma in word_obj.form_of:
                if not self.wordlist.has_word(lemma):
                    continue
                for w in self.wordlist.get_words(lemma, word_obj.pos):
                    if w not in seen:
                        seen.add(w)
                        items += self.get_word_page(w, seen, follow_lemmas=False)

        return items


    # Sort etymology groups
    #   first, etymologies containing an exact match for target
    #   second, by pos of the word matching target
    #   finally, by the text of etymology
    @staticmethod
    def sort_ety(primary, options):
        for option in options:
            if option.word == primary:
                return option.pos + "::" + (option.etymology or "")

        return 'zzz' + "::" + (options[0].etymology or "")

    def group_ety(self, primary, words):
        groups = collections.defaultdict(list)
        for word in words:
            ety = word.etymology
            groups[ety].append(word)

        return sorted(groups.values(), key=lambda x: self.sort_ety(primary, x))

    @staticmethod
    def group_pos(words):
        groups = {}
        for word in words:
            pos = word.pos
            groups[pos] = groups.get(pos, [])
            groups[pos].append(word)
        return groups

    def build_entry(self, primary, targets):
        seen = set()
        pages = []

        words = []
        for word,pos in targets:
            for w in self.wordlist.get_words(word, pos):
                if w not in seen:
                    words.append(w)
                    seen.add(w)

        etys = self.group_ety(primary, words)
        for ety_words in etys:
            for pos, pos_words in sorted(self.group_pos(ety_words).items()):
                for w in pos_words:
                    pages += self.get_word_page(w, seen)

            if ety_words[0].etymology:
                pages += self.format_etymology(ety_words[0].etymology)

        return "".join(pages).strip()


    def is_valid_target(self, word, pos):
        """ Returns true if a given word, pos is in the wordlist and 
        has a sense other than just a "form of" """
        for word in self.wordlist.get_words(word,pos):
            for sense in word.senses:
                # If a sense is just a "form of", don't include it
                if sense.formtype: # and not self.nonform:
                    continue
                return True
        return False

    def get_valid_targets(self, targets):
        """ Take a list of [ (word, pos) ] and returns the same, minus any
        entries that aren't in the wordlist or that don't contain useful information """

        valid_targets = []
        for target in targets:
            word, pos = target
            if self.is_valid_target(word, pos):
                valid_targets.append(target)

        return valid_targets


    def add_key(self, all_pages, key, targets):

        targets = self.get_valid_targets(targets)

        if not targets:
            return

        # Important to sort tagets so we can identify duplicates
        # Sort by pos, then lemma so the page is ordered nicely
        target_key = tuple(sorted((lemma,pos) for lemma,pos in targets))

        all_pages[target_key].append(key)


    def iter_allforms(self):
        line_data = []
        lemmas = []
        prev_form = None
        prev_pos = None
        for form, pos, lemma in self.allforms.all:
            if form != prev_form or pos != prev_pos:
                if lemmas:
                    yield [prev_form, prev_pos] + lemmas
                lemmas = []
            lemmas.append(lemma)
            prev_pos = pos
            prev_form = form
        yield [prev_form, prev_pos] + lemmas

    def export(self, verbose=False):

        prev_form = None
        form_targets = []

        all_pages = collections.defaultdict(list)

        form_count = 0
        for form, pos, *lemmas in self.iter_allforms():
            form_count += 1

            if form_count % 1000 == 0 and verbose:
                print(form_count, file=sys.stderr, end="\r")

            if prev_form != form:
                if prev_form:
                    self.add_key(all_pages, prev_form, form_targets)
                form_targets = [(form,pos)]

            for lemma in lemmas:
                target = (lemma, pos)
                if target not in form_targets:

                    if self.wordlist.has_word(lemma, pos):
                        form_targets.append(target)
                    else:
                        # missing entries are usually generated forms that have been removed
                        continue

            prev_form = form

        if prev_form:
            self.add_key(all_pages, prev_form, form_targets)

        yield f"##:pagecount:{len(all_pages)}\n##:formcount:{form_count}"

        count = 0
        for targets,keys in sorted(all_pages.items(), key=lambda x: self.get_primary_word(x[1])):
            count += 1
            if count % 1000 == 0 and verbose:
                print(count, file=sys.stderr, end="\r")

            primary = self.get_primary_word(keys)

            entry = self.build_entry(primary, targets)

            yield "_____"
            keys.remove(primary)

            yield ";   ".join([primary] + sorted(keys))
            yield entry
