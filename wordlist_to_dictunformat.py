#!/usr/bin/python3

import argparse
import os
import re
import sys

from .wordlist import Wordlist

wordlist = None
all_pages = {}

formtypes = {
    "pl": "plural",
    "m": "masculine",
    "mpl": "masculine plural",
    "f": "feminine",
    "fpl": "feminine plural"
}

def format_forms(formtype, forms):
    return formtypes[formtype] + ' "' + \
            '" or "'.join(forms) \
            + '"'

def get_word_header(word_obj):
    line = [f"{word_obj.word} ({word_obj.pos})"]

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
    for word_obj in wordlist.all_words.get(word,{}).get(pos,[]):
        if not word_obj.senses:
            continue

        items.append(get_word_header(word_obj))
        for i,sense in enumerate(word_obj.senses, 1):
            items.append(get_sense_data(i, sense))
        items.append("")

        if not recursive:
            for lemma in word_obj.form_of:
                if lemma not in wordlist.all_words:
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

all_pages = {}
def add_key(key, targets):
    if targets not in all_pages:
        all_pages[targets] = {
            "keys": [key],
            "data": build_page(targets)
        }
    else:
        if key not in all_pages[targets]["keys"]:
            all_pages[targets]["keys"].append(key)

def export(data, langid, description):

    global wordlist
    wordlist = Wordlist(data)

    disambig = set()
    ambig_forms = 0
    for form, lemmas in wordlist.all_forms.items():
        form_targets = set()
        for pos,lemma,formtype in [x.split(":") for x in sorted(lemmas)]:
            form_targets.add((lemma,pos))

        if len(form_targets) > 1:
            ambig_forms += 1
            disambig.add(tuple(sorted(form_targets)))
        add_key(form, tuple(sorted(form_targets)))

    name = "Wiktionary"
    if langid != "en":
        name += f" ({langid}-en)"

    yield f"""\
_____
00-database-info
##:name:{name}
##:url:en.wiktionary.org
##:pagecount:{len(all_pages)}
##:formcount:{len(wordlist.all_forms)}
##:description:{description}\
"""
    for pagename,page in sorted(all_pages.items()):
        yield "_____"
        yield "|".join(page["keys"])
        yield page["data"]

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description="Convert wordlist to dictunformat")
    parser.add_argument("wordlist", help="wordlist")
    parser.add_argument("--lang-id", help="language id")
    parser.add_argument("--description", help="description", default="")
    args = parser.parse_args()

    with open(args.wordlist) as infile:
        for line in export(infile, args.lang_id, args.description):
            print(line)
