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
_____
00-database-info
##:name:Wiktionary (es-en)
##:url:en.wiktionary.org
##:pagecount:2
##:formcount:4
##:description:test
_____
asca|ascas
asca (n, m), plural "ascas"
1. (mycology) ascus
      Synonyms: teca
_____
asco|ascos
asca (n, m), plural "ascas"
1. (mycology) ascus
      Synonyms: teca

asco (n, m), plural "ascos"
1. disgust
2. nausea
3. disgusting person

asco (n, m), plural "ascos"
1. alternative form of "asca"
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
_____
00-database-info
##:name:Wiktionary (es-en)
##:url:en.wiktionary.org
##:pagecount:3
##:formcount:340
##:description:test
_____
bifurcar|bifurca|bifurcaba|bifurcabais|bifurcaban|bifurcabas|bifurcad|bifurcadla|bifurcadlas|bifurcadle|bifurcadles|bifurcadlo|bifurcadlos|bifurcadme|bifurcadmela|bifurcadmelas|bifurcadmele|bifurcadmeles|bifurcadmelo|bifurcadmelos|bifurcadnos|bifurcadnosla|bifurcadnoslas|bifurcadnosle|bifurcadnosles|bifurcadnoslo|bifurcadnoslos|bifurcadosla|bifurcadoslas|bifurcadosle|bifurcadosles|bifurcadoslo|bifurcadoslos|bifurcamos|bifurcan|bifurcando|bifurcara|bifurcarais|bifurcaran|bifurcaras|bifurcare|bifurcareis|bifurcaremos|bifurcaren|bifurcares|bifurcaron|bifurcará|bifurcarán|bifurcarás|bifurcaré|bifurcaréis|bifurcaría|bifurcaríais|bifurcaríamos|bifurcarían|bifurcarías|bifurcas|bifurcase|bifurcaseis|bifurcasen|bifurcases|bifurcaste|bifurcasteis|bifurco|bifurcá|bifurcábamos|bifurcáis|bifurcáramos|bifurcáremos|bifurcás|bifurcásemos|bifurcó|bifurque|bifurquemos|bifurquen|bifurques|bifurqué|bifurquéis|bifurquémoos|bifurquémosla|bifurquémoslas|bifurquémosle|bifurquémosles|bifurquémoslo|bifurquémoslos|bifurquémosnosla|bifurquémosnoslas|bifurquémosnosle|bifurquémosnosles|bifurquémosnoslo|bifurquémosnoslos|bifurquémososla|bifurquémososlas|bifurquémososle|bifurquémososles|bifurquémososlo|bifurquémososlos|bifurquémoste|bifurquémostela|bifurquémostelas|bifurquémostele|bifurquémosteles|bifurquémostelo|bifurquémostelos|bifurqués|bifúrcala|bifúrcalas|bifúrcale|bifúrcales|bifúrcalo|bifúrcalos|bifúrcame|bifúrcamela|bifúrcamelas|bifúrcamele|bifúrcameles|bifúrcamelo|bifúrcamelos|bifúrcanos|bifúrcanosla|bifúrcanoslas|bifúrcanosle|bifúrcanosles|bifúrcanoslo|bifúrcanoslos|bifúrcatela|bifúrcatelas|bifúrcatele|bifúrcateles|bifúrcatelo|bifúrcatelos|bifúrquela|bifúrquelas|bifúrquele|bifúrqueles|bifúrquelo|bifúrquelos|bifúrqueme|bifúrquemela|bifúrquemelas|bifúrquemele|bifúrquemeles|bifúrquemelo|bifúrquemelos|bifúrquenla|bifúrquenlas|bifúrquenle|bifúrquenles|bifúrquenlo|bifúrquenlos|bifúrquenme|bifúrquenmela|bifúrquenmelas|bifúrquenmele|bifúrquenmeles|bifúrquenmelo|bifúrquenmelos|bifúrquennos|bifúrquennosla|bifúrquennoslas|bifúrquennosle|bifúrquennosles|bifúrquennoslo|bifúrquennoslos|bifúrquenos|bifúrquenosla|bifúrquenoslas|bifúrquenosle|bifúrquenosles|bifúrquenoslo|bifúrquenoslos|bifúrquensela|bifúrquenselas|bifúrquensele|bifúrquenseles|bifúrquenselo|bifúrquenselos|bifúrquesela|bifúrqueselas|bifúrquesele|bifúrqueseles|bifúrqueselo|bifúrqueselos|no bifurque|no bifurquemos|no bifurquen|no bifurques|no bifurquéis
bifurcar (v)
1. (transitive) to bifurcate, to cause to fork off
2. (reflexive) to diverge, fork off
_____
bifurcarse|bifurcada|bifurcadas|bifurcado|bifurcados|bifurcaos|bifurcarla|bifurcarlas|bifurcarle|bifurcarles|bifurcarlo|bifurcarlos|bifurcarme|bifurcarmela|bifurcarmelas|bifurcarmele|bifurcarmeles|bifurcarmelo|bifurcarmelos|bifurcarnos|bifurcarnosla|bifurcarnoslas|bifurcarnosle|bifurcarnosles|bifurcarnoslo|bifurcarnoslos|bifurcaros|bifurcarosla|bifurcaroslas|bifurcarosle|bifurcarosles|bifurcaroslo|bifurcaroslos|bifurcarsela|bifurcarselas|bifurcarsele|bifurcarseles|bifurcarselo|bifurcarselos|bifurcarte|bifurcartela|bifurcartelas|bifurcartele|bifurcarteles|bifurcartelo|bifurcartelos|bifurcándola|bifurcándolas|bifurcándole|bifurcándoles|bifurcándolo|bifurcándolos|bifurcándome|bifurcándomela|bifurcándomelas|bifurcándomele|bifurcándomeles|bifurcándomelo|bifurcándomelos|bifurcándonos|bifurcándonosla|bifurcándonoslas|bifurcándonosle|bifurcándonosles|bifurcándonoslo|bifurcándonoslos|bifurcándoos|bifurcándoosla|bifurcándooslas|bifurcándoosle|bifurcándoosles|bifurcándooslo|bifurcándooslos|bifurcándose|bifurcándosela|bifurcándoselas|bifurcándosele|bifurcándoseles|bifurcándoselo|bifurcándoselos|bifurcándote|bifurcándotela|bifurcándotelas|bifurcándotele|bifurcándoteles|bifurcándotelo|bifurcándotelos|bifurquémonos|bifúrcate|bifúrquense|bifúrquese
bifurcar (v)
1. (transitive) to bifurcate, to cause to fork off
2. (reflexive) to diverge, fork off

bifurcarse (v)
1. to split, divide, fork, branch off
_____
bifurcate|me bifurcaba|me bifurcara|me bifurcare|me bifurcaré|me bifurcaría|me bifurcase|me bifurco|me bifurque|me bifurqué|no nos bifurquemos|no os bifurquéis|no se bifurque|no se bifurquen|no te bifurques|nos bifurcamos|nos bifurcaremos|nos bifurcaríamos|nos bifurcábamos|nos bifurcáramos|nos bifurcáremos|nos bifurcásemos|nos bifurquemos|os bifurcabais|os bifurcarais|os bifurcareis|os bifurcaréis|os bifurcaríais|os bifurcaseis|os bifurcasteis|os bifurcáis|os bifurquéis|se bifurca|se bifurcaba|se bifurcaban|se bifurcan|se bifurcara|se bifurcaran|se bifurcare|se bifurcaren|se bifurcaron|se bifurcará|se bifurcarán|se bifurcaría|se bifurcarían|se bifurcase|se bifurcasen|se bifurcó|se bifurque|se bifurquen|te bifurcabas|te bifurcaras|te bifurcares|te bifurcarás|te bifurcarías|te bifurcas|te bifurcases|te bifurcaste|te bifurcás|te bifurques|te bifurqués
bifurcarse (v)
1. to split, divide, fork, branch off
"""
    v1 = "\n".join(exporter.export(wordlist_data.splitlines(), None, "es", "test"))
    v2 = "\n".join(exporter.export(wordlist_data.splitlines(), None, "es", "test"))
    v3 = "\n".join(exporter.export(wordlist_data.splitlines(), None, "es", "test"))
    assert v1 == v2 == v3

    print("\n".join(exporter.export(wordlist_data.splitlines(), None, "es", "test")))
    assert "\n".join(exporter.export(wordlist_data.splitlines(), None, "es", "test")) == expected.strip()

