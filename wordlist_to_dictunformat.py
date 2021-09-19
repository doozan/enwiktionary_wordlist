#!/usr/bin/python3

import csv
import collections
import os
import re
import sys

from .wordlist import Wordlist
from .all_forms import AllForms

wordlist = None

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

def format_etymology(ety):
    return ety.encode('latin-1', 'backslashreplace').decode('unicode-escape')

def format_use_notes(usage):
    if r"\n" not in usage:
        return "Note: " + re.sub(r"\*\s+]*","", usage)
    else:
        return "Note:\n" + re.sub(r"\\n", "\n", usage)

def get_first_lemma(words):
    """ Returns the first item in a list that is a lemma """
    for word in words:
        if wordlist.has_lemma(word):
            return word

def get_word_header(word_obj):
    line = [f"{word_obj.word}"]
    if word_obj.genders:
        # TODO: pretty format genders
        line.append(f" ({word_obj.pos}, {word_obj.genders})")
        #line.append(f" ({word_obj.pos}, {word_obj.genders})")
    else:
        line.append(f" ({word_obj.pos})")

    if word_obj.pos != "v" and word_obj.forms:
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
        if word_obj.etymology:
            items.append(format_etymology(word_obj.etymology))
        for i,sense in enumerate(word_obj.senses, 1):
            items.append(get_sense_data(i, sense))
        if word_obj.use_notes:
            items.append(format_use_notes(word_obj.use_notes))
        items.append("")

        if not recursive:
            for lemma in word_obj.form_of:
                if not wordlist.has_word(lemma):
                    continue
                lemma_data = get_word_page(seen, lemma, pos, recursive=True)
                if lemma_data:
                    items.append(lemma_data)

    return "\n".join(items).strip()

def build_entry(targets):
    seen = set()
    pages = []

    for pos,word in targets:
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


def add_key(all_pages, key, targets):

    targets = get_valid_targets(targets)

    if not targets:
        return

    # Important to sort tagets so we can identify duplicates
    # Sort by pos, then lemma so the page is ordered nicely
    #target_key = ";".join([f"{pos}:{lemma}" for lemma,pos in sorted(targets)])
    target_key = ";".join([f"{pos}:{lemma}" for lemma,pos in sorted(targets, key=lambda x: (x[1], x[0]))])

    all_pages[target_key].append(key)


def iter_allforms(allforms_data, wordlist):
    """ if allforms_data is supplied, treat it as a csv
    otherwise, generate all_forms from wordlist """

    if allforms_data:
        yield from csv.reader(allforms_data)
    else:
        all_forms = AllForms.from_wordlist(wordlist)

        for form, poslemmas in all_forms.all_forms.items():
            data = collections.defaultdict(list)
            for poslemma in poslemmas:
                pos, lemma = poslemma.split("|")
                data[pos].append(lemma)

            for pos, lemmas in data.items():
                yield [form, pos] + lemmas


def export(wordlist_data, allforms_data, langid, description, low_memory=False, verbose=False):

    cache_words = not low_memory
    global wordlist
    wordlist = Wordlist(wordlist_data, cache_words)

    print("start memory", mem_use(), file=sys.stderr)

    prev_form = None
    form_targets = []

    all_pages = collections.defaultdict(list)

    form_count = 0
    for form, pos, *lemmas in iter_allforms(allforms_data, wordlist):
        form_count += 1

        if form_count == 1:
            print("loop memory", mem_use(), file=sys.stderr)
        if form_count % 1000 == 0 and verbose:
            print(form_count, mem_use(), file=sys.stderr, end="\r")

        if prev_form != form:
            if prev_form:
                add_key(all_pages, prev_form, form_targets)
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

                    raise ValueError("entry not found")

        prev_form = form

    if prev_form:
        add_key(all_pages, prev_form, form_targets)

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

    count = 0
    for targets,keys in sorted(all_pages.items()):
        count += 1
        if count % 1000 == 0 and verbose:
            print(count, mem_use(), file=sys.stderr, end="\r")

        entry = build_entry([t.split(":") for t in targets.split(";")])

        yield "_____"
        lemma = get_first_lemma(keys)
        if lemma:
            keys.remove(lemma)
        else:
            keys.sort()
            lemma = keys.pop(0)

        yield "|".join([lemma] + sorted(keys))
        yield entry

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description="Convert wordlist to dictunformat")
    parser.add_argument("wordlist", help="wordlist")
    parser.add_argument("allforms", help="all_forms csv file")
    parser.add_argument("--lang-id", help="language id")
    parser.add_argument("--description", help="description", default="")
    parser.add_argument("--low-mem", help="Optimize for low memory devices", default=False, action='store_true')
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()

    wordlist_data = open(args.wordlist)
    if args.allforms:
        allforms_data = open(args.allforms)

    for line in export(wordlist_data, allforms_data, args.lang_id, args.description, args.low_mem, args.verbose):
        print(line)

    wordlist_data.close()
    if args.allforms:
        allforms_data.close()
