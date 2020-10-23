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

import pytest
from make_dictionary import DictionaryBuilder
import mwparserfromhell

builder = DictionaryBuilder("Spanish", "es")

def test_chapó():

    orig_text="""\
{{also|chapo}}
==Spanish==

===Etymology 1===

====Verb====
{{head|es|verb form}}
# {{es-verb form of|person=third-person|number=singular|tense=preterit|mood=indicative|ending=ar|chapar}}

===Etymology 2===
Borrowed from {{bor|es|fr|chapeau}}, from {{der|es|VL.|*cappellus}}. Doublet of the inherited {{doublet|es|capillo|notext=1}}, and of {{m|es|capelo}} (from Italian), as well as {{m|es|chapeo}}, also from the French word.

===Pronunciation===
* {{es-IPA}}

===Interjection===
{{es-interj}}

# {{non-gloss definition|Used to express [[appreciation]]}}; [[hat tip]]
#: '''''Chapó''', señor.''
"""

    lang_entry = builder.get_language_entry(orig_text)
    assert lang_entry != ""
    entry = builder.parse_entry(lang_entry, "chapó")

    assert entry == ["chapó {interj} :: Used to express appreciation; hat tip"]


def test_bolivariano():

    orig_text="""\
==Portuguese==

===Adjective===
{{pt-adj|bolivarian|o}}

# [[Bolivarian]] {{gloss|Of or pertaining to [[w:Simón Bolívar|Simón Bolívar]].}}

----

==Spanish==

===Adjective===
{{es-adj|f=bolivariana}}

# [[Bolivarian]] {{gloss|Of or pertaining to [[w:Simón Bolívar|Simón Bolívar]].}}
"""

    lang_entry = builder.get_language_entry(orig_text)
    assert lang_entry != ""
    entry = builder.parse_entry(lang_entry, "bolivariano")

    assert "\n".join(entry) == """\
bolivariano {meta-adj} :: f=bolivariana; fpl=bolivarianas; pl=bolivarianos
bolivariano {adj} :: Bolivarian (Of or pertaining to Simón Bolívar.)"""

def test_compeltada():
    orig_text="""\
==Catalan==

===Pronunciation===
* {{ca-IPA}}

===Verb===
{{head|ca|past participle|g=f-s}}

# {{ca-verb form of|g=f|m=ptc|t=past|completar}}

----

==Portuguese==

===Verb===
{{pt-pp|completad|completar}}

# {{pt-verb-form-of|completar}}

----

==Spanish==

===Pronunciation===
* {{es-IPA}}

===Adjective===
{{head|es|adjective form}}

# {{es-adj form of|completado|f|sg}}

===Verb===
{{head|es|past participle form}}

# {{es-verb form of|mood=participle|gen=f|num=s|ending=ar|completar}}

===Noun===
{{es-noun|f}}

# {{lb|es|Chile}} [[party]] or meeting where they eat [[completo]]s ([[hot-dog]]s)
"""

    lang_entry = builder.get_language_entry(orig_text)
    assert lang_entry != ""
    entry = builder.parse_entry(lang_entry, "completada")

    assert "\n".join(entry) == """\
completada {meta-noun} :: pl=completadas
completada {f} [Chile] :: party or meeting where they eat completos (hot-dogs)"""


def test_yero():
    orig_text="""\
==Spanish==

===Etymology 1===
{{cln|es|syncopic forms}}Syncopated from {{m|es|yervo}}, from {{inh|es|la|ervum}}.

====Noun====
{{es-noun|m}}

# any variety of [[bitter vetch]] (''[[Vicia ervilia]]'')
#: {{syn|es|alcarceña}}

===Etymology 2===

====Verb====
{{head|es|verb form}}

# {{es-verb form of|yerar|ending=-ar|mood=indicative|tense=present|number=s|person=1}}

----
"""

    lang_entry = builder.get_language_entry(orig_text)
    assert lang_entry != ""
    print(lang_entry)
    entry = builder.parse_entry(lang_entry, "yero")

    assert "\n".join(entry) == """\
yero {meta-noun} :: pl=yeros
yero {m} | alcarceña :: any variety of bitter vetch (Vicia ervilia)"""


def test_wiki_to_text():

    wiki = mwparserfromhell.parse("{{gloss|a weak unstable acid, H<sub>2</sub>CO<sub>3</sub>}}")
    text = builder.wiki_to_text(wiki)
    assert text == "(a weak unstable acid, H2CO3)"

def test_repanoche():
    orig_text="""\
==Spanish== 

===Noun===
{{es-noun|f|-}}

# {{lb|es|Spain}} {{only used in|es|ser la repanocha}}
"""

    lang_entry = builder.get_language_entry(orig_text)
    assert lang_entry != ""
    print(lang_entry)
    entry = builder.parse_entry(lang_entry, "repanoche")

    assert "\n".join(entry) == """\
repanoche {f} [Spain] :: only used in "ser la repanocha"\
"""


def test_wiki_to_text():

    wiki = mwparserfromhell.parse("{{gloss|a weak unstable acid, H<sub>2</sub>CO<sub>3</sub>}}")
    text = builder.wiki_to_text(wiki)
    assert text == "(a weak unstable acid, H2CO3)"

    wiki = mwparserfromhell.parse("[[test|blah]]")
    text = builder.wiki_to_text(wiki)
    assert text == "blah"

    wiki = mwparserfromhell.parse("[[w:Spain|Spain]]")
    text = builder.wiki_to_text(wiki)
    assert text == "Spain"

    wiki = mwparserfromhell.parse("{{indtr|es|en|.also|.figurative}}")
    text = builder.wiki_to_text(wiki)
    assert text == "(also figurative, transitive with en)"

def test_fullentry():
    orig_text="""\
==Spanish==

===Verb===
{{es-verb|descans|ar}}

# {{indtr|es|en|.also|.figurative}} to [[sit]], to [[rest]] on
"""

    lang_entry = builder.get_language_entry(orig_text)
    assert lang_entry != ""
    entry = builder.parse_entry(lang_entry, "test")

    assert entry[0] == "test {vt} :: (also figurative, transitive with en) to sit, to rest on"

def test_meta_noun():
    orig_text="""\
==Spanish==

===Noun===
{{es-noun|mf|youtubers|pl2=youtuber|f=youtuberista|fpl=youtuberistas}}

# A person or a member of a group of people regarded as undesirable
"""

    lang_entry = builder.get_language_entry(orig_text)
    assert lang_entry != ""
    entry = builder.parse_entry(lang_entry, "youtuber")

    assert entry[0] == "youtuber {meta-noun} :: f=youtuberista; fpl=youtuberistas; pl=youtubers; pl=youtuber"

def test_meta_adj():
    orig_text="""\
==Spanish==

===Adjective===
{{es-adj|pl=youtubers|pl2=youtuber|f=youtuberista|fpl=youtuberistas}}

# A person or a member of a group of people regarded as undesirable
"""

    lang_entry = builder.get_language_entry(orig_text)
    assert lang_entry != ""
    entry = builder.parse_entry(lang_entry, "youtuber")

    assert entry[0] == "youtuber {meta-adj} :: f=youtuberista; fpl=youtuberistas; pl=youtubers; pl=youtuber"

def test_meta_verb():
    orig_text="""\
==Spanish==

===Verb===
{{es-verb|absten|er|pres=abstengo|pret=abstuve}}

# {{lb|es|reflexive}} to [[abstain]]

====Conjugation====
{{es-conj-er|abs|p=-tener|combined=1}}
"""

    lang_entry = builder.get_language_entry(orig_text)
    assert lang_entry != ""
    entry = builder.parse_entry(lang_entry, "abstener")

    assert entry[0] == "abstener {meta-verb} :: pattern=-tener; stem=abs"

def test_multi_meta_verb():
    orig_text="""\
==Spanish==

===Verb===
{{es-verb|adecu|ar|pres=adecúo}}

# {{lb|es|transitive}} to [[adapt]], [[adjust]]

====Conjugation====
''This verb has two possible conjugations.''
{{es-conj-ar|adec||p=u-ú|combined=1}}
{{es-conj-ar|adecu|combined=1}}
"""

    lang_entry = builder.get_language_entry(orig_text)
    assert lang_entry != ""
    entry = builder.parse_entry(lang_entry, "adecuar")

    assert "\n".join(entry)=="""\
adecuar {meta-verb} :: pattern=u-ú; stem=adec; stem=
adecuar {meta-verb} :: stem=adecu
adecuar {vt} :: to adapt, adjust"""

def test_protector():
    orig_text="""\
==Spanish==

===Adjective===
{{es-adj|f=protectora|mpl=protectores|f2=protectriz|fpl2=protectrices}}

# [[protective]]

===Noun===
{{es-noun|m|protectores|f=protectora|f2=protectriz}}

# {{l|en|protector}} {{gloss|someone who protects or guards}}

{{es-noun|m}}

# {{l|en|protector}} {{gloss|a device or mechanism which is designed to protect}}
"""

    lang_entry = builder.get_language_entry(orig_text)
    assert lang_entry != ""
    entry = builder.parse_entry(lang_entry, "protector")

    assert "\n".join(entry)=="""\
protector {meta-adj} :: f=protectora; f=protectriz; fpl=protectrices; pl=protectores
protector {adj} :: protective
protector {meta-noun} :: f=protectora; f=protectriz; fpl=protectoras; fpl=protectrices; pl=protectores
protector {m} :: protector (someone who protects or guards)
protector {meta-noun} :: pl=protectores
protector {m} :: protector (a device or mechanism which is designed to protect)"""

def test_aterrar():
    orig_text="""\
==Spanish==

===Etymology 1===
{{af|es|a-|tierra|-ar|t2=land}}

====Verb====
{{es-verb|aterr|ar|pres=atierro}}

# {{lb|es|transitive}} to [[bring down]], to [[ground]]

=====Conjugation=====
{{es-conj-ar|at|rr|p=e-ie|combined=1}}

===Etymology 2===
From {{af|es|a-|terreō|lang2=la}}.

====Verb====
{{es-verb|aterr|ar}}

# {{lb|es|transitive}} to [[scare]]

=====Conjugation=====
{{es-conj-ar|aterr|combined=1}}
"""

    lang_entry = builder.get_language_entry(orig_text)
    assert lang_entry != ""
    entry = builder.parse_entry(lang_entry, "aterrar")

    assert "\n".join(entry)=="""\
aterrar {meta-verb} :: pattern=e-ie; stem=at; stem=rr
aterrar {meta-verb} :: stem=aterr
aterrar {vt} :: to bring down, to ground
aterrar {vt} :: to scare"""

def test_atentar():
    orig_text="""\
==Spanish==

===Etymology 1===
From {{der|es|la|attentō}}.

====Verb====
{{es-verb|atent|ar|pres=atiento}}

# {{lb|es|intransitive}} to commit a violent or criminal [[attack]], to [[strike]]

===Etymology 2===
{{rfe|es}}

====Verb====
{{es-verb|atent|ar}}

# {{lb|es|transitive|obsolete}} to [[touch]]
# {{synonym of|es|tentar}}

===Conjugation===
{{es-conj-ar|at|nt|p=e-ie|combined=1}}
"""

    lang_entry = builder.get_language_entry(orig_text)
    assert lang_entry != ""
    entry = builder.parse_entry(lang_entry, "atentar")

    assert "\n".join(entry)=="""\
atentar {meta-verb} :: pattern=e-ie; stem=at; stem=nt
atentar {vi} :: to commit a violent or criminal attack, to strike
atentar {vt} [obsolete] :: to touch
atentar {v} :: synonym of "tentar"\
"""


def test_billon():
    orig_text="""\
==Spanish==

===Numeral===
{{es-noun|m|billones}}
{{enum|es|millón|trillón|cardinal number|10<sup>12</sup>}}

# 10<sup>12</sup>; a [[trillion]] (''short system'')
# {{lb|es|obsolete}} 10<sup>9</sup>: a [[billion]] (''long system'')
"""

    lang_entry = builder.get_language_entry(orig_text)
    assert lang_entry != ""
    entry = builder.parse_entry(lang_entry, "billón")

    assert "\n".join(entry)=="""\
billón {meta-noun} :: pl=billones
billón {num} :: 10^12; a trillion (short system)
billón {num} [obsolete] :: 10^9: a billion (long system)"""


def test_aquestos():
    orig_text="""\
==Spanish==

===Pronunciation===
* {{es-IPA}}

===Determiner===
{{head|es|determiner form}}

# {{masculine plural of|es|aqueste}}

===Pronoun===
{{head|es|pronoun form}}

# {{masculine plural of|es|aqueste}}
"""

    lang_entry = builder.get_language_entry(orig_text)
    assert lang_entry != ""
    entry = builder.parse_entry(lang_entry, "aquestos")

    assert "\n".join(entry)==""

def test_robot():
    orig_text="""\
==Spanish==

===Noun===
{{es-noun|m}}

# {{l|en|robot}}
"""

    lang_entry = builder.get_language_entry(orig_text)
    assert lang_entry != ""
    entry = builder.parse_entry(lang_entry, "robot")

    assert "\n".join(entry)=="""\
robot {meta-noun} :: pl=robots
robot {m} :: robot"""

def test_angla():
    orig_text="""\
==Spanish==

===Pronunciation===
* {{es-IPA}}

===Adjective===
{{head|es|adjective form|g=f-s}}

# {{adj form of|es|anglo||f|s}}

===Noun===
{{es-noun|f|m=anglo}}

# {{female equivalent of|es|anglo}}
"""

    lang_entry = builder.get_language_entry(orig_text)
    assert lang_entry != ""
    entry = builder.parse_entry(lang_entry, "angla")

    assert "\n".join(entry)=="""\
angla {meta-noun} :: m=anglo; mpl=anglos; pl=anglas
angla {f} :: female equivalent of "anglo"\
"""

def test_cherry():
    orig_text="""\
==Spanish==

===Noun===
{{es-noun|m|+|pl2=cherries}}

# {{l|en|cherry tomato}}
"""

    lang_entry = builder.get_language_entry(orig_text)
    assert lang_entry != ""
    entry = builder.parse_entry(lang_entry, "cherry")

    assert "\n".join(entry)=="""\
cherry {meta-noun} :: pl=cherrys; pl=cherries
cherry {m} :: cherry tomato"""


def test_torpon():
    orig_text="""\
==Spanish==

===Adjective===
{{es-adj|f=torpona|mpl=torpones}}

# [[clumsy]]
"""

    lang_entry = builder.get_language_entry(orig_text)
    assert lang_entry != ""
    entry = builder.parse_entry(lang_entry, "torpón")

    assert "\n".join(entry)=="""\
torpón {meta-adj} :: f=torpona; fpl=torponas; pl=torpones
torpón {adj} :: clumsy\
"""

def test_trailing_periods():
    orig_text="""\
==Spanish==

===Proper noun===
{{es-proper noun|m}}

# {{lb|es|Spain}} {{alternative spelling of|es|México}}.
# {{alternative spelling of|es|test.}}
# [[test]]
"""

    lang_entry = builder.get_language_entry(orig_text)
    assert lang_entry != ""
    entry = builder.parse_entry(lang_entry, "Mejico")

    print("\n".join(entry))
    assert "\n".join(entry)=="""\
Mejico {m} [Spain] :: alternative spelling of "México"
Mejico {m} :: alternative spelling of "test."
Mejico {m} :: test\
"""
