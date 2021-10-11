import enwiktionary_wordlist.wordlist_to_dictunformat as exporter

def test_forms_text():
    exporter.all_pages = {}

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
asca|ascas
<b>asca</b> <i>noun, m</i> (<i>pl</i> ascas)
<ol style="padding:0; margin-left: 1em; margin-top: .2em; margin-bottom: 1em">
<li>[<i>mycology</i>] ascus<div style="font-size: 80%">Synonyms: teca</div></li>
</ol>
_____
asco|ascos
<b>asca</b> <i>noun, m</i> (<i>pl</i> ascas)
<ol style="padding:0; margin-left: 1em; margin-top: .2em; margin-bottom: 1em">
<li>[<i>mycology</i>] ascus<div style="font-size: 80%">Synonyms: teca</div></li>
</ol>
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
    print("\n".join(exporter.export(data.splitlines(), None, "es", "test")))
    assert "\n".join(exporter.export(data.splitlines(), None, "es", "test")) == expected.strip()


def test_forms_bifurcar():
    exporter.all_pages = {}

    wordlist_data = """\
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
##:formcount:340
_____
bifurcar|bifurca|bifurcaba|bifurcabais|bifurcaban|bifurcabas|bifurcad|bifurcadla|bifurcadlas|bifurcadle|bifurcadles|bifurcadlo|bifurcadlos|bifurcadme|bifurcadmela|bifurcadmelas|bifurcadmele|bifurcadmeles|bifurcadmelo|bifurcadmelos|bifurcadnos|bifurcadnosla|bifurcadnoslas|bifurcadnosle|bifurcadnosles|bifurcadnoslo|bifurcadnoslos|bifurcadosla|bifurcadoslas|bifurcadosle|bifurcadosles|bifurcadoslo|bifurcadoslos|bifurcamos|bifurcan|bifurcando|bifurcara|bifurcarais|bifurcaran|bifurcaras|bifurcare|bifurcareis|bifurcaremos|bifurcaren|bifurcares|bifurcaron|bifurcará|bifurcarán|bifurcarás|bifurcaré|bifurcaréis|bifurcaría|bifurcaríais|bifurcaríamos|bifurcarían|bifurcarías|bifurcas|bifurcase|bifurcaseis|bifurcasen|bifurcases|bifurcaste|bifurcasteis|bifurco|bifurcá|bifurcábamos|bifurcáis|bifurcáramos|bifurcáremos|bifurcás|bifurcásemos|bifurcó|bifurque|bifurquemos|bifurquen|bifurques|bifurqué|bifurquéis|bifurquémoos|bifurquémosla|bifurquémoslas|bifurquémosle|bifurquémosles|bifurquémoslo|bifurquémoslos|bifurquémosnosla|bifurquémosnoslas|bifurquémosnosle|bifurquémosnosles|bifurquémosnoslo|bifurquémosnoslos|bifurquémososla|bifurquémososlas|bifurquémososle|bifurquémososles|bifurquémososlo|bifurquémososlos|bifurquémoste|bifurquémostela|bifurquémostelas|bifurquémostele|bifurquémosteles|bifurquémostelo|bifurquémostelos|bifurqués|bifúrcala|bifúrcalas|bifúrcale|bifúrcales|bifúrcalo|bifúrcalos|bifúrcame|bifúrcamela|bifúrcamelas|bifúrcamele|bifúrcameles|bifúrcamelo|bifúrcamelos|bifúrcanos|bifúrcanosla|bifúrcanoslas|bifúrcanosle|bifúrcanosles|bifúrcanoslo|bifúrcanoslos|bifúrcatela|bifúrcatelas|bifúrcatele|bifúrcateles|bifúrcatelo|bifúrcatelos|bifúrquela|bifúrquelas|bifúrquele|bifúrqueles|bifúrquelo|bifúrquelos|bifúrqueme|bifúrquemela|bifúrquemelas|bifúrquemele|bifúrquemeles|bifúrquemelo|bifúrquemelos|bifúrquenla|bifúrquenlas|bifúrquenle|bifúrquenles|bifúrquenlo|bifúrquenlos|bifúrquenme|bifúrquenmela|bifúrquenmelas|bifúrquenmele|bifúrquenmeles|bifúrquenmelo|bifúrquenmelos|bifúrquennos|bifúrquennosla|bifúrquennoslas|bifúrquennosle|bifúrquennosles|bifúrquennoslo|bifúrquennoslos|bifúrquenos|bifúrquenosla|bifúrquenoslas|bifúrquenosle|bifúrquenosles|bifúrquenoslo|bifúrquenoslos|bifúrquensela|bifúrquenselas|bifúrquensele|bifúrquenseles|bifúrquenselo|bifúrquenselos|bifúrquesela|bifúrqueselas|bifúrquesele|bifúrqueseles|bifúrqueselo|bifúrqueselos|no bifurque|no bifurquemos|no bifurquen|no bifurques|no bifurquéis
<b>bifurcar</b> <i>verb</i>
<ol style="padding:0; margin-left: 1em; margin-top: .2em; margin-bottom: 1em">
<li>[<i>transitive</i>] to bifurcate, to cause to fork off</li>
<li>[<i>reflexive</i>] to diverge, fork off</li>
</ol>
_____
bifurcarse|bifurcada|bifurcadas|bifurcado|bifurcados|bifurcaos|bifurcarla|bifurcarlas|bifurcarle|bifurcarles|bifurcarlo|bifurcarlos|bifurcarme|bifurcarmela|bifurcarmelas|bifurcarmele|bifurcarmeles|bifurcarmelo|bifurcarmelos|bifurcarnos|bifurcarnosla|bifurcarnoslas|bifurcarnosle|bifurcarnosles|bifurcarnoslo|bifurcarnoslos|bifurcaros|bifurcarosla|bifurcaroslas|bifurcarosle|bifurcarosles|bifurcaroslo|bifurcaroslos|bifurcarsela|bifurcarselas|bifurcarsele|bifurcarseles|bifurcarselo|bifurcarselos|bifurcarte|bifurcartela|bifurcartelas|bifurcartele|bifurcarteles|bifurcartelo|bifurcartelos|bifurcándola|bifurcándolas|bifurcándole|bifurcándoles|bifurcándolo|bifurcándolos|bifurcándome|bifurcándomela|bifurcándomelas|bifurcándomele|bifurcándomeles|bifurcándomelo|bifurcándomelos|bifurcándonos|bifurcándonosla|bifurcándonoslas|bifurcándonosle|bifurcándonosles|bifurcándonoslo|bifurcándonoslos|bifurcándoos|bifurcándoosla|bifurcándooslas|bifurcándoosle|bifurcándoosles|bifurcándooslo|bifurcándooslos|bifurcándose|bifurcándosela|bifurcándoselas|bifurcándosele|bifurcándoseles|bifurcándoselo|bifurcándoselos|bifurcándote|bifurcándotela|bifurcándotelas|bifurcándotele|bifurcándoteles|bifurcándotelo|bifurcándotelos|bifurquémonos|bifúrcate|bifúrquense|bifúrquese
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
bifurcate|me bifurcaba|me bifurcara|me bifurcare|me bifurcaré|me bifurcaría|me bifurcase|me bifurco|me bifurque|me bifurqué|no nos bifurquemos|no os bifurquéis|no se bifurque|no se bifurquen|no te bifurques|nos bifurcamos|nos bifurcaremos|nos bifurcaríamos|nos bifurcábamos|nos bifurcáramos|nos bifurcáremos|nos bifurcásemos|nos bifurquemos|os bifurcabais|os bifurcarais|os bifurcareis|os bifurcaréis|os bifurcaríais|os bifurcaseis|os bifurcasteis|os bifurcáis|os bifurquéis|se bifurca|se bifurcaba|se bifurcaban|se bifurcan|se bifurcara|se bifurcaran|se bifurcare|se bifurcaren|se bifurcaron|se bifurcará|se bifurcarán|se bifurcaría|se bifurcarían|se bifurcase|se bifurcasen|se bifurcó|se bifurque|se bifurquen|te bifurcabas|te bifurcaras|te bifurcares|te bifurcarás|te bifurcarías|te bifurcas|te bifurcases|te bifurcaste|te bifurcás|te bifurques|te bifurqués
<b>bifurcarse</b> <i>verb</i>
<ol style="padding:0; margin-left: 1em; margin-top: .2em; margin-bottom: 1em">
<li>to split, divide, fork, branch off</li>
</ol>\
"""

    v1 = "\n".join(exporter.export(wordlist_data.splitlines(), None, "es", "test"))
    v2 = "\n".join(exporter.export(wordlist_data.splitlines(), None, "es", "test"))
    v3 = "\n".join(exporter.export(wordlist_data.splitlines(), None, "es", "test"))
    assert v1 == v2 == v3

    print("\n".join(exporter.export(wordlist_data.splitlines(), None, "es", "test")))
    assert "\n".join(exporter.export(wordlist_data.splitlines(), None, "es", "test")) == expected.strip()


def test_lentes():
    exporter.all_pages = {}

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
    print("\n".join(exporter.export(data.splitlines(), None, "es", "test")))
    assert "\n".join(exporter.export(data.splitlines(), None, "es", "test")) == expected.strip()
