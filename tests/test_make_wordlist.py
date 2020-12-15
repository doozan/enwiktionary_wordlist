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
from enwiktionary_wordlist.make_wordlist import WordlistBuilder
import mwparserfromhell

builder = WordlistBuilder("Spanish", "es")

def test_chapo():

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

    entry = builder.entry_to_text(lang_entry, "chapó")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
_____
chapó
pos: v
  meta: {{head|es|verb form}}
  gloss: inflection of "chapar"
pos: interj
  meta: {{es-interj}}
  gloss: Used to express appreciation; hat tip\
"""

    entry = builder.entry_to_mbformat(lang_entry, "chapó")

    assert "\n".join(entry) == """\
chapó {v-meta} :: {{head|es|verb form}}
chapó {v} :: inflection of "chapar"
chapó {interj-meta} :: {{es-interj}}
chapó {interj} :: Used to express appreciation; hat tip\
"""


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

    entry = builder.entry_to_text(lang_entry, "bolivariano")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
_____
bolivariano
pos: adj
  meta: {{es-adj|f=bolivariana}}
  gloss: Bolivarian (Of or pertaining to Simón Bolívar.)\
"""

    entry = builder.entry_to_mbformat(lang_entry, "bolivariano")

    assert "\n".join(entry) == """\
bolivariano {adj-meta} :: {{es-adj|f=bolivariana}}
bolivariano {adj} :: Bolivarian (Of or pertaining to Simón Bolívar.)"""

def test_completada():
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

    entry = builder.entry_to_text(lang_entry, "completada")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
_____
completada
pos: adj
  meta: {{head|es|adjective form}}
pos: v
  meta: {{head|es|past participle form}}
  gloss: inflection of "completar"
pos: n
  meta: {{es-noun|f}}
  g: f
  gloss: party or meeting where they eat completos (hot-dogs)
    q: Chile\
"""

    entry = builder.entry_to_mbformat(lang_entry, "completada")

    assert "\n".join(entry) == """\
completada {adj-meta} :: {{head|es|adjective form}}
completada {v-meta} :: {{head|es|past participle form}}
completada {v} :: inflection of "completar"
completada {n-meta} :: {{es-noun|f}}
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

    entry = builder.entry_to_text(lang_entry, "yero")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
_____
yero
pos: n
  meta: {{es-noun|m}}
  g: m
  gloss: any variety of bitter vetch (Vicia ervilia)
    syn: alcarceña
pos: v
  meta: {{head|es|verb form}}
  gloss: inflection of "yerar"\
"""

    entry = builder.entry_to_mbformat(lang_entry, "yero")

    assert "\n".join(entry) == """\
yero {n-meta} :: {{es-noun|m}}
yero {m} | alcarceña :: any variety of bitter vetch (Vicia ervilia)
yero {v-meta} :: {{head|es|verb form}}
yero {v} :: inflection of "yerar"\
"""


def test_repanoche():
    orig_text="""\
==Spanish== 

===Noun===
{{es-noun|f|-}}

# {{lb|es|Spain}} {{only used in|es|ser la repanocha}}
"""

    lang_entry = builder.get_language_entry(orig_text)
    assert lang_entry != ""

    entry = builder.entry_to_text(lang_entry, "repanoche")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
_____
repanoche
pos: n
  meta: {{es-noun|f|-}}
  g: f
  gloss: only used in "ser la repanocha"
    q: Spain\
"""

    entry = builder.entry_to_mbformat(lang_entry, "repanoche")

    assert "\n".join(entry) == """\
repanoche {n-meta} :: {{es-noun|f|-}}
repanoche {f} [Spain] :: only used in "ser la repanocha"\
"""


def test_fullentry():
    orig_text="""\
==Spanish==

===Verb===
{{es-verb|descans|ar}}

# {{indtr|es|en|.also|.figurative}} to [[sit]], to [[rest]] on

====Conjugation====
{{es-conj-ar|descans|combined=1}}
"""

    lang_entry = builder.get_language_entry(orig_text)
    assert lang_entry != ""

    entry = builder.entry_to_text(lang_entry, "test")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
_____
test
pos: v
  meta: {{es-verb|descans|ar}} {{es-conj-ar|descans|combined=1}}
  gloss: (also figurative, transitive with en) to sit, to rest on
    q: transitive\
"""

    entry = builder.entry_to_mbformat(lang_entry, "test")

    print("\n".join(entry))
    assert "\n".join(entry) == """\
test {v-meta} :: {{es-verb|descans|ar}} {{es-conj-ar|descans|combined=1}}
test {vt} :: (also figurative, transitive with en) to sit, to rest on\
"""

def test_noun_forms():
    orig_text="""\
==Spanish==

===Noun===
{{es-noun|mf|youtubers|pl2=youtuber|f=youtuberista|fpl=youtuberistas}}

# A person or a member of a group of people regarded as undesirable
"""

    lang_entry = builder.get_language_entry(orig_text)
    assert lang_entry != ""

    entry = builder.entry_to_text(lang_entry, "youtuber")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
_____
youtuber
pos: n
  meta: {{es-noun|mf|youtubers|pl2=youtuber|f=youtuberista|fpl=youtuberistas}}
  g: mf
  gloss: A person or a member of a group of people regarded as undesirable\
"""

    entry = builder.entry_to_mbformat(lang_entry, "youtuber")

    print( "\n".join(entry))
    assert lang_entry != """
youtuber {mf} :: A person or a member of a group of people regarded as undesirable
"""

def test_adj_forms():
    orig_text="""\
==Spanish==

===Adjective===
{{es-adj|pl=youtubers|pl2=youtuber|f=youtuberista|fpl=youtuberistas}}

# A person or a member of a group of people regarded as undesirable
"""

    lang_entry = builder.get_language_entry(orig_text)
    assert lang_entry != ""

    entry = builder.entry_to_text(lang_entry, "youtuber")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
_____
youtuber
pos: adj
  meta: {{es-adj|pl=youtubers|pl2=youtuber|f=youtuberista|fpl=youtuberistas}}
  gloss: A person or a member of a group of people regarded as undesirable\
"""

    entry = builder.entry_to_mbformat(lang_entry, "youtuber")

    assert "\n".join(entry) == """\
youtuber {adj-meta} :: {{es-adj|pl=youtubers|pl2=youtuber|f=youtuberista|fpl=youtuberistas}}
youtuber {adj} :: A person or a member of a group of people regarded as undesirable\
"""

def test_verb_forms():
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

    entry = builder.entry_to_text(lang_entry, "abstener")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
_____
abstener
pos: v
  meta: {{es-verb|absten|er|pres=abstengo|pret=abstuve}} {{es-conj-er|abs|p=-tener|combined=1}}
  gloss: to abstain
    q: reflexive\
"""

    entry = builder.entry_to_mbformat(lang_entry, "abstener")

    assert "\n".join(entry) == """\
abstener {v-meta} :: {{es-verb|absten|er|pres=abstengo|pret=abstuve}} {{es-conj-er|abs|p=-tener|combined=1}}
abstener {vr} :: to abstain\
"""

#    assert entry[0] == "abstener {v-forms} :: pattern=-tener; stem=abs"

def test_multi_form_verb():
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

    entry = builder.entry_to_text(lang_entry, "adecuar")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
_____
adecuar
pos: v
  meta: {{es-verb|adecu|ar|pres=adecúo}} {{es-conj-ar|adec||p=u-ú|combined=1}} {{es-conj-ar|adecu|combined=1}}
  gloss: to adapt, adjust
    q: transitive\
"""

    entry = builder.entry_to_mbformat(lang_entry, "adecuar")

    assert "\n".join(entry)=="""\
adecuar {v-meta} :: {{es-verb|adecu|ar|pres=adecúo}} {{es-conj-ar|adec||p=u-ú|combined=1}} {{es-conj-ar|adecu|combined=1}}
adecuar {vt} :: to adapt, adjust\
"""

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

    entry = builder.entry_to_text(lang_entry, "protector")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
_____
protector
pos: adj
  meta: {{es-adj|f=protectora|mpl=protectores|f2=protectriz|fpl2=protectrices}}
  gloss: protective
pos: n
  meta: {{es-noun|m|protectores|f=protectora|f2=protectriz}}
  g: m
  gloss: protector (someone who protects or guards)
pos: n
  meta: {{es-noun|m}}
  g: m
  gloss: protector (a device or mechanism which is designed to protect)\
"""

    entry = builder.entry_to_mbformat(lang_entry, "protector")

    assert "\n".join(entry)=="""\
protector {adj-meta} :: {{es-adj|f=protectora|mpl=protectores|f2=protectriz|fpl2=protectrices}}
protector {adj} :: protective
protector {n-meta} :: {{es-noun|m|protectores|f=protectora|f2=protectriz}}
protector {m} :: protector (someone who protects or guards)
protector {n-meta} :: {{es-noun|m}}
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

    entry = builder.entry_to_text(lang_entry, "aterrar")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
_____
aterrar
pos: v
  meta: {{es-verb|aterr|ar|pres=atierro}} {{es-conj-ar|at|rr|p=e-ie|combined=1}}
  gloss: to bring down, to ground
    q: transitive
pos: v
  meta: {{es-verb|aterr|ar}} {{es-conj-ar|aterr|combined=1}}
  gloss: to scare
    q: transitive\
"""

    entry = builder.entry_to_mbformat(lang_entry, "aterrar")

    assert "\n".join(entry)=="""\
aterrar {v-meta} :: {{es-verb|aterr|ar|pres=atierro}} {{es-conj-ar|at|rr|p=e-ie|combined=1}}
aterrar {vt} :: to bring down, to ground
aterrar {v-meta} :: {{es-verb|aterr|ar}} {{es-conj-ar|aterr|combined=1}}
aterrar {vt} :: to scare\
"""

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

    entry = builder.entry_to_text(lang_entry, "atentar")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
_____
atentar
pos: v
  meta: {{es-verb|atent|ar|pres=atiento}} {{es-conj-ar|at|nt|p=e-ie|combined=1}}
  gloss: to commit a violent or criminal attack, to strike
    q: intransitive
pos: v
  meta: {{es-verb|atent|ar}} {{es-conj-ar|at|nt|p=e-ie|combined=1}}
  gloss: to touch
    q: transitive, obsolete
  gloss: synonym of "tentar"\
"""

    entry = builder.entry_to_mbformat(lang_entry, "atentar")

    assert "\n".join(entry)=="""\
atentar {v-meta} :: {{es-verb|atent|ar|pres=atiento}} {{es-conj-ar|at|nt|p=e-ie|combined=1}}
atentar {vi} :: to commit a violent or criminal attack, to strike
atentar {v-meta} :: {{es-verb|atent|ar}} {{es-conj-ar|at|nt|p=e-ie|combined=1}}
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

    entry = builder.entry_to_text(lang_entry, "billón")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
_____
billón
pos: num
  meta: {{es-noun|m|billones}}
  g: m
  gloss: 10^12; a trillion (short system)
  gloss: 10^9: a billion (long system)
    q: obsolete\
"""

    entry = builder.entry_to_mbformat(lang_entry, "billón")

    assert "\n".join(entry)=="""\
billón {num-meta} :: {{es-noun|m|billones}}
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

    expected = """\
aquestos {determiner-meta} :: {{head|es|determiner form}}
aquestos {determiner} :: masculine plural of "aqueste"
aquestos {pron-meta} :: {{head|es|pronoun form}}
aquestos {pron} :: masculine plural of "aqueste"\
"""

    lang_entry = builder.get_language_entry(orig_text)
    assert lang_entry != ""

    entry = builder.entry_to_text(lang_entry, "aquestos")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
_____
aquestos
pos: determiner
  meta: {{head|es|determiner form}}
  gloss: masculine plural of "aqueste"
pos: pron
  meta: {{head|es|pronoun form}}
  gloss: masculine plural of "aqueste"\
"""

    entry = builder.entry_to_mbformat(lang_entry, "aquestos")

    assert "\n".join(entry)==expected

def test_robot():
    orig_text="""\
==Spanish==

===Noun===
{{es-noun|m}}

# {{l|en|robot}}
"""

    lang_entry = builder.get_language_entry(orig_text)
    assert lang_entry != ""

    entry = builder.entry_to_text(lang_entry, "robot")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
_____
robot
pos: n
  meta: {{es-noun|m}}
  g: m
  gloss: robot\
"""

    entry = builder.entry_to_mbformat(lang_entry, "robot")

    assert "\n".join(entry)=="""\
robot {n-meta} :: {{es-noun|m}}
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

    entry = builder.entry_to_text(lang_entry, "angla")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
_____
angla
pos: adj
  meta: {{head|es|adjective form|g=f-s}}
  g: f-s
  gloss: adjective form of "anglo"
pos: n
  meta: {{es-noun|f|m=anglo}}
  g: f
  gloss: female equivalent of "anglo"\
"""

    entry = builder.entry_to_mbformat(lang_entry, "angla")

    print("\n".join(entry))

    assert "\n".join(entry)=="""\
angla {adj-meta} :: {{head|es|adjective form|g=f-s}}
angla {adj} :: adjective form of "anglo"
angla {n-meta} :: {{es-noun|f|m=anglo}}
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

    entry = builder.entry_to_text(lang_entry, "cherry")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
_____
cherry
pos: n
  meta: {{es-noun|m|+|pl2=cherries}}
  g: m
  gloss: cherry tomato\
"""

    entry = builder.entry_to_mbformat(lang_entry, "cherry")

    assert "\n".join(entry)=="""\
cherry {n-meta} :: {{es-noun|m|+|pl2=cherries}}
cherry {m} :: cherry tomato\
"""


def test_torpon():
    orig_text="""\
==Spanish==

===Adjective===
{{es-adj|f=torpona|mpl=torpones}}

# [[clumsy]]
"""

    lang_entry = builder.get_language_entry(orig_text)
    assert lang_entry != ""

    entry = builder.entry_to_text(lang_entry, "torpón")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
_____
torpón
pos: adj
  meta: {{es-adj|f=torpona|mpl=torpones}}
  gloss: clumsy\
"""

    entry = builder.entry_to_mbformat(lang_entry, "torpón")

    assert "\n".join(entry)=="""\
torpón {adj-meta} :: {{es-adj|f=torpona|mpl=torpones}}
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

    entry = builder.entry_to_text(lang_entry, "Mejico")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
_____
Mejico
pos: prop
  meta: {{es-proper noun|m}}
  g: m
  gloss: alternative spelling of "México"
    q: Spain
  gloss: alternative spelling of "test."
  gloss: test\
"""

    entry = builder.entry_to_mbformat(lang_entry, "Mejico")

    print("\n".join(entry))
    assert "\n".join(entry)=="""\
Mejico {n-meta} :: {{es-proper noun|m}}
Mejico {m} [Spain] :: alternative spelling of "México"
Mejico {m} :: alternative spelling of "test."
Mejico {m} :: test\
"""

# This fails because "adjective form" headwords are ignored right now
def test_headword():
    orig_text="""\
==Spanish==

===Adjective===
{{head|es|adjective form|g=m|apocopate||standard form|alguno}}

# {{lb|es|before the noun}} {{apocopic form of|es|alguno}}; [[some]]
"""

    lang_entry = builder.get_language_entry(orig_text)
    assert lang_entry != ""

    entry = builder.entry_to_text(lang_entry, "algún")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
_____
algún
pos: adj
  meta: {{head|es|adjective form|g=m|apocopate||standard form|alguno}}
  g: m
  gloss: apocopic form of "alguno"; some
    q: before the noun\
"""

    entry = builder.entry_to_mbformat(lang_entry, "algún")

    print("\n".join(entry))
    assert "\n".join(entry)=="""\
algún {adj-meta} :: {{head|es|adjective form|g=m|apocopate||standard form|alguno}}
algún {adj} [before the noun] :: apocopic form of "alguno"; some\
"""


def test_noconj():
    orig_text="""\
==Spanish==

===Verb===
{{es-verb|descans|ar}}

# {{indtr|es|en|.also|.figurative}} to [[sit]], to [[rest]] on
"""

    lang_entry = builder.get_language_entry(orig_text)
    assert lang_entry != ""

    entry = builder.entry_to_text(lang_entry, "test")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
_____
test
pos: v
  meta: {{es-verb|descans|ar}}
  gloss: (also figurative, transitive with en) to sit, to rest on
    q: transitive\
"""

    entry = builder.entry_to_mbformat(lang_entry, "test")

    assert "\n".join(entry) == """\
test {v-meta} :: {{es-verb|descans|ar}}
test {vt} :: (also figurative, transitive with en) to sit, to rest on\
"""


def test_bad_conjugation():
    orig_text="""\
==Spanish==

===Verb===
{{es-verb|decae|ar|pres=decaigo|pret=decaí|part=decaído}}

# to [[decay]]

====Conjugation====
{{es-conj-er|p=caer|de|combined=1}}
"""

    lang_entry = builder.get_language_entry(orig_text)
    assert lang_entry != ""

    entry = builder.entry_to_text(lang_entry, "decaer")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
_____
test
pos: v
  meta: {{es-verb|descans|ar}}
  gloss: (also figurative, transitive with en) to sit, to rest on
    q: transitive\
"""

    entry = builder.entry_to_mbformat(lang_entry, "decaer")

    print("\n".join(entry))
    assert "\n".join(entry) == """\
decaer {v-meta} :: {{es-verb|decae|ar|pres=decaigo|pret=decaí|part=decaído}} {{es-conj-er|p=caer|de|combined=1}}
decaer {v} :: to decay\
"""


def test_abandonar():
    orig_text="""\
==Spanish==
{{root|es|ine-pro|*bʰeh₂-|id=speak}}

===Etymology===
From {{bor|es|fr|abandonner}}, from {{der|es|gem-pro|*bannaną}}.

===Pronunciation===
* {{es-IPA}}

===Verb===
{{es-verb|abandon|ar}}

# to [[abandon]], to [[leave]]
#: {{uxi|es|La '''abandonó''' por otra mujer.|He abandoned her for another woman.}}
# to [[neglect]]
#: {{syn|es|descuidar}}

====Conjugation====
{{es-conj-ar|abandon|combined=1}}

"""

    lang_entry = builder.get_language_entry(orig_text)
    assert lang_entry != ""

    entry = builder.entry_to_text(lang_entry, "abandonar")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
_____
abandonar
pos: v
  meta: {{es-verb|abandon|ar}} {{es-conj-ar|abandon|combined=1}}
  gloss: to abandon, to leave
  gloss: to neglect
    syn: descuidar\
"""

    entry = builder.entry_to_mbformat(lang_entry, "abandonar")

    assert "\n".join(entry) == """\
abandonar {v-meta} :: {{es-verb|abandon|ar}} {{es-conj-ar|abandon|combined=1}}
abandonar {v} :: to abandon, to leave
abandonar {v} | descuidar :: to neglect\
"""


def test_bad_conjugation():
    orig_text="""\
==Spanish==

===Verb===
{{es-verb|decae|ar|pres=decaigo|pret=decaí|part=decaído}}

# to [[decay]]

====Conjugation====
{{es-conj-er|p=caer|de|combined=1}}
"""

    lang_entry = builder.get_language_entry(orig_text)
    assert lang_entry != ""

    entry = builder.entry_to_text(lang_entry, "decaer")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
_____
decaer
pos: v
  meta: {{es-verb|decae|ar|pres=decaigo|pret=decaí|part=decaído}} {{es-conj-er|p=caer|de|combined=1}}
  gloss: to decay\
"""

    entry = builder.entry_to_mbformat(lang_entry, "decaer")

    print("\n".join(entry))
    assert "\n".join(entry) == """\
decaer {v-meta} :: {{es-verb|decae|ar|pres=decaigo|pret=decaí|part=decaído}} {{es-conj-er|p=caer|de|combined=1}}
decaer {v} :: to decay\
"""

def test_f():

    orig_text="""\
==Spanish==

===Pronunciation===
{{qualifier|letter name}}
* {{es-IPA|efe}}
* {{audio|es|letter f es es.flac|Audio (Spain)}}

===Letter===
{{head|es|letter|lower case||upper case|F}}

# {{Latn-def|es|letter|6|ef}}
"""

    lang_entry = builder.get_language_entry(orig_text)
    assert lang_entry != ""

    entry = builder.entry_to_text(lang_entry, "f")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
_____
f
pos: letter
  meta: {{head|es|letter|lower case||upper case|F}}
  gloss: letter: ef\
"""

    entry = builder.entry_to_mbformat(lang_entry, "f")

    print("\n".join(entry))
    assert "\n".join(entry) == """\
f {letter-meta} :: {{head|es|letter|lower case||upper case|F}}
f {letter} :: letter: ef\
"""


def test_ingo():

    orig_text="""\
==Spanish==

===Suffix===
{{es-suffix|f=-inga}}

# {{lb|es|mostly|Bolivia}} A [[diminutive]] suffix
#: ''{{l|es|chica}}'' → (''girl'') ''{{l|es|chiquitinga}}'' (''little girl'')
#: ''{{l|es|señorito}}'' → (''master'') ''{{l|es|señoritingo}}'' (''little brat'')
"""

    lang_entry = builder.get_language_entry(orig_text)
    assert lang_entry != ""

    entry = builder.entry_to_text(lang_entry, "-ingo")

    print("\n".join(entry))
    assert "\n".join(entry) == """\
_____
-ingo
pos: suffix
  meta: {{es-suffix|f=-inga}}
  gloss: A diminutive suffix
    q: chiefly Bolivia\
"""


