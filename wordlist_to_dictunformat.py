#!/usr/bin/python3

import csv
import os
import re
import sys

from .wordlist import Wordlist
from .all_forms import AllForms

wordlist = None
all_pages = {}

formtypes = {
    "pl": "plural",
    "m": "masculine",
    "mpl": "masculine plural",
    "f": "feminine",
    "fpl": "feminine plural"
}

def mem_use():
    with open('/proc/self/status') as f:
        memusage = f.read().split('VmRSS:')[1].split('\n')[0][:-3]

    return int(memusage.strip())

def format_forms(formtype, forms):
    return formtypes[formtype] + ' "' + \
            '" or "'.join(forms) \
            + '"'

def get_word_header(word_obj):
    line = [f"{word_obj.word}"]
    if word_obj.genders:
        # TODO: pretty format genders
        line.append(f" ({word_obj.pos}, {word_obj.genders})")
        #line.append(f" ({word_obj.pos}, {word_obj.genders})")
    else:
        line.append(f" ({word_obj.pos})")

    if word_obj.forms:
        form_items = []
        for formtype in formtypes.keys():
            forms = word_obj.forms.get(formtype)
            if forms:
                form_items.append(format_forms(formtype, forms))

        if form_items:
            line.append(", ")
            line.append(", ".join(form_items))

    return "".join(line).strip()

def get_sense_data(idx, sense):
    lines = []

    line = [f"{idx}."]
    if sense.qualifier:
        line.append("("+sense.qualifier+")")

    line.append(sense.gloss)
    lines.append(" ".join(line))

    if sense.synonyms:
        lines.append("      Synonyms: " + "; ".join(sense.synonyms))

    return "\n".join(lines)


def get_word_page(seen, word, pos, recursive=False):
    if (word,pos) in seen:
        return
    seen.add((word,pos))

    items = []
    for word_obj in wordlist.get_words(word, pos):
        if not word_obj.senses:
            continue

        items.append(get_word_header(word_obj))
        for i,sense in enumerate(word_obj.senses, 1):
            items.append(get_sense_data(i, sense))
        items.append("")

        if not recursive:
            for lemma in word_obj.form_of:
                if not wordlist.has_word(lemma):
                    continue
                lemma_data = get_word_page(seen, lemma, pos, recursive=True)
                if lemma_data:
                    items.append(lemma_data)

    return "\n".join(items).strip()

def build_page(targets):
    seen = set()
    pages = []
    for word,pos in targets:
        page = get_word_page(seen, word, pos)
        if page:
            pages.append(page)
    return "\n\n".join(pages)


def is_valid_target(word, pos):
    """ Returns true if a given word, pos is in the wordlist and 
    has a sense other than just a "form of" """
    for word in wordlist.get_words(word,pos):
        for sense in word.senses:
            # If a sense is just a "form of", don't include it
            if sense.formtype: # and not self.nonform:
                continue
            return True
    return False

def get_valid_targets(targets):
    """ Take a list of [ (word, pos) ] and returns the same, minus any
    entries that aren't in the wordlist or that don't contain useful information """

    valid_targets = []
    for target in targets:
        word, pos = target
        if is_valid_target(word, pos):
            valid_targets.append(target)

    return valid_targets


all_pages = {}
def add_key(key, targets):

    targets = get_valid_targets(targets)

    if not targets:
        return

    target_key = ";".join([f"{lemma}:{pos}" for lemma,pos in sorted(targets)])

    if target_key not in all_pages:
        all_pages[target_key] = set([key])
    else:
        all_pages[target_key].add(key)


def iter_allforms(allforms_data, wordlist):
    """ if allforms_data is supplied, treat it as a csv
    otherwise, generate all_froms from wordlist """

    if allforms_data:
        yield from csv.reader(allforms_data)
    else:
        all_forms = AllForms.from_wordlist(wordlist)

        for form, poslemmas in all_forms.all_forms.items():
            data = {}
            for poslemma in poslemmas:
                pos, lemma = poslemma.split("|")
                if pos not in data:
                    data[pos] = [lemma]
                elif lemma not in data[pos]:
                    data[pos].append(lemma)

            for pos, lemmas in data.items():
                yield [form, pos] + lemmas


def export(wordlist_data, allforms_data, langid, description, low_memory=False):

    cache_words = not low_memory
    global wordlist
    wordlist = Wordlist(wordlist_data, cache_words)

    print("start memory", mem_use(), file=sys.stderr)

    prev_form = None
    form_targets = []

    form_count = 0
    for form, pos, *lemmas in iter_allforms(allforms_data, wordlist):
        form_count += 1

        if form_count == 1:
            print("loop memory", mem_use(), file=sys.stderr)
        if form_count % 1000 == 0:
            print(form_count, file=sys.stderr, end="\r")

        if prev_form != form:
            if prev_form:
                add_key(prev_form, form_targets)
            form_targets = [(form,pos)]

        for lemma in lemmas:
            target = (lemma, pos)
            if target not in form_targets:

                if wordlist.has_word(lemma, pos):
                    form_targets.append(target)
                else:
                    print(form,lemma,pos,"not found in db", file=sys.stderr)
                    if not wordlist.has_word(lemma):
                        print("XXX", form,lemma,pos,"not found in db", file=sys.stderr)
                    else:
                        print("XXX", lemma, "is found in db", file=sys.stderr)
                        for word in wordlist.get_words(lemma):
                            print(word.word, word.pos, file=sys.stderr)

                        exit()

        prev_form = form

    if prev_form:
        add_key(prev_form, sorted(form_targets))

    print("dumping memory", mem_use(), file=sys.stderr)

    name = "Wiktionary"
    if langid != "en":
        name += f" ({langid}-en)"

    yield f"""\
_____
00-database-info
##:name:{name}
##:url:en.wiktionary.org
##:pagecount:{len(all_pages)}
##:formcount:{form_count}
##:description:{description}\
"""

    first = True
    for targets,keys in sorted(all_pages.items()):

        #tgs =[t.split(":") for t in targets.split(";")]
        #print(targets, tgs, keys, file=sys.stderr)
        entry = build_page([t.split(":") for t in targets.split(";")])

        if first:
            print("sorted memory", mem_use(), file=sys.stderr)
            first = False

        yield "_____"
        yield "|".join(sorted(keys))
        yield entry

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description="Convert wordlist to dictunformat")
    parser.add_argument("wordlist", help="wordlist")
    parser.add_argument("allforms", help="all_forms csv file")
    parser.add_argument("--lang-id", help="language id")
    parser.add_argument("--description", help="description", default="")
    args = parser.parse_args()

    wordlist_data = open(args.wordlist)
    if args.allforms:
        allforms_data = open(args.allforms)

    for line in export(wordlist_data, allforms_data, args.lang_id, args.description):
        print(line)

    wordlist_data.close()
    if args.allforms:
        allforms_data.close()
