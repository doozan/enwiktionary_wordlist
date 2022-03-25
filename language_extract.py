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

import bz2
import re
from collections import namedtuple

WiktionaryPage = namedtuple('WiktionaryPage', 'title text revision')

class LanguageFile:
    @staticmethod
    def iter_articles(filename):
        """ Yields (title, text, revision) for each article in filename """
        with bz2.open(filename, "rt") as infile:
            pattern = r'^_____([^:]*)(:@)?(.*?)_____$'
            entry = []
            title = None
            for line in infile:
                match = re.match(pattern, line)
                if match:
                    if entry:
                        entry[-1] = entry[-1].strip()
                        yield WiktionaryPage(title, "".join(entry), revision)
                    title = match.group(1)
                    revision = match.group(3)
                    entry = []
                else:
                    if title is None:
                        raise ValueError("File is not a recognized format")
                    entry.append(line)
            if entry:
                entry[-1] = entry[-1].strip()
                yield WiktionaryPage(title, "".join(entry), revision)

    def __init__(self, lang_name):

        start = fr"(^|\n)==\s*{lang_name}\s*==\s*\n"
        re_endings = [ r"==[^=]+==", r"----" ]
        endings = "|".join(re_endings)
        newlines = r"(\n\s*){1,2}"
        pattern = fr"{start}.*?(?={newlines}({endings})|$)"

        self._re_pattern = re.compile(pattern, re.DOTALL)

    def get_language_entry(self, text):
        """
        Return the entire body text of the language entry
        """

        res = re.search(self._re_pattern, text)
        if res:
            return res.group(0)
