from enwiktionary_wordlist.wordlist import Wordlist
from enwiktionary_wordlist.all_forms import AllForms

def test_forms_complex():
    # protectora should be a form of protector even though it has a secondary
    # declaration as a lemma

    wordlist_data = """\
_____
protector
pos: n
  meta: {{es-noun|m|protectores|f=protectora|f2=protectriz}}
  forms: f=protectora; f=protectriz; fpl=protectoras; fpl=protectrices; pl=protectores
  g: m
  gloss: protector (someone who protects or guards)
pos: n
  meta: {{es-noun|m}}
  forms: pl=protectores
  g: m
  gloss: protector (a device or mechanism which is designed to protect)
_____
protectora
pos: n
  meta: {{es-noun|f|m=protector}}
  forms: m=protector; mpl=protectores; pl=protectoras
  g: f
  gloss: female equivalent of "protector"
pos: n
  meta: {{es-noun|f}}
  forms: pl=protectoras
  g: f
  gloss: animal shelter (an organization that provides temporary homes for stray pet animals)
    syn: protectora de animales
_____
protectoras
pos: n
  meta: {{head|es|noun plural form|g=f-p}}
  g: f-p
  gloss: inflection of "protector"
_____
protectores
pos: n
  meta: {{head|es|noun plural form|g=m-p}}
  g: m-p
  gloss: inflection of "protector"
_____
protectrices
pos: n
  meta: {{head|es|noun plural form|g=f-p}}
  g: f-p
  gloss: inflection of "protector"
_____
protectriz
pos: n
  meta: {{es-noun|f|m=protector}}
  forms: m=protector; mpl=protectores; pl=protectrices
  g: f
  gloss: alternative form of "protectora"
    q: uncommon
"""
    expected = {
'protector': ['n|protector'],
'protectora': ['n|protector', 'n|protectora'],
'protectoras': ['n|protector', 'n|protectora'],
'protectores': ['n|protector'],
'protectrices': ['n|protector'],
'protectriz': ['n|protector'],
}

    wordlist = Wordlist(wordlist_data.splitlines())
    assert dict(AllForms.from_wordlist(wordlist).all_forms) == expected


def test_secondary_lemma_unique_forms():
    # test2 should be alt of test, but
    # test2s should only be a form of test2s (since it cannot be an alt of test)

    wordlist_data = """\
_____
test
pos: n
  meta: {{es-noun|m|-}}
  gloss: test
_____
test2
pos: n
  meta: {{es-noun|m|-}}
  gloss: alternative form of "test"
pos: n
  meta: {{es-noun|m|test2s}}
  g: m
  gloss: test2
"""

    expected = {
'test': ['n|test'],
'test2': ['n|test', 'n|test2'],
'test2s': ['n|test2']
}

    wordlist = Wordlist(wordlist_data.splitlines())
    assert AllForms.from_wordlist(wordlist).all_forms == expected


def test_secondary_lemma_no_unique_forms():

    wordlist_data = """\
_____
test
pos: n
  meta: {{es-noun|m|-}}
  gloss: test
_____
test2
pos: n
  meta: {{es-noun|m|test2s}}
  gloss: alternative form of "test"
pos: n
  meta: {{es-noun|m|test2s}}
  g: m
  gloss: test2
"""

    expected = {
'test': ['n|test'],
'test2': ['n|test', 'n|test2'],
'test2s': ['n|test', 'n|test2']
}

    wordlist = Wordlist(wordlist_data.splitlines())
    assert AllForms.from_wordlist(wordlist).all_forms == expected


def test_forms_text():

    wordlist_data = """\
testo {n-meta} :: {{es-noun|m}}
testo {m} :: test
testo {n-meta} :: {{es-noun|m|testoz}}
testo {m} :: test2
testa {n-meta} :: {{es-noun|f}}
testa {f} :: feminine noun of "testo"
"""
    expected = {
'testa': ['n|testo'],
'testas': ['n|testo'],
'testo': ['n|testo'],
'testos': ['n|testo'],
'testoz': ['n|testo'],
}

    wordlist = Wordlist(wordlist_data.splitlines())
    assert AllForms.from_wordlist(wordlist).all_forms == expected

def test_forms_redirection():

    wordlist_data = """\
test1 {n-meta} :: {{es-noun|m|-}}
test1 {m} :: test
test2 {n-meta} :: {{es-noun|m|-}}
test2 {m} :: alternate form of "test1"
test3 {n-meta} :: {{es-noun|m|-}}
test3 {m} :: alternate form of "test2"
test4 {n-meta} :: {{es-noun|m|-}}
test4 {m} :: alternate form of "test3"
"""

    expected = {
'test1': ['n|test1'],
'test2': ['n|test1'],
'test3': ['n|test1'],
'test4': ['n|test1']
}

    wordlist = Wordlist(wordlist_data.splitlines())
    assert AllForms.from_wordlist(wordlist).all_forms == expected


def test_asco_forms():

    wordlist_data = """\
_____
asca
pos: n
  meta: {{es-noun|m}}
  forms: pl=ascas
  g: m
  gloss: ascus
    q: mycology
    syn: teca
_____
asco
pos: n
  meta: {{es-noun|m}}
  forms: pl=ascos
  g: m
  gloss: disgust
  gloss: nausea
  gloss: disgusting person
pos: n
  meta: {{es-noun|m}}
  forms: pl=ascos
  g: m
  gloss: alternative form of "asca"
"""

    expected = {
'asca': ['n|asca'],
'ascas': ['n|asca'],
'asco': ['n|asco', 'n|asca'],
'ascos': ['n|asco', 'n|asca']
}

    wordlist = Wordlist(wordlist_data.splitlines())
    assert AllForms.from_wordlist(wordlist).all_forms == expected


def test_verb_forms():
    wordlist_data = """\
_____
bifurcar
pos: verb
  meta: {{es-verb}} {{es-conj}}
  gloss: to bifurcate, to cause to fork off
    q: transitive
  gloss: To diverge, fork off
    q: reflexive
_____
bifurcarse
pos: verb
  meta: {{es-verb}} {{es-conj}}
  gloss: to split, divide, fork, branch off
"""

    expected = {
'bifurcaríamos': ['verb|bifurcar'],
'bifurcaría': ['verb|bifurcar'],
'bifurcaríais': ['verb|bifurcar'],
'bifurcarías': ['verb|bifurcar'],
'bifurcarían': ['verb|bifurcar'],
'bifurcaremos': ['verb|bifurcar'],
'bifurcaré': ['verb|bifurcar'],
'bifurcaréis': ['verb|bifurcar'],
'bifurcarás': ['verb|bifurcar'],
'bifurcarán': ['verb|bifurcar'],
'bifurcará': ['verb|bifurcar'],
'bifurcáremos': ['verb|bifurcar'],
'bifurcare': ['verb|bifurcar'],
'bifurcareis': ['verb|bifurcar'],
'bifurcares': ['verb|bifurcar'],
'bifurcaren': ['verb|bifurcar'],
'bifurcando': ['verb|bifurcar'],
'bifurcándola': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándolas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándole': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándoles': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándolo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándolos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándome': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándomela': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándomelas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándomele': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándomeles': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándomelo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándomelos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándonos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándonosla': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándonoslas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándonosle': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándonosles': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándonoslo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándonoslos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándoos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándoosla': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándooslas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándoosle': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándoosles': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándooslo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándooslos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándose': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándosela': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándoselas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándosele': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándoseles': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándoselo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándoselos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándote': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándotela': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándotelas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándotele': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándoteles': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándotelo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándotelos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquemos': ['verb|bifurcar'],
'bifurquémosla': ['verb|bifurcar'],
'bifurquémoslas': ['verb|bifurcar'],
'bifurquémosle': ['verb|bifurcar'],
'bifurquémosles': ['verb|bifurcar'],
'bifurquémoslo': ['verb|bifurcar'],
'bifurquémoslos': ['verb|bifurcar'],
'bifurquémonos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémosnosla': ['verb|bifurcar'],
'bifurquémosnoslas': ['verb|bifurcar'],
'bifurquémosnosle': ['verb|bifurcar'],
'bifurquémosnosles': ['verb|bifurcar'],
'bifurquémosnoslo': ['verb|bifurcar'],
'bifurquémosnoslos': ['verb|bifurcar'],
'bifurquémoos': ['verb|bifurcar'],
'bifurquémososla': ['verb|bifurcar'],
'bifurquémososlas': ['verb|bifurcar'],
'bifurquémososle': ['verb|bifurcar'],
'bifurquémososles': ['verb|bifurcar'],
'bifurquémososlo': ['verb|bifurcar'],
'bifurquémososlos': ['verb|bifurcar'],
'bifurquémoste': ['verb|bifurcar'],
'bifurquémostela': ['verb|bifurcar'],
'bifurquémostelas': ['verb|bifurcar'],
'bifurquémostele': ['verb|bifurcar'],
'bifurquémosteles': ['verb|bifurcar'],
'bifurquémostelo': ['verb|bifurcar'],
'bifurquémostelos': ['verb|bifurcar'],
'bifurcad': ['verb|bifurcar'],
'bifurcadla': ['verb|bifurcar'],
'bifurcadlas': ['verb|bifurcar'],
'bifurcadle': ['verb|bifurcar'],
'bifurcadles': ['verb|bifurcar'],
'bifurcadlo': ['verb|bifurcar'],
'bifurcadlos': ['verb|bifurcar'],
'bifurcadme': ['verb|bifurcar'],
'bifurcadmela': ['verb|bifurcar'],
'bifurcadmelas': ['verb|bifurcar'],
'bifurcadmele': ['verb|bifurcar'],
'bifurcadmeles': ['verb|bifurcar'],
'bifurcadmelo': ['verb|bifurcar'],
'bifurcadmelos': ['verb|bifurcar'],
'bifurcadnos': ['verb|bifurcar'],
'bifurcadnosla': ['verb|bifurcar'],
'bifurcadnoslas': ['verb|bifurcar'],
'bifurcadnosle': ['verb|bifurcar'],
'bifurcadnosles': ['verb|bifurcar'],
'bifurcadnoslo': ['verb|bifurcar'],
'bifurcadnoslos': ['verb|bifurcar'],
'bifurcaos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcadosla': ['verb|bifurcar'],
'bifurcadoslas': ['verb|bifurcar'],
'bifurcadosle': ['verb|bifurcar'],
'bifurcadosles': ['verb|bifurcar'],
'bifurcadoslo': ['verb|bifurcar'],
'bifurcadoslos': ['verb|bifurcar'],
'bifurca': ['verb|bifurcar'],
'bifúrcala': ['verb|bifurcar'],
'bifúrcalas': ['verb|bifurcar'],
'bifúrcale': ['verb|bifurcar'],
'bifúrcales': ['verb|bifurcar'],
'bifúrcalo': ['verb|bifurcar'],
'bifúrcalos': ['verb|bifurcar'],
'bifúrcame': ['verb|bifurcar'],
'bifúrcamela': ['verb|bifurcar'],
'bifúrcamelas': ['verb|bifurcar'],
'bifúrcamele': ['verb|bifurcar'],
'bifúrcameles': ['verb|bifurcar'],
'bifúrcamelo': ['verb|bifurcar'],
'bifúrcamelos': ['verb|bifurcar'],
'bifúrcanos': ['verb|bifurcar'],
'bifúrcanosla': ['verb|bifurcar'],
'bifúrcanoslas': ['verb|bifurcar'],
'bifúrcanosle': ['verb|bifurcar'],
'bifúrcanosles': ['verb|bifurcar'],
'bifúrcanoslo': ['verb|bifurcar'],
'bifúrcanoslos': ['verb|bifurcar'],
'bifúrcate': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrcatela': ['verb|bifurcar'],
'bifúrcatelas': ['verb|bifurcar'],
'bifúrcatele': ['verb|bifurcar'],
'bifúrcateles': ['verb|bifurcar'],
'bifúrcatelo': ['verb|bifurcar'],
'bifúrcatelos': ['verb|bifurcar'],
'bifurcá': ['verb|bifurcar'],
'bifurquen': ['verb|bifurcar'],
'bifúrquenla': ['verb|bifurcar'],
'bifúrquenlas': ['verb|bifurcar'],
'bifúrquenle': ['verb|bifurcar'],
'bifúrquenles': ['verb|bifurcar'],
'bifúrquenlo': ['verb|bifurcar'],
'bifúrquenlos': ['verb|bifurcar'],
'bifúrquenme': ['verb|bifurcar'],
'bifúrquenmela': ['verb|bifurcar'],
'bifúrquenmelas': ['verb|bifurcar'],
'bifúrquenmele': ['verb|bifurcar'],
'bifúrquenmeles': ['verb|bifurcar'],
'bifúrquenmelo': ['verb|bifurcar'],
'bifúrquenmelos': ['verb|bifurcar'],
'bifúrquennos': ['verb|bifurcar'],
'bifúrquennosla': ['verb|bifurcar'],
'bifúrquennoslas': ['verb|bifurcar'],
'bifúrquennosle': ['verb|bifurcar'],
'bifúrquennosles': ['verb|bifurcar'],
'bifúrquennoslo': ['verb|bifurcar'],
'bifúrquennoslos': ['verb|bifurcar'],
'bifúrquense': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquensela': ['verb|bifurcar'],
'bifúrquenselas': ['verb|bifurcar'],
'bifúrquensele': ['verb|bifurcar'],
'bifúrquenseles': ['verb|bifurcar'],
'bifúrquenselo': ['verb|bifurcar'],
'bifúrquenselos': ['verb|bifurcar'],
'bifurque': ['verb|bifurcar'],
'bifúrquela': ['verb|bifurcar'],
'bifúrquelas': ['verb|bifurcar'],
'bifúrquele': ['verb|bifurcar'],
'bifúrqueles': ['verb|bifurcar'],
'bifúrquelo': ['verb|bifurcar'],
'bifúrquelos': ['verb|bifurcar'],
'bifúrqueme': ['verb|bifurcar'],
'bifúrquemela': ['verb|bifurcar'],
'bifúrquemelas': ['verb|bifurcar'],
'bifúrquemele': ['verb|bifurcar'],
'bifúrquemeles': ['verb|bifurcar'],
'bifúrquemelo': ['verb|bifurcar'],
'bifúrquemelos': ['verb|bifurcar'],
'bifúrquenos': ['verb|bifurcar'],
'bifúrquenosla': ['verb|bifurcar'],
'bifúrquenoslas': ['verb|bifurcar'],
'bifúrquenosle': ['verb|bifurcar'],
'bifúrquenosles': ['verb|bifurcar'],
'bifúrquenoslo': ['verb|bifurcar'],
'bifúrquenoslos': ['verb|bifurcar'],
'bifúrquese': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquesela': ['verb|bifurcar'],
'bifúrqueselas': ['verb|bifurcar'],
'bifúrquesele': ['verb|bifurcar'],
'bifúrqueseles': ['verb|bifurcar'],
'bifúrqueselo': ['verb|bifurcar'],
'bifúrqueselos': ['verb|bifurcar'],
'bifurcábamos': ['verb|bifurcar'],
'bifurcaba': ['verb|bifurcar'],
'bifurcabais': ['verb|bifurcar'],
'bifurcabas': ['verb|bifurcar'],
'bifurcaban': ['verb|bifurcar'],
'bifurcáramos': ['verb|bifurcar'],
'bifurcara': ['verb|bifurcar'],
'bifurcarais': ['verb|bifurcar'],
'bifurcaras': ['verb|bifurcar'],
'bifurcaran': ['verb|bifurcar'],
'bifurcásemos': ['verb|bifurcar'],
'bifurcase': ['verb|bifurcar'],
'bifurcaseis': ['verb|bifurcar'],
'bifurcases': ['verb|bifurcar'],
'bifurcasen': ['verb|bifurcar'],
'bifurcar': ['verb|bifurcar'],
'bifurcarla': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarlas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarle': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarles': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarlo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarlos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarme': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarmela': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarmelas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarmele': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarmeles': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarmelo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarmelos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarnos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarnosla': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarnoslas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarnosle': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarnosles': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarnoslo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarnoslos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcaros': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarosla': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcaroslas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarosle': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarosles': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcaroslo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcaroslos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarse': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarsela': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarselas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarsele': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarseles': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarselo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarselos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarte': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcartela': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcartelas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcartele': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarteles': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcartelo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcartelos': ['verb|bifurcar', 'verb|bifurcarse'],
'no bifurquemos': ['verb|bifurcar'],
'no bifurquéis': ['verb|bifurcar'],
'no bifurques': ['verb|bifurcar'],
'no bifurquen': ['verb|bifurcar'],
'no bifurque': ['verb|bifurcar'],
'bifurcadas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcada': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcados': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcado': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcamos': ['verb|bifurcar'],
'bifurco': ['verb|bifurcar'],
'bifurcáis': ['verb|bifurcar'],
'bifurcas': ['verb|bifurcar'],
'bifurcás': ['verb|bifurcar'],
'bifurcan': ['verb|bifurcar'],
'bifurquéis': ['verb|bifurcar'],
'bifurques': ['verb|bifurcar'],
'bifurqués': ['verb|bifurcar'],
'bifurqué': ['verb|bifurcar'],
'bifurcasteis': ['verb|bifurcar'],
'bifurcaste': ['verb|bifurcar'],
'bifurcaron': ['verb|bifurcar'],
'bifurcó': ['verb|bifurcar'],
'nos bifurcaríamos': ['verb|bifurcarse'],
'me bifurcaría': ['verb|bifurcarse'],
'os bifurcaríais': ['verb|bifurcarse'],
'te bifurcarías': ['verb|bifurcarse'],
'se bifurcarían': ['verb|bifurcarse'],
'se bifurcaría': ['verb|bifurcarse'],
'nos bifurcaremos': ['verb|bifurcarse'],
'me bifurcaré': ['verb|bifurcarse'],
'os bifurcaréis': ['verb|bifurcarse'],
'te bifurcarás': ['verb|bifurcarse'],
'se bifurcarán': ['verb|bifurcarse'],
'se bifurcará': ['verb|bifurcarse'],
'nos bifurcáremos': ['verb|bifurcarse'],
'me bifurcare': ['verb|bifurcarse'],
'os bifurcareis': ['verb|bifurcarse'],
'te bifurcares': ['verb|bifurcarse'],
'se bifurcaren': ['verb|bifurcarse'],
'se bifurcare': ['verb|bifurcarse'],
'bifurcate': ['verb|bifurcarse'],
'nos bifurcábamos': ['verb|bifurcarse'],
'me bifurcaba': ['verb|bifurcarse'],
'os bifurcabais': ['verb|bifurcarse'],
'te bifurcabas': ['verb|bifurcarse'],
'se bifurcaban': ['verb|bifurcarse'],
'se bifurcaba': ['verb|bifurcarse'],
'nos bifurcáramos': ['verb|bifurcarse'],
'me bifurcara': ['verb|bifurcarse'],
'os bifurcarais': ['verb|bifurcarse'],
'te bifurcaras': ['verb|bifurcarse'],
'se bifurcaran': ['verb|bifurcarse'],
'se bifurcara': ['verb|bifurcarse'],
'nos bifurcásemos': ['verb|bifurcarse'],
'me bifurcase': ['verb|bifurcarse'],
'os bifurcaseis': ['verb|bifurcarse'],
'te bifurcases': ['verb|bifurcarse'],
'se bifurcasen': ['verb|bifurcarse'],
'se bifurcase': ['verb|bifurcarse'],
'no nos bifurquemos': ['verb|bifurcarse'],
'no os bifurquéis': ['verb|bifurcarse'],
'no te bifurques': ['verb|bifurcarse'],
'no se bifurquen': ['verb|bifurcarse'],
'no se bifurque': ['verb|bifurcarse'],
'nos bifurcamos': ['verb|bifurcarse'],
'me bifurco': ['verb|bifurcarse'],
'os bifurcáis': ['verb|bifurcarse'],
'te bifurcas': ['verb|bifurcarse'],
'te bifurcás': ['verb|bifurcarse'],
'se bifurcan': ['verb|bifurcarse'],
'se bifurca': ['verb|bifurcarse'],
'nos bifurquemos': ['verb|bifurcarse'],
'me bifurque': ['verb|bifurcarse'],
'os bifurquéis': ['verb|bifurcarse'],
'te bifurques': ['verb|bifurcarse'],
'te bifurqués': ['verb|bifurcarse'],
'se bifurquen': ['verb|bifurcarse'],
'se bifurque': ['verb|bifurcarse'],
'me bifurqué': ['verb|bifurcarse'],
'os bifurcasteis': ['verb|bifurcarse'],
'te bifurcaste': ['verb|bifurcarse'],
'se bifurcaron': ['verb|bifurcarse'],
'se bifurcó': ['verb|bifurcarse']
}
    wordlist = Wordlist(wordlist_data.splitlines())
    print(AllForms.from_wordlist(wordlist).all_forms)
    assert AllForms.from_wordlist(wordlist).all_forms == expected


def test_afecto():
    wordlist_data = """\
_____
afecto
pos: adj
  meta: {{es-adj|f=afecta}}
  forms: f=afecta; fpl=afectas; pl=afectos
  gloss: test
"""
    expected = {
'afecta': ['adj|afecto'],
'afectas': ['adj|afecto'],
'afectos': ['adj|afecto'],
'afecto': ['adj|afecto']}

    wordlist = Wordlist(wordlist_data.splitlines())
    assert AllForms.from_wordlist(wordlist).all_forms == expected

def test_ninguno():
    wordlist_data = """\
_____
ningún
pos: adj
  meta: {{head|es|adjective form|g=m|apocopate||standard form|ninguno}}
  gloss: test
"""
    expected = {
'ninguno': ['adj|ningún'],
'ningún': ['adj|ningún']
}

    wordlist = Wordlist(wordlist_data.splitlines())
    assert AllForms.from_wordlist(wordlist).all_forms == expected


def test_mmap(tmpdir):
    allforms_data = """\
test,adj,a1,a2,a3
test,noun,n1,n2,n3
"test1,test2",noun,test1,test2,test3
"""

    p = tmpdir.mkdir("allforms").join("allforms.csv")
    p.write(allforms_data)

    allforms = AllForms.from_file(p)
    assert allforms.all_forms == {'test': 0, 'test1,test2': 37}

    assert allforms.get_lemmas('test') == ['adj|a1', 'adj|a2', 'adj|a3', 'noun|n1', 'noun|n2', 'noun|n3']
    assert allforms.get_lemmas('test1,test2') == ['noun|test1', 'noun|test2', 'noun|test3']
