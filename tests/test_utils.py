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

from enwiktionary_wordlist.utils import wiki_to_text, make_language_pattern
import mwparserfromhell
import re

def test_wiki_to_text():

    wiki = mwparserfromhell.parse("{{gloss|a weak unstable acid, H<sub>2</sub>CO<sub>3</sub>}}")
    text = wiki_to_text(wiki, "test")
    assert text == "(a weak unstable acid, H2CO3)"

    wiki = mwparserfromhell.parse("[[test|blah]]")
    text = wiki_to_text(wiki, "test")
    assert text == "blah"

    wiki = mwparserfromhell.parse("[[w:Spain|Spain]]")
    text = wiki_to_text(wiki, "test")
    assert text == "Spain"

    wiki = mwparserfromhell.parse("{{indtr|es|en|.also|.figurative}}")
    text = wiki_to_text(wiki, "test")
    assert text == "(also figuratively, transitive with en)"


def test_language_match():
    lang1 = """\
==Sabir==

===Verb===
{{head|pml|verb}}

# to [[speak]]

===References===
* Feissat et Demonchy, ''Dictionnaire de la Langue Franque, ou Petit Mauresque''\
"""

    lang2 = """\
==Spanish==

===Verb===
{{es-verb}}

# {{lb|es|intransitive}} to [[talk]]; to [[speak]]; to [[communicate]] using [[word]]s

===Further reading===
* {{R:DRAE}}

{{C|es|Talking}}\
"""

    lang3 = """\
==Tagalong==

===Verb===
{{head|pml|verb}}

# to [[speak]]\
"""

    page_text = "\n\n----\n\n".join([lang1, lang2, lang3])

    pattern = make_language_pattern("Sabir")
    print(pattern)
    assert re.search(pattern, page_text).group(0).strip() == lang1

    pattern = make_language_pattern("Spanish")
    assert re.search(pattern, page_text).group(0).strip() == lang2

    pattern = make_language_pattern("Tagalong")
    assert re.search(pattern, page_text).group(0).strip() == lang3

    # Also matches if the ---- is missing
    page_text = "\n".join([lang1, lang2, lang3])

    pattern = make_language_pattern("Sabir")
    assert re.search(pattern, page_text).group(0).strip() == lang1

    pattern = make_language_pattern("Spanish")
    assert re.search(pattern, page_text).group(0).strip() == lang2

    pattern = make_language_pattern("Tagalong")
    assert re.search(pattern, page_text).group(0).strip() == lang3
