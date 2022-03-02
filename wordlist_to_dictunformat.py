#!/usr/bin/python3

import csv
import collections
import html
import os
import re
import sys

from .wordlist import Wordlist
from .all_forms import AllForms

wordlist = None

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

def mem_use():
    with open('/proc/self/status') as f:
        memusage = f.read().split('VmRSS:')[1].split('\n')[0][:-3]

    return int(memusage.strip())


def is_lemma(word):
    if word.meta and " form" in word.meta:
        return False
    return True

def get_primary_word(words):
    """ Returns the first item in a list that is a lemma
    If nothing found, returns the first word in the list
    """
    for word in words:
        if any(is_lemma(w) for w in wordlist.get_words(word)):
            return word

    words.sort()
    return words[0]

def format_word(word_obj):
    items = []
    items += format_header(word_obj)

    items.append('<ol style="padding:0; margin-left: 1em; margin-top: .2em; margin-bottom: 1em">\n')
    for i,sense in enumerate(word_obj.senses, 1):
        items += format_sense_data(i, sense)
    items.append('</ol>\n')

    if word_obj.use_notes:
        items += format_use_notes(word_obj.use_notes)
    items.append("")

#    if word_obj.etymology:
#        items.append(format_etymology(word_obj.etymology))

    return items

def format_header(word_obj):
    line = [f"<b>{word_obj.word}</b>"]

    line.append(" <i>")
    line.append(display_pos.get(word_obj.pos, word_obj.pos))
    if word_obj.genders:
        if word_obj.genders not in display_gender:
            print(f"Unknown gender {word_obj.word}: '{word_obj.genders}'", file=sys.stderr)
        line.append(f", {display_gender.get(word_obj.genders, word_obj.genders)}")
    line.append("</i>")

    if word_obj.pos != "v" and word_obj.forms:
        form_items = []
        for formtype in formtypes.keys():
            forms = word_obj.forms.get(formtype)
            if forms:
                if formtype not in formtypes:
                    print(f"Unknown formtype {word_obj.word}: '{formtype}'", file=sys.stderr)
                else:
                    form_items.append(f'<i>{formtypes[formtype]}</i> {" <i>or</i> ".join(forms)}')

        if form_items:
            line.append(" (")
            line.append(", ".join(form_items))
            line.append(")")

    line.append("\n")

    return line

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

def format_etymology(ety):
    # TODO: better formatting
    return '<p style="margin-top: 1em"><i>Etymology:</i> ' + html.escape(ety.encode('latin-1', 'backslashreplace').decode('unicode-escape')) + "</p>\n"

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

def format_forms_text(formtype, forms):
    return formtypes[formtype] + ' "' + \
            '" or "'.join(forms) \
            + '"'

def format_etymology_text(ety):
    return ety.encode('latin-1', 'backslashreplace').decode('unicode-escape')

def format_use_notes_text(usage):
    if r"\n" not in usage:
        return "Note: " + re.sub(r"\*\s+]*","", usage)
    else:
        return "Note:\n" + re.sub(r"\\n", "\n", usage)


def format_header_text(word_obj):
    line = [f"{word_obj.word}"]
    if word_obj.genders:
        # TODO: pretty format genders
        line.append(f" ({word_obj.pos}, {display_gender[word_obj.genders]})")
    else:
        line.append(f" ({word_obj.pos})")

    if word_obj.pos != "v" and word_obj.forms:
        form_items = []
        for formtype in formtypes.keys():
            forms = word_obj.forms.get(formtype)
            if forms:
                form_items.append(format_forms_text(formtype, forms))

        if form_items:
            line.append(", ")
            line.append(", ".join(form_items))

    return "".join(line).strip()

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


def format_word_text(word_obj):
    items = []
    items.append(format_header_text(word_obj))
    if word_obj.etymology:
        items.append(format_etymology_text(word_obj.etymology))
    for i,sense in enumerate(word_obj.senses, 1):
        items.append(format_sense_data_text(i, sense))
    if word_obj.use_notes:
        items.append(format_use_notes_text(word_obj.use_notes))
    items.append("")

    return items


def get_word_page(word_obj, seen, follow_lemmas=True):

    items = []
    if not word_obj.senses:
        return []

    items += format_word(word_obj)

    if follow_lemmas:
        for lemma in word_obj.form_of:
            if not wordlist.has_word(lemma):
                continue
            for w in wordlist.get_words(lemma, word_obj.pos):
                if w not in seen:
                    seen.add(w)
                    items += get_word_page(w, seen, follow_lemmas=False)

    return items


# Sort etymology groups
#   first, etymologies containing an exact match for target
#   second, by pos of the word matching target
#   finally, by the text of etymology

def sort_ety(primary, options):
    for option in options:
        if option.word == primary:
            return option.pos + "::" + (option.etymology or "")

    return 'zzz' + "::" + (options[0].etymology or "")

def group_ety(primary, words):
    groups = collections.defaultdict(list)
    for word in words:
        ety = word.etymology
        groups[ety].append(word)

    return sorted(groups.values(), key=lambda x: sort_ety(primary, x))

def group_pos(words):
    groups = {}
    for word in words:
        pos = word.pos
        groups[pos] = groups.get(pos, [])
        groups[pos].append(word)
    return groups

def build_entry(primary, targets):
    seen = set()
    pages = []

    words = []
    for pos,word in targets:
        for w in wordlist.get_words(word, pos):
            if w not in seen:
                words.append(w)
                seen.add(w)

    etys = group_ety(primary, words)
    for ety_words in etys:
        for pos, pos_words in sorted(group_pos(ety_words).items()):
            for w in pos_words:
                pages += get_word_page(w, seen)

        if ety_words[0].etymology:
            pages += format_etymology(ety_words[0].etymology)

    return "".join(pages).strip()


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
        allforms = AllForms.from_wordlist(wordlist)

        line_data = []
        lemmas = []
        prev_form = None
        prev_pos = None
        for form, pos, lemma in sorted(allforms.all):
            if form != prev_form or pos != prev_pos:
                if lemmas:
                    yield [prev_form, prev_pos] + lemmas
                lemmas = []
            lemmas.append(lemma)
            prev_pos = pos
            prev_form = form
        yield [prev_form, prev_pos] + lemmas

    return

def export(wordlist_data, allforms_data, low_memory=False, verbose=False):

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

    yield f"##:pagecount:{len(all_pages)}\n##:formcount:{form_count}"


    count = 0
    for targets,keys in sorted(all_pages.items(), key=lambda x: get_primary_word(x[1])):
        count += 1
        if count % 1000 == 0 and verbose:
            print(count, mem_use(), file=sys.stderr, end="\r")

        primary = get_primary_word(keys)
        entry = build_entry(primary, [t.split(":") for t in targets.split(";")])

        yield "_____"
        keys.remove(primary)

        yield "|".join([primary] + sorted(keys))
        yield entry

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description="Convert wordlist to dictunformat")
    parser.add_argument("wordlist", help="wordlist")
    parser.add_argument("allforms", help="all_forms csv file")
    parser.add_argument("--name", help="dictionary name", required=True)
    parser.add_argument("--from-lang-id", help="from language id", required=True)
    parser.add_argument("--to-lang-id", help="to language id", required=True)
    parser.add_argument("--description", help="description", default="", required=True)
    parser.add_argument("--url", help="source url")
    parser.add_argument("--low-mem", help="Optimize for low memory devices", default=False, action='store_true')
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()

    wordlist_data = open(args.wordlist)
    if args.allforms:
        allforms_data = open(args.allforms)

    name = f"{args.name} ({args.from_lang_id}-{args.to_lang_id})"

    print("_____")
    print("00-database-info")
    print(f"##:name:{name}")
    if args.url:
        print(f"##:url:{args.url}")
    if args.description:
        print(f"##:description:{args.description}")

    for line in export(wordlist_data, allforms_data, args.low_mem, args.verbose):
        print(line)

    wordlist_data.close()
    if args.allforms:
        allforms_data.close()
