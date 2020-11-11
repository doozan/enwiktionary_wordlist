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
bolivariano {adj-forms} :: f=bolivariana; fpl=bolivarianas; pl=bolivarianos
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
completada {noun-forms} :: pl=completadas
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
yero {noun-forms} :: pl=yeros
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
test {verb-forms} :: 1=descansar; 10=descansa; 11=descansamos; 12=descansáis; 13=descansan; 14=descansaba; 15=descansabas; 16=descansaba; 17=descansábamos; 18=descansabais; 19=descansaban; 2=descansando; 20=descansé; 21=descansaste; 22=descansó; 23=descansamos; 24=descansasteis; 25=descansaron; 26=descansaré; 27=descansarás; 28=descansará; 29=descansaremos; 3=descansado; 30=descansaréis; 31=descansarán; 32=descansaría; 33=descansarías; 34=descansaría; 35=descansaríamos; 36=descansaríais; 37=descansarían; 38=descanse; 39=descanses; 4=descansada; 40=descansés; 41=descanse; 42=descansemos; 43=descanséis; 44=descansen; 45=descansara; 46=descansaras; 47=descansara; 48=descansáramos; 49=descansarais; 5=descansados; 50=descansaran; 51=descansase; 52=descansases; 53=descansase; 54=descansásemos; 55=descansaseis; 56=descansasen; 57=descansare; 58=descansares; 59=descansare; 6=descansadas; 60=descansáremos; 61=descansareis; 62=descansaren; 63=descansa; 64=descansá; 65=descanse; 66=descansemos; 67=descansad; 68=descansen; 69=descanses; 7=descanso; 70=descanse; 71=descansemos; 72=descanséis; 73=descansen; 8=descansas; 9=descansás; ger_acc-dat_1=descansándómela; ger_acc-dat_1=descansándómelas; ger_acc-dat_1=descansándómelo; ger_acc-dat_1=descansándómelos; ger_acc-dat_2=descansándótela; ger_acc-dat_2=descansándótelas; ger_acc-dat_2=descansándótelo; ger_acc-dat_2=descansándótelos; ger_acc-dat_3=descansándola; ger_acc-dat_3=descansándose; ger_acc-dat_3=descansándólola; ger_acc-dat_3=descansándólolas; ger_acc-dat_3=descansándólolo; ger_acc-dat_3=descansándólolos; ger_acc-dat_4=descansándónosla; ger_acc-dat_4=descansándónoslas; ger_acc-dat_4=descansándónoslo; ger_acc-dat_4=descansándónoslos; ger_acc-dat_5=descansándóosla; ger_acc-dat_5=descansándóoslas; ger_acc-dat_5=descansándóoslo; ger_acc-dat_5=descansándóoslos; ger_acc-dat_6=descansándolas; ger_acc-dat_6=descansándose; ger_acc-dat_6=descansándólosla; ger_acc-dat_6=descansándóloslas; ger_acc-dat_6=descansándóloslo; ger_acc-dat_6=descansándóloslos; ger_acc-dat_7=descansándósela; ger_acc-dat_7=descansándóselas; ger_acc-dat_7=descansándóselo; ger_acc-dat_7=descansándóselos; ger_acc_1=descansándome; ger_acc_2=descansándote; ger_acc_3=descansándolo; ger_acc_4=descansándonos; ger_acc_5=descansándoos; ger_acc_6=descansándolos; ger_acc_7=descansándose; ger_dat_1=descansándome; ger_dat_2=descansándote; ger_dat_3=descansándole; ger_dat_3=descansándose; ger_dat_4=descansándonos; ger_dat_5=descansándoos; ger_dat_6=descansándoles; ger_dat_6=descansándose; imp_1p_acc-dat_2=descansémóstela; imp_1p_acc-dat_2=descansémóstelas; imp_1p_acc-dat_2=descansémóstelo; imp_1p_acc-dat_2=descansémóstelos; imp_1p_acc-dat_3=descansémosla; imp_1p_acc-dat_3=descansémóslola; imp_1p_acc-dat_3=descansémóslolas; imp_1p_acc-dat_3=descansémóslolo; imp_1p_acc-dat_3=descansémóslolos; imp_1p_acc-dat_4=descansémónosla; imp_1p_acc-dat_4=descansémónoslas; imp_1p_acc-dat_4=descansémónoslo; imp_1p_acc-dat_4=descansémónoslos; imp_1p_acc-dat_5=descansémóosla; imp_1p_acc-dat_5=descansémóoslas; imp_1p_acc-dat_5=descansémóoslo; imp_1p_acc-dat_5=descansémóoslos; imp_1p_acc-dat_6=descansémoslas; imp_1p_acc-dat_6=descansémóslosla; imp_1p_acc-dat_6=descansémósloslas; imp_1p_acc-dat_6=descansémósloslo; imp_1p_acc-dat_6=descansémósloslos; imp_1p_acc_2=descansémoste; imp_1p_acc_3=descansémoslo; imp_1p_acc_4=descansémonos; imp_1p_acc_5=descansémoos; imp_1p_acc_6=descansémoslos; imp_1p_dat_2=descansémoste; imp_1p_dat_3=descansémosle; imp_1p_dat_4=descansémonos; imp_1p_dat_5=descansémoos; imp_1p_dat_6=descansémosles; imp_f2p_acc-dat_1=descánsénmela; imp_f2p_acc-dat_1=descánsénmelas; imp_f2p_acc-dat_1=descánsénmelo; imp_f2p_acc-dat_1=descánsénmelos; imp_f2p_acc-dat_3=descánsenla; imp_f2p_acc-dat_3=descánsénlola; imp_f2p_acc-dat_3=descánsénlolas; imp_f2p_acc-dat_3=descánsénlolo; imp_f2p_acc-dat_3=descánsénlolos; imp_f2p_acc-dat_4=descánsénnosla; imp_f2p_acc-dat_4=descánsénnoslas; imp_f2p_acc-dat_4=descánsénnoslo; imp_f2p_acc-dat_4=descánsénnoslos; imp_f2p_acc-dat_6=descánsenlas; imp_f2p_acc-dat_6=descánsense; imp_f2p_acc-dat_6=descánsénlosla; imp_f2p_acc-dat_6=descánsénloslas; imp_f2p_acc-dat_6=descánsénloslo; imp_f2p_acc-dat_6=descánsénloslos; imp_f2p_acc-dat_7=descánsénsela; imp_f2p_acc-dat_7=descánsénselas; imp_f2p_acc-dat_7=descánsénselo; imp_f2p_acc-dat_7=descánsénselos; imp_f2p_acc_1=descánsenme; imp_f2p_acc_3=descánsenlo; imp_f2p_acc_4=descánsennos; imp_f2p_acc_6=descánsenlos; imp_f2p_acc_7=descánsense; imp_f2p_dat_1=descánsenme; imp_f2p_dat_3=descánsenle; imp_f2p_dat_4=descánsennos; imp_f2p_dat_6=descánsenles; imp_f2p_dat_6=descánsense; imp_f2s_acc-dat_1=descánsémela; imp_f2s_acc-dat_1=descánsémelas; imp_f2s_acc-dat_1=descánsémelo; imp_f2s_acc-dat_1=descánsémelos; imp_f2s_acc-dat_3=descánsela; imp_f2s_acc-dat_3=descánsese; imp_f2s_acc-dat_3=descánsélola; imp_f2s_acc-dat_3=descánsélolas; imp_f2s_acc-dat_3=descánsélolo; imp_f2s_acc-dat_3=descánsélolos; imp_f2s_acc-dat_4=descánsénosla; imp_f2s_acc-dat_4=descánsénoslas; imp_f2s_acc-dat_4=descánsénoslo; imp_f2s_acc-dat_4=descánsénoslos; imp_f2s_acc-dat_6=descánselas; imp_f2s_acc-dat_6=descánsélosla; imp_f2s_acc-dat_6=descánséloslas; imp_f2s_acc-dat_6=descánséloslo; imp_f2s_acc-dat_6=descánséloslos; imp_f2s_acc-dat_7=descánsésela; imp_f2s_acc-dat_7=descánséselas; imp_f2s_acc-dat_7=descánséselo; imp_f2s_acc-dat_7=descánséselos; imp_f2s_acc_1=descánseme; imp_f2s_acc_3=descánselo; imp_f2s_acc_4=descánsenos; imp_f2s_acc_6=descánselos; imp_f2s_acc_7=descánsese; imp_f2s_dat_1=descánseme; imp_f2s_dat_3=descánsele; imp_f2s_dat_3=descánsese; imp_f2s_dat_4=descánsenos; imp_f2s_dat_6=descánseles; imp_i2p_acc-dat_1=descansádmela; imp_i2p_acc-dat_1=descansádmelas; imp_i2p_acc-dat_1=descansádmelo; imp_i2p_acc-dat_1=descansádmelos; imp_i2p_acc-dat_3=descansadla; imp_i2p_acc-dat_3=descansádlola; imp_i2p_acc-dat_3=descansádlolas; imp_i2p_acc-dat_3=descansádlolo; imp_i2p_acc-dat_3=descansádlolos; imp_i2p_acc-dat_4=descansádnosla; imp_i2p_acc-dat_4=descansádnoslas; imp_i2p_acc-dat_4=descansádnoslo; imp_i2p_acc-dat_4=descansádnoslos; imp_i2p_acc-dat_5=descansáosla; imp_i2p_acc-dat_5=descansáoslas; imp_i2p_acc-dat_5=descansáoslo; imp_i2p_acc-dat_5=descansáoslos; imp_i2p_acc-dat_6=descansadlas; imp_i2p_acc-dat_6=descansádlosla; imp_i2p_acc-dat_6=descansádloslas; imp_i2p_acc-dat_6=descansádloslo; imp_i2p_acc-dat_6=descansádloslos; imp_i2p_acc-dat_7=descansádosla; imp_i2p_acc-dat_7=descansádoslas; imp_i2p_acc-dat_7=descansádoslo; imp_i2p_acc-dat_7=descansádoslos; imp_i2p_acc_1=descansadme; imp_i2p_acc_3=descansadlo; imp_i2p_acc_4=descansadnos; imp_i2p_acc_5=descansaos; imp_i2p_acc_6=descansadlos; imp_i2p_acc_7=descansados; imp_i2p_dat_1=descansadme; imp_i2p_dat_3=descansadle; imp_i2p_dat_4=descansadnos; imp_i2p_dat_5=descansaos; imp_i2p_dat_6=descansadles; imp_i2s_acc-dat_1=descánsámela; imp_i2s_acc-dat_1=descánsámelas; imp_i2s_acc-dat_1=descánsámelo; imp_i2s_acc-dat_1=descánsámelos; imp_i2s_acc-dat_2=descánsátela; imp_i2s_acc-dat_2=descánsátelas; imp_i2s_acc-dat_2=descánsátelo; imp_i2s_acc-dat_2=descánsátelos; imp_i2s_acc-dat_3=descánsala; imp_i2s_acc-dat_3=descánsálola; imp_i2s_acc-dat_3=descánsálolas; imp_i2s_acc-dat_3=descánsálolo; imp_i2s_acc-dat_3=descánsálolos; imp_i2s_acc-dat_4=descánsánosla; imp_i2s_acc-dat_4=descánsánoslas; imp_i2s_acc-dat_4=descánsánoslo; imp_i2s_acc-dat_4=descánsánoslos; imp_i2s_acc-dat_6=descánsalas; imp_i2s_acc-dat_6=descánsálosla; imp_i2s_acc-dat_6=descánsáloslas; imp_i2s_acc-dat_6=descánsáloslo; imp_i2s_acc-dat_6=descánsáloslos; imp_i2s_acc_1=descánsame; imp_i2s_acc_2=descánsate; imp_i2s_acc_3=descánsalo; imp_i2s_acc_4=descánsanos; imp_i2s_acc_6=descánsalos; imp_i2s_dat_1=descánsame; imp_i2s_dat_2=descánsate; imp_i2s_dat_3=descánsale; imp_i2s_dat_4=descánsanos; imp_i2s_dat_6=descánsales; inf_acc-dat_1=descansármela; inf_acc-dat_1=descansármelas; inf_acc-dat_1=descansármelo; inf_acc-dat_1=descansármelos; inf_acc-dat_2=descansártela; inf_acc-dat_2=descansártelas; inf_acc-dat_2=descansártelo; inf_acc-dat_2=descansártelos; inf_acc-dat_3=descansarla; inf_acc-dat_3=descansarse; inf_acc-dat_3=descansárlola; inf_acc-dat_3=descansárlolas; inf_acc-dat_3=descansárlolo; inf_acc-dat_3=descansárlolos; inf_acc-dat_4=descansárnosla; inf_acc-dat_4=descansárnoslas; inf_acc-dat_4=descansárnoslo; inf_acc-dat_4=descansárnoslos; inf_acc-dat_5=descansárosla; inf_acc-dat_5=descansároslas; inf_acc-dat_5=descansároslo; inf_acc-dat_5=descansároslos; inf_acc-dat_6=descansarlas; inf_acc-dat_6=descansarse; inf_acc-dat_6=descansárlosla; inf_acc-dat_6=descansárloslas; inf_acc-dat_6=descansárloslo; inf_acc-dat_6=descansárloslos; inf_acc-dat_7=descansársela; inf_acc-dat_7=descansárselas; inf_acc-dat_7=descansárselo; inf_acc-dat_7=descansárselos; inf_acc_1=descansarme; inf_acc_2=descansarte; inf_acc_3=descansarlo; inf_acc_4=descansarnos; inf_acc_5=descansaros; inf_acc_6=descansarlos; inf_acc_7=descansarse; inf_dat_1=descansarme; inf_dat_2=descansarte; inf_dat_3=descansarle; inf_dat_3=descansarse; inf_dat_4=descansarnos; inf_dat_5=descansaros; inf_dat_6=descansarles; inf_dat_6=descansarse
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
    entry = builder.parse_entry(lang_entry, "youtuber")

    print( "\n".join(entry))
    assert lang_entry != """
youtuber {noun-forms} :: f=youtuberista; fpl=youtuberistas; pl=youtuber; pl=youtubers
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
    entry = builder.parse_entry(lang_entry, "youtuber")

    assert "\n".join(entry) == """\
youtuber {adj-forms} :: f=youtuberista; fpl=youtuberistas; pl=youtuber; pl=youtubers
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
    entry = builder.parse_entry(lang_entry, "abstener")

    assert "\n".join(entry) == """\
abstener {verb-forms} :: 1=abstener; 10=abstiene; 11=abstenemos; 12=abstenéis; 13=abstienen; 14=abstenía; 15=abstenías; 16=abstenía; 17=absteníamos; 18=absteníais; 19=abstenían; 2=absteniendo; 20=abstuve; 21=abstuviste; 22=abstuvo; 23=abstuvimos; 24=abstuvisteis; 25=abstuvieron; 26=abstendré; 27=abstendrás; 28=abstendrá; 29=abstendremos; 3=abstenido; 30=abstendréis; 31=abstendrán; 32=abstendría; 33=abstendrías; 34=abstendría; 35=abstendríamos; 36=abstendríais; 37=abstendrían; 38=abstenga; 39=abstengas; 4=abstenida; 41=abstenga; 42=abstengamos; 43=abstengáis; 44=abstengan; 45=abstuviera; 46=abstuvieras; 47=abstuviera; 48=abstuviéramos; 49=abstuvierais; 5=abstenidos; 50=abstuvieran; 51=abstuviese; 52=abstuvieses; 53=abstuviese; 54=abstuviésemos; 55=abstuvieseis; 56=abstuviesen; 57=abstuviere; 58=abstuvieres; 59=abstuviere; 6=abstenidas; 60=abstuviéremos; 61=abstuviereis; 62=abstuvieren; 63=abstén; 64=abstené; 65=abstenga; 66=abstengamos; 67=abstened; 68=abstengan; 69=abstengas; 7=abstengo; 70=abstenga; 71=abstengamos; 72=abstengáis; 73=abstengan; 8=abstienes; 9=abstenés; ger_acc-dat_1=absteniéndómela; ger_acc-dat_1=absteniéndómelas; ger_acc-dat_1=absteniéndómelo; ger_acc-dat_1=absteniéndómelos; ger_acc-dat_2=absteniéndótela; ger_acc-dat_2=absteniéndótelas; ger_acc-dat_2=absteniéndótelo; ger_acc-dat_2=absteniéndótelos; ger_acc-dat_3=absteniéndola; ger_acc-dat_3=absteniéndose; ger_acc-dat_3=absteniéndólola; ger_acc-dat_3=absteniéndólolas; ger_acc-dat_3=absteniéndólolo; ger_acc-dat_3=absteniéndólolos; ger_acc-dat_4=absteniéndónosla; ger_acc-dat_4=absteniéndónoslas; ger_acc-dat_4=absteniéndónoslo; ger_acc-dat_4=absteniéndónoslos; ger_acc-dat_5=absteniéndóosla; ger_acc-dat_5=absteniéndóoslas; ger_acc-dat_5=absteniéndóoslo; ger_acc-dat_5=absteniéndóoslos; ger_acc-dat_6=absteniéndolas; ger_acc-dat_6=absteniéndose; ger_acc-dat_6=absteniéndólosla; ger_acc-dat_6=absteniéndóloslas; ger_acc-dat_6=absteniéndóloslo; ger_acc-dat_6=absteniéndóloslos; ger_acc-dat_7=absteniéndósela; ger_acc-dat_7=absteniéndóselas; ger_acc-dat_7=absteniéndóselo; ger_acc-dat_7=absteniéndóselos; ger_acc_1=absteniéndome; ger_acc_2=absteniéndote; ger_acc_3=absteniéndolo; ger_acc_4=absteniéndonos; ger_acc_5=absteniéndoos; ger_acc_6=absteniéndolos; ger_acc_7=absteniéndose; ger_dat_1=absteniéndome; ger_dat_2=absteniéndote; ger_dat_3=absteniéndole; ger_dat_3=absteniéndose; ger_dat_4=absteniéndonos; ger_dat_5=absteniéndoos; ger_dat_6=absteniéndoles; ger_dat_6=absteniéndose; imp_1p_acc-dat_2=abstengámóstela; imp_1p_acc-dat_2=abstengámóstelas; imp_1p_acc-dat_2=abstengámóstelo; imp_1p_acc-dat_2=abstengámóstelos; imp_1p_acc-dat_3=abstengámosla; imp_1p_acc-dat_3=abstengámóslola; imp_1p_acc-dat_3=abstengámóslolas; imp_1p_acc-dat_3=abstengámóslolo; imp_1p_acc-dat_3=abstengámóslolos; imp_1p_acc-dat_4=abstengámónosla; imp_1p_acc-dat_4=abstengámónoslas; imp_1p_acc-dat_4=abstengámónoslo; imp_1p_acc-dat_4=abstengámónoslos; imp_1p_acc-dat_5=abstengámóosla; imp_1p_acc-dat_5=abstengámóoslas; imp_1p_acc-dat_5=abstengámóoslo; imp_1p_acc-dat_5=abstengámóoslos; imp_1p_acc-dat_6=abstengámoslas; imp_1p_acc-dat_6=abstengámóslosla; imp_1p_acc-dat_6=abstengámósloslas; imp_1p_acc-dat_6=abstengámósloslo; imp_1p_acc-dat_6=abstengámósloslos; imp_1p_acc_2=abstengámoste; imp_1p_acc_3=abstengámoslo; imp_1p_acc_4=abstengámonos; imp_1p_acc_5=abstengámoos; imp_1p_acc_6=abstengámoslos; imp_1p_dat_2=abstengámoste; imp_1p_dat_3=abstengámosle; imp_1p_dat_4=abstengámonos; imp_1p_dat_5=abstengámoos; imp_1p_dat_6=abstengámosles; imp_f2p_acc-dat_1=absténgánmela; imp_f2p_acc-dat_1=absténgánmelas; imp_f2p_acc-dat_1=absténgánmelo; imp_f2p_acc-dat_1=absténgánmelos; imp_f2p_acc-dat_3=absténganla; imp_f2p_acc-dat_3=absténgánlola; imp_f2p_acc-dat_3=absténgánlolas; imp_f2p_acc-dat_3=absténgánlolo; imp_f2p_acc-dat_3=absténgánlolos; imp_f2p_acc-dat_4=absténgánnosla; imp_f2p_acc-dat_4=absténgánnoslas; imp_f2p_acc-dat_4=absténgánnoslo; imp_f2p_acc-dat_4=absténgánnoslos; imp_f2p_acc-dat_6=absténganlas; imp_f2p_acc-dat_6=absténganse; imp_f2p_acc-dat_6=absténgánlosla; imp_f2p_acc-dat_6=absténgánloslas; imp_f2p_acc-dat_6=absténgánloslo; imp_f2p_acc-dat_6=absténgánloslos; imp_f2p_acc-dat_7=absténgánsela; imp_f2p_acc-dat_7=absténgánselas; imp_f2p_acc-dat_7=absténgánselo; imp_f2p_acc-dat_7=absténgánselos; imp_f2p_acc_1=absténganme; imp_f2p_acc_3=absténganlo; imp_f2p_acc_4=absténgannos; imp_f2p_acc_6=absténganlos; imp_f2p_acc_7=absténganse; imp_f2p_dat_1=absténganme; imp_f2p_dat_3=absténganle; imp_f2p_dat_4=absténgannos; imp_f2p_dat_6=absténganles; imp_f2p_dat_6=absténganse; imp_f2s_acc-dat_1=absténgámela; imp_f2s_acc-dat_1=absténgámelas; imp_f2s_acc-dat_1=absténgámelo; imp_f2s_acc-dat_1=absténgámelos; imp_f2s_acc-dat_3=absténgala; imp_f2s_acc-dat_3=absténgase; imp_f2s_acc-dat_3=absténgálola; imp_f2s_acc-dat_3=absténgálolas; imp_f2s_acc-dat_3=absténgálolo; imp_f2s_acc-dat_3=absténgálolos; imp_f2s_acc-dat_4=absténgánosla; imp_f2s_acc-dat_4=absténgánoslas; imp_f2s_acc-dat_4=absténgánoslo; imp_f2s_acc-dat_4=absténgánoslos; imp_f2s_acc-dat_6=absténgalas; imp_f2s_acc-dat_6=absténgálosla; imp_f2s_acc-dat_6=absténgáloslas; imp_f2s_acc-dat_6=absténgáloslo; imp_f2s_acc-dat_6=absténgáloslos; imp_f2s_acc-dat_7=absténgásela; imp_f2s_acc-dat_7=absténgáselas; imp_f2s_acc-dat_7=absténgáselo; imp_f2s_acc-dat_7=absténgáselos; imp_f2s_acc_1=absténgame; imp_f2s_acc_3=absténgalo; imp_f2s_acc_4=absténganos; imp_f2s_acc_6=absténgalos; imp_f2s_acc_7=absténgase; imp_f2s_dat_1=absténgame; imp_f2s_dat_3=absténgale; imp_f2s_dat_3=absténgase; imp_f2s_dat_4=absténganos; imp_f2s_dat_6=absténgales; imp_i2p_acc-dat_1=abstenédmela; imp_i2p_acc-dat_1=abstenédmelas; imp_i2p_acc-dat_1=abstenédmelo; imp_i2p_acc-dat_1=abstenédmelos; imp_i2p_acc-dat_3=abstenedla; imp_i2p_acc-dat_3=abstenédlola; imp_i2p_acc-dat_3=abstenédlolas; imp_i2p_acc-dat_3=abstenédlolo; imp_i2p_acc-dat_3=abstenédlolos; imp_i2p_acc-dat_4=abstenédnosla; imp_i2p_acc-dat_4=abstenédnoslas; imp_i2p_acc-dat_4=abstenédnoslo; imp_i2p_acc-dat_4=abstenédnoslos; imp_i2p_acc-dat_5=abstenéosla; imp_i2p_acc-dat_5=abstenéoslas; imp_i2p_acc-dat_5=abstenéoslo; imp_i2p_acc-dat_5=abstenéoslos; imp_i2p_acc-dat_6=abstenedlas; imp_i2p_acc-dat_6=abstenédlosla; imp_i2p_acc-dat_6=abstenédloslas; imp_i2p_acc-dat_6=abstenédloslo; imp_i2p_acc-dat_6=abstenédloslos; imp_i2p_acc-dat_7=abstenédosla; imp_i2p_acc-dat_7=abstenédoslas; imp_i2p_acc-dat_7=abstenédoslo; imp_i2p_acc-dat_7=abstenédoslos; imp_i2p_acc_1=abstenedme; imp_i2p_acc_3=abstenedlo; imp_i2p_acc_4=abstenednos; imp_i2p_acc_5=absteneos; imp_i2p_acc_6=abstenedlos; imp_i2p_acc_7=abstenedos; imp_i2p_dat_1=abstenedme; imp_i2p_dat_3=abstenedle; imp_i2p_dat_4=abstenednos; imp_i2p_dat_5=absteneos; imp_i2p_dat_6=abstenedles; imp_i2s_acc-dat_1=absténmela; imp_i2s_acc-dat_1=absténmelas; imp_i2s_acc-dat_1=absténmelo; imp_i2s_acc-dat_1=absténmelos; imp_i2s_acc-dat_2=absténtela; imp_i2s_acc-dat_2=absténtelas; imp_i2s_acc-dat_2=absténtelo; imp_i2s_acc-dat_2=absténtelos; imp_i2s_acc-dat_3=abstenla; imp_i2s_acc-dat_3=absténlola; imp_i2s_acc-dat_3=absténlolas; imp_i2s_acc-dat_3=absténlolo; imp_i2s_acc-dat_3=absténlolos; imp_i2s_acc-dat_4=absténnosla; imp_i2s_acc-dat_4=absténnoslas; imp_i2s_acc-dat_4=absténnoslo; imp_i2s_acc-dat_4=absténnoslos; imp_i2s_acc-dat_6=abstenlas; imp_i2s_acc-dat_6=absténlosla; imp_i2s_acc-dat_6=absténloslas; imp_i2s_acc-dat_6=absténloslo; imp_i2s_acc-dat_6=absténloslos; imp_i2s_acc_1=abstenme; imp_i2s_acc_2=abstente; imp_i2s_acc_3=abstenlo; imp_i2s_acc_4=abstennos; imp_i2s_acc_6=abstenlos; imp_i2s_dat_1=abstenme; imp_i2s_dat_2=abstente; imp_i2s_dat_3=abstenle; imp_i2s_dat_4=abstennos; imp_i2s_dat_6=abstenles; inf_acc-dat_1=abstenérmela; inf_acc-dat_1=abstenérmelas; inf_acc-dat_1=abstenérmelo; inf_acc-dat_1=abstenérmelos; inf_acc-dat_2=abstenértela; inf_acc-dat_2=abstenértelas; inf_acc-dat_2=abstenértelo; inf_acc-dat_2=abstenértelos; inf_acc-dat_3=abstenerla; inf_acc-dat_3=abstenerse; inf_acc-dat_3=abstenérlola; inf_acc-dat_3=abstenérlolas; inf_acc-dat_3=abstenérlolo; inf_acc-dat_3=abstenérlolos; inf_acc-dat_4=abstenérnosla; inf_acc-dat_4=abstenérnoslas; inf_acc-dat_4=abstenérnoslo; inf_acc-dat_4=abstenérnoslos; inf_acc-dat_5=abstenérosla; inf_acc-dat_5=abstenéroslas; inf_acc-dat_5=abstenéroslo; inf_acc-dat_5=abstenéroslos; inf_acc-dat_6=abstenerlas; inf_acc-dat_6=abstenerse; inf_acc-dat_6=abstenérlosla; inf_acc-dat_6=abstenérloslas; inf_acc-dat_6=abstenérloslo; inf_acc-dat_6=abstenérloslos; inf_acc-dat_7=abstenérsela; inf_acc-dat_7=abstenérselas; inf_acc-dat_7=abstenérselo; inf_acc-dat_7=abstenérselos; inf_acc_1=abstenerme; inf_acc_2=abstenerte; inf_acc_3=abstenerlo; inf_acc_4=abstenernos; inf_acc_5=absteneros; inf_acc_6=abstenerlos; inf_acc_7=abstenerse; inf_dat_1=abstenerme; inf_dat_2=abstenerte; inf_dat_3=abstenerle; inf_dat_3=abstenerse; inf_dat_4=abstenernos; inf_dat_5=absteneros; inf_dat_6=abstenerles; inf_dat_6=abstenerse
abstener {vr} :: to abstain\
"""

#    assert entry[0] == "abstener {verb-forms} :: pattern=-tener; stem=abs"

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
    entry = builder.parse_entry(lang_entry, "adecuar")

    assert "\n".join(entry)=="""\
adecuar {verb-forms} :: 1=adecuar; 10=adecua; 10=adecúa; 11=adecuamos; 12=adecuáis; 13=adecuan; 13=adecúan; 14=adecuaba; 15=adecuabas; 16=adecuaba; 17=adecuábamos; 18=adecuabais; 19=adecuaban; 2=adecuando; 20=adecué; 21=adecuaste; 22=adecuó; 23=adecuamos; 24=adecuasteis; 25=adecuaron; 26=adecuaré; 27=adecuarás; 28=adecuará; 29=adecuaremos; 3=adecuado; 30=adecuaréis; 31=adecuarán; 32=adecuaría; 33=adecuarías; 34=adecuaría; 35=adecuaríamos; 36=adecuaríais; 37=adecuarían; 38=adecue; 38=adecúe; 39=adecues; 39=adecúes; 4=adecuada; 40=adecués; 41=adecue; 41=adecúe; 42=adecuemos; 43=adecuéis; 44=adecuen; 44=adecúen; 45=adecuara; 46=adecuaras; 47=adecuara; 48=adecuáramos; 49=adecuarais; 5=adecuados; 50=adecuaran; 51=adecuase; 52=adecuases; 53=adecuase; 54=adecuásemos; 55=adecuaseis; 56=adecuasen; 57=adecuare; 58=adecuares; 59=adecuare; 6=adecuadas; 60=adecuáremos; 61=adecuareis; 62=adecuaren; 63=adecua; 63=adecúa; 64=adecuá; 65=adecue; 65=adecúe; 66=adecuemos; 67=adecuad; 68=adecuen; 68=adecúen; 69=adecues; 69=adecúes; 7=adecuo; 7=adecúo; 70=adecue; 70=adecúe; 71=adecuemos; 72=adecuéis; 73=adecuen; 73=adecúen; 8=adecuas; 8=adecúas; 9=adecuás; ger_acc-dat_1=adecuándómela; ger_acc-dat_1=adecuándómelas; ger_acc-dat_1=adecuándómelo; ger_acc-dat_1=adecuándómelos; ger_acc-dat_2=adecuándótela; ger_acc-dat_2=adecuándótelas; ger_acc-dat_2=adecuándótelo; ger_acc-dat_2=adecuándótelos; ger_acc-dat_3=adecuándola; ger_acc-dat_3=adecuándose; ger_acc-dat_3=adecuándólola; ger_acc-dat_3=adecuándólolas; ger_acc-dat_3=adecuándólolo; ger_acc-dat_3=adecuándólolos; ger_acc-dat_4=adecuándónosla; ger_acc-dat_4=adecuándónoslas; ger_acc-dat_4=adecuándónoslo; ger_acc-dat_4=adecuándónoslos; ger_acc-dat_5=adecuándóosla; ger_acc-dat_5=adecuándóoslas; ger_acc-dat_5=adecuándóoslo; ger_acc-dat_5=adecuándóoslos; ger_acc-dat_6=adecuándolas; ger_acc-dat_6=adecuándose; ger_acc-dat_6=adecuándólosla; ger_acc-dat_6=adecuándóloslas; ger_acc-dat_6=adecuándóloslo; ger_acc-dat_6=adecuándóloslos; ger_acc-dat_7=adecuándósela; ger_acc-dat_7=adecuándóselas; ger_acc-dat_7=adecuándóselo; ger_acc-dat_7=adecuándóselos; ger_acc_1=adecuándome; ger_acc_2=adecuándote; ger_acc_3=adecuándolo; ger_acc_4=adecuándonos; ger_acc_5=adecuándoos; ger_acc_6=adecuándolos; ger_acc_7=adecuándose; ger_dat_1=adecuándome; ger_dat_2=adecuándote; ger_dat_3=adecuándole; ger_dat_3=adecuándose; ger_dat_4=adecuándonos; ger_dat_5=adecuándoos; ger_dat_6=adecuándoles; ger_dat_6=adecuándose; imp_1p_acc-dat_2=adecuémóstela; imp_1p_acc-dat_2=adecuémóstelas; imp_1p_acc-dat_2=adecuémóstelo; imp_1p_acc-dat_2=adecuémóstelos; imp_1p_acc-dat_3=adecuémosla; imp_1p_acc-dat_3=adecuémóslola; imp_1p_acc-dat_3=adecuémóslolas; imp_1p_acc-dat_3=adecuémóslolo; imp_1p_acc-dat_3=adecuémóslolos; imp_1p_acc-dat_4=adecuémónosla; imp_1p_acc-dat_4=adecuémónoslas; imp_1p_acc-dat_4=adecuémónoslo; imp_1p_acc-dat_4=adecuémónoslos; imp_1p_acc-dat_5=adecuémóosla; imp_1p_acc-dat_5=adecuémóoslas; imp_1p_acc-dat_5=adecuémóoslo; imp_1p_acc-dat_5=adecuémóoslos; imp_1p_acc-dat_6=adecuémoslas; imp_1p_acc-dat_6=adecuémóslosla; imp_1p_acc-dat_6=adecuémósloslas; imp_1p_acc-dat_6=adecuémósloslo; imp_1p_acc-dat_6=adecuémósloslos; imp_1p_acc_2=adecuémoste; imp_1p_acc_3=adecuémoslo; imp_1p_acc_4=adecuémonos; imp_1p_acc_5=adecuémoos; imp_1p_acc_6=adecuémoslos; imp_1p_dat_2=adecuémoste; imp_1p_dat_3=adecuémosle; imp_1p_dat_4=adecuémonos; imp_1p_dat_5=adecuémoos; imp_1p_dat_6=adecuémosles; imp_f2p_acc-dat_1=adécuénmela; imp_f2p_acc-dat_1=adécuénmelas; imp_f2p_acc-dat_1=adécuénmelo; imp_f2p_acc-dat_1=adécuénmelos; imp_f2p_acc-dat_3=adécuenla; imp_f2p_acc-dat_3=adécuénlola; imp_f2p_acc-dat_3=adécuénlolas; imp_f2p_acc-dat_3=adécuénlolo; imp_f2p_acc-dat_3=adécuénlolos; imp_f2p_acc-dat_4=adécuénnosla; imp_f2p_acc-dat_4=adécuénnoslas; imp_f2p_acc-dat_4=adécuénnoslo; imp_f2p_acc-dat_4=adécuénnoslos; imp_f2p_acc-dat_6=adécuenlas; imp_f2p_acc-dat_6=adécuense; imp_f2p_acc-dat_6=adécuénlosla; imp_f2p_acc-dat_6=adécuénloslas; imp_f2p_acc-dat_6=adécuénloslo; imp_f2p_acc-dat_6=adécuénloslos; imp_f2p_acc-dat_7=adécuénsela; imp_f2p_acc-dat_7=adécuénselas; imp_f2p_acc-dat_7=adécuénselo; imp_f2p_acc-dat_7=adécuénselos; imp_f2p_acc_1=adécuenme; imp_f2p_acc_3=adécuenlo; imp_f2p_acc_4=adécuennos; imp_f2p_acc_6=adécuenlos; imp_f2p_acc_7=adécuense; imp_f2p_dat_1=adécuenme; imp_f2p_dat_3=adécuenle; imp_f2p_dat_4=adécuennos; imp_f2p_dat_6=adécuenles; imp_f2p_dat_6=adécuense; imp_f2s_acc-dat_1=adécuémela; imp_f2s_acc-dat_1=adécuémelas; imp_f2s_acc-dat_1=adécuémelo; imp_f2s_acc-dat_1=adécuémelos; imp_f2s_acc-dat_3=adécuela; imp_f2s_acc-dat_3=adécuese; imp_f2s_acc-dat_3=adécuélola; imp_f2s_acc-dat_3=adécuélolas; imp_f2s_acc-dat_3=adécuélolo; imp_f2s_acc-dat_3=adécuélolos; imp_f2s_acc-dat_4=adécuénosla; imp_f2s_acc-dat_4=adécuénoslas; imp_f2s_acc-dat_4=adécuénoslo; imp_f2s_acc-dat_4=adécuénoslos; imp_f2s_acc-dat_6=adécuelas; imp_f2s_acc-dat_6=adécuélosla; imp_f2s_acc-dat_6=adécuéloslas; imp_f2s_acc-dat_6=adécuéloslo; imp_f2s_acc-dat_6=adécuéloslos; imp_f2s_acc-dat_7=adécuésela; imp_f2s_acc-dat_7=adécuéselas; imp_f2s_acc-dat_7=adécuéselo; imp_f2s_acc-dat_7=adécuéselos; imp_f2s_acc_1=adécueme; imp_f2s_acc_3=adécuelo; imp_f2s_acc_4=adécuenos; imp_f2s_acc_6=adécuelos; imp_f2s_acc_7=adécuese; imp_f2s_dat_1=adécueme; imp_f2s_dat_3=adécuele; imp_f2s_dat_3=adécuese; imp_f2s_dat_4=adécuenos; imp_f2s_dat_6=adécueles; imp_i2p_acc-dat_1=adecuádmela; imp_i2p_acc-dat_1=adecuádmelas; imp_i2p_acc-dat_1=adecuádmelo; imp_i2p_acc-dat_1=adecuádmelos; imp_i2p_acc-dat_3=adecuadla; imp_i2p_acc-dat_3=adecuádlola; imp_i2p_acc-dat_3=adecuádlolas; imp_i2p_acc-dat_3=adecuádlolo; imp_i2p_acc-dat_3=adecuádlolos; imp_i2p_acc-dat_4=adecuádnosla; imp_i2p_acc-dat_4=adecuádnoslas; imp_i2p_acc-dat_4=adecuádnoslo; imp_i2p_acc-dat_4=adecuádnoslos; imp_i2p_acc-dat_5=adecuáosla; imp_i2p_acc-dat_5=adecuáoslas; imp_i2p_acc-dat_5=adecuáoslo; imp_i2p_acc-dat_5=adecuáoslos; imp_i2p_acc-dat_6=adecuadlas; imp_i2p_acc-dat_6=adecuádlosla; imp_i2p_acc-dat_6=adecuádloslas; imp_i2p_acc-dat_6=adecuádloslo; imp_i2p_acc-dat_6=adecuádloslos; imp_i2p_acc-dat_7=adecuádosla; imp_i2p_acc-dat_7=adecuádoslas; imp_i2p_acc-dat_7=adecuádoslo; imp_i2p_acc-dat_7=adecuádoslos; imp_i2p_acc_1=adecuadme; imp_i2p_acc_3=adecuadlo; imp_i2p_acc_4=adecuadnos; imp_i2p_acc_5=adecuaos; imp_i2p_acc_6=adecuadlos; imp_i2p_acc_7=adecuados; imp_i2p_dat_1=adecuadme; imp_i2p_dat_3=adecuadle; imp_i2p_dat_4=adecuadnos; imp_i2p_dat_5=adecuaos; imp_i2p_dat_6=adecuadles; imp_i2s_acc-dat_1=adecúámela; imp_i2s_acc-dat_1=adecúámelas; imp_i2s_acc-dat_1=adecúámelo; imp_i2s_acc-dat_1=adecúámelos; imp_i2s_acc-dat_1=adécuámela; imp_i2s_acc-dat_1=adécuámelas; imp_i2s_acc-dat_1=adécuámelo; imp_i2s_acc-dat_1=adécuámelos; imp_i2s_acc-dat_2=adecúátela; imp_i2s_acc-dat_2=adecúátelas; imp_i2s_acc-dat_2=adecúátelo; imp_i2s_acc-dat_2=adecúátelos; imp_i2s_acc-dat_2=adécuátela; imp_i2s_acc-dat_2=adécuátelas; imp_i2s_acc-dat_2=adécuátelo; imp_i2s_acc-dat_2=adécuátelos; imp_i2s_acc-dat_3=adecúala; imp_i2s_acc-dat_3=adecúálola; imp_i2s_acc-dat_3=adecúálolas; imp_i2s_acc-dat_3=adecúálolo; imp_i2s_acc-dat_3=adecúálolos; imp_i2s_acc-dat_3=adécuala; imp_i2s_acc-dat_3=adécuálola; imp_i2s_acc-dat_3=adécuálolas; imp_i2s_acc-dat_3=adécuálolo; imp_i2s_acc-dat_3=adécuálolos; imp_i2s_acc-dat_4=adecúánosla; imp_i2s_acc-dat_4=adecúánoslas; imp_i2s_acc-dat_4=adecúánoslo; imp_i2s_acc-dat_4=adecúánoslos; imp_i2s_acc-dat_4=adécuánosla; imp_i2s_acc-dat_4=adécuánoslas; imp_i2s_acc-dat_4=adécuánoslo; imp_i2s_acc-dat_4=adécuánoslos; imp_i2s_acc-dat_6=adecúalas; imp_i2s_acc-dat_6=adecúálosla; imp_i2s_acc-dat_6=adecúáloslas; imp_i2s_acc-dat_6=adecúáloslo; imp_i2s_acc-dat_6=adecúáloslos; imp_i2s_acc-dat_6=adécualas; imp_i2s_acc-dat_6=adécuálosla; imp_i2s_acc-dat_6=adécuáloslas; imp_i2s_acc-dat_6=adécuáloslo; imp_i2s_acc-dat_6=adécuáloslos; imp_i2s_acc_1=adecúame; imp_i2s_acc_1=adécuame; imp_i2s_acc_2=adecúate; imp_i2s_acc_2=adécuate; imp_i2s_acc_3=adecúalo; imp_i2s_acc_3=adécualo; imp_i2s_acc_4=adecúanos; imp_i2s_acc_4=adécuanos; imp_i2s_acc_6=adecúalos; imp_i2s_acc_6=adécualos; imp_i2s_dat_1=adecúame; imp_i2s_dat_1=adécuame; imp_i2s_dat_2=adecúate; imp_i2s_dat_2=adécuate; imp_i2s_dat_3=adecúale; imp_i2s_dat_3=adécuale; imp_i2s_dat_4=adecúanos; imp_i2s_dat_4=adécuanos; imp_i2s_dat_6=adecúales; imp_i2s_dat_6=adécuales; inf_acc-dat_1=adecuármela; inf_acc-dat_1=adecuármelas; inf_acc-dat_1=adecuármelo; inf_acc-dat_1=adecuármelos; inf_acc-dat_2=adecuártela; inf_acc-dat_2=adecuártelas; inf_acc-dat_2=adecuártelo; inf_acc-dat_2=adecuártelos; inf_acc-dat_3=adecuarla; inf_acc-dat_3=adecuarse; inf_acc-dat_3=adecuárlola; inf_acc-dat_3=adecuárlolas; inf_acc-dat_3=adecuárlolo; inf_acc-dat_3=adecuárlolos; inf_acc-dat_4=adecuárnosla; inf_acc-dat_4=adecuárnoslas; inf_acc-dat_4=adecuárnoslo; inf_acc-dat_4=adecuárnoslos; inf_acc-dat_5=adecuárosla; inf_acc-dat_5=adecuároslas; inf_acc-dat_5=adecuároslo; inf_acc-dat_5=adecuároslos; inf_acc-dat_6=adecuarlas; inf_acc-dat_6=adecuarse; inf_acc-dat_6=adecuárlosla; inf_acc-dat_6=adecuárloslas; inf_acc-dat_6=adecuárloslo; inf_acc-dat_6=adecuárloslos; inf_acc-dat_7=adecuársela; inf_acc-dat_7=adecuárselas; inf_acc-dat_7=adecuárselo; inf_acc-dat_7=adecuárselos; inf_acc_1=adecuarme; inf_acc_2=adecuarte; inf_acc_3=adecuarlo; inf_acc_4=adecuarnos; inf_acc_5=adecuaros; inf_acc_6=adecuarlos; inf_acc_7=adecuarse; inf_dat_1=adecuarme; inf_dat_2=adecuarte; inf_dat_3=adecuarle; inf_dat_3=adecuarse; inf_dat_4=adecuarnos; inf_dat_5=adecuaros; inf_dat_6=adecuarles; inf_dat_6=adecuarse
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
    entry = builder.parse_entry(lang_entry, "protector")

    assert "\n".join(entry)=="""\
protector {adj-forms} :: f=protectora; f=protectriz; fpl=protectrices; pl=protectores
protector {adj} :: protective
protector {noun-forms} :: f=protectora; f=protectriz; fpl=protectoras; fpl=protectrices; pl=protectores
protector {m} :: protector (someone who protects or guards)
protector {noun-forms} :: pl=protectores
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

    print("\n".join(entry))
    assert "\n".join(entry)=="""\
aterrar {verb-forms} :: 1=aterrar; 10=atierra; 11=aterramos; 12=aterráis; 13=atierran; 14=aterraba; 15=aterrabas; 16=aterraba; 17=aterrábamos; 18=aterrabais; 19=aterraban; 2=aterrando; 20=aterré; 21=aterraste; 22=aterró; 23=aterramos; 24=aterrasteis; 25=aterraron; 26=aterraré; 27=aterrarás; 28=aterrará; 29=aterraremos; 3=aterrado; 30=aterraréis; 31=aterrarán; 32=aterraría; 33=aterrarías; 34=aterraría; 35=aterraríamos; 36=aterraríais; 37=aterrarían; 38=atierre; 39=atierres; 4=aterrada; 40=aterrés; 41=atierre; 42=aterremos; 43=aterréis; 44=atierren; 45=aterrara; 46=aterraras; 47=aterrara; 48=aterráramos; 49=aterrarais; 5=aterrados; 50=aterraran; 51=aterrase; 52=aterrases; 53=aterrase; 54=aterrásemos; 55=aterraseis; 56=aterrasen; 57=aterrare; 58=aterrares; 59=aterrare; 6=aterradas; 60=aterráremos; 61=aterrareis; 62=aterraren; 63=atierra; 64=aterrá; 65=atierre; 66=aterremos; 67=aterrad; 68=atierren; 69=atierres; 7=atierro; 70=atierre; 71=aterremos; 72=aterréis; 73=atierren; 8=atierras; 9=aterrás; ger_acc-dat_1=aterrándómela; ger_acc-dat_1=aterrándómelas; ger_acc-dat_1=aterrándómelo; ger_acc-dat_1=aterrándómelos; ger_acc-dat_2=aterrándótela; ger_acc-dat_2=aterrándótelas; ger_acc-dat_2=aterrándótelo; ger_acc-dat_2=aterrándótelos; ger_acc-dat_3=aterrándola; ger_acc-dat_3=aterrándose; ger_acc-dat_3=aterrándólola; ger_acc-dat_3=aterrándólolas; ger_acc-dat_3=aterrándólolo; ger_acc-dat_3=aterrándólolos; ger_acc-dat_4=aterrándónosla; ger_acc-dat_4=aterrándónoslas; ger_acc-dat_4=aterrándónoslo; ger_acc-dat_4=aterrándónoslos; ger_acc-dat_5=aterrándóosla; ger_acc-dat_5=aterrándóoslas; ger_acc-dat_5=aterrándóoslo; ger_acc-dat_5=aterrándóoslos; ger_acc-dat_6=aterrándolas; ger_acc-dat_6=aterrándose; ger_acc-dat_6=aterrándólosla; ger_acc-dat_6=aterrándóloslas; ger_acc-dat_6=aterrándóloslo; ger_acc-dat_6=aterrándóloslos; ger_acc-dat_7=aterrándósela; ger_acc-dat_7=aterrándóselas; ger_acc-dat_7=aterrándóselo; ger_acc-dat_7=aterrándóselos; ger_acc_1=aterrándome; ger_acc_2=aterrándote; ger_acc_3=aterrándolo; ger_acc_4=aterrándonos; ger_acc_5=aterrándoos; ger_acc_6=aterrándolos; ger_acc_7=aterrándose; ger_dat_1=aterrándome; ger_dat_2=aterrándote; ger_dat_3=aterrándole; ger_dat_3=aterrándose; ger_dat_4=aterrándonos; ger_dat_5=aterrándoos; ger_dat_6=aterrándoles; ger_dat_6=aterrándose; imp_1p_acc-dat_2=aterrémóstela; imp_1p_acc-dat_2=aterrémóstelas; imp_1p_acc-dat_2=aterrémóstelo; imp_1p_acc-dat_2=aterrémóstelos; imp_1p_acc-dat_3=aterrémosla; imp_1p_acc-dat_3=aterrémóslola; imp_1p_acc-dat_3=aterrémóslolas; imp_1p_acc-dat_3=aterrémóslolo; imp_1p_acc-dat_3=aterrémóslolos; imp_1p_acc-dat_4=aterrémónosla; imp_1p_acc-dat_4=aterrémónoslas; imp_1p_acc-dat_4=aterrémónoslo; imp_1p_acc-dat_4=aterrémónoslos; imp_1p_acc-dat_5=aterrémóosla; imp_1p_acc-dat_5=aterrémóoslas; imp_1p_acc-dat_5=aterrémóoslo; imp_1p_acc-dat_5=aterrémóoslos; imp_1p_acc-dat_6=aterrémoslas; imp_1p_acc-dat_6=aterrémóslosla; imp_1p_acc-dat_6=aterrémósloslas; imp_1p_acc-dat_6=aterrémósloslo; imp_1p_acc-dat_6=aterrémósloslos; imp_1p_acc_2=aterrémoste; imp_1p_acc_3=aterrémoslo; imp_1p_acc_4=aterrémonos; imp_1p_acc_5=aterrémoos; imp_1p_acc_6=aterrémoslos; imp_1p_dat_2=aterrémoste; imp_1p_dat_3=aterrémosle; imp_1p_dat_4=aterrémonos; imp_1p_dat_5=aterrémoos; imp_1p_dat_6=aterrémosles; imp_f2p_acc-dat_1=atiérrénmela; imp_f2p_acc-dat_1=atiérrénmelas; imp_f2p_acc-dat_1=atiérrénmelo; imp_f2p_acc-dat_1=atiérrénmelos; imp_f2p_acc-dat_3=atiérrenla; imp_f2p_acc-dat_3=atiérrénlola; imp_f2p_acc-dat_3=atiérrénlolas; imp_f2p_acc-dat_3=atiérrénlolo; imp_f2p_acc-dat_3=atiérrénlolos; imp_f2p_acc-dat_4=atiérrénnosla; imp_f2p_acc-dat_4=atiérrénnoslas; imp_f2p_acc-dat_4=atiérrénnoslo; imp_f2p_acc-dat_4=atiérrénnoslos; imp_f2p_acc-dat_6=atiérrenlas; imp_f2p_acc-dat_6=atiérrense; imp_f2p_acc-dat_6=atiérrénlosla; imp_f2p_acc-dat_6=atiérrénloslas; imp_f2p_acc-dat_6=atiérrénloslo; imp_f2p_acc-dat_6=atiérrénloslos; imp_f2p_acc-dat_7=atiérrénsela; imp_f2p_acc-dat_7=atiérrénselas; imp_f2p_acc-dat_7=atiérrénselo; imp_f2p_acc-dat_7=atiérrénselos; imp_f2p_acc_1=atiérrenme; imp_f2p_acc_3=atiérrenlo; imp_f2p_acc_4=atiérrennos; imp_f2p_acc_6=atiérrenlos; imp_f2p_acc_7=atiérrense; imp_f2p_dat_1=atiérrenme; imp_f2p_dat_3=atiérrenle; imp_f2p_dat_4=atiérrennos; imp_f2p_dat_6=atiérrenles; imp_f2p_dat_6=atiérrense; imp_f2s_acc-dat_1=atiérrémela; imp_f2s_acc-dat_1=atiérrémelas; imp_f2s_acc-dat_1=atiérrémelo; imp_f2s_acc-dat_1=atiérrémelos; imp_f2s_acc-dat_3=atiérrela; imp_f2s_acc-dat_3=atiérrese; imp_f2s_acc-dat_3=atiérrélola; imp_f2s_acc-dat_3=atiérrélolas; imp_f2s_acc-dat_3=atiérrélolo; imp_f2s_acc-dat_3=atiérrélolos; imp_f2s_acc-dat_4=atiérrénosla; imp_f2s_acc-dat_4=atiérrénoslas; imp_f2s_acc-dat_4=atiérrénoslo; imp_f2s_acc-dat_4=atiérrénoslos; imp_f2s_acc-dat_6=atiérrelas; imp_f2s_acc-dat_6=atiérrélosla; imp_f2s_acc-dat_6=atiérréloslas; imp_f2s_acc-dat_6=atiérréloslo; imp_f2s_acc-dat_6=atiérréloslos; imp_f2s_acc-dat_7=atiérrésela; imp_f2s_acc-dat_7=atiérréselas; imp_f2s_acc-dat_7=atiérréselo; imp_f2s_acc-dat_7=atiérréselos; imp_f2s_acc_1=atiérreme; imp_f2s_acc_3=atiérrelo; imp_f2s_acc_4=atiérrenos; imp_f2s_acc_6=atiérrelos; imp_f2s_acc_7=atiérrese; imp_f2s_dat_1=atiérreme; imp_f2s_dat_3=atiérrele; imp_f2s_dat_3=atiérrese; imp_f2s_dat_4=atiérrenos; imp_f2s_dat_6=atiérreles; imp_i2p_acc-dat_1=aterrádmela; imp_i2p_acc-dat_1=aterrádmelas; imp_i2p_acc-dat_1=aterrádmelo; imp_i2p_acc-dat_1=aterrádmelos; imp_i2p_acc-dat_3=aterradla; imp_i2p_acc-dat_3=aterrádlola; imp_i2p_acc-dat_3=aterrádlolas; imp_i2p_acc-dat_3=aterrádlolo; imp_i2p_acc-dat_3=aterrádlolos; imp_i2p_acc-dat_4=aterrádnosla; imp_i2p_acc-dat_4=aterrádnoslas; imp_i2p_acc-dat_4=aterrádnoslo; imp_i2p_acc-dat_4=aterrádnoslos; imp_i2p_acc-dat_5=aterráosla; imp_i2p_acc-dat_5=aterráoslas; imp_i2p_acc-dat_5=aterráoslo; imp_i2p_acc-dat_5=aterráoslos; imp_i2p_acc-dat_6=aterradlas; imp_i2p_acc-dat_6=aterrádlosla; imp_i2p_acc-dat_6=aterrádloslas; imp_i2p_acc-dat_6=aterrádloslo; imp_i2p_acc-dat_6=aterrádloslos; imp_i2p_acc-dat_7=aterrádosla; imp_i2p_acc-dat_7=aterrádoslas; imp_i2p_acc-dat_7=aterrádoslo; imp_i2p_acc-dat_7=aterrádoslos; imp_i2p_acc_1=aterradme; imp_i2p_acc_3=aterradlo; imp_i2p_acc_4=aterradnos; imp_i2p_acc_5=aterraos; imp_i2p_acc_6=aterradlos; imp_i2p_acc_7=aterrados; imp_i2p_dat_1=aterradme; imp_i2p_dat_3=aterradle; imp_i2p_dat_4=aterradnos; imp_i2p_dat_5=aterraos; imp_i2p_dat_6=aterradles; imp_i2s_acc-dat_1=atiérrámela; imp_i2s_acc-dat_1=atiérrámelas; imp_i2s_acc-dat_1=atiérrámelo; imp_i2s_acc-dat_1=atiérrámelos; imp_i2s_acc-dat_2=atiérrátela; imp_i2s_acc-dat_2=atiérrátelas; imp_i2s_acc-dat_2=atiérrátelo; imp_i2s_acc-dat_2=atiérrátelos; imp_i2s_acc-dat_3=atiérrala; imp_i2s_acc-dat_3=atiérrálola; imp_i2s_acc-dat_3=atiérrálolas; imp_i2s_acc-dat_3=atiérrálolo; imp_i2s_acc-dat_3=atiérrálolos; imp_i2s_acc-dat_4=atiérránosla; imp_i2s_acc-dat_4=atiérránoslas; imp_i2s_acc-dat_4=atiérránoslo; imp_i2s_acc-dat_4=atiérránoslos; imp_i2s_acc-dat_6=atiérralas; imp_i2s_acc-dat_6=atiérrálosla; imp_i2s_acc-dat_6=atiérráloslas; imp_i2s_acc-dat_6=atiérráloslo; imp_i2s_acc-dat_6=atiérráloslos; imp_i2s_acc_1=atiérrame; imp_i2s_acc_2=atiérrate; imp_i2s_acc_3=atiérralo; imp_i2s_acc_4=atiérranos; imp_i2s_acc_6=atiérralos; imp_i2s_dat_1=atiérrame; imp_i2s_dat_2=atiérrate; imp_i2s_dat_3=atiérrale; imp_i2s_dat_4=atiérranos; imp_i2s_dat_6=atiérrales; inf_acc-dat_1=aterrármela; inf_acc-dat_1=aterrármelas; inf_acc-dat_1=aterrármelo; inf_acc-dat_1=aterrármelos; inf_acc-dat_2=aterrártela; inf_acc-dat_2=aterrártelas; inf_acc-dat_2=aterrártelo; inf_acc-dat_2=aterrártelos; inf_acc-dat_3=aterrarla; inf_acc-dat_3=aterrarse; inf_acc-dat_3=aterrárlola; inf_acc-dat_3=aterrárlolas; inf_acc-dat_3=aterrárlolo; inf_acc-dat_3=aterrárlolos; inf_acc-dat_4=aterrárnosla; inf_acc-dat_4=aterrárnoslas; inf_acc-dat_4=aterrárnoslo; inf_acc-dat_4=aterrárnoslos; inf_acc-dat_5=aterrárosla; inf_acc-dat_5=aterrároslas; inf_acc-dat_5=aterrároslo; inf_acc-dat_5=aterrároslos; inf_acc-dat_6=aterrarlas; inf_acc-dat_6=aterrarse; inf_acc-dat_6=aterrárlosla; inf_acc-dat_6=aterrárloslas; inf_acc-dat_6=aterrárloslo; inf_acc-dat_6=aterrárloslos; inf_acc-dat_7=aterrársela; inf_acc-dat_7=aterrárselas; inf_acc-dat_7=aterrárselo; inf_acc-dat_7=aterrárselos; inf_acc_1=aterrarme; inf_acc_2=aterrarte; inf_acc_3=aterrarlo; inf_acc_4=aterrarnos; inf_acc_5=aterraros; inf_acc_6=aterrarlos; inf_acc_7=aterrarse; inf_dat_1=aterrarme; inf_dat_2=aterrarte; inf_dat_3=aterrarle; inf_dat_3=aterrarse; inf_dat_4=aterrarnos; inf_dat_5=aterraros; inf_dat_6=aterrarles; inf_dat_6=aterrarse
aterrar {vt} :: to bring down, to ground
aterrar {verb-forms} :: 1=aterrar; 10=aterra; 11=aterramos; 12=aterráis; 13=aterran; 14=aterraba; 15=aterrabas; 16=aterraba; 17=aterrábamos; 18=aterrabais; 19=aterraban; 2=aterrando; 20=aterré; 21=aterraste; 22=aterró; 23=aterramos; 24=aterrasteis; 25=aterraron; 26=aterraré; 27=aterrarás; 28=aterrará; 29=aterraremos; 3=aterrado; 30=aterraréis; 31=aterrarán; 32=aterraría; 33=aterrarías; 34=aterraría; 35=aterraríamos; 36=aterraríais; 37=aterrarían; 38=aterre; 39=aterres; 4=aterrada; 40=aterrés; 41=aterre; 42=aterremos; 43=aterréis; 44=aterren; 45=aterrara; 46=aterraras; 47=aterrara; 48=aterráramos; 49=aterrarais; 5=aterrados; 50=aterraran; 51=aterrase; 52=aterrases; 53=aterrase; 54=aterrásemos; 55=aterraseis; 56=aterrasen; 57=aterrare; 58=aterrares; 59=aterrare; 6=aterradas; 60=aterráremos; 61=aterrareis; 62=aterraren; 63=aterra; 64=aterrá; 65=aterre; 66=aterremos; 67=aterrad; 68=aterren; 69=aterres; 7=aterro; 70=aterre; 71=aterremos; 72=aterréis; 73=aterren; 8=aterras; 9=aterrás; ger_acc-dat_1=aterrándómela; ger_acc-dat_1=aterrándómelas; ger_acc-dat_1=aterrándómelo; ger_acc-dat_1=aterrándómelos; ger_acc-dat_2=aterrándótela; ger_acc-dat_2=aterrándótelas; ger_acc-dat_2=aterrándótelo; ger_acc-dat_2=aterrándótelos; ger_acc-dat_3=aterrándola; ger_acc-dat_3=aterrándose; ger_acc-dat_3=aterrándólola; ger_acc-dat_3=aterrándólolas; ger_acc-dat_3=aterrándólolo; ger_acc-dat_3=aterrándólolos; ger_acc-dat_4=aterrándónosla; ger_acc-dat_4=aterrándónoslas; ger_acc-dat_4=aterrándónoslo; ger_acc-dat_4=aterrándónoslos; ger_acc-dat_5=aterrándóosla; ger_acc-dat_5=aterrándóoslas; ger_acc-dat_5=aterrándóoslo; ger_acc-dat_5=aterrándóoslos; ger_acc-dat_6=aterrándolas; ger_acc-dat_6=aterrándose; ger_acc-dat_6=aterrándólosla; ger_acc-dat_6=aterrándóloslas; ger_acc-dat_6=aterrándóloslo; ger_acc-dat_6=aterrándóloslos; ger_acc-dat_7=aterrándósela; ger_acc-dat_7=aterrándóselas; ger_acc-dat_7=aterrándóselo; ger_acc-dat_7=aterrándóselos; ger_acc_1=aterrándome; ger_acc_2=aterrándote; ger_acc_3=aterrándolo; ger_acc_4=aterrándonos; ger_acc_5=aterrándoos; ger_acc_6=aterrándolos; ger_acc_7=aterrándose; ger_dat_1=aterrándome; ger_dat_2=aterrándote; ger_dat_3=aterrándole; ger_dat_3=aterrándose; ger_dat_4=aterrándonos; ger_dat_5=aterrándoos; ger_dat_6=aterrándoles; ger_dat_6=aterrándose; imp_1p_acc-dat_2=aterrémóstela; imp_1p_acc-dat_2=aterrémóstelas; imp_1p_acc-dat_2=aterrémóstelo; imp_1p_acc-dat_2=aterrémóstelos; imp_1p_acc-dat_3=aterrémosla; imp_1p_acc-dat_3=aterrémóslola; imp_1p_acc-dat_3=aterrémóslolas; imp_1p_acc-dat_3=aterrémóslolo; imp_1p_acc-dat_3=aterrémóslolos; imp_1p_acc-dat_4=aterrémónosla; imp_1p_acc-dat_4=aterrémónoslas; imp_1p_acc-dat_4=aterrémónoslo; imp_1p_acc-dat_4=aterrémónoslos; imp_1p_acc-dat_5=aterrémóosla; imp_1p_acc-dat_5=aterrémóoslas; imp_1p_acc-dat_5=aterrémóoslo; imp_1p_acc-dat_5=aterrémóoslos; imp_1p_acc-dat_6=aterrémoslas; imp_1p_acc-dat_6=aterrémóslosla; imp_1p_acc-dat_6=aterrémósloslas; imp_1p_acc-dat_6=aterrémósloslo; imp_1p_acc-dat_6=aterrémósloslos; imp_1p_acc_2=aterrémoste; imp_1p_acc_3=aterrémoslo; imp_1p_acc_4=aterrémonos; imp_1p_acc_5=aterrémoos; imp_1p_acc_6=aterrémoslos; imp_1p_dat_2=aterrémoste; imp_1p_dat_3=aterrémosle; imp_1p_dat_4=aterrémonos; imp_1p_dat_5=aterrémoos; imp_1p_dat_6=aterrémosles; imp_f2p_acc-dat_1=atérrénmela; imp_f2p_acc-dat_1=atérrénmelas; imp_f2p_acc-dat_1=atérrénmelo; imp_f2p_acc-dat_1=atérrénmelos; imp_f2p_acc-dat_3=atérrenla; imp_f2p_acc-dat_3=atérrénlola; imp_f2p_acc-dat_3=atérrénlolas; imp_f2p_acc-dat_3=atérrénlolo; imp_f2p_acc-dat_3=atérrénlolos; imp_f2p_acc-dat_4=atérrénnosla; imp_f2p_acc-dat_4=atérrénnoslas; imp_f2p_acc-dat_4=atérrénnoslo; imp_f2p_acc-dat_4=atérrénnoslos; imp_f2p_acc-dat_6=atérrenlas; imp_f2p_acc-dat_6=atérrense; imp_f2p_acc-dat_6=atérrénlosla; imp_f2p_acc-dat_6=atérrénloslas; imp_f2p_acc-dat_6=atérrénloslo; imp_f2p_acc-dat_6=atérrénloslos; imp_f2p_acc-dat_7=atérrénsela; imp_f2p_acc-dat_7=atérrénselas; imp_f2p_acc-dat_7=atérrénselo; imp_f2p_acc-dat_7=atérrénselos; imp_f2p_acc_1=atérrenme; imp_f2p_acc_3=atérrenlo; imp_f2p_acc_4=atérrennos; imp_f2p_acc_6=atérrenlos; imp_f2p_acc_7=atérrense; imp_f2p_dat_1=atérrenme; imp_f2p_dat_3=atérrenle; imp_f2p_dat_4=atérrennos; imp_f2p_dat_6=atérrenles; imp_f2p_dat_6=atérrense; imp_f2s_acc-dat_1=atérrémela; imp_f2s_acc-dat_1=atérrémelas; imp_f2s_acc-dat_1=atérrémelo; imp_f2s_acc-dat_1=atérrémelos; imp_f2s_acc-dat_3=atérrela; imp_f2s_acc-dat_3=atérrese; imp_f2s_acc-dat_3=atérrélola; imp_f2s_acc-dat_3=atérrélolas; imp_f2s_acc-dat_3=atérrélolo; imp_f2s_acc-dat_3=atérrélolos; imp_f2s_acc-dat_4=atérrénosla; imp_f2s_acc-dat_4=atérrénoslas; imp_f2s_acc-dat_4=atérrénoslo; imp_f2s_acc-dat_4=atérrénoslos; imp_f2s_acc-dat_6=atérrelas; imp_f2s_acc-dat_6=atérrélosla; imp_f2s_acc-dat_6=atérréloslas; imp_f2s_acc-dat_6=atérréloslo; imp_f2s_acc-dat_6=atérréloslos; imp_f2s_acc-dat_7=atérrésela; imp_f2s_acc-dat_7=atérréselas; imp_f2s_acc-dat_7=atérréselo; imp_f2s_acc-dat_7=atérréselos; imp_f2s_acc_1=atérreme; imp_f2s_acc_3=atérrelo; imp_f2s_acc_4=atérrenos; imp_f2s_acc_6=atérrelos; imp_f2s_acc_7=atérrese; imp_f2s_dat_1=atérreme; imp_f2s_dat_3=atérrele; imp_f2s_dat_3=atérrese; imp_f2s_dat_4=atérrenos; imp_f2s_dat_6=atérreles; imp_i2p_acc-dat_1=aterrádmela; imp_i2p_acc-dat_1=aterrádmelas; imp_i2p_acc-dat_1=aterrádmelo; imp_i2p_acc-dat_1=aterrádmelos; imp_i2p_acc-dat_3=aterradla; imp_i2p_acc-dat_3=aterrádlola; imp_i2p_acc-dat_3=aterrádlolas; imp_i2p_acc-dat_3=aterrádlolo; imp_i2p_acc-dat_3=aterrádlolos; imp_i2p_acc-dat_4=aterrádnosla; imp_i2p_acc-dat_4=aterrádnoslas; imp_i2p_acc-dat_4=aterrádnoslo; imp_i2p_acc-dat_4=aterrádnoslos; imp_i2p_acc-dat_5=aterráosla; imp_i2p_acc-dat_5=aterráoslas; imp_i2p_acc-dat_5=aterráoslo; imp_i2p_acc-dat_5=aterráoslos; imp_i2p_acc-dat_6=aterradlas; imp_i2p_acc-dat_6=aterrádlosla; imp_i2p_acc-dat_6=aterrádloslas; imp_i2p_acc-dat_6=aterrádloslo; imp_i2p_acc-dat_6=aterrádloslos; imp_i2p_acc-dat_7=aterrádosla; imp_i2p_acc-dat_7=aterrádoslas; imp_i2p_acc-dat_7=aterrádoslo; imp_i2p_acc-dat_7=aterrádoslos; imp_i2p_acc_1=aterradme; imp_i2p_acc_3=aterradlo; imp_i2p_acc_4=aterradnos; imp_i2p_acc_5=aterraos; imp_i2p_acc_6=aterradlos; imp_i2p_acc_7=aterrados; imp_i2p_dat_1=aterradme; imp_i2p_dat_3=aterradle; imp_i2p_dat_4=aterradnos; imp_i2p_dat_5=aterraos; imp_i2p_dat_6=aterradles; imp_i2s_acc-dat_1=atérrámela; imp_i2s_acc-dat_1=atérrámelas; imp_i2s_acc-dat_1=atérrámelo; imp_i2s_acc-dat_1=atérrámelos; imp_i2s_acc-dat_2=atérrátela; imp_i2s_acc-dat_2=atérrátelas; imp_i2s_acc-dat_2=atérrátelo; imp_i2s_acc-dat_2=atérrátelos; imp_i2s_acc-dat_3=atérrala; imp_i2s_acc-dat_3=atérrálola; imp_i2s_acc-dat_3=atérrálolas; imp_i2s_acc-dat_3=atérrálolo; imp_i2s_acc-dat_3=atérrálolos; imp_i2s_acc-dat_4=atérránosla; imp_i2s_acc-dat_4=atérránoslas; imp_i2s_acc-dat_4=atérránoslo; imp_i2s_acc-dat_4=atérránoslos; imp_i2s_acc-dat_6=atérralas; imp_i2s_acc-dat_6=atérrálosla; imp_i2s_acc-dat_6=atérráloslas; imp_i2s_acc-dat_6=atérráloslo; imp_i2s_acc-dat_6=atérráloslos; imp_i2s_acc_1=atérrame; imp_i2s_acc_2=atérrate; imp_i2s_acc_3=atérralo; imp_i2s_acc_4=atérranos; imp_i2s_acc_6=atérralos; imp_i2s_dat_1=atérrame; imp_i2s_dat_2=atérrate; imp_i2s_dat_3=atérrale; imp_i2s_dat_4=atérranos; imp_i2s_dat_6=atérrales; inf_acc-dat_1=aterrármela; inf_acc-dat_1=aterrármelas; inf_acc-dat_1=aterrármelo; inf_acc-dat_1=aterrármelos; inf_acc-dat_2=aterrártela; inf_acc-dat_2=aterrártelas; inf_acc-dat_2=aterrártelo; inf_acc-dat_2=aterrártelos; inf_acc-dat_3=aterrarla; inf_acc-dat_3=aterrarse; inf_acc-dat_3=aterrárlola; inf_acc-dat_3=aterrárlolas; inf_acc-dat_3=aterrárlolo; inf_acc-dat_3=aterrárlolos; inf_acc-dat_4=aterrárnosla; inf_acc-dat_4=aterrárnoslas; inf_acc-dat_4=aterrárnoslo; inf_acc-dat_4=aterrárnoslos; inf_acc-dat_5=aterrárosla; inf_acc-dat_5=aterrároslas; inf_acc-dat_5=aterrároslo; inf_acc-dat_5=aterrároslos; inf_acc-dat_6=aterrarlas; inf_acc-dat_6=aterrarse; inf_acc-dat_6=aterrárlosla; inf_acc-dat_6=aterrárloslas; inf_acc-dat_6=aterrárloslo; inf_acc-dat_6=aterrárloslos; inf_acc-dat_7=aterrársela; inf_acc-dat_7=aterrárselas; inf_acc-dat_7=aterrárselo; inf_acc-dat_7=aterrárselos; inf_acc_1=aterrarme; inf_acc_2=aterrarte; inf_acc_3=aterrarlo; inf_acc_4=aterrarnos; inf_acc_5=aterraros; inf_acc_6=aterrarlos; inf_acc_7=aterrarse; inf_dat_1=aterrarme; inf_dat_2=aterrarte; inf_dat_3=aterrarle; inf_dat_3=aterrarse; inf_dat_4=aterrarnos; inf_dat_5=aterraros; inf_dat_6=aterrarles; inf_dat_6=aterrarse
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
atentar {verb-forms} :: 1=atentar; 10=atienta; 11=atentamos; 12=atentáis; 13=atientan; 14=atentaba; 15=atentabas; 16=atentaba; 17=atentábamos; 18=atentabais; 19=atentaban; 2=atentando; 20=atenté; 21=atentaste; 22=atentó; 23=atentamos; 24=atentasteis; 25=atentaron; 26=atentaré; 27=atentarás; 28=atentará; 29=atentaremos; 3=atentado; 30=atentaréis; 31=atentarán; 32=atentaría; 33=atentarías; 34=atentaría; 35=atentaríamos; 36=atentaríais; 37=atentarían; 38=atiente; 39=atientes; 4=atentada; 40=atentés; 41=atiente; 42=atentemos; 43=atentéis; 44=atienten; 45=atentara; 46=atentaras; 47=atentara; 48=atentáramos; 49=atentarais; 5=atentados; 50=atentaran; 51=atentase; 52=atentases; 53=atentase; 54=atentásemos; 55=atentaseis; 56=atentasen; 57=atentare; 58=atentares; 59=atentare; 6=atentadas; 60=atentáremos; 61=atentareis; 62=atentaren; 63=atienta; 64=atentá; 65=atiente; 66=atentemos; 67=atentad; 68=atienten; 69=atientes; 7=atiento; 70=atiente; 71=atentemos; 72=atentéis; 73=atienten; 8=atientas; 9=atentás; ger_acc-dat_1=atentándómela; ger_acc-dat_1=atentándómelas; ger_acc-dat_1=atentándómelo; ger_acc-dat_1=atentándómelos; ger_acc-dat_2=atentándótela; ger_acc-dat_2=atentándótelas; ger_acc-dat_2=atentándótelo; ger_acc-dat_2=atentándótelos; ger_acc-dat_3=atentándola; ger_acc-dat_3=atentándose; ger_acc-dat_3=atentándólola; ger_acc-dat_3=atentándólolas; ger_acc-dat_3=atentándólolo; ger_acc-dat_3=atentándólolos; ger_acc-dat_4=atentándónosla; ger_acc-dat_4=atentándónoslas; ger_acc-dat_4=atentándónoslo; ger_acc-dat_4=atentándónoslos; ger_acc-dat_5=atentándóosla; ger_acc-dat_5=atentándóoslas; ger_acc-dat_5=atentándóoslo; ger_acc-dat_5=atentándóoslos; ger_acc-dat_6=atentándolas; ger_acc-dat_6=atentándose; ger_acc-dat_6=atentándólosla; ger_acc-dat_6=atentándóloslas; ger_acc-dat_6=atentándóloslo; ger_acc-dat_6=atentándóloslos; ger_acc-dat_7=atentándósela; ger_acc-dat_7=atentándóselas; ger_acc-dat_7=atentándóselo; ger_acc-dat_7=atentándóselos; ger_acc_1=atentándome; ger_acc_2=atentándote; ger_acc_3=atentándolo; ger_acc_4=atentándonos; ger_acc_5=atentándoos; ger_acc_6=atentándolos; ger_acc_7=atentándose; ger_dat_1=atentándome; ger_dat_2=atentándote; ger_dat_3=atentándole; ger_dat_3=atentándose; ger_dat_4=atentándonos; ger_dat_5=atentándoos; ger_dat_6=atentándoles; ger_dat_6=atentándose; imp_1p_acc-dat_2=atentémóstela; imp_1p_acc-dat_2=atentémóstelas; imp_1p_acc-dat_2=atentémóstelo; imp_1p_acc-dat_2=atentémóstelos; imp_1p_acc-dat_3=atentémosla; imp_1p_acc-dat_3=atentémóslola; imp_1p_acc-dat_3=atentémóslolas; imp_1p_acc-dat_3=atentémóslolo; imp_1p_acc-dat_3=atentémóslolos; imp_1p_acc-dat_4=atentémónosla; imp_1p_acc-dat_4=atentémónoslas; imp_1p_acc-dat_4=atentémónoslo; imp_1p_acc-dat_4=atentémónoslos; imp_1p_acc-dat_5=atentémóosla; imp_1p_acc-dat_5=atentémóoslas; imp_1p_acc-dat_5=atentémóoslo; imp_1p_acc-dat_5=atentémóoslos; imp_1p_acc-dat_6=atentémoslas; imp_1p_acc-dat_6=atentémóslosla; imp_1p_acc-dat_6=atentémósloslas; imp_1p_acc-dat_6=atentémósloslo; imp_1p_acc-dat_6=atentémósloslos; imp_1p_acc_2=atentémoste; imp_1p_acc_3=atentémoslo; imp_1p_acc_4=atentémonos; imp_1p_acc_5=atentémoos; imp_1p_acc_6=atentémoslos; imp_1p_dat_2=atentémoste; imp_1p_dat_3=atentémosle; imp_1p_dat_4=atentémonos; imp_1p_dat_5=atentémoos; imp_1p_dat_6=atentémosles; imp_f2p_acc-dat_1=atiénténmela; imp_f2p_acc-dat_1=atiénténmelas; imp_f2p_acc-dat_1=atiénténmelo; imp_f2p_acc-dat_1=atiénténmelos; imp_f2p_acc-dat_3=atiéntenla; imp_f2p_acc-dat_3=atiénténlola; imp_f2p_acc-dat_3=atiénténlolas; imp_f2p_acc-dat_3=atiénténlolo; imp_f2p_acc-dat_3=atiénténlolos; imp_f2p_acc-dat_4=atiénténnosla; imp_f2p_acc-dat_4=atiénténnoslas; imp_f2p_acc-dat_4=atiénténnoslo; imp_f2p_acc-dat_4=atiénténnoslos; imp_f2p_acc-dat_6=atiéntenlas; imp_f2p_acc-dat_6=atiéntense; imp_f2p_acc-dat_6=atiénténlosla; imp_f2p_acc-dat_6=atiénténloslas; imp_f2p_acc-dat_6=atiénténloslo; imp_f2p_acc-dat_6=atiénténloslos; imp_f2p_acc-dat_7=atiénténsela; imp_f2p_acc-dat_7=atiénténselas; imp_f2p_acc-dat_7=atiénténselo; imp_f2p_acc-dat_7=atiénténselos; imp_f2p_acc_1=atiéntenme; imp_f2p_acc_3=atiéntenlo; imp_f2p_acc_4=atiéntennos; imp_f2p_acc_6=atiéntenlos; imp_f2p_acc_7=atiéntense; imp_f2p_dat_1=atiéntenme; imp_f2p_dat_3=atiéntenle; imp_f2p_dat_4=atiéntennos; imp_f2p_dat_6=atiéntenles; imp_f2p_dat_6=atiéntense; imp_f2s_acc-dat_1=atiéntémela; imp_f2s_acc-dat_1=atiéntémelas; imp_f2s_acc-dat_1=atiéntémelo; imp_f2s_acc-dat_1=atiéntémelos; imp_f2s_acc-dat_3=atiéntela; imp_f2s_acc-dat_3=atiéntese; imp_f2s_acc-dat_3=atiéntélola; imp_f2s_acc-dat_3=atiéntélolas; imp_f2s_acc-dat_3=atiéntélolo; imp_f2s_acc-dat_3=atiéntélolos; imp_f2s_acc-dat_4=atiénténosla; imp_f2s_acc-dat_4=atiénténoslas; imp_f2s_acc-dat_4=atiénténoslo; imp_f2s_acc-dat_4=atiénténoslos; imp_f2s_acc-dat_6=atiéntelas; imp_f2s_acc-dat_6=atiéntélosla; imp_f2s_acc-dat_6=atiéntéloslas; imp_f2s_acc-dat_6=atiéntéloslo; imp_f2s_acc-dat_6=atiéntéloslos; imp_f2s_acc-dat_7=atiéntésela; imp_f2s_acc-dat_7=atiéntéselas; imp_f2s_acc-dat_7=atiéntéselo; imp_f2s_acc-dat_7=atiéntéselos; imp_f2s_acc_1=atiénteme; imp_f2s_acc_3=atiéntelo; imp_f2s_acc_4=atiéntenos; imp_f2s_acc_6=atiéntelos; imp_f2s_acc_7=atiéntese; imp_f2s_dat_1=atiénteme; imp_f2s_dat_3=atiéntele; imp_f2s_dat_3=atiéntese; imp_f2s_dat_4=atiéntenos; imp_f2s_dat_6=atiénteles; imp_i2p_acc-dat_1=atentádmela; imp_i2p_acc-dat_1=atentádmelas; imp_i2p_acc-dat_1=atentádmelo; imp_i2p_acc-dat_1=atentádmelos; imp_i2p_acc-dat_3=atentadla; imp_i2p_acc-dat_3=atentádlola; imp_i2p_acc-dat_3=atentádlolas; imp_i2p_acc-dat_3=atentádlolo; imp_i2p_acc-dat_3=atentádlolos; imp_i2p_acc-dat_4=atentádnosla; imp_i2p_acc-dat_4=atentádnoslas; imp_i2p_acc-dat_4=atentádnoslo; imp_i2p_acc-dat_4=atentádnoslos; imp_i2p_acc-dat_5=atentáosla; imp_i2p_acc-dat_5=atentáoslas; imp_i2p_acc-dat_5=atentáoslo; imp_i2p_acc-dat_5=atentáoslos; imp_i2p_acc-dat_6=atentadlas; imp_i2p_acc-dat_6=atentádlosla; imp_i2p_acc-dat_6=atentádloslas; imp_i2p_acc-dat_6=atentádloslo; imp_i2p_acc-dat_6=atentádloslos; imp_i2p_acc-dat_7=atentádosla; imp_i2p_acc-dat_7=atentádoslas; imp_i2p_acc-dat_7=atentádoslo; imp_i2p_acc-dat_7=atentádoslos; imp_i2p_acc_1=atentadme; imp_i2p_acc_3=atentadlo; imp_i2p_acc_4=atentadnos; imp_i2p_acc_5=atentaos; imp_i2p_acc_6=atentadlos; imp_i2p_acc_7=atentados; imp_i2p_dat_1=atentadme; imp_i2p_dat_3=atentadle; imp_i2p_dat_4=atentadnos; imp_i2p_dat_5=atentaos; imp_i2p_dat_6=atentadles; imp_i2s_acc-dat_1=atiéntámela; imp_i2s_acc-dat_1=atiéntámelas; imp_i2s_acc-dat_1=atiéntámelo; imp_i2s_acc-dat_1=atiéntámelos; imp_i2s_acc-dat_2=atiéntátela; imp_i2s_acc-dat_2=atiéntátelas; imp_i2s_acc-dat_2=atiéntátelo; imp_i2s_acc-dat_2=atiéntátelos; imp_i2s_acc-dat_3=atiéntala; imp_i2s_acc-dat_3=atiéntálola; imp_i2s_acc-dat_3=atiéntálolas; imp_i2s_acc-dat_3=atiéntálolo; imp_i2s_acc-dat_3=atiéntálolos; imp_i2s_acc-dat_4=atiéntánosla; imp_i2s_acc-dat_4=atiéntánoslas; imp_i2s_acc-dat_4=atiéntánoslo; imp_i2s_acc-dat_4=atiéntánoslos; imp_i2s_acc-dat_6=atiéntalas; imp_i2s_acc-dat_6=atiéntálosla; imp_i2s_acc-dat_6=atiéntáloslas; imp_i2s_acc-dat_6=atiéntáloslo; imp_i2s_acc-dat_6=atiéntáloslos; imp_i2s_acc_1=atiéntame; imp_i2s_acc_2=atiéntate; imp_i2s_acc_3=atiéntalo; imp_i2s_acc_4=atiéntanos; imp_i2s_acc_6=atiéntalos; imp_i2s_dat_1=atiéntame; imp_i2s_dat_2=atiéntate; imp_i2s_dat_3=atiéntale; imp_i2s_dat_4=atiéntanos; imp_i2s_dat_6=atiéntales; inf_acc-dat_1=atentármela; inf_acc-dat_1=atentármelas; inf_acc-dat_1=atentármelo; inf_acc-dat_1=atentármelos; inf_acc-dat_2=atentártela; inf_acc-dat_2=atentártelas; inf_acc-dat_2=atentártelo; inf_acc-dat_2=atentártelos; inf_acc-dat_3=atentarla; inf_acc-dat_3=atentarse; inf_acc-dat_3=atentárlola; inf_acc-dat_3=atentárlolas; inf_acc-dat_3=atentárlolo; inf_acc-dat_3=atentárlolos; inf_acc-dat_4=atentárnosla; inf_acc-dat_4=atentárnoslas; inf_acc-dat_4=atentárnoslo; inf_acc-dat_4=atentárnoslos; inf_acc-dat_5=atentárosla; inf_acc-dat_5=atentároslas; inf_acc-dat_5=atentároslo; inf_acc-dat_5=atentároslos; inf_acc-dat_6=atentarlas; inf_acc-dat_6=atentarse; inf_acc-dat_6=atentárlosla; inf_acc-dat_6=atentárloslas; inf_acc-dat_6=atentárloslo; inf_acc-dat_6=atentárloslos; inf_acc-dat_7=atentársela; inf_acc-dat_7=atentárselas; inf_acc-dat_7=atentárselo; inf_acc-dat_7=atentárselos; inf_acc_1=atentarme; inf_acc_2=atentarte; inf_acc_3=atentarlo; inf_acc_4=atentarnos; inf_acc_5=atentaros; inf_acc_6=atentarlos; inf_acc_7=atentarse; inf_dat_1=atentarme; inf_dat_2=atentarte; inf_dat_3=atentarle; inf_dat_3=atentarse; inf_dat_4=atentarnos; inf_dat_5=atentaros; inf_dat_6=atentarles; inf_dat_6=atentarse
atentar {vi} :: to commit a violent or criminal attack, to strike
atentar {verb-forms} :: 1=atentar; 10=atienta; 11=atentamos; 12=atentáis; 13=atientan; 14=atentaba; 15=atentabas; 16=atentaba; 17=atentábamos; 18=atentabais; 19=atentaban; 2=atentando; 20=atenté; 21=atentaste; 22=atentó; 23=atentamos; 24=atentasteis; 25=atentaron; 26=atentaré; 27=atentarás; 28=atentará; 29=atentaremos; 3=atentado; 30=atentaréis; 31=atentarán; 32=atentaría; 33=atentarías; 34=atentaría; 35=atentaríamos; 36=atentaríais; 37=atentarían; 38=atiente; 39=atientes; 4=atentada; 40=atentés; 41=atiente; 42=atentemos; 43=atentéis; 44=atienten; 45=atentara; 46=atentaras; 47=atentara; 48=atentáramos; 49=atentarais; 5=atentados; 50=atentaran; 51=atentase; 52=atentases; 53=atentase; 54=atentásemos; 55=atentaseis; 56=atentasen; 57=atentare; 58=atentares; 59=atentare; 6=atentadas; 60=atentáremos; 61=atentareis; 62=atentaren; 63=atienta; 64=atentá; 65=atiente; 66=atentemos; 67=atentad; 68=atienten; 69=atientes; 7=atiento; 70=atiente; 71=atentemos; 72=atentéis; 73=atienten; 8=atientas; 9=atentás; ger_acc-dat_1=atentándómela; ger_acc-dat_1=atentándómelas; ger_acc-dat_1=atentándómelo; ger_acc-dat_1=atentándómelos; ger_acc-dat_2=atentándótela; ger_acc-dat_2=atentándótelas; ger_acc-dat_2=atentándótelo; ger_acc-dat_2=atentándótelos; ger_acc-dat_3=atentándola; ger_acc-dat_3=atentándose; ger_acc-dat_3=atentándólola; ger_acc-dat_3=atentándólolas; ger_acc-dat_3=atentándólolo; ger_acc-dat_3=atentándólolos; ger_acc-dat_4=atentándónosla; ger_acc-dat_4=atentándónoslas; ger_acc-dat_4=atentándónoslo; ger_acc-dat_4=atentándónoslos; ger_acc-dat_5=atentándóosla; ger_acc-dat_5=atentándóoslas; ger_acc-dat_5=atentándóoslo; ger_acc-dat_5=atentándóoslos; ger_acc-dat_6=atentándolas; ger_acc-dat_6=atentándose; ger_acc-dat_6=atentándólosla; ger_acc-dat_6=atentándóloslas; ger_acc-dat_6=atentándóloslo; ger_acc-dat_6=atentándóloslos; ger_acc-dat_7=atentándósela; ger_acc-dat_7=atentándóselas; ger_acc-dat_7=atentándóselo; ger_acc-dat_7=atentándóselos; ger_acc_1=atentándome; ger_acc_2=atentándote; ger_acc_3=atentándolo; ger_acc_4=atentándonos; ger_acc_5=atentándoos; ger_acc_6=atentándolos; ger_acc_7=atentándose; ger_dat_1=atentándome; ger_dat_2=atentándote; ger_dat_3=atentándole; ger_dat_3=atentándose; ger_dat_4=atentándonos; ger_dat_5=atentándoos; ger_dat_6=atentándoles; ger_dat_6=atentándose; imp_1p_acc-dat_2=atentémóstela; imp_1p_acc-dat_2=atentémóstelas; imp_1p_acc-dat_2=atentémóstelo; imp_1p_acc-dat_2=atentémóstelos; imp_1p_acc-dat_3=atentémosla; imp_1p_acc-dat_3=atentémóslola; imp_1p_acc-dat_3=atentémóslolas; imp_1p_acc-dat_3=atentémóslolo; imp_1p_acc-dat_3=atentémóslolos; imp_1p_acc-dat_4=atentémónosla; imp_1p_acc-dat_4=atentémónoslas; imp_1p_acc-dat_4=atentémónoslo; imp_1p_acc-dat_4=atentémónoslos; imp_1p_acc-dat_5=atentémóosla; imp_1p_acc-dat_5=atentémóoslas; imp_1p_acc-dat_5=atentémóoslo; imp_1p_acc-dat_5=atentémóoslos; imp_1p_acc-dat_6=atentémoslas; imp_1p_acc-dat_6=atentémóslosla; imp_1p_acc-dat_6=atentémósloslas; imp_1p_acc-dat_6=atentémósloslo; imp_1p_acc-dat_6=atentémósloslos; imp_1p_acc_2=atentémoste; imp_1p_acc_3=atentémoslo; imp_1p_acc_4=atentémonos; imp_1p_acc_5=atentémoos; imp_1p_acc_6=atentémoslos; imp_1p_dat_2=atentémoste; imp_1p_dat_3=atentémosle; imp_1p_dat_4=atentémonos; imp_1p_dat_5=atentémoos; imp_1p_dat_6=atentémosles; imp_f2p_acc-dat_1=atiénténmela; imp_f2p_acc-dat_1=atiénténmelas; imp_f2p_acc-dat_1=atiénténmelo; imp_f2p_acc-dat_1=atiénténmelos; imp_f2p_acc-dat_3=atiéntenla; imp_f2p_acc-dat_3=atiénténlola; imp_f2p_acc-dat_3=atiénténlolas; imp_f2p_acc-dat_3=atiénténlolo; imp_f2p_acc-dat_3=atiénténlolos; imp_f2p_acc-dat_4=atiénténnosla; imp_f2p_acc-dat_4=atiénténnoslas; imp_f2p_acc-dat_4=atiénténnoslo; imp_f2p_acc-dat_4=atiénténnoslos; imp_f2p_acc-dat_6=atiéntenlas; imp_f2p_acc-dat_6=atiéntense; imp_f2p_acc-dat_6=atiénténlosla; imp_f2p_acc-dat_6=atiénténloslas; imp_f2p_acc-dat_6=atiénténloslo; imp_f2p_acc-dat_6=atiénténloslos; imp_f2p_acc-dat_7=atiénténsela; imp_f2p_acc-dat_7=atiénténselas; imp_f2p_acc-dat_7=atiénténselo; imp_f2p_acc-dat_7=atiénténselos; imp_f2p_acc_1=atiéntenme; imp_f2p_acc_3=atiéntenlo; imp_f2p_acc_4=atiéntennos; imp_f2p_acc_6=atiéntenlos; imp_f2p_acc_7=atiéntense; imp_f2p_dat_1=atiéntenme; imp_f2p_dat_3=atiéntenle; imp_f2p_dat_4=atiéntennos; imp_f2p_dat_6=atiéntenles; imp_f2p_dat_6=atiéntense; imp_f2s_acc-dat_1=atiéntémela; imp_f2s_acc-dat_1=atiéntémelas; imp_f2s_acc-dat_1=atiéntémelo; imp_f2s_acc-dat_1=atiéntémelos; imp_f2s_acc-dat_3=atiéntela; imp_f2s_acc-dat_3=atiéntese; imp_f2s_acc-dat_3=atiéntélola; imp_f2s_acc-dat_3=atiéntélolas; imp_f2s_acc-dat_3=atiéntélolo; imp_f2s_acc-dat_3=atiéntélolos; imp_f2s_acc-dat_4=atiénténosla; imp_f2s_acc-dat_4=atiénténoslas; imp_f2s_acc-dat_4=atiénténoslo; imp_f2s_acc-dat_4=atiénténoslos; imp_f2s_acc-dat_6=atiéntelas; imp_f2s_acc-dat_6=atiéntélosla; imp_f2s_acc-dat_6=atiéntéloslas; imp_f2s_acc-dat_6=atiéntéloslo; imp_f2s_acc-dat_6=atiéntéloslos; imp_f2s_acc-dat_7=atiéntésela; imp_f2s_acc-dat_7=atiéntéselas; imp_f2s_acc-dat_7=atiéntéselo; imp_f2s_acc-dat_7=atiéntéselos; imp_f2s_acc_1=atiénteme; imp_f2s_acc_3=atiéntelo; imp_f2s_acc_4=atiéntenos; imp_f2s_acc_6=atiéntelos; imp_f2s_acc_7=atiéntese; imp_f2s_dat_1=atiénteme; imp_f2s_dat_3=atiéntele; imp_f2s_dat_3=atiéntese; imp_f2s_dat_4=atiéntenos; imp_f2s_dat_6=atiénteles; imp_i2p_acc-dat_1=atentádmela; imp_i2p_acc-dat_1=atentádmelas; imp_i2p_acc-dat_1=atentádmelo; imp_i2p_acc-dat_1=atentádmelos; imp_i2p_acc-dat_3=atentadla; imp_i2p_acc-dat_3=atentádlola; imp_i2p_acc-dat_3=atentádlolas; imp_i2p_acc-dat_3=atentádlolo; imp_i2p_acc-dat_3=atentádlolos; imp_i2p_acc-dat_4=atentádnosla; imp_i2p_acc-dat_4=atentádnoslas; imp_i2p_acc-dat_4=atentádnoslo; imp_i2p_acc-dat_4=atentádnoslos; imp_i2p_acc-dat_5=atentáosla; imp_i2p_acc-dat_5=atentáoslas; imp_i2p_acc-dat_5=atentáoslo; imp_i2p_acc-dat_5=atentáoslos; imp_i2p_acc-dat_6=atentadlas; imp_i2p_acc-dat_6=atentádlosla; imp_i2p_acc-dat_6=atentádloslas; imp_i2p_acc-dat_6=atentádloslo; imp_i2p_acc-dat_6=atentádloslos; imp_i2p_acc-dat_7=atentádosla; imp_i2p_acc-dat_7=atentádoslas; imp_i2p_acc-dat_7=atentádoslo; imp_i2p_acc-dat_7=atentádoslos; imp_i2p_acc_1=atentadme; imp_i2p_acc_3=atentadlo; imp_i2p_acc_4=atentadnos; imp_i2p_acc_5=atentaos; imp_i2p_acc_6=atentadlos; imp_i2p_acc_7=atentados; imp_i2p_dat_1=atentadme; imp_i2p_dat_3=atentadle; imp_i2p_dat_4=atentadnos; imp_i2p_dat_5=atentaos; imp_i2p_dat_6=atentadles; imp_i2s_acc-dat_1=atiéntámela; imp_i2s_acc-dat_1=atiéntámelas; imp_i2s_acc-dat_1=atiéntámelo; imp_i2s_acc-dat_1=atiéntámelos; imp_i2s_acc-dat_2=atiéntátela; imp_i2s_acc-dat_2=atiéntátelas; imp_i2s_acc-dat_2=atiéntátelo; imp_i2s_acc-dat_2=atiéntátelos; imp_i2s_acc-dat_3=atiéntala; imp_i2s_acc-dat_3=atiéntálola; imp_i2s_acc-dat_3=atiéntálolas; imp_i2s_acc-dat_3=atiéntálolo; imp_i2s_acc-dat_3=atiéntálolos; imp_i2s_acc-dat_4=atiéntánosla; imp_i2s_acc-dat_4=atiéntánoslas; imp_i2s_acc-dat_4=atiéntánoslo; imp_i2s_acc-dat_4=atiéntánoslos; imp_i2s_acc-dat_6=atiéntalas; imp_i2s_acc-dat_6=atiéntálosla; imp_i2s_acc-dat_6=atiéntáloslas; imp_i2s_acc-dat_6=atiéntáloslo; imp_i2s_acc-dat_6=atiéntáloslos; imp_i2s_acc_1=atiéntame; imp_i2s_acc_2=atiéntate; imp_i2s_acc_3=atiéntalo; imp_i2s_acc_4=atiéntanos; imp_i2s_acc_6=atiéntalos; imp_i2s_dat_1=atiéntame; imp_i2s_dat_2=atiéntate; imp_i2s_dat_3=atiéntale; imp_i2s_dat_4=atiéntanos; imp_i2s_dat_6=atiéntales; inf_acc-dat_1=atentármela; inf_acc-dat_1=atentármelas; inf_acc-dat_1=atentármelo; inf_acc-dat_1=atentármelos; inf_acc-dat_2=atentártela; inf_acc-dat_2=atentártelas; inf_acc-dat_2=atentártelo; inf_acc-dat_2=atentártelos; inf_acc-dat_3=atentarla; inf_acc-dat_3=atentarse; inf_acc-dat_3=atentárlola; inf_acc-dat_3=atentárlolas; inf_acc-dat_3=atentárlolo; inf_acc-dat_3=atentárlolos; inf_acc-dat_4=atentárnosla; inf_acc-dat_4=atentárnoslas; inf_acc-dat_4=atentárnoslo; inf_acc-dat_4=atentárnoslos; inf_acc-dat_5=atentárosla; inf_acc-dat_5=atentároslas; inf_acc-dat_5=atentároslo; inf_acc-dat_5=atentároslos; inf_acc-dat_6=atentarlas; inf_acc-dat_6=atentarse; inf_acc-dat_6=atentárlosla; inf_acc-dat_6=atentárloslas; inf_acc-dat_6=atentárloslo; inf_acc-dat_6=atentárloslos; inf_acc-dat_7=atentársela; inf_acc-dat_7=atentárselas; inf_acc-dat_7=atentárselo; inf_acc-dat_7=atentárselos; inf_acc_1=atentarme; inf_acc_2=atentarte; inf_acc_3=atentarlo; inf_acc_4=atentarnos; inf_acc_5=atentaros; inf_acc_6=atentarlos; inf_acc_7=atentarse; inf_dat_1=atentarme; inf_dat_2=atentarte; inf_dat_3=atentarle; inf_dat_3=atentarse; inf_dat_4=atentarnos; inf_dat_5=atentaros; inf_dat_6=atentarles; inf_dat_6=atentarse
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
billón {noun-forms} :: pl=billones
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
robot {noun-forms} :: pl=robots
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
angla {noun-forms} :: m=anglo; mpl=anglos; pl=anglas
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
cherry {noun-forms} :: pl=cherries; pl=cherrys
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
    entry = builder.parse_entry(lang_entry, "torpón")

    assert "\n".join(entry)=="""\
torpón {adj-forms} :: f=torpona; fpl=torponas; pl=torpones
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
    entry = builder.parse_entry(lang_entry, "abandonar")

    assert "\n".join(entry) == """\
abandonar {verb-forms} :: 1=abandonar; 10=abandona; 11=abandonamos; 12=abandonáis; 13=abandonan; 14=abandonaba; 15=abandonabas; 16=abandonaba; 17=abandonábamos; 18=abandonabais; 19=abandonaban; 2=abandonando; 20=abandoné; 21=abandonaste; 22=abandonó; 23=abandonamos; 24=abandonasteis; 25=abandonaron; 26=abandonaré; 27=abandonarás; 28=abandonará; 29=abandonaremos; 3=abandonado; 30=abandonaréis; 31=abandonarán; 32=abandonaría; 33=abandonarías; 34=abandonaría; 35=abandonaríamos; 36=abandonaríais; 37=abandonarían; 38=abandone; 39=abandones; 4=abandonada; 40=abandonés; 41=abandone; 42=abandonemos; 43=abandonéis; 44=abandonen; 45=abandonara; 46=abandonaras; 47=abandonara; 48=abandonáramos; 49=abandonarais; 5=abandonados; 50=abandonaran; 51=abandonase; 52=abandonases; 53=abandonase; 54=abandonásemos; 55=abandonaseis; 56=abandonasen; 57=abandonare; 58=abandonares; 59=abandonare; 6=abandonadas; 60=abandonáremos; 61=abandonareis; 62=abandonaren; 63=abandona; 64=abandoná; 65=abandone; 66=abandonemos; 67=abandonad; 68=abandonen; 69=abandones; 7=abandono; 70=abandone; 71=abandonemos; 72=abandonéis; 73=abandonen; 8=abandonas; 9=abandonás; ger_acc-dat_1=abandonándómela; ger_acc-dat_1=abandonándómelas; ger_acc-dat_1=abandonándómelo; ger_acc-dat_1=abandonándómelos; ger_acc-dat_2=abandonándótela; ger_acc-dat_2=abandonándótelas; ger_acc-dat_2=abandonándótelo; ger_acc-dat_2=abandonándótelos; ger_acc-dat_3=abandonándola; ger_acc-dat_3=abandonándose; ger_acc-dat_3=abandonándólola; ger_acc-dat_3=abandonándólolas; ger_acc-dat_3=abandonándólolo; ger_acc-dat_3=abandonándólolos; ger_acc-dat_4=abandonándónosla; ger_acc-dat_4=abandonándónoslas; ger_acc-dat_4=abandonándónoslo; ger_acc-dat_4=abandonándónoslos; ger_acc-dat_5=abandonándóosla; ger_acc-dat_5=abandonándóoslas; ger_acc-dat_5=abandonándóoslo; ger_acc-dat_5=abandonándóoslos; ger_acc-dat_6=abandonándolas; ger_acc-dat_6=abandonándose; ger_acc-dat_6=abandonándólosla; ger_acc-dat_6=abandonándóloslas; ger_acc-dat_6=abandonándóloslo; ger_acc-dat_6=abandonándóloslos; ger_acc-dat_7=abandonándósela; ger_acc-dat_7=abandonándóselas; ger_acc-dat_7=abandonándóselo; ger_acc-dat_7=abandonándóselos; ger_acc_1=abandonándome; ger_acc_2=abandonándote; ger_acc_3=abandonándolo; ger_acc_4=abandonándonos; ger_acc_5=abandonándoos; ger_acc_6=abandonándolos; ger_acc_7=abandonándose; ger_dat_1=abandonándome; ger_dat_2=abandonándote; ger_dat_3=abandonándole; ger_dat_3=abandonándose; ger_dat_4=abandonándonos; ger_dat_5=abandonándoos; ger_dat_6=abandonándoles; ger_dat_6=abandonándose; imp_1p_acc-dat_2=abandonémóstela; imp_1p_acc-dat_2=abandonémóstelas; imp_1p_acc-dat_2=abandonémóstelo; imp_1p_acc-dat_2=abandonémóstelos; imp_1p_acc-dat_3=abandonémosla; imp_1p_acc-dat_3=abandonémóslola; imp_1p_acc-dat_3=abandonémóslolas; imp_1p_acc-dat_3=abandonémóslolo; imp_1p_acc-dat_3=abandonémóslolos; imp_1p_acc-dat_4=abandonémónosla; imp_1p_acc-dat_4=abandonémónoslas; imp_1p_acc-dat_4=abandonémónoslo; imp_1p_acc-dat_4=abandonémónoslos; imp_1p_acc-dat_5=abandonémóosla; imp_1p_acc-dat_5=abandonémóoslas; imp_1p_acc-dat_5=abandonémóoslo; imp_1p_acc-dat_5=abandonémóoslos; imp_1p_acc-dat_6=abandonémoslas; imp_1p_acc-dat_6=abandonémóslosla; imp_1p_acc-dat_6=abandonémósloslas; imp_1p_acc-dat_6=abandonémósloslo; imp_1p_acc-dat_6=abandonémósloslos; imp_1p_acc_2=abandonémoste; imp_1p_acc_3=abandonémoslo; imp_1p_acc_4=abandonémonos; imp_1p_acc_5=abandonémoos; imp_1p_acc_6=abandonémoslos; imp_1p_dat_2=abandonémoste; imp_1p_dat_3=abandonémosle; imp_1p_dat_4=abandonémonos; imp_1p_dat_5=abandonémoos; imp_1p_dat_6=abandonémosles; imp_f2p_acc-dat_1=abandónénmela; imp_f2p_acc-dat_1=abandónénmelas; imp_f2p_acc-dat_1=abandónénmelo; imp_f2p_acc-dat_1=abandónénmelos; imp_f2p_acc-dat_3=abandónenla; imp_f2p_acc-dat_3=abandónénlola; imp_f2p_acc-dat_3=abandónénlolas; imp_f2p_acc-dat_3=abandónénlolo; imp_f2p_acc-dat_3=abandónénlolos; imp_f2p_acc-dat_4=abandónénnosla; imp_f2p_acc-dat_4=abandónénnoslas; imp_f2p_acc-dat_4=abandónénnoslo; imp_f2p_acc-dat_4=abandónénnoslos; imp_f2p_acc-dat_6=abandónenlas; imp_f2p_acc-dat_6=abandónense; imp_f2p_acc-dat_6=abandónénlosla; imp_f2p_acc-dat_6=abandónénloslas; imp_f2p_acc-dat_6=abandónénloslo; imp_f2p_acc-dat_6=abandónénloslos; imp_f2p_acc-dat_7=abandónénsela; imp_f2p_acc-dat_7=abandónénselas; imp_f2p_acc-dat_7=abandónénselo; imp_f2p_acc-dat_7=abandónénselos; imp_f2p_acc_1=abandónenme; imp_f2p_acc_3=abandónenlo; imp_f2p_acc_4=abandónennos; imp_f2p_acc_6=abandónenlos; imp_f2p_acc_7=abandónense; imp_f2p_dat_1=abandónenme; imp_f2p_dat_3=abandónenle; imp_f2p_dat_4=abandónennos; imp_f2p_dat_6=abandónenles; imp_f2p_dat_6=abandónense; imp_f2s_acc-dat_1=abandónémela; imp_f2s_acc-dat_1=abandónémelas; imp_f2s_acc-dat_1=abandónémelo; imp_f2s_acc-dat_1=abandónémelos; imp_f2s_acc-dat_3=abandónela; imp_f2s_acc-dat_3=abandónese; imp_f2s_acc-dat_3=abandónélola; imp_f2s_acc-dat_3=abandónélolas; imp_f2s_acc-dat_3=abandónélolo; imp_f2s_acc-dat_3=abandónélolos; imp_f2s_acc-dat_4=abandónénosla; imp_f2s_acc-dat_4=abandónénoslas; imp_f2s_acc-dat_4=abandónénoslo; imp_f2s_acc-dat_4=abandónénoslos; imp_f2s_acc-dat_6=abandónelas; imp_f2s_acc-dat_6=abandónélosla; imp_f2s_acc-dat_6=abandónéloslas; imp_f2s_acc-dat_6=abandónéloslo; imp_f2s_acc-dat_6=abandónéloslos; imp_f2s_acc-dat_7=abandónésela; imp_f2s_acc-dat_7=abandónéselas; imp_f2s_acc-dat_7=abandónéselo; imp_f2s_acc-dat_7=abandónéselos; imp_f2s_acc_1=abandóneme; imp_f2s_acc_3=abandónelo; imp_f2s_acc_4=abandónenos; imp_f2s_acc_6=abandónelos; imp_f2s_acc_7=abandónese; imp_f2s_dat_1=abandóneme; imp_f2s_dat_3=abandónele; imp_f2s_dat_3=abandónese; imp_f2s_dat_4=abandónenos; imp_f2s_dat_6=abandóneles; imp_i2p_acc-dat_1=abandonádmela; imp_i2p_acc-dat_1=abandonádmelas; imp_i2p_acc-dat_1=abandonádmelo; imp_i2p_acc-dat_1=abandonádmelos; imp_i2p_acc-dat_3=abandonadla; imp_i2p_acc-dat_3=abandonádlola; imp_i2p_acc-dat_3=abandonádlolas; imp_i2p_acc-dat_3=abandonádlolo; imp_i2p_acc-dat_3=abandonádlolos; imp_i2p_acc-dat_4=abandonádnosla; imp_i2p_acc-dat_4=abandonádnoslas; imp_i2p_acc-dat_4=abandonádnoslo; imp_i2p_acc-dat_4=abandonádnoslos; imp_i2p_acc-dat_5=abandonáosla; imp_i2p_acc-dat_5=abandonáoslas; imp_i2p_acc-dat_5=abandonáoslo; imp_i2p_acc-dat_5=abandonáoslos; imp_i2p_acc-dat_6=abandonadlas; imp_i2p_acc-dat_6=abandonádlosla; imp_i2p_acc-dat_6=abandonádloslas; imp_i2p_acc-dat_6=abandonádloslo; imp_i2p_acc-dat_6=abandonádloslos; imp_i2p_acc-dat_7=abandonádosla; imp_i2p_acc-dat_7=abandonádoslas; imp_i2p_acc-dat_7=abandonádoslo; imp_i2p_acc-dat_7=abandonádoslos; imp_i2p_acc_1=abandonadme; imp_i2p_acc_3=abandonadlo; imp_i2p_acc_4=abandonadnos; imp_i2p_acc_5=abandonaos; imp_i2p_acc_6=abandonadlos; imp_i2p_acc_7=abandonados; imp_i2p_dat_1=abandonadme; imp_i2p_dat_3=abandonadle; imp_i2p_dat_4=abandonadnos; imp_i2p_dat_5=abandonaos; imp_i2p_dat_6=abandonadles; imp_i2s_acc-dat_1=abandónámela; imp_i2s_acc-dat_1=abandónámelas; imp_i2s_acc-dat_1=abandónámelo; imp_i2s_acc-dat_1=abandónámelos; imp_i2s_acc-dat_2=abandónátela; imp_i2s_acc-dat_2=abandónátelas; imp_i2s_acc-dat_2=abandónátelo; imp_i2s_acc-dat_2=abandónátelos; imp_i2s_acc-dat_3=abandónala; imp_i2s_acc-dat_3=abandónálola; imp_i2s_acc-dat_3=abandónálolas; imp_i2s_acc-dat_3=abandónálolo; imp_i2s_acc-dat_3=abandónálolos; imp_i2s_acc-dat_4=abandónánosla; imp_i2s_acc-dat_4=abandónánoslas; imp_i2s_acc-dat_4=abandónánoslo; imp_i2s_acc-dat_4=abandónánoslos; imp_i2s_acc-dat_6=abandónalas; imp_i2s_acc-dat_6=abandónálosla; imp_i2s_acc-dat_6=abandónáloslas; imp_i2s_acc-dat_6=abandónáloslo; imp_i2s_acc-dat_6=abandónáloslos; imp_i2s_acc_1=abandóname; imp_i2s_acc_2=abandónate; imp_i2s_acc_3=abandónalo; imp_i2s_acc_4=abandónanos; imp_i2s_acc_6=abandónalos; imp_i2s_dat_1=abandóname; imp_i2s_dat_2=abandónate; imp_i2s_dat_3=abandónale; imp_i2s_dat_4=abandónanos; imp_i2s_dat_6=abandónales; inf_acc-dat_1=abandonármela; inf_acc-dat_1=abandonármelas; inf_acc-dat_1=abandonármelo; inf_acc-dat_1=abandonármelos; inf_acc-dat_2=abandonártela; inf_acc-dat_2=abandonártelas; inf_acc-dat_2=abandonártelo; inf_acc-dat_2=abandonártelos; inf_acc-dat_3=abandonarla; inf_acc-dat_3=abandonarse; inf_acc-dat_3=abandonárlola; inf_acc-dat_3=abandonárlolas; inf_acc-dat_3=abandonárlolo; inf_acc-dat_3=abandonárlolos; inf_acc-dat_4=abandonárnosla; inf_acc-dat_4=abandonárnoslas; inf_acc-dat_4=abandonárnoslo; inf_acc-dat_4=abandonárnoslos; inf_acc-dat_5=abandonárosla; inf_acc-dat_5=abandonároslas; inf_acc-dat_5=abandonároslo; inf_acc-dat_5=abandonároslos; inf_acc-dat_6=abandonarlas; inf_acc-dat_6=abandonarse; inf_acc-dat_6=abandonárlosla; inf_acc-dat_6=abandonárloslas; inf_acc-dat_6=abandonárloslo; inf_acc-dat_6=abandonárloslos; inf_acc-dat_7=abandonársela; inf_acc-dat_7=abandonárselas; inf_acc-dat_7=abandonárselo; inf_acc-dat_7=abandonárselos; inf_acc_1=abandonarme; inf_acc_2=abandonarte; inf_acc_3=abandonarlo; inf_acc_4=abandonarnos; inf_acc_5=abandonaros; inf_acc_6=abandonarlos; inf_acc_7=abandonarse; inf_dat_1=abandonarme; inf_dat_2=abandonarte; inf_dat_3=abandonarle; inf_dat_3=abandonarse; inf_dat_4=abandonarnos; inf_dat_5=abandonaros; inf_dat_6=abandonarles; inf_dat_6=abandonarse
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
    entry = builder.parse_entry(lang_entry, "decaer")

    print("\n".join(entry))
    assert "\n".join(entry) == """\
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
    entry = builder.parse_entry(lang_entry, "f")

    print("\n".join(entry))
    assert "\n".join(entry) == """\
f {letter-forms} :: upper_case=F
f {letter} :: letter: ef\
"""


