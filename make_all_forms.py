#!/usr/bin/python3

import argparse
import csv
import io
import sys
from .wordlist import Wordlist

class AllForms:

    def __init__(self, wordlist_data):
        self.wordlist = Wordlist(wordlist_data)
        self.all_forms = set()
        self.load_all_forms()
        del self.wordlist

    def export(self):

        # Convert to list and then sort on each key in reverse order of importance (pos, form)
        self.all_forms = list(self.all_forms)
        self.all_forms.sort(key=lambda x: x.split("|")[1])
        self.all_forms.sort(key=lambda x: x.split("|")[0])

        yield from self.as_text()

    def as_text(self):

        lemmas = []
        prev_form = None
        prev_pos = None
        first = True

        for item in self.all_forms:
            form, pos, lemma = item.split("|")
            if prev_form and (prev_form != form or prev_pos != pos):
                yield self.make_line(prev_form, prev_pos, lemmas)

                lemmas = []
            #if lemma != form and lemma not in lemmas:
            if lemma not in lemmas:
                lemmas.append(lemma)

            prev_form = form
            prev_pos = pos

        if prev_form:
            yield self.make_line(prev_form, prev_pos, lemmas)

    def make_line(self, form, pos, lemmas):
        si = io.StringIO()
        cw = csv.writer(si)
        cw.writerow([form,pos]+sorted(lemmas))
        return si.getvalue().strip()

    def add_form(self, form, pos, formtype, lemma):

        if form == "-":
#            if pos != "verb":
#                print(f"Bad form '-' referenced by {lemma} {formtype} {pos}", file=sys.stderr)
            return

        # target = (pos, lemma, formtype)
        # memory 1102820

        #target = f"{pos}:{lemma}:{formtype}"
        # memory 1048596

        #target = (pos, lemma)
        # memory 908408

        # target = f"{pos}:{lemma}"
        # memory 917540

        # target = None
        # memory 738848

        #form = f"{pos}:{form}"
        #target = lemma
        # memory 786204

        #form = f"{pos}:{form}"
        #target = f"{lemma}:{formtype}"
        # memory 1059896

        # form = (pos, form)
        # target = lemma
        # memory 871904

        # form = (pos,form,lemma)
        # memory 777496

        #rform = f"{lemma};{pos};{form}"
        value = f"{form}|{pos}|{lemma}"
        # memory 695364

        self.all_forms.add(value)

    #    if lemma.startswith("-ach") or form.startswith("-ach"):
    #        print(lemma, pos, formtype, form, value, file=sys.stderr)


    def load_all_forms(self):
        """
        Return a list of all known word form/lemma combinations
        [ "form|pos|lemma", ... ]
        """

        count = 0
        #for word in self.wordlist.iter_all_words():
        for pos_list in self.wordlist.all_words.values():
            for words in pos_list.values():
                for word in words:
                    count += 1
                    if count % 1000 == 0:
                        print(count, end="\r", file=sys.stderr)
                    self.process_word_forms(word)

    def process_word_forms(self, word):
        if not len(word.senses):
            return

        for lemma, formtypes in self.wordlist.get_lemmas(word).items():
            for lemma_formtype in formtypes:
                self.add_form(word.word, word.common_pos, lemma_formtype, lemma)

                for formtype, forms in word.forms.items():
                    for form in forms:
                        if lemma_formtype == "f" and not word.is_lemma:
                            if formtype in ["m", "mpl"]:
                                continue
                            elif formtype in ["pl", "fpl"]:
                                formtype = "fpl"

                        self.add_form(form, word.common_pos, formtype, lemma)

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description="Generate forms-to-lemmas data from wordlist")
    parser.add_argument("wordlist", help="wordlist")
    args = parser.parse_args()

    with open(args.wordlist) as infile:

        all_forms = AllForms(infile)
        for line in all_forms.export():
            print(line)
