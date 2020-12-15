#!/usr/bin/python3
#
# Copyright (c) 2020 Jeff Doozan
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
Extract all articles with the specified language
"""

import bz2
import os
from pywikibot import xmlreader
import re
import sys
from enwiktionary_parser.languages.all_ids import languages as lang_ids


def make_pattern(lang_sections):
    section_titles = "|".join(map(re.escape, lang_sections))
    start = fr"(^|\n)==\s*(?P<section_title>{section_titles})\s*==\s*\n"
    endings = r"==[^=]+==|----"
    newlines = r"(\n\s*)+"
    pattern = fr"{start}.*?(?={newlines}({endings})|$)"
    return re.compile(pattern, re.DOTALL)

def main():

    import argparse

    argparser = argparse.ArgumentParser(description="Extract language sections from enwiktionary dump")
    argparser.add_argument("--xml", help="XML file to load", required=True)
    argparser.add_argument("--lang", action="append", help="Language to dump, can be specified multiple times", required=True)
    argparser.add_argument("--outdir", help="Path to save extracted languages", default=".")
    argparser.add_argument("--limit", type=int, help="Limit processing to first N articles")

    args = argparser.parse_args()

    lang_sections = []
    for lang_id in args.lang:
        if lang_id not in lang_ids:
            raise ValueError(f"Unknown language id: {args.lang_id}")
        lang_sections.append(lang_ids[lang_id])

    if not os.path.isfile(args.xml):
        raise FileNotFoundError(f"Cannot open: {args.xml}")

    dump = xmlreader.XmlDump(args.xml)
    parser = dump.parse()

    count = 0
    lang_count = {}

    file_handles = {}
    pattern = {}
    for lang_name in lang_sections:
        filename = lang_name + ".txt.bz2"
        outfile = os.path.join(args.outdir, filename)
        file_handles[lang_name] = bz2.open(outfile, "wt")
        lang_count[lang_name] = 0
    match_pattern = make_pattern(lang_sections)

    for entry in parser:
        if not count % 1000:
            print(count, end = '\r', file=sys.stderr)

        if args.limit and count >= args.limit:
            break
        count += 1

        if ":" in entry.title:
            continue

        for res in re.finditer(match_pattern, entry.text):
            lang_name = res.group("section_title")
            lang_entry = res.group(0)

            lang_count[lang_name] += 1
            file_handles[lang_name].write(f"_____{entry.title}_____\n{lang_entry}\n")

    print(f"Total articles: {count}")
    for lang_name in lang_sections:
        file_handles[lang_name].close
        print(f"Total in {lang_name}: {lang_count[lang_name]}")


if __name__ == "__main__":
    main()
