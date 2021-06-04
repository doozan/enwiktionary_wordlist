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
    assert AllForms.from_wordlist(wordlist).all_forms == expected


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
'bifurcar': ['verb|bifurcar'],
'bifurca': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcamos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcáis': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcan': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcaba': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcabas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcábamos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcabais': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcaban': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcando': ['verb|bifurcar'],
'bifurqué': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcaste': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcó': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcasteis': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcaron': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcaré': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarás': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcará': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcaremos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcado': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcaréis': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarán': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcaría': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarías': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcaríamos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcaríais': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarían': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurque': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurques': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcada': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurqués': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquemos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquéis': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquen': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcara': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcaras': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcáramos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarais': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcados': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcaran': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcase': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcases': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcásemos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcaseis': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcasen': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcare': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcares': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcadas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcáremos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcareis': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcaren': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcá': ['verb|bifurcar'],
'bifurcad': ['verb|bifurcar'],
'bifurco': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcás': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándómela': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándómelas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándómelo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándómelos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándótela': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándótelas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándótelo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándótelos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándósela': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándóselas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándóselo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándóselos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándónosla': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándónoslas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándónoslo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándónoslos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándóosla': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándóoslas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándóoslo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándóoslos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándome': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándote': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándola': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándolo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándose': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándonos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándoos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándolas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándolos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándole': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándoles': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémóstela': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémóstelas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémóstelo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémóstelos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémónosla': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémónoslas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémónoslo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémónoslos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémóosla': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémóoslas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémóoslo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémóoslos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémoste': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémosla': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémoslo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémonos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémoos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémoslas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémoslos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémosle': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémosles': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquénmela': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquénmelas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquénmelo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquénmelos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquénnosla': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquénnoslas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquénnoslo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquénnoslos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquénsela': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquénselas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquénselo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquénselos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquenme': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquenla': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquenlo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquennos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquenlas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquenlos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquense': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquenle': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquenles': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquémela': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquémelas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquémelo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquémelos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquésela': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquéselas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquéselo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquéselos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquénosla': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquénoslas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquénoslo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquénoslos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrqueme': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquela': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquelo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquese': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquenos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquelas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquelos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquele': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrqueles': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcádmela': ['verb|bifurcar'],
'bifurcádmelas': ['verb|bifurcar'],
'bifurcádmelo': ['verb|bifurcar'],
'bifurcádmelos': ['verb|bifurcar'],
'bifurcádnosla': ['verb|bifurcar'],
'bifurcádnoslas': ['verb|bifurcar'],
'bifurcádnoslo': ['verb|bifurcar'],
'bifurcádnoslos': ['verb|bifurcar'],
'bifurcáosla': ['verb|bifurcar'],
'bifurcáoslas': ['verb|bifurcar'],
'bifurcáoslo': ['verb|bifurcar'],
'bifurcáoslos': ['verb|bifurcar'],
'bifurcádosla': ['verb|bifurcar'],
'bifurcádoslas': ['verb|bifurcar'],
'bifurcádoslo': ['verb|bifurcar'],
'bifurcádoslos': ['verb|bifurcar'],
'bifurcadme': ['verb|bifurcar'],
'bifurcadla': ['verb|bifurcar'],
'bifurcadlo': ['verb|bifurcar'],
'bifurcadnos': ['verb|bifurcar'],
'bifurcaos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcadlas': ['verb|bifurcar'],
'bifurcadlos': ['verb|bifurcar'],
'bifurcadle': ['verb|bifurcar'],
'bifurcadles': ['verb|bifurcar'],
'bifúrcámela': ['verb|bifurcar'],
'bifúrcámelas': ['verb|bifurcar'],
'bifúrcámelo': ['verb|bifurcar'],
'bifúrcámelos': ['verb|bifurcar'],
'bifúrcátela': ['verb|bifurcar'],
'bifúrcátelas': ['verb|bifurcar'],
'bifúrcátelo': ['verb|bifurcar'],
'bifúrcátelos': ['verb|bifurcar'],
'bifúrcánosla': ['verb|bifurcar'],
'bifúrcánoslas': ['verb|bifurcar'],
'bifúrcánoslo': ['verb|bifurcar'],
'bifúrcánoslos': ['verb|bifurcar'],
'bifúrcame': ['verb|bifurcar'],
'bifúrcate': ['verb|bifurcar'],
'bifúrcala': ['verb|bifurcar'],
'bifúrcalo': ['verb|bifurcar'],
'bifúrcanos': ['verb|bifurcar'],
'bifúrcalas': ['verb|bifurcar'],
'bifúrcalos': ['verb|bifurcar'],
'bifúrcale': ['verb|bifurcar'],
'bifúrcales': ['verb|bifurcar'],
'bifurcármela': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcármelas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcármelo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcármelos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcártela': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcártelas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcártelo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcártelos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcársela': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcárselas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcárselo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcárselos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcárnosla': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcárnoslas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcárnoslo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcárnoslos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcárosla': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcároslas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcároslo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcároslos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarme': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarte': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarla': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarlo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarse': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarnos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcaros': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarlas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarlos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarle': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarles': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcate': ['verb|bifurcarse'],
'bifurcaósmela': ['verb|bifurcarse'],
'bifurcaósmelas': ['verb|bifurcarse'],
'bifurcaósmelo': ['verb|bifurcarse'],
'bifurcaósmelos': ['verb|bifurcarse'],
'bifurcaósnosla': ['verb|bifurcarse'],
'bifurcaósnoslas': ['verb|bifurcarse'],
'bifurcaósnoslo': ['verb|bifurcarse'],
'bifurcaósnoslos': ['verb|bifurcarse'],
'bifurcaóosla': ['verb|bifurcarse'],
'bifurcaóoslas': ['verb|bifurcarse'],
'bifurcaóoslo': ['verb|bifurcarse'],
'bifurcaóoslos': ['verb|bifurcarse'],
'bifurcaósosla': ['verb|bifurcarse'],
'bifurcaósoslas': ['verb|bifurcarse'],
'bifurcaósoslo': ['verb|bifurcarse'],
'bifurcaósoslos': ['verb|bifurcarse'],
'bifurcaosme': ['verb|bifurcarse'],
'bifurcaosla': ['verb|bifurcarse'],
'bifurcaoslo': ['verb|bifurcarse'],
'bifurcaosnos': ['verb|bifurcarse'],
'bifurcaoos': ['verb|bifurcarse'],
'bifurcaoslas': ['verb|bifurcarse'],
'bifurcaoslos': ['verb|bifurcarse'],
'bifurcaosos': ['verb|bifurcarse'],
'bifurcaosle': ['verb|bifurcarse'],
'bifurcaosles': ['verb|bifurcarse'],
'bifurcátémela': ['verb|bifurcarse'],
'bifurcátémelas': ['verb|bifurcarse'],
'bifurcátémelo': ['verb|bifurcarse'],
'bifurcátémelos': ['verb|bifurcarse'],
'bifurcátétela': ['verb|bifurcarse'],
'bifurcátételas': ['verb|bifurcarse'],
'bifurcátételo': ['verb|bifurcarse'],
'bifurcátételos': ['verb|bifurcarse'],
'bifurcáténosla': ['verb|bifurcarse'],
'bifurcáténoslas': ['verb|bifurcarse'],
'bifurcáténoslo': ['verb|bifurcarse'],
'bifurcáténoslos': ['verb|bifurcarse'],
'bifurcáteme': ['verb|bifurcarse'],
'bifurcátete': ['verb|bifurcarse'],
'bifurcátela': ['verb|bifurcarse'],
'bifurcátelo': ['verb|bifurcarse'],
'bifurcátenos': ['verb|bifurcarse'],
'bifurcátelas': ['verb|bifurcarse'],
'bifurcátelos': ['verb|bifurcarse'],
'bifurcátele': ['verb|bifurcarse'],
'bifurcáteles': ['verb|bifurcarse']}

    wordlist = Wordlist(wordlist_data.splitlines())
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
