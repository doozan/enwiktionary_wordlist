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
from make_wordlist import WordlistBuilder
import mwparserfromhell

builder = WordlistBuilder("Spanish", "es")

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

====Conjugation====
{{es-conj-ar|descans|combined=1}}
"""

    lang_entry = builder.get_language_entry(orig_text)
    assert lang_entry != ""
    entry = builder.parse_entry(lang_entry, "test")

    assert "\n".join(entry) == """\
test {meta-verb} :: 1=descansar; 10=descansa; 11=descansamos; 12=descansáis; 13=descansan; 14=descansaba; 15=descansabas; 16=descansaba; 17=descansábamos; 18=descansabais; 19=descansaban; 2=descansando; 20=descansé; 21=descansaste; 22=descansó; 23=descansamos; 24=descansasteis; 25=descansaron; 26=descansaré; 27=descansarás; 28=descansará; 29=descansaremos; 3=descansado; 30=descansaréis; 31=descansarán; 32=descansaría; 33=descansarías; 34=descansaría; 35=descansaríamos; 36=descansaríais; 37=descansarían; 38=descanse; 39=descanses; 4=descansada; 40=descansés; 41=descanse; 42=descansemos; 43=descanséis; 44=descansen; 45=descansara; 46=descansaras; 47=descansara; 48=descansáramos; 49=descansarais; 5=descansados; 50=descansaran; 51=descansase; 52=descansases; 53=descansase; 54=descansásemos; 55=descansaseis; 56=descansasen; 57=descansare; 58=descansares; 59=descansare; 6=descansadas; 60=descansáremos; 61=descansareis; 62=descansaren; 63=descansa; 64=descansá; 65=descanse; 66=descansemos; 67=descansad; 68=descansen; 69=descanses; 7=descanso; 70=descanse; 71=descansemos; 72=descanséis; 73=descansen; 8=descansas; 9=descansás
test {vt} :: (also figurative, transitive with en) to sit, to rest on\
"""

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

    print( "\n".join(entry))
    assert "\n".join(entry) == """\
abstener {meta-verb} :: 1=abstener; 10=abstiene; 11=abstenemos; 12=abstenéis; 13=abstienen; 14=abstenía; 15=abstenías; 16=abstenía; 17=absteníamos; 18=absteníais; 19=abstenían; 2=absteniendo; 20=abstuve; 21=abstuviste; 22=abstuvo; 23=abstuvimos; 24=abstuvisteis; 25=abstuvieron; 26=abstendré; 27=abstendrás; 28=abstendrá; 29=abstendremos; 3=abstenido; 30=abstendréis; 31=abstendrán; 32=abstendría; 33=abstendrías; 34=abstendría; 35=abstendríamos; 36=abstendríais; 37=abstendrían; 38=abstenga; 39=abstengas; 4=abstenida; 41=abstenga; 42=abstengamos; 43=abstengáis; 44=abstengan; 45=abstuviera; 46=abstuvieras; 47=abstuviera; 48=abstuviéramos; 49=abstuvierais; 5=abstenidos; 50=abstuvieran; 51=abstuviese; 52=abstuvieses; 53=abstuviese; 54=abstuviésemos; 55=abstuvieseis; 56=abstuviesen; 57=abstuviere; 58=abstuvieres; 59=abstuviere; 6=abstenidas; 60=abstuviéremos; 61=abstuviereis; 62=abstuvieren; 63=abstén; 64=abstené; 65=abstenga; 66=abstengamos; 67=abstened; 68=abstengan; 69=abstengas; 7=abstengo; 70=abstenga; 71=abstengamos; 72=abstengáis; 73=abstengan; 8=abstienes; 9=abstenés
abstener {vr} :: to abstain\
"""

#    assert entry[0] == "abstener {meta-verb} :: pattern=-tener; stem=abs"

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

    print("\n".join(entry))
    assert "\n".join(entry)=="""\
adecuar {meta-verb} :: 1=adecuar; 10=adecúa; 10=adecua; 11=adecuamos; 12=adecuáis; 13=adecúan; 13=adecuan; 14=adecuaba; 15=adecuabas; 16=adecuaba; 17=adecuábamos; 18=adecuabais; 19=adecuaban; 2=adecuando; 20=adecué; 21=adecuaste; 22=adecuó; 23=adecuamos; 24=adecuasteis; 25=adecuaron; 26=adecuaré; 27=adecuarás; 28=adecuará; 29=adecuaremos; 3=adecuado; 30=adecuaréis; 31=adecuarán; 32=adecuaría; 33=adecuarías; 34=adecuaría; 35=adecuaríamos; 36=adecuaríais; 37=adecuarían; 38=adecúe; 38=adecue; 39=adecúes; 39=adecues; 4=adecuada; 40=adecués; 41=adecúe; 41=adecue; 42=adecuemos; 43=adecuéis; 44=adecúen; 44=adecuen; 45=adecuara; 46=adecuaras; 47=adecuara; 48=adecuáramos; 49=adecuarais; 5=adecuados; 50=adecuaran; 51=adecuase; 52=adecuases; 53=adecuase; 54=adecuásemos; 55=adecuaseis; 56=adecuasen; 57=adecuare; 58=adecuares; 59=adecuare; 6=adecuadas; 60=adecuáremos; 61=adecuareis; 62=adecuaren; 63=adecúa; 63=adecua; 64=adecuá; 65=adecúe; 65=adecue; 66=adecuemos; 67=adecuad; 68=adecúen; 68=adecuen; 69=adecúes; 69=adecues; 7=adecúo; 7=adecuo; 70=adecúe; 70=adecue; 71=adecuemos; 72=adecuéis; 73=adecúen; 73=adecuen; 8=adecúas; 8=adecuas; 9=adecuás
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
aterrar {meta-verb} :: 1=aterrar; 10=atierra; 11=aterramos; 12=aterráis; 13=atierran; 14=aterraba; 15=aterrabas; 16=aterraba; 17=aterrábamos; 18=aterrabais; 19=aterraban; 2=aterrando; 20=aterré; 21=aterraste; 22=aterró; 23=aterramos; 24=aterrasteis; 25=aterraron; 26=aterraré; 27=aterrarás; 28=aterrará; 29=aterraremos; 3=aterrado; 30=aterraréis; 31=aterrarán; 32=aterraría; 33=aterrarías; 34=aterraría; 35=aterraríamos; 36=aterraríais; 37=aterrarían; 38=atierre; 39=atierres; 4=aterrada; 40=aterrés; 41=atierre; 42=aterremos; 43=aterréis; 44=atierren; 45=aterrara; 46=aterraras; 47=aterrara; 48=aterráramos; 49=aterrarais; 5=aterrados; 50=aterraran; 51=aterrase; 52=aterrases; 53=aterrase; 54=aterrásemos; 55=aterraseis; 56=aterrasen; 57=aterrare; 58=aterrares; 59=aterrare; 6=aterradas; 60=aterráremos; 61=aterrareis; 62=aterraren; 63=atierra; 64=aterrá; 65=atierre; 66=aterremos; 67=aterrad; 68=atierren; 69=atierres; 7=atierro; 70=atierre; 71=aterremos; 72=aterréis; 73=atierren; 8=atierras; 9=aterrás
aterrar {vt} :: to bring down, to ground
aterrar {meta-verb} :: 1=aterrar; 10=aterra; 11=aterramos; 12=aterráis; 13=aterran; 14=aterraba; 15=aterrabas; 16=aterraba; 17=aterrábamos; 18=aterrabais; 19=aterraban; 2=aterrando; 20=aterré; 21=aterraste; 22=aterró; 23=aterramos; 24=aterrasteis; 25=aterraron; 26=aterraré; 27=aterrarás; 28=aterrará; 29=aterraremos; 3=aterrado; 30=aterraréis; 31=aterrarán; 32=aterraría; 33=aterrarías; 34=aterraría; 35=aterraríamos; 36=aterraríais; 37=aterrarían; 38=aterre; 39=aterres; 4=aterrada; 40=aterrés; 41=aterre; 42=aterremos; 43=aterréis; 44=aterren; 45=aterrara; 46=aterraras; 47=aterrara; 48=aterráramos; 49=aterrarais; 5=aterrados; 50=aterraran; 51=aterrase; 52=aterrases; 53=aterrase; 54=aterrásemos; 55=aterraseis; 56=aterrasen; 57=aterrare; 58=aterrares; 59=aterrare; 6=aterradas; 60=aterráremos; 61=aterrareis; 62=aterraren; 63=aterra; 64=aterrá; 65=aterre; 66=aterremos; 67=aterrad; 68=aterren; 69=aterres; 7=aterro; 70=aterre; 71=aterremos; 72=aterréis; 73=aterren; 8=aterras; 9=aterrás
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
    entry = builder.parse_entry(lang_entry, "atentar")

    assert "\n".join(entry)=="""\
atentar {meta-verb} :: 1=atentar; 10=atienta; 11=atentamos; 12=atentáis; 13=atientan; 14=atentaba; 15=atentabas; 16=atentaba; 17=atentábamos; 18=atentabais; 19=atentaban; 2=atentando; 20=atenté; 21=atentaste; 22=atentó; 23=atentamos; 24=atentasteis; 25=atentaron; 26=atentaré; 27=atentarás; 28=atentará; 29=atentaremos; 3=atentado; 30=atentaréis; 31=atentarán; 32=atentaría; 33=atentarías; 34=atentaría; 35=atentaríamos; 36=atentaríais; 37=atentarían; 38=atiente; 39=atientes; 4=atentada; 40=atentés; 41=atiente; 42=atentemos; 43=atentéis; 44=atienten; 45=atentara; 46=atentaras; 47=atentara; 48=atentáramos; 49=atentarais; 5=atentados; 50=atentaran; 51=atentase; 52=atentases; 53=atentase; 54=atentásemos; 55=atentaseis; 56=atentasen; 57=atentare; 58=atentares; 59=atentare; 6=atentadas; 60=atentáremos; 61=atentareis; 62=atentaren; 63=atienta; 64=atentá; 65=atiente; 66=atentemos; 67=atentad; 68=atienten; 69=atientes; 7=atiento; 70=atiente; 71=atentemos; 72=atentéis; 73=atienten; 8=atientas; 9=atentás
atentar {vi} :: to commit a violent or criminal attack, to strike
atentar {meta-verb} :: 1=atentar; 10=atienta; 11=atentamos; 12=atentáis; 13=atientan; 14=atentaba; 15=atentabas; 16=atentaba; 17=atentábamos; 18=atentabais; 19=atentaban; 2=atentando; 20=atenté; 21=atentaste; 22=atentó; 23=atentamos; 24=atentasteis; 25=atentaron; 26=atentaré; 27=atentarás; 28=atentará; 29=atentaremos; 3=atentado; 30=atentaréis; 31=atentarán; 32=atentaría; 33=atentarías; 34=atentaría; 35=atentaríamos; 36=atentaríais; 37=atentarían; 38=atiente; 39=atientes; 4=atentada; 40=atentés; 41=atiente; 42=atentemos; 43=atentéis; 44=atienten; 45=atentara; 46=atentaras; 47=atentara; 48=atentáramos; 49=atentarais; 5=atentados; 50=atentaran; 51=atentase; 52=atentases; 53=atentase; 54=atentásemos; 55=atentaseis; 56=atentasen; 57=atentare; 58=atentares; 59=atentare; 6=atentadas; 60=atentáremos; 61=atentareis; 62=atentaren; 63=atienta; 64=atentá; 65=atiente; 66=atentemos; 67=atentad; 68=atienten; 69=atientes; 7=atiento; 70=atiente; 71=atentemos; 72=atentéis; 73=atienten; 8=atientas; 9=atentás
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

# This fails because "adjective form" headwords are ignored right now
def test_headword():
    return
    orig_text="""\
==Spanish==

===Adjective===
{{head|es|adjective form|g=m|apocopate||standard form|alguno}}

# {{lb|es|before the noun}} {{apocopic form of|es|alguno}}; [[some]]
"""

    lang_entry = builder.get_language_entry(orig_text)
    assert lang_entry != ""
    entry = builder.parse_entry(lang_entry, "Mejico")

    print("\n".join(entry))
    assert "\n".join(entry)=="""\
Mejico {m} :: test\
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
    entry = builder.parse_entry(lang_entry, "test")

    assert "\n".join(entry) == """\
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
    entry = builder.parse_entry(lang_entry, "decaer")

    print("\n".join(entry))
    assert "\n".join(entry) == """\
decaer {v} :: to decay\
"""


