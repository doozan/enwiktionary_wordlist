#!/usr/bin/python3

import argparse
import json
import sys
from wordlist import Wordlist

def export(data, lemmas=False, json=False):

    wordlist = Wordlist(data)

    if json:
        yield from as_json(wordlist.all_forms)
    else:
        yield from as_text(wordlist.all_forms)

def as_text(all_items):
    for word, types in sorted(all_items.items()):
        for pos, targets in sorted(types.items()):
            forms = [f"{formtype}={form}" for formtype, forms in targets.items() for form in forms]
            if forms == [f"{pos}={word}"]:
                yield f"{word} {{{pos}}}"
            else:
                yield f"{word} {{{pos}}} " + "; ".join(sorted(forms))

def as_json(all_items):

    line = None
    yield "{"
    for word, types in sorted(all_items.items()):
        line_data = {word: types}
        if len(types) == 1:
            pos,targets = next(items.values())
            if len(targets) == 1 and targets.get(pos) == [word]:
                line_data = {word: pos}
        if line:
            yield line + ","
        line = json.dumps(line_data, ensure_ascii=False)[1:-1]
    yield line
    yield "}"

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description="Generate forms-to-lemmas data from wordlist")
    parser.add_argument("wordlist", help="wordlist")
    parser.add_argument("--json", help="format data as json", action='store_true')
    args = parser.parse_args()

    with open(args.wordlist) as infile:
        for line in export(infile, args.lemmas, args.json):
            print(line)
