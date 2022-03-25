#!/usr/bin/python3
#
# Copyright (c) 2022 Jeff Doozan
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
from collections import namedtuple

"""
Parses a data file formatted as:

_____item1_____
article data
...
_____item2_____
...

"""

Article = namedtuple("Article", "title text")
class WikiExtract:

    @classmethod
    def iter_articles(cls, iterable):
        """ Yields (article_title, article_text) for each article in iterable """
        entry = []
        title = None
        for line in iterable:
            if line.startswith("_____") and line.endswith("_____\n"):
                if entry:
                    entry[-1] = entry[-1].rstrip("\n")
                    yield Article(title, "".join(entry))
                title = line[5:-6]
                entry = []
            else:
                if title is None:
                    raise ValueError("File is not a recognized format", line, line.startswith("_____"), line.endswith("_____\n"))
                entry.append(line)
        if entry:
            entry[-1] = entry[-1].rstrip("\n")
            yield Article(title, "".join(entry))

    @classmethod
    def iter_articles_from_txt(cls, filename):
        with open(filename, "r") as infile:
            yield from cls.iter_articles(infile)

    @classmethod
    def iter_articles_from_bz2(cls, filename):
        with bz2.open(filename, "rt") as infile:
            yield from cls.iter_articles(infile)


ArticleWithRev = namedtuple("ArticleWithRev", "title text revision")
class WikiExtractWithRev(WikiExtract):

    @classmethod
    def iter_articles(cls, iterable):
        """ Yields (title, text, revision) for each article in iterable """
        for fulltitle, text in super().iter_articles(iterable):
            title, _, revision = fulltitle.partition(":@")
            yield ArticleWithRev(title, text, revision)
