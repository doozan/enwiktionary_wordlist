#!/usr/bin/python3

import argparse
import csv
import io
import sys
from .wordlist import Wordlist
from .all_forms import AllForms

def export(allforms):

    line_data = []
    lemmas = []
    prev_pos = None
    prev_form = None
    for form, pos, lemma in sorted(allforms.all):
        if form != prev_form or pos != prev_pos:
            if lemmas:
                line_data.append((prev_form, prev_pos, lemmas))
            lemmas = []
        lemmas.append(lemma)
        prev_form = form
        prev_pos = pos
    line_data.append((prev_form, prev_pos, lemmas))

    yield from make_lines(line_data)

def make_lines(line_data):
    for form, pos, lemmas in line_data:
        si = io.StringIO()
        cw = csv.writer(si)
        cw.writerow([form,pos]+sorted(lemmas))
        yield si.getvalue().strip()

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description="Generate forms-to-lemmas data from wordlist")
    parser.add_argument("wordlist", help="wordlist")
    parser.add_argument("--resolve-lemmas", help="Resolve 'form of' lemmas to final lemma", action='store_true', default=False)
    parser.add_argument("--low-mem", help="Use less memory", action='store_true', default=False)
    args = parser.parse_args()

    cache_words = not args.low_mem

    with open(args.wordlist) as wordlist_data:
        wordlist = Wordlist(wordlist_data, cache_words=cache_words)

        all_forms = AllForms.from_wordlist(wordlist, args.resolve_lemmas)

        for line in export(all_forms):
            print(line)
