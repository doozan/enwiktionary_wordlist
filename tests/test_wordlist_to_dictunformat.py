from enwiktionary_wordlist.wordlist import Wordlist
from enwiktionary_wordlist.wordlist_to_dictunformat import WordlistToDictunformat


def test_forms_text():
    data = """\
_____
asca
pos: n
  meta: {{es-noun|m}}
  g: m
  gloss: ascus
    q: mycology
    syn: teca
_____
asco
pos: n
  meta: {{es-noun|m}}
  g: m
  gloss: disgust
  gloss: nausea
  gloss: disgusting person
pos: n
  meta: {{es-noun|m}}
  g: m
  gloss: alternative form of "asca"
"""

    expected = """\
##:pagecount:2
##:formcount:4
_____
asca;   ascas
<b>asca</b> <i>noun, m</i> (<i>pl</i> ascas)
<ol style="padding:0; margin-left: 1em; margin-top: .2em; margin-bottom: 1em">
<li>[<i>mycology</i>] ascus<div style="font-size: 80%">Synonyms: teca</div></li>
</ol>
_____
asco;   ascos
<b>asco</b> <i>noun, m</i> (<i>pl</i> ascos)
<ol style="padding:0; margin-left: 1em; margin-top: .2em; margin-bottom: 1em">
<li>disgust</li>
<li>nausea</li>
<li>disgusting person</li>
</ol>
<b>asco</b> <i>noun, m</i> (<i>pl</i> ascos)
<ol style="padding:0; margin-left: 1em; margin-top: .2em; margin-bottom: 1em">
<li>alternative form of &quot;asca&quot;</li>
</ol>
<b>asca</b> <i>noun, m</i> (<i>pl</i> ascas)
<ol style="padding:0; margin-left: 1em; margin-top: .2em; margin-bottom: 1em">
<li>[<i>mycology</i>] ascus<div style="font-size: 80%">Synonyms: teca</div></li>
</ol>\
"""

    wordlist = Wordlist(data.splitlines())
    exporter = WordlistToDictunformat(wordlist)
    res = "\n".join(exporter.export())
    assert res == expected


def test_forms_bifurcar():

    # This is less important now that reflexive defs have been moved to the -xr lemma

    data = """\
_____
bifurcar
pos: v
  meta: {{es-verb}} {{es-conj}}
  gloss: to bifurcate, to cause to fork off
    q: transitive
  gloss: to diverge, fork off
    q: reflexive
_____
bifurcarse
pos: v
  meta: {{es-verb}} {{es-conj}}
  gloss: to split, divide, fork, branch off
"""

    expected = """\
##:pagecount:3
##:formcount:275
_____
bifurcad;   bifurcadla;   bifurcadlas;   bifurcadle;   bifurcadles;   bifurcadlo;   bifurcadlos;   bifurcadme;   bifurcadnos;   bifurcando;   bifurcá;   bifurcádmela;   bifurcádmelas;   bifurcádmele;   bifurcádmeles;   bifurcádmelo;   bifurcádmelos;   bifurcádnosla;   bifurcádnoslas;   bifurcádnosle;   bifurcádnosles;   bifurcádnoslo;   bifurcádnoslos;   bifurcádosla;   bifurcádoslas;   bifurcádosle;   bifurcádosles;   bifurcádoslo;   bifurcádoslos;   bifurquémoos;   bifurquémosla;   bifurquémoslas;   bifurquémosle;   bifurquémosles;   bifurquémoslo;   bifurquémoslos;   bifurquémosnosla;   bifurquémosnoslas;   bifurquémosnosle;   bifurquémosnosles;   bifurquémosnoslo;   bifurquémosnoslos;   bifurquémososla;   bifurquémososlas;   bifurquémososle;   bifurquémososles;   bifurquémososlo;   bifurquémososlos;   bifurquémoste;   bifurquémostela;   bifurquémostelas;   bifurquémostele;   bifurquémosteles;   bifurquémostelo;   bifurquémostelos;   bifúrcala;   bifúrcalas;   bifúrcale;   bifúrcales;   bifúrcalo;   bifúrcalos;   bifúrcame;   bifúrcamela;   bifúrcamelas;   bifúrcamele;   bifúrcameles;   bifúrcamelo;   bifúrcamelos;   bifúrcanos;   bifúrcanosla;   bifúrcanoslas;   bifúrcanosle;   bifúrcanosles;   bifúrcanoslo;   bifúrcanoslos;   bifúrcatela;   bifúrcatelas;   bifúrcatele;   bifúrcateles;   bifúrcatelo;   bifúrcatelos;   bifúrquela;   bifúrquelas;   bifúrquele;   bifúrqueles;   bifúrquelo;   bifúrquelos;   bifúrqueme;   bifúrquemela;   bifúrquemelas;   bifúrquemele;   bifúrquemeles;   bifúrquemelo;   bifúrquemelos;   bifúrquenla;   bifúrquenlas;   bifúrquenle;   bifúrquenles;   bifúrquenlo;   bifúrquenlos;   bifúrquenme;   bifúrquenmela;   bifúrquenmelas;   bifúrquenmele;   bifúrquenmeles;   bifúrquenmelo;   bifúrquenmelos;   bifúrquennos;   bifúrquennosla;   bifúrquennoslas;   bifúrquennosle;   bifúrquennosles;   bifúrquennoslo;   bifúrquennoslos;   bifúrquenos;   bifúrquenosla;   bifúrquenoslas;   bifúrquenosle;   bifúrquenosles;   bifúrquenoslo;   bifúrquenoslos;   bifúrquensela;   bifúrquenselas;   bifúrquensele;   bifúrquenseles;   bifúrquenselo;   bifúrquenselos;   bifúrquesela;   bifúrqueselas;   bifúrquesele;   bifúrqueseles;   bifúrqueselo;   bifúrqueselos
<b>bifurcar</b> <i>verb</i>
<ol style="padding:0; margin-left: 1em; margin-top: .2em; margin-bottom: 1em">
<li>[<i>transitive</i>] to bifurcate, to cause to fork off</li>
<li>[<i>reflexive</i>] to diverge, fork off</li>
</ol>
_____
bifurcar;   bifurca;   bifurcaba;   bifurcabais;   bifurcaban;   bifurcabas;   bifurcada;   bifurcadas;   bifurcado;   bifurcados;   bifurcamos;   bifurcan;   bifurcaos;   bifurcara;   bifurcarais;   bifurcaran;   bifurcaras;   bifurcare;   bifurcareis;   bifurcaremos;   bifurcaren;   bifurcares;   bifurcarla;   bifurcarlas;   bifurcarle;   bifurcarles;   bifurcarlo;   bifurcarlos;   bifurcarme;   bifurcarnos;   bifurcaron;   bifurcaros;   bifurcarse;   bifurcarte;   bifurcará;   bifurcarán;   bifurcarás;   bifurcaré;   bifurcaréis;   bifurcaría;   bifurcaríais;   bifurcaríamos;   bifurcarían;   bifurcarías;   bifurcas;   bifurcase;   bifurcaseis;   bifurcasen;   bifurcases;   bifurcaste;   bifurcasteis;   bifurco;   bifurcábamos;   bifurcáis;   bifurcándola;   bifurcándolas;   bifurcándole;   bifurcándoles;   bifurcándolo;   bifurcándolos;   bifurcándome;   bifurcándomela;   bifurcándomelas;   bifurcándomele;   bifurcándomeles;   bifurcándomelo;   bifurcándomelos;   bifurcándonos;   bifurcándonosla;   bifurcándonoslas;   bifurcándonosle;   bifurcándonosles;   bifurcándonoslo;   bifurcándonoslos;   bifurcándoos;   bifurcándoosla;   bifurcándooslas;   bifurcándoosle;   bifurcándoosles;   bifurcándooslo;   bifurcándooslos;   bifurcándose;   bifurcándosela;   bifurcándoselas;   bifurcándosele;   bifurcándoseles;   bifurcándoselo;   bifurcándoselos;   bifurcándote;   bifurcándotela;   bifurcándotelas;   bifurcándotele;   bifurcándoteles;   bifurcándotelo;   bifurcándotelos;   bifurcáramos;   bifurcáremos;   bifurcármela;   bifurcármelas;   bifurcármele;   bifurcármeles;   bifurcármelo;   bifurcármelos;   bifurcárnosla;   bifurcárnoslas;   bifurcárnosle;   bifurcárnosles;   bifurcárnoslo;   bifurcárnoslos;   bifurcárosla;   bifurcároslas;   bifurcárosle;   bifurcárosles;   bifurcároslo;   bifurcároslos;   bifurcársela;   bifurcárselas;   bifurcársele;   bifurcárseles;   bifurcárselo;   bifurcárselos;   bifurcártela;   bifurcártelas;   bifurcártele;   bifurcárteles;   bifurcártelo;   bifurcártelos;   bifurcás;   bifurcásemos;   bifurcó;   bifurque;   bifurquemos;   bifurquen;   bifurques;   bifurqué;   bifurquéis;   bifurquémonos;   bifurqués;   bifúrcate;   bifúrquense;   bifúrquese
<b>bifurcar</b> <i>verb</i>
<ol style="padding:0; margin-left: 1em; margin-top: .2em; margin-bottom: 1em">
<li>[<i>transitive</i>] to bifurcate, to cause to fork off</li>
<li>[<i>reflexive</i>] to diverge, fork off</li>
</ol>
<b>bifurcarse</b> <i>verb</i>
<ol style="padding:0; margin-left: 1em; margin-top: .2em; margin-bottom: 1em">
<li>to split, divide, fork, branch off</li>
</ol>
_____
bifurcate
<b>bifurcarse</b> <i>verb</i>
<ol style="padding:0; margin-left: 1em; margin-top: .2em; margin-bottom: 1em">
<li>to split, divide, fork, branch off</li>
</ol>"""

    wordlist = Wordlist(data.splitlines())
    exporter = WordlistToDictunformat(wordlist)
    res = "\n".join(exporter.export())
    print(res)
    assert res == expected


def test_lentes():

    data = """\
_____
lente
pos: n
  meta: {{es-noun|m}}
  g: m
  etymology: Borrowed from Latin "lēns, lentem" (“lentil”), in Medieval Latin later taking on the sense of "lens". Cognate with English "lens".
  gloss: lens
  gloss: glasses (in the plural, by extension)
    syn: anteojos
_____
lentes
pos: n
  meta: {{es-noun|m-p}}
  g: m-p
  gloss: eyeglasses
    syn: anteojos; gafas
  gloss: inflection of "lente"
"""

    expected = """\
##:pagecount:2
##:formcount:2
_____
lente
<b>lente</b> <i>noun, m</i> (<i>pl</i> lentes)
<ol style="padding:0; margin-left: 1em; margin-top: .2em; margin-bottom: 1em">
<li>lens</li>
<li>glasses (in the plural, by extension)<div style="font-size: 80%">Synonyms: anteojos</div></li>
</ol>
<p style="margin-top: 1em"><i>Etymology:</i> Borrowed from Latin &quot;lēns, lentem&quot; (“lentil”), in Medieval Latin later taking on the sense of &quot;lens&quot;. Cognate with English &quot;lens&quot;.</p>
_____
lentes
<b>lentes</b> <i>noun, m pl</i>
<ol style="padding:0; margin-left: 1em; margin-top: .2em; margin-bottom: 1em">
<li>eyeglasses<div style="font-size: 80%">Synonyms: anteojos; gafas</div></li>
<li>inflection of &quot;lente&quot;</li>
</ol>
<b>lente</b> <i>noun, m</i> (<i>pl</i> lentes)
<ol style="padding:0; margin-left: 1em; margin-top: .2em; margin-bottom: 1em">
<li>lens</li>
<li>glasses (in the plural, by extension)<div style="font-size: 80%">Synonyms: anteojos</div></li>
</ol>
<p style="margin-top: 1em"><i>Etymology:</i> Borrowed from Latin &quot;lēns, lentem&quot; (“lentil”), in Medieval Latin later taking on the sense of &quot;lens&quot;. Cognate with English &quot;lens&quot;.</p>\
"""

    wordlist = Wordlist(data.splitlines())
    exporter = WordlistToDictunformat(wordlist)
    res = "\n".join(exporter.export())
    assert res == expected
