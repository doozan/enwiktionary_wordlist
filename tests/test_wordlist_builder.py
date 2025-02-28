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
from enwiktionary_wordlist.wordlist_builder import WordlistBuilder
from enwiktionary_wordlist.wordlist import Wordlist
import mwparserfromhell

import enwiktionary_templates

builder = WordlistBuilder("Spanish", "es", expand_templates=True)

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

    entry = builder.entry_to_text(orig_text, "chapó")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: v
  meta: {{head|es|verb form}}
  gloss: pret_3s of "chapar"
pos: interj
  meta: {{es-interj}}
  etymology: Borrowed from French "chapeau", from VL "*cappellus". Doublet of the inherited capillo, and of capelo (from Italian), as well as chapeo, also from the French word.
  gloss: Used to express appreciation; hat tip\
"""


def test_bolivariano():

    orig_text="""\
==Spanish==

===Adjective===
{{es-adj|f=bolivariana}}

# [[Bolivarian]] {{gloss|Of or pertaining to [[w:Simón Bolívar|Simón Bolívar]].}}
"""

    entry = builder.entry_to_text(orig_text, "bolivariano")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: adj
  meta: {{es-adj|f=bolivariana}}
  gloss: Bolivarian (Of or pertaining to Simón Bolívar.)\
"""

def test_completada():
    orig_text="""\
==Spanish==

===Pronunciation===
* {{es-IPA}}

===Adjective===
{{head|es|adjective form}}

# {{adj form of|es|completado||f|s}}

===Verb===
{{head|es|past participle form}}

# {{es-verb form of|mood=participle|gen=f|num=s|ending=ar|completar}}

===Noun===
{{es-noun|f}}

# {{lb|es|Chile}} [[party]] or meeting where they eat [[completo]]s ([[hot-dog]]s)
"""

    entry = builder.entry_to_text(orig_text, "completada")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: adj
  meta: {{head|es|adjective form}}
  gloss: feminine singular of "completado"
pos: v
  meta: {{head|es|past participle form}}
  gloss: pp_fs of "completar"
pos: n
  meta: {{es-noun|f}}
  g: f
  gloss: party or meeting where they eat completos (hot-dogs)
    q: Chile\
"""


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

"""

    entry = builder.entry_to_text(orig_text, "yero")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: n
  meta: {{es-noun|m}}
  g: m
  etymology: Syncopated from yervo, from Latin "ervum".
  gloss: any variety of bitter vetch (Vicia ervilia)
    syn: alcarceña
pos: v
  meta: {{head|es|verb form}}
  gloss: pres_1s of "yerar"\
"""


def test_repanoche():
    orig_text="""\
==Spanish== 

===Noun===
{{es-noun|f|-}}

# {{lb|es|Spain}} {{only used in|es|ser la repanocha}}
"""

    entry = builder.entry_to_text(orig_text, "repanoche")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: n
  meta: {{es-noun|f|-}}
  g: f
  gloss: only used in "ser la repanocha"
    q: Spain\
"""

def test_fullentry():
    orig_text="""\
==Spanish==

===Verb===
{{es-verb|descans|ar}}

# {{lb|es|intransitive|also|figurative}} to [[sit]], to [[rest]] on

====Conjugation====
{{es-conj-ar|descans|combined=1}}
"""

    entry = builder.entry_to_text(orig_text, "test")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: v
  meta: {{es-verb|descans|ar}} {{es-conj-ar|descans|combined=1}}
  gloss: to sit, to rest on
    q: intransitive, also figuratively\
"""

def test_noun_forms():
    orig_text="""\
==Spanish==

===Noun===
{{es-noun|mf|youtubers|pl2=youtuber|f=youtuberista|fpl=youtuberistas}}

# A person or a member of a group of people regarded as undesirable
"""

    entry = builder.entry_to_text(orig_text, "youtuber")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: n
  meta: {{es-noun|mf|youtubers|pl2=youtuber|f=youtuberista|fpl=youtuberistas}}
  g: mf
  gloss: A person or a member of a group of people regarded as undesirable\
"""

def test_adj_forms():
    orig_text="""\
==Spanish==

===Adjective===
{{es-adj|pl=youtubers|pl2=youtuber|f=youtuberista|fpl=youtuberistas}}

# A person or a member of a group of people regarded as undesirable
"""

    entry = builder.entry_to_text(orig_text, "youtuber")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: adj
  meta: {{es-adj|pl=youtubers|pl2=youtuber|f=youtuberista|fpl=youtuberistas}}
  gloss: A person or a member of a group of people regarded as undesirable\
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

    entry = builder.entry_to_text(orig_text, "abstener")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: v
  meta: {{es-verb|absten|er|pres=abstengo|pret=abstuve}} {{es-conj-er|abs|p=-tener|combined=1}}
  gloss: to abstain
    q: reflexive\
"""

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

    entry = builder.entry_to_text(orig_text, "adecuar")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: v
  meta: {{es-verb|adecu|ar|pres=adecúo}} {{es-conj-ar|adec||p=u-ú|combined=1}} {{es-conj-ar|adecu|combined=1}}
  gloss: to adapt, adjust
    q: transitive\
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

===Noun===
{{es-noun|m}}

# {{l|en|protector}} {{gloss|a device or mechanism which is designed to protect}}
"""

    entry = builder.entry_to_text(orig_text, "protector")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
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

    entry = builder.entry_to_text(orig_text, "aterrar")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: v
  meta: {{es-verb|aterr|ar|pres=atierro}} {{es-conj-ar|at|rr|p=e-ie|combined=1}}
  etymology: a- + tierra ("land") + -ar
  gloss: to bring down, to ground
    q: transitive
pos: v
  meta: {{es-verb|aterr|ar}} {{es-conj-ar|aterr|combined=1}}
  etymology: From a- + Latin "terreō".
  gloss: to scare
    q: transitive\
"""

def test_atentar():
    orig_text="""\
==Spanish==

===Etymology 1===
From {{der|es|la|attentō}}.

====Verb====
{{es-verb|atent|ar|pres=atiento}}

# {{lb|es|intransitive}} to commit a violent or criminal [[attack]], to [[strike]]

=====Conjugation=====
{{es-conj-ar|at|nt|p=e-ie|combined=1}}

===Etymology 2===
{{rfe|es}}

====Verb====
{{es-verb|atent|ar}}

# {{lb|es|transitive|obsolete}} to [[touch]]
# {{synonym of|es|tentar}}

=====Conjugation=====
{{es-conj-ar|at|nt|p=e-ie|combined=1}}
"""

    entry = builder.entry_to_text(orig_text, "atentar")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: v
  meta: {{es-verb|atent|ar|pres=atiento}} {{es-conj-ar|at|nt|p=e-ie|combined=1}}
  etymology: From Latin "attentō".
  gloss: to commit a violent or criminal attack, to strike
    q: intransitive
pos: v
  meta: {{es-verb|atent|ar}} {{es-conj-ar|at|nt|p=e-ie|combined=1}}
  gloss: to touch
    q: transitive, obsolete
  gloss: synonym of "tentar"\
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

    entry = builder.entry_to_text(orig_text, "billón")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: num
  meta: {{es-noun|m|billones}}
  g: m
  gloss: 10^12; a trillion (short system)
  gloss: 10^9: a billion (long system)
    q: obsolete\
"""

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


    entry = builder.entry_to_text(orig_text, "aquestos")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: determiner
  meta: {{head|es|determiner form}}
  gloss: masculine plural of "aqueste"
pos: pron
  meta: {{head|es|pronoun form}}
  gloss: masculine plural of "aqueste"\
"""

def test_robot():
    orig_text="""\
==Spanish==

===Noun===
{{es-noun|m}}

# {{l|en|robot}}
"""

    entry = builder.entry_to_text(orig_text, "robot")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: n
  meta: {{es-noun|m}}
  g: m
  gloss: robot\
"""

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

    entry = builder.entry_to_text(orig_text, "angla")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: adj
  meta: {{head|es|adjective form|g=f-s}}
  g: f-s
  gloss: feminine singular of "anglo"
pos: n
  meta: {{es-noun|f|m=anglo}}
  g: f
  gloss: female equivalent of "anglo"\
"""

def test_cherry():
    orig_text="""\
==Spanish==

===Noun===
{{es-noun|m|+|pl2=cherries}}

# {{l|en|cherry tomato}}
"""

    entry = builder.entry_to_text(orig_text, "cherry")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: n
  meta: {{es-noun|m|+|pl2=cherries}}
  g: m
  gloss: cherry tomato\
"""

def test_torpon():
    orig_text="""\
==Spanish==

===Adjective===
{{es-adj|f=torpona|mpl=torpones}}

# [[clumsy]]
"""

    entry = builder.entry_to_text(orig_text, "torpón")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: adj
  meta: {{es-adj|f=torpona|mpl=torpones}}
  gloss: clumsy\
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

    entry = builder.entry_to_text(orig_text, "Mejico")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: prop
  meta: {{es-proper noun|m}}
  g: m
  gloss: alternative spelling of "México"
    q: Spain
  gloss: alternative spelling of "test."
  gloss: test\
"""

# This fails because "adjective form" headwords are ignored right now
def test_headword():
    orig_text="""\
==Spanish==

===Adjective===
{{head|es|adjective form|g=m|apocopate||standard form|alguno}}

# {{lb|es|before the noun}} {{apocopic form of|es|alguno}}; [[some]]
"""

    entry = builder.entry_to_text(orig_text, "algún")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: adj
  meta: {{head|es|adjective form|g=m|apocopate||standard form|alguno}}
  g: m
  gloss: apocopic form of "alguno"; some
    q: before the noun\
"""

def test_noconj():
    orig_text="""\
==Spanish==

===Verb===
{{es-verb|descans|ar}}

# {{lb|es|intransitive|also|figurative}} to [[sit]], to [[rest]] on
"""

    entry = builder.entry_to_text(orig_text, "test")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: v
  meta: {{es-verb|descans|ar}}
  gloss: to sit, to rest on
    q: intransitive, also figuratively\
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

    entry = builder.entry_to_text(orig_text, "decaer")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: v
  meta: {{es-verb|descans|ar}}
  gloss: (also figuratively, transitive with en) to sit, to rest on
    q: transitive\
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

    entry = builder.entry_to_text(orig_text, "abandonar")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: v
  meta: {{es-verb|abandon|ar}} {{es-conj-ar|abandon|combined=1}}
  etymology: From French "abandonner", from Proto-Germanic "*bannaną".
  gloss: to abandon, to leave
  gloss: to neglect
    syn: descuidar\
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

    entry = builder.entry_to_text(orig_text, "decaer")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: v
  meta: {{es-verb|decae|ar|pres=decaigo|pret=decaí|part=decaído}} {{es-conj-er|p=caer|de|combined=1}}
  gloss: to decay\
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

    entry = builder.entry_to_text(orig_text, "f")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: letter
  meta: {{head|es|letter|lower case||upper case|F}}
  gloss: letter: ef\
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

    entry = builder.entry_to_text(orig_text, "-ingo")

    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: suffix
  meta: {{es-suffix|f=-inga}}
  gloss: A diminutive suffix
    q: chiefly Bolivia\
"""

def test_usage():
    orig_text="""\
==Spanish==

===Noun===
{{es-noun|m}}

# test

====Usage notes====

# test {{gloss|test}}

----
"""

    entry = builder.entry_to_text(orig_text, "test")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: n
  meta: {{es-noun|m}}
  g: m
  usage: test (test)
  gloss: test\
"""

def test_usage2():
    orig_text="""\
==Spanish==

===Etymology===
Form of {{m|es|-cilla}}, rebracketed from words ending in ''-e''.

===Suffix===
{{es-noun|f}}{{cln|es|diminutive suffixes}}

# {{alternative form of|es|-ecillo}}; {{n-g|added to feminine nouns to form diminutives}}
#: {{sufex|es|tienda|t1=shop|tiendecilla|t2=little shop}}
#: {{sufex|es|red|t1=net|redecilla|t2=small net; hairnet; reticulum}}
#: {{sufex|es|diosa|t1=goddess|diosecilla|t2=minor goddess}}
#: {{sufex|es|mano|t1=hand|manecilla|t2=hand (of a clock); needle (of an instrument); doorknob}}

====Usage notes====
* If the noun has a final vowel (usually {{m|es|-a}}), it is dropped before adding {{m|es||-ecilla}}.
* In most cases, {{m|es||-ecilla}} is used simply to indicate a small or endeared thing, without changing the basic meaning of the noun; however, in some cases, it is used to effect a greater change in meaning, as shown in the examples above.
----
"""

    entry = builder.entry_to_text(orig_text, "-ecilla")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: suffix
  meta: {{es-noun|f}}
  g: f
  usage: * If the noun has a final vowel (usually -a), it is dropped before adding -ecilla.\\n* In most cases, -ecilla is used simply to indicate a small or endeared thing, without changing the basic meaning of the noun; however, in some cases, it is used to effect a greater change in meaning, as shown in the examples above.
  etymology: Form of -cilla, rebracketed from words ending in -e.
  gloss: alternative form of "-ecillo"; added to feminine nouns to form diminutives\
"""

def test_hubert():
    orig_text="""\
==Spanish==

===Proper noun===
{{es-proper noun|m}}

# [[Hubert]]
"""

    entry = builder.entry_to_text(orig_text, "Hubert")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: prop
  meta: {{es-proper noun|m}}
  g: m
  gloss: Hubert\
"""

def test_abajo():
    orig_text="""\
==Spanish==

===Alternative forms===
* {{alter|es|abaxo||obsolete}}

===Pronunciation===
{{es-IPA}}
* {{audio|es|Es-am-lat-abajo.ogg|Audio (Latin America)}}

===Etymology 1===
{{compound|es|a|t1=to|bajo|t2=down}}. Cognate to {{cog|fr|à bas}}, which is also used in sense “[[down with]]”. Compare {{cog|en|abase}} and {{inh|nap|VL.|[[ad]] [[bassum]]}}.

====Adverb====
{{es-adv}}

# [[down]]
#: {{syn|es|ayuso|q1=obsolete|yuso|q2=obsolete}}
#: {{ant|es|arriba}}
# [[downstairs]]
#: {{ux|es|'''Abajo''' están la cocina y el salón.|The kitchen and lounge are '''downstairs'''.}}
# [[below]]

=====Derived terms=====
{{der3|es|
|abajeño
|boca abajo
|cuesta abajo
|de abajo
|echar abajo
|irse por la pata abajo
|para arriba y para abajo
|para abajo
|quark abajo
|venirse abajo
|hacia abajo
}}

=====Related terms=====
* {{l|es|bajar}}

====Interjection====
{{head|es|interjection}}

# {{lb|es|figuratively}} [[down with]], away with
#: {{ant|es|viva}}
#* '''1810''', {{w|Miguel Hidalgo y Costilla}}, ''{{w|Grito de Dolores}},'' September 16th:
#*: ¡Viva la Virgen de Guadalupe!, ¡'''Abajo''' el mal gobierno!

===Etymology 2===
{{nonlemma}}

====Verb====
{{head|es|verb form}}

# {{es-verb form of|ending=ar|mood=indicative|tense=present|pers=1|number=singular|abajar}}

===Further reading===
* {{R:DRAE}}
"""

    entry = builder.entry_to_text(orig_text, "abajo")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: adv
  meta: {{es-adv}}
  etymology: a ("to") + bajo ("down"). Cognate to French "à bas", which is also used in sense “down with”. Compare English "abase" and VL "ad bassum".
  gloss: down
    syn: (obsolete) ayuso; (obsolete) yuso
  gloss: downstairs
  gloss: below
pos: interj
  meta: {{head|es|interjection}}
  etymology: a ("to") + bajo ("down"). Cognate to French "à bas", which is also used in sense “down with”. Compare English "abase" and VL "ad bassum".
  gloss: down with, away with
    q: figuratively
pos: v
  meta: {{head|es|verb form}}
  gloss: pres_1s of "abajar"\
"""


def test_ll():
    orig_text="""\
==Spanish==

===Alternative forms===
* {{alter|es|Ꝇ||ligature}}

===Letter===
{{head|es|letter|upper case||lower case|ll|mixed case|Ll}}

# ''[[elle]]'', the 14th letter of the Spanish alphabet, after ''[[L]]'' and before ''[[M]]''

====Usage notes====
Since 1994, this letter is treated as two separate ''[[L]]'' letters for collation purposes only. In 2010, this letter was officially dropped by the [[RAE]] from the Spanish alphabet.

[[Category:mul:Hundred]]
"""

    entry = builder.entry_to_text(orig_text, "LL")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: letter
  meta: {{head|es|letter|upper case||lower case|ll|mixed case|Ll}}
  usage: Since 1994, this letter is treated as two separate L letters for collation purposes only. In 2010, this letter was officially dropped by the RAE from the Spanish alphabet.
  gloss: elle, the 14th letter of the Spanish alphabet, after L and before M\
"""

def test_malinchista():

    orig_text="""\
==Spanish==

===Etymology===
{{named-after|es|La Malinche|wplink==}} {{suffix|es||ista}}.

===Noun===
{{es-noun|mf}}

# {{lb|es|Mexico|pejorative}} One who has a preference or infatuation for [[foreign]] (non-Mexican) culture, products or people
#* '''1972''', Manuel Garza Toba, ''Hojas sueltas de París: crónica'', page 152:
#*: —'''Malinchista'''! —¡Ah, te habías tardado! Desde que se inventó esa palabrita ya no podemos mirar fuera de México, porque nos sellan con … —Bueno, mira, si quieres, soy '''malinchista''' pues; pero ten en cuenta que me lo dices sólo por nada.

====Related terms====
* {{l|es|malinche}}
* {{l|es|malinchismo}}

===Further reading===
* {{R:DRAE}}
"""

    entry = builder.entry_to_text(orig_text, "malinchista")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: n
  meta: {{es-noun|mf}}
  g: mf
  etymology: Named after La Malinche  + -ista.
  gloss: One who has a preference or infatuation for foreign (non-Mexican) culture, products or people
    q: Mexico, derogatory\
"""

def test_guia():

    orig_text="""\
==Spanish==

===Etymology===
Probably from the verb {{m|es|guiar}}. Cf. also {{cog|fr|guide}} ({{cog|fro|guie}}), {{cog|it|guida}}.

===Pronunciation===
{{es-IPA}}
* {{rhymes|es|ia}}

===Noun===
{{es-noun|mf}}

# [[guide]] {{gloss|person}}

====Usage notes====
{{es-note-noun-common-gender-a}}

===Noun===
{{es-noun|f}}

# [[guidebook]]
# [[directory]]
# [[cocket]]

====Derived terms====
{{der3|es
|audioguía
|guía de viaje
|guía turística
|guía turístico
|perro guía
}}

====Descendants====
* {{desc|tl|giya|bor=1}}

===Verb===
{{head|es|verb form}}

# {{es-verb form of|ending=ar|mood=imperative|sense=affirmative|pers=2|formal=no|number=singular|guiar}}
# {{es-verb form of|ending=ar|mood=indicative|tense=present|pers=2|formal=yes|number=singular|guiar}}
# {{es-verb form of|ending=ar|mood=indicative|tense=present|pers=3|number=singular|guiar}}

{{cln|es|nouns with irregular gender}}
"""

    entry = builder.entry_to_text(orig_text, "test")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: n
  meta: {{es-noun|mf}}
  g: mf
  usage: The noun test is like several other Spanish nouns with a human referent and ending in a. The masculine articles and adjectives are used when the referent is known to be male, a group of males, a group of mixed or unknown gender, or an individual of unknown or unspecified gender. The feminine articles and adjectives are used if the referent is known to be female or a group of females.
  etymology: Probably from the verb guiar. Cf. also French "guide" (Old French "guie"), Italian "guida".
  gloss: guide (person)
pos: n
  meta: {{es-noun|f}}
  g: f
  etymology: Probably from the verb guiar. Cf. also French "guide" (Old French "guie"), Italian "guida".
  gloss: guidebook
  gloss: directory
  gloss: cocket
pos: v
  meta: {{head|es|verb form}}
  etymology: Probably from the verb guiar. Cf. also French "guide" (Old French "guie"), Italian "guida".
  gloss: imp_2s of "guiar"
  gloss: pres_2sf of "guiar"
  gloss: pres_3s of "guiar"\
"""

def test_usagenotes_nested():

    orig_text="""\
==Spanish==

===Noun===
{{es-noun|mf}}

# [[guide]] {{gloss|person}}

====Usage notes====
test usage notes

===Noun===
{{es-noun|f}}

# [[guidebook]]
"""

    entry = builder.entry_to_text(orig_text, "test")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: n
  meta: {{es-noun|mf}}
  g: mf
  usage: test usage notes
  gloss: guide (person)
pos: n
  meta: {{es-noun|f}}
  g: f
  gloss: guidebook\
"""

def test_usagenotes_l3():

    orig_text="""\
==Spanish==

===Noun===
{{es-noun|mf}}

# [[guide]] {{gloss|person}}

===Usage notes===
test usage notes

===Noun===
{{es-noun|f}}

# [[guidebook]]
"""

    entry = builder.entry_to_text(orig_text, "test")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: n
  meta: {{es-noun|mf}}
  g: mf
  usage: test usage notes
  gloss: guide (person)
pos: n
  meta: {{es-noun|f}}
  g: f
  gloss: guidebook\
"""

def test_usagenotes_l3_multi():

    orig_text="""\
==Spanish==

===Noun===
{{es-noun|mf}}

# [[guide]] {{gloss|person}}

===Adjective===
{{es-adj}}

# [[guide]]

===Usage notes===
test usage notes
"""

    entry = builder.entry_to_text(orig_text, "test")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: n
  meta: {{es-noun|mf}}
  g: mf
  usage: test usage notes
  gloss: guide (person)
pos: adj
  meta: {{es-adj}}
  usage: test usage notes
  gloss: guide\
"""

def test_usagenotes_l3_multi_nested():

    orig_text="""\
==Spanish==

===Noun===
{{es-noun|mf}}

# [[guide]] {{gloss|person}}

===Adjective===
{{es-adj}}

# [[guide]]

====Usage notes====
test usage notes
"""

    entry = builder.entry_to_text(orig_text, "test")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: n
  meta: {{es-noun|mf}}
  g: mf
  gloss: guide (person)
pos: adj
  meta: {{es-adj}}
  usage: test usage notes
  gloss: guide\
"""

def test_ety_multi():

    orig_text="""\
==Spanish==

===Etymology 1===
From {{inh|es|la|est}}, from {{inh|es|itc-pro|*est}}, from {{inh|es|ine-pro|*h₁ésti}}. Cognate with {{cog|sa|अस्ति|tr=ásti}}, {{cog|en|is}}.

===Verb===
{{head|es|verb form}}

# {{es-verb form of|mood=ind|tense=pres|num=s|pers=2|formal=y|ending=er|ser}}
# {{es-verb form of|mood=ind|tense=pres|num=s|pers=3|ending=er|ser|nodot=1}}; (he/she/it/one) [[is]]

===Etymology 2===

===Noun===
{{head|es|noun form}}

# {{plural of|es|e}}
"""

    entry = builder.entry_to_text(orig_text, "test")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: v
  meta: {{head|es|verb form}}
  etymology: From Latin "est", from Proto-Italic "*est", from Proto-Indo-European "*h₁ésti". Cognate with Sanskrit "अस्ति", English "is".
  gloss: pres_2sf of "ser"
  gloss: pres_3s of "ser"; (he/she/it/one) is
pos: n
  meta: {{head|es|noun form}}
  gloss: plural of "e"\
"""

def test_noun_multi():

    orig_text="""\
==Spanish==

===Noun===
{{es-noun|f}}

# [[blanket]], [[coverlet]]

===Noun===
{{es-noun|f|m=1}}

# {{female equivalent of|es|chivo}}; young female [[goat]], [[kid]]
"""

    entry = builder.entry_to_text(orig_text, "test")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: n
  meta: {{es-noun|f}}
  g: f
  gloss: blanket, coverlet
pos: n
  meta: {{es-noun|f|m=1}}
  g: f
  gloss: female equivalent of "chivo"; young female goat, kid\
"""

def test_is_generated():

    wordlist_data="""\
_____
morena
pos: n
  meta: {{es-noun|f}}
  g: f
  etymology: See moreno. Ultimately related to English "Moor".
  gloss: female equivalent of "moreno"
pos: adj
  meta: {{head|es|adjective form}}
  etymology: See moreno. Ultimately related to English "Moor".
  gloss: feminine singular of "moreno"
pos: n
  meta: {{es-noun|f}}
  g: f
  etymology: from Latin "muraena" (“sea eel, lamprey”), from Ancient Greek "σμυραινα", from σμυρος (“sea eel”).
  gloss: moray
    q: zoology
_____
morenas
pos: adj
  meta: {{head|es|adjective form}}
  gloss: feminine plural of "moreno"
pos: n
  meta: {{head|es|noun form|g=f-p}}
  g: f-p
  gloss: plural of "morena"
_____
moreno
pos: adj
  meta: {{es-adj|sup=morenísimo}}
  etymology: From moro + -eno.
  gloss: dark colored
  gloss: dark-skinned, tan
  gloss: dark-haired
pos: n
  meta: {{es-noun|m|f=morena}}
  g: m
  etymology: From moro + -eno.
  gloss: a dark-skinned or tan person
  gloss: a person with dark-hair
_____
morenos
pos: adj
  meta: {{head|es|adjective form}}
  gloss: masculine plural of "moreno"
pos: n
  meta: {{head|es|noun form|g=m-p}}
  g: m-p
  gloss: plural of "moreno"\
"""

    expected = """\
_____
morena
pos: n
  meta: {{es-noun|f}}
  g: f
  etymology: See moreno. Ultimately related to English "Moor".
  gloss: female equivalent of "moreno"
pos: n
  meta: {{es-noun|f}}
  g: f
  etymology: from Latin "muraena" (“sea eel, lamprey”), from Ancient Greek "σμυραινα", from σμυρος (“sea eel”).
  gloss: moray
    q: zoology
_____
moreno
pos: adj
  meta: {{es-adj|sup=morenísimo}}
  etymology: From moro + -eno.
  gloss: dark colored
  gloss: dark-skinned, tan
  gloss: dark-haired
pos: n
  meta: {{es-noun|m|f=morena}}
  g: m
  etymology: From moro + -eno.
  gloss: a dark-skinned or tan person
  gloss: a person with dark-hair\
"""

    wordlist_full = Wordlist(wordlist_data.splitlines())

    res = "\n".join(WordlistBuilder.from_wordlist(wordlist_full, exclude_generated=False, exclude_empty=False))
    assert res == wordlist_data

    res = "\n".join(WordlistBuilder.from_wordlist(wordlist_full, exclude_generated=True, exclude_empty=True))
    print(res)
    assert res == expected


def test_participles():

    # participles should be considered verb forms and should pass is_generated()

    hablado_wiki = """\
==Spanish==
===Participle===
{{es-past participle}}

# {{past participle of|es|hablar}}
"""
    hablado_data = """\
pos: part
  meta: {{es-past participle}}
  gloss: past participle of "hablar"\
"""
    entry = builder.entry_to_text(hablado_wiki, "hablado")
    print("\n".join(entry))
    assert "\n".join(entry) == hablado_data


    hablados_wiki = """\
==Spanish==
===Participle===
{{es-past participle}}

# {{masculine plural of|es|hablado}}
"""
    hablados_data = """\
pos: part
  meta: {{es-past participle}}
  gloss: masculine plural of "hablado"\
"""
    entry = builder.entry_to_text(hablados_wiki, "hablados")
    print("\n".join(entry))
    assert "\n".join(entry) == hablados_data


    hablada_wiki = """\
==Spanish==
===Participle===
{{es-past participle}}

# {{feminine singular of|es|hablado}}
"""
    hablada_data = """\
pos: part
  meta: {{es-past participle}}
  gloss: feminine singular of "hablado"\
"""
    entry = builder.entry_to_text(hablada_wiki, "hablada")
    print("\n".join(entry))
    assert "\n".join(entry) == hablada_data


    habladas_wiki = """\
==Spanish==
===Participle===
{{es-past participle}}

# {{feminine plural of|es|hablado}}
"""
    habladas_data = """\
pos: part
  meta: {{es-past participle}}
  gloss: feminine plural of "hablado"\
"""
    entry = builder.entry_to_text(habladas_wiki, "habladas")
    print("\n".join(entry))
    assert "\n".join(entry) == habladas_data


    hablar_data = """\
pos: v
  meta: {{es-verb}} {{es-conj}}
  gloss: to talk\
"""

    wordlist_data=f"""\
_____
hablada
{hablada_data}
_____
habladas
{habladas_data}
_____
hablado
{hablado_data}
_____
hablados
{hablados_data}
_____
hablar
{hablar_data}\
"""

    expected = f"""\
_____
hablar
{hablar_data}\
"""
    wordlist_full = Wordlist(wordlist_data.splitlines())

    res = "\n".join(WordlistBuilder.from_wordlist(wordlist_full, exclude_generated=False, exclude_empty=False))
    print(wordlist_data)
    assert res == wordlist_data

    res = "\n".join(WordlistBuilder.from_wordlist(wordlist_full, exclude_generated=True, exclude_empty=True))
    print(res)
    assert res == expected


def test_empty_verb():

    # Empty verbs should generate text, but that text may be ignored if
    # --exclude-empty is used

    orig_text="""\
==Spanish==

===Etymology===
{{af|es|a-|mojama|-ar}}

===Pronunciation===
{{es-IPA}}

===Verb===
{{es-verb}}

# {{rfdef|es}}

====Conjugation====
{{es-conj|nocomb=1}}

===Further reading===
* {{R:DRAE}}
"""

    entry = builder.entry_to_text(orig_text, "bolivariano")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: v
  meta: {{es-verb}} {{es-conj|nocomb=1}}
  etymology: a- + mojama + -ar\
"""

def test_senseid():
    orig_text="""\
==Spanish==

===Noun===
{{es-noun}}

# {{senseid|es|taxonomy}} {{lb|es|countable|biology|taxonomy}} A [[category]] in the [[classification]] of [[organism]]s, ranking below [[order]] and above [[genus]]; a [[taxon]] at that rank.
"""

    entry = builder.entry_to_text(orig_text, "family")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: n
  meta: {{es-noun}}
  gloss: A category in the classification of organisms, ranking below order and above genus; a taxon at that rank
    id: taxonomy
    q: countable, biology, taxonomy\
"""



def test_multi_past_participle():
    orig_text="""\
==Spanish==

===Verb===
{{es-verb}}

# to [[refry]]

====Conjugation====
{{es-conj|nocomb=1}}
"""

    entry = builder.entry_to_text(orig_text, "refreír")
    print("\n".join(entry))
    assert "\n".join(entry) == """\
pos: v
  meta: {{es-verb}} {{es-conj|nocomb=1}}
  gloss: to refry\
"""

def test_subsense():
    orig_text="""\
==Spanish==

===Noun===
{{es-noun|m}}

# sense 1
## {{lb|es|Chile}} subsense 1
## subsense 2
# sense 2
"""


    wordlist_data = """\
_____
test
pos: n
  meta: {{es-noun|m}}
  g: m
  gloss: sense 1
    _gloss: subsense 1
      q: Chile
    _gloss: subsense 2
  gloss: sense 2\
"""

    entry = builder.entry_to_text(orig_text, "refreír")
    print("\n".join(entry))
    entry = ["_____", "test"] + entry
    assert "\n".join(entry) == wordlist_data


    wordlist = Wordlist(wordlist_data.splitlines())

    new_entry = next(WordlistBuilder.from_wordlist(wordlist, exclude_generated=False, exclude_empty=False))
    print(new_entry)
    assert new_entry == wordlist_data
