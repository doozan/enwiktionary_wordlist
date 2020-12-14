#!/usr/bin/python3

import argparse
import csv
import io
import sys
from .wordlist import Wordlist
from .all_forms import AllForms

def export(forms):

    for form, poslemmas in sorted(forms.all_forms.items()):
        data = {}
        for poslemma in poslemmas:
            pos, lemma = poslemma.split("|")
            if pos not in data:
                data[pos] = [lemma]
            elif lemma not in data[pos]:
                data[pos].append(lemma)

        yield from make_lines(form, data)

def make_lines(form, data):
    for pos, lemmas in sorted(data.items()):
        si = io.StringIO()
        cw = csv.writer(si)
        cw.writerow([form,pos]+sorted(lemmas))
        yield si.getvalue().strip()

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description="Generate forms-to-lemmas data from wordlist")
    parser.add_argument("wordlist", help="wordlist")
    parser.add_argument("--low-mem", help="Use less memory", action='store_true', default=False)
    args = parser.parse_args()

    cache_words = not args.low_mem

    with open(args.wordlist) as wordlist_data:
        wordlist = Wordlist(wordlist_data, cache_words=cache_words)

        all_forms = AllForms.from_wordlist(wordlist)

        for line in export(all_forms):
            print(line)
