from enwiktionary_wordlist.wordlist import Wordlist
from enwiktionary_wordlist.all_forms import AllForms

def test_mf_noun():

    # all feminines should resolve to protector since there are no feminine lemmas

    wordlist_data = """\
_____
protector
pos: n
  meta: {{es-noun|m|protectores|f=protectora|f2=protectriz}}
  g: m
  gloss: protector
"""

    expected = {
'protector': ['n|protector'],
'protectora': ['n|protector'],
'protectoras': ['n|protector'],
'protectores': ['n|protector'],
'protectriz': ['n|protector'],
'protectrices': ['n|protector'],
}

    wordlist = Wordlist(wordlist_data.splitlines())
    allforms = AllForms.from_wordlist(wordlist, resolve_lemmas=True)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v
    allforms = AllForms.from_wordlist(wordlist, resolve_lemmas=False)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v


def test_f_equiv():

    # protectora is a lemma and should be an option for itself and its plurals

    wordlist_data = """\
_____
protector
pos: n
  meta: {{es-noun|m|protectores|f=protectora|f2=protectriz}}
  g: m
  gloss: protector
_____
protectora
pos: n
  meta: {{es-noun|f|+|pl2=protectora_altpl}}
  g: f
  gloss: female equivalent of "protector"
pos: n
  meta: {{es-noun|f|+|pl2=protectora_altpl2}}
  g: f
  gloss: not a form of the masculine
"""

    expected = {
'protector': ['n|protector'],
'protectora': ['n|protector', 'n|protectora'],
'protectoras': ['n|protector', 'n|protectora'],
'protectores': ['n|protector'],
'protectriz': ['n|protector'],
'protectrices': ['n|protector'],
'protectora_altpl': ['n|protectora'],
'protectora_altpl2': ['n|protectora'],
}

    wordlist = Wordlist(wordlist_data.splitlines())
    allforms = AllForms.from_wordlist(wordlist, resolve_lemmas=True)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v


    # The result should be the same if the feminine has a m= in the headword and defs
    wordlist_data = """\
_____
protector
pos: n
  meta: {{es-noun|m|protectores|f=protectora|f2=protectriz}}
  g: m
  gloss: protector
_____
protectora
pos: n
  meta: {{es-noun|f|+|pl2=protectora_altpl|m=protector}}
  g: f
  gloss: protectora
pos: n
  meta: {{es-noun|f|+|pl2=protectora_altpl2}}
  g: f
  gloss: not a form of the masculine
"""

    wordlist = Wordlist(wordlist_data.splitlines())
    allforms = AllForms.from_wordlist(wordlist, resolve_lemmas=True)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v
    allforms = AllForms.from_wordlist(wordlist, resolve_lemmas=False)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v


def test_alt_lemmas():

    # alt_protectora/alt_protectora_pl should only be forms of alt_protectora

    wordlist_data = """\
_____
protector
pos: n
  meta: {{es-noun|m|protectores|f=protectora|f2=protectriz}}
  g: m
  gloss: protector
_____
alt_protectora
pos: n
  meta: {{es-noun|f|alt_protectora_pl|m=protector}}
  g: f
  gloss: female protector
"""

    expected = {
'protector': ['n|protector'],
'protectora': ['n|protector'],
'protectoras': ['n|protector'],
'protectores': ['n|protector'],
'protectriz': ['n|protector'],
'protectrices': ['n|protector'],
'alt_protectora': ['n|alt_protectora'],
'alt_protectora_pl': ['n|alt_protectora'],
}

    wordlist = Wordlist(wordlist_data.splitlines())
    allforms = AllForms.from_wordlist(wordlist, resolve_lemmas=True)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v
    allforms = AllForms.from_wordlist(wordlist, resolve_lemmas=False)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v



def test_is_lemma():

    wordlist_data = """\
_____
protector
pos: n
  meta: {{es-noun|m|protectores|f=protectora|f2=protectriz}}
  g: m
  gloss: protector
_____
protectora
pos: n
  meta: {{es-noun|f|m=protector}}
  g: f
  gloss: female equivalent of "protector"
pos: n
  meta: {{es-noun|f}}
  g: f
  gloss: animal shelter (an organization that provides temporary homes for stray pet animals)
pos: n
  meta: {{head|es|noun}}
  g: f
  gloss: using head
pos: n
  meta: {{head|es|noun form}}
  g: f
  gloss: using head form
"""

    wordlist = Wordlist(wordlist_data.splitlines())

    words = wordlist.get_words("protector", "n")
    assert AllForms.is_lemma(words[0]) == True

    words = wordlist.get_words("protectora", "n")
    assert AllForms.is_lemma(words[0]) == True
    assert AllForms.is_lemma(words[1]) == True
    assert AllForms.is_lemma(words[2]) == True
    assert AllForms.is_lemma(words[3]) == False


def test_forms_complex1():
    # protectora should be a form of protector even though it has a secondary
    # declaration as a lemma

    wordlist_data = """\
_____
protector
pos: n
  meta: {{es-noun|m|protectores|f=protectora|f2=protectriz}}
  g: m
  gloss: protector (someone who protects or guards)
pos: n
  meta: {{es-noun|m}}
  g: m
  gloss: protector (a device or mechanism which is designed to protect)
_____
protectora
pos: n
  meta: {{es-noun|f|m=protector}}
  g: f
  gloss: female equivalent of "protector"
pos: n
  meta: {{es-noun|f}}
  g: f
  gloss: animal shelter (an organization that provides temporary homes for stray pet animals)
    syn: protectora de animales
_____
protectoras
pos: n
  meta: {{head|es|noun plural form|g=f-p}}
  g: f-p
  gloss: plural of "protectora"
_____
protectores
pos: n
  meta: {{head|es|noun plural form|g=m-p}}
  g: m-p
  gloss: plural of "protector"
_____
protectrices
pos: n
  meta: {{head|es|noun plural form|g=f-p}}
  g: f-p
  gloss: plural of "protectriz"
_____
protectriz
pos: n
  meta: {{es-noun|f|m=protector}}
  g: f
  gloss: alternative form of "protectora"
    q: uncommon
"""
    expected = {
'protector': ['n|protector'],
'protectora': ['n|protector', 'n|protectora'],
'protectoras': ['n|protector', 'n|protectora'],
'protectores': ['n|protector'],
'protectrices': ['n|protector', 'n|protectriz'],
'protectriz': ['n|protector', 'n|protectriz'],
}

    wordlist = Wordlist(wordlist_data.splitlines())
    allforms = AllForms.from_wordlist(wordlist)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v


def test_forms_text1():

    wordlist_data = """\
testo {n-meta} :: {{es-noun|m}}
testo {m} :: test
testo {n-meta} :: {{es-noun|m|testoz}}
testo {m} :: test2
testa {n-meta} :: {{es-noun|f}}
testa {f} :: feminine noun of "testo"
"""
    expected = {
'testa': ['n|testa'],
'testas': ['n|testa'],
'testo': ['n|testo'],
'testos': ['n|testo'],
'testoz': ['n|testo'],
}

    wordlist = Wordlist(wordlist_data.splitlines())
    allforms = AllForms.from_wordlist(wordlist)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v
    allforms = AllForms.from_wordlist(wordlist, resolve_lemmas=False)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v

def notest_forms_redirection():

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
    allforms = AllForms.from_wordlist(wordlist)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v

    # this should be different
    allforms = AllForms.from_wordlist(wordlist, resolve_lemmas=False)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v


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
'asco': ['n|asco'],
'ascos': ['n|asco']
}

    wordlist = Wordlist(wordlist_data.splitlines())
    allforms = AllForms.from_wordlist(wordlist)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v
    allforms = AllForms.from_wordlist(wordlist, resolve_lemmas=False)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v


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
'bifurcaríamos': ['verb|bifurcar'],
'bifurcaría': ['verb|bifurcar'],
'bifurcaríais': ['verb|bifurcar'],
'bifurcarían': ['verb|bifurcar'],
'bifurcarías': ['verb|bifurcar'],
'bifurcaremos': ['verb|bifurcar'],
'bifurcaré': ['verb|bifurcar'],
'bifurcaréis': ['verb|bifurcar'],
'bifurcarán': ['verb|bifurcar'],
'bifurcarás': ['verb|bifurcar'],
'bifurcará': ['verb|bifurcar'],
'bifurcáremos': ['verb|bifurcar'],
'bifurcare': ['verb|bifurcar'],
'bifurcareis': ['verb|bifurcar'],
'bifurcaren': ['verb|bifurcar'],
'bifurcares': ['verb|bifurcar'],
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
'bifurcádmela': ['verb|bifurcar'],
'bifurcádmelas': ['verb|bifurcar'],
'bifurcádmele': ['verb|bifurcar'],
'bifurcádmeles': ['verb|bifurcar'],
'bifurcádmelo': ['verb|bifurcar'],
'bifurcádmelos': ['verb|bifurcar'],
'bifurcadnos': ['verb|bifurcar'],
'bifurcádnosla': ['verb|bifurcar'],
'bifurcádnoslas': ['verb|bifurcar'],
'bifurcádnosle': ['verb|bifurcar'],
'bifurcádnosles': ['verb|bifurcar'],
'bifurcádnoslo': ['verb|bifurcar'],
'bifurcádnoslos': ['verb|bifurcar'],
'bifurcaos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcádosla': ['verb|bifurcar'],
'bifurcádoslas': ['verb|bifurcar'],
'bifurcádosle': ['verb|bifurcar'],
'bifurcádosles': ['verb|bifurcar'],
'bifurcádoslo': ['verb|bifurcar'],
'bifurcádoslos': ['verb|bifurcar'],
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
'bifurcá': ['verb|bifurcar'],
'bifurcábamos': ['verb|bifurcar'],
'bifurcaba': ['verb|bifurcar'],
'bifurcabais': ['verb|bifurcar'],
'bifurcaban': ['verb|bifurcar'],
'bifurcabas': ['verb|bifurcar'],
'bifurcáramos': ['verb|bifurcar'],
'bifurcara': ['verb|bifurcar'],
'bifurcarais': ['verb|bifurcar'],
'bifurcaran': ['verb|bifurcar'],
'bifurcaras': ['verb|bifurcar'],
'bifurcásemos': ['verb|bifurcar'],
'bifurcase': ['verb|bifurcar'],
'bifurcaseis': ['verb|bifurcar'],
'bifurcasen': ['verb|bifurcar'],
'bifurcases': ['verb|bifurcar'],
'bifurcarla': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarlas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarle': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarles': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarlo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarlos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarme': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcármela': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcármelas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcármele': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcármeles': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcármelo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcármelos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarnos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcárnosla': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcárnoslas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcárnosle': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcárnosles': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcárnoslo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcárnoslos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcaros': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcárosla': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcároslas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcárosle': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcárosles': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcároslo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcároslos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarse': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcársela': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcárselas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcársele': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcárseles': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcárselo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcárselos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarte': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcártela': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcártelas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcártele': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcárteles': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcártelo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcártelos': ['verb|bifurcar', 'verb|bifurcarse'],
'no bifurquemos': ['verb|bifurcar'],
'no bifurquéis': ['verb|bifurcar'],
'no bifurquen': ['verb|bifurcar'],
'no bifurques': ['verb|bifurcar'],
'no bifurque': ['verb|bifurcar'],
'bifurcadas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcada': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcados': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcado': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcamos': ['verb|bifurcar'],
'bifurco': ['verb|bifurcar'],
'bifurcáis': ['verb|bifurcar'],
'bifurcan': ['verb|bifurcar'],
'bifurcas': ['verb|bifurcar'],
'bifurcás': ['verb|bifurcar'],
'bifurquéis': ['verb|bifurcar'],
'bifurques': ['verb|bifurcar'],
'bifurqués': ['verb|bifurcar'],
'bifurqué': ['verb|bifurcar'],
'bifurcasteis': ['verb|bifurcar'],
'bifurcaron': ['verb|bifurcar'],
'bifurcaste': ['verb|bifurcar'],
'bifurcó': ['verb|bifurcar'],
'nos bifurcaríamos': ['verb|bifurcarse'],
'me bifurcaría': ['verb|bifurcarse'],
'os bifurcaríais': ['verb|bifurcarse'],
'se bifurcarían': ['verb|bifurcarse'],
'te bifurcarías': ['verb|bifurcarse'],
'se bifurcaría': ['verb|bifurcarse'],
'nos bifurcaremos': ['verb|bifurcarse'],
'me bifurcaré': ['verb|bifurcarse'],
'os bifurcaréis': ['verb|bifurcarse'],
'se bifurcarán': ['verb|bifurcarse'],
'te bifurcarás': ['verb|bifurcarse'],
'se bifurcará': ['verb|bifurcarse'],
'nos bifurcáremos': ['verb|bifurcarse'],
'me bifurcare': ['verb|bifurcarse'],
'os bifurcareis': ['verb|bifurcarse'],
'se bifurcaren': ['verb|bifurcarse'],
'te bifurcares': ['verb|bifurcarse'],
'se bifurcare': ['verb|bifurcarse'],
'bifurcate': ['verb|bifurcarse'],
'nos bifurcábamos': ['verb|bifurcarse'],
'me bifurcaba': ['verb|bifurcarse'],
'os bifurcabais': ['verb|bifurcarse'],
'se bifurcaban': ['verb|bifurcarse'],
'te bifurcabas': ['verb|bifurcarse'],
'se bifurcaba': ['verb|bifurcarse'],
'nos bifurcáramos': ['verb|bifurcarse'],
'me bifurcara': ['verb|bifurcarse'],
'os bifurcarais': ['verb|bifurcarse'],
'se bifurcaran': ['verb|bifurcarse'],
'te bifurcaras': ['verb|bifurcarse'],
'se bifurcara': ['verb|bifurcarse'],
'nos bifurcásemos': ['verb|bifurcarse'],
'me bifurcase': ['verb|bifurcarse'],
'os bifurcaseis': ['verb|bifurcarse'],
'se bifurcasen': ['verb|bifurcarse'],
'te bifurcases': ['verb|bifurcarse'],
'se bifurcase': ['verb|bifurcarse'],
'no nos bifurquemos': ['verb|bifurcarse'],
'no os bifurquéis': ['verb|bifurcarse'],
'no se bifurquen': ['verb|bifurcarse'],
'no te bifurques': ['verb|bifurcarse'],
'no se bifurque': ['verb|bifurcarse'],
'nos bifurcamos': ['verb|bifurcarse'],
'me bifurco': ['verb|bifurcarse'],
'os bifurcáis': ['verb|bifurcarse'],
'se bifurcan': ['verb|bifurcarse'],
'te bifurcas': ['verb|bifurcarse'],
'se bifurca': ['verb|bifurcarse'],
'te bifurcás': ['verb|bifurcarse'],
'nos bifurquemos': ['verb|bifurcarse'],
'me bifurque': ['verb|bifurcarse'],
'os bifurquéis': ['verb|bifurcarse'],
'se bifurquen': ['verb|bifurcarse'],
'te bifurques': ['verb|bifurcarse'],
'se bifurque': ['verb|bifurcarse'],
'te bifurqués': ['verb|bifurcarse'],
'me bifurqué': ['verb|bifurcarse'],
'os bifurcasteis': ['verb|bifurcarse'],
'se bifurcaron': ['verb|bifurcarse'],
'te bifurcaste': ['verb|bifurcarse'],
'se bifurcó': ['verb|bifurcarse']
}
    wordlist = Wordlist(wordlist_data.splitlines())
    allforms = AllForms.from_wordlist(wordlist)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v
    allforms = AllForms.from_wordlist(wordlist, resolve_lemmas=False)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v


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
    allforms = AllForms.from_wordlist(wordlist)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v
    allforms = AllForms.from_wordlist(wordlist, resolve_lemmas=False)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v

def test_nonlemma():

    # lemmas can use meta to make forms
    wordlist_data = """\
_____
ningún
pos: determiner
  meta: {{head|es|determiner|g=m|masculine|ninguno|feminine|ninguna}}
  gloss: test
"""
    expected = {'ningún': ['determiner|ningún']}
    wordlist = Wordlist(wordlist_data.splitlines())
    allforms = AllForms.from_wordlist(wordlist)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v
    allforms = AllForms.from_wordlist(wordlist, resolve_lemmas=False)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v

    # but forms can't
    wordlist_data = """\
_____
ningún
pos: determiner
  meta: {{head|es|determiner form|g=m|masculine|ninguno|feminine|ninguna}}
  gloss: test
"""
    expected = {}
    wordlist = Wordlist(wordlist_data.splitlines())
    allforms = AllForms.from_wordlist(wordlist)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v
    allforms = AllForms.from_wordlist(wordlist, resolve_lemmas=False)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v

    # however, forms can declare themselves forms of existing lemmas
    wordlist_data = """\
_____
ninguno
pos: determiner
  meta: {{head|es|determiner|g=m|feminine|ninguna}}
  gloss: no; none
_____
ningún
pos: determiner
  meta: {{head|es|determiner form|g=m|masculine|ninguno|feminine|ninguna}}
  gloss: apocopic form of "ninguno"
"""
    expected = {
            'ninguno': ['determiner|ninguno'],
            'ninguna': ['determiner|ninguno'],
            'ningún': ['determiner|ninguno']}
    wordlist = Wordlist(wordlist_data.splitlines())
    allforms = AllForms.from_wordlist(wordlist)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v
    allforms = AllForms.from_wordlist(wordlist, resolve_lemmas=False)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v




def test_mmap(tmpdir):
    allforms_data = """\
test,adj,a1,a2,a3
test,noun,n1,n2,n3
"test1,test2",noun,test1,test2,test3
"""

    p = tmpdir.mkdir("allforms").join("allforms.csv")
    p.write(allforms_data)

    allforms = AllForms.from_file(p)
#    assert allforms.all_forms == {'test': 0, 'test1,test2': 37}

    assert allforms.get_lemmas('test') == ['adj|a1', 'adj|a2', 'adj|a3', 'noun|n1', 'noun|n2', 'noun|n3']
    assert allforms.get_lemmas('test1,test2') == ['noun|test1', 'noun|test2', 'noun|test3']


def test_actor():

    # masculine with female forms
    # feminine with male forms

    wordlist_data="""\
_____
actor
pos: n
  meta: {{es-noun|m|f=actriz}}
  g: m
  gloss: An actor (person who performs in a theatrical play or movie)
_____
actriz
pos: n
  meta: {{es-noun|f|m=actor}}
  g: f
  gloss: actress
"""
    expected = {
        'actores': ['n|actor'],
        'actriz': ['n|actor', 'n|actriz'],
        'actrices': ['n|actor', 'n|actriz'],
        'actor': ['n|actor']
    }

    wordlist = Wordlist(wordlist_data.splitlines())
    allforms = AllForms.from_wordlist(wordlist)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v
    allforms = AllForms.from_wordlist(wordlist, resolve_lemmas=False)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v

def test_male_lemma():

    # male lemma with feminine equivalent

    wordlist_data="""\
_____
coneja
pos: n
  meta: {{es-noun|f|m=conejo}}
  g: f
  gloss: female equivalent of "conejo"
_____
conejo
pos: n
  meta: {{es-noun|m|f=coneja}}
  g: m
  gloss: rabbit
"""
    expected = {
        'coneja':  ['n|coneja', 'n|conejo'],
        'conejas': ['n|coneja', 'n|conejo'],
        'conejo':  ['n|conejo'],
        'conejos': ['n|conejo'],
    }

    wordlist = Wordlist(wordlist_data.splitlines())
    allforms = AllForms.from_wordlist(wordlist)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v

def test_female_lemma():

    # feminine lemma with male forms

    # There's no way to distinguish this from a 'normal' m/f pair where the masculine
    # in the preferred lemma.

    wordlist_data="""\
_____
cabra
pos: n
  meta: {{es-noun|f|m=cabro}}
  g: f
  gloss: goat, primary lemma
_____
cabro
pos: n
  meta: {{es-noun|m|f=cabra}}
  g: m
  gloss: male goat
"""

    # Ideally this would be reversed, but there's no way of knowing that the female lemma is the 'main' lemma
    expected = {
        'cabra': ['n|cabra', 'n|cabro'],
        'cabras': ['n|cabra', 'n|cabro'],
        'cabro': ['n|cabro'],
        'cabros': ['n|cabro'],
    }

    wordlist = Wordlist(wordlist_data.splitlines())
    allforms = AllForms.from_wordlist(wordlist)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v
    allforms = AllForms.from_wordlist(wordlist, resolve_lemmas=False)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v

def test_latine():

    # non binary shouldn't add forms to binary words

    wordlist_data="""\
_____
latine
pos: n
  meta: {{es-noun|mf|m=latino|f=latina}}
  g: mf
  gloss: someone of Latin American descent, regardless of gender; e.g. a Latino or Latina
_____
latino
  pos: n
  meta: {{es-noun|m|f=latina}}
  g: m
  etymology: Borrowed from Latin "latīnus". Compare ladino.
  gloss: a Latino
_____
latina
pos: n
  meta: {{es-noun|f|m=latino}}
  g: f
  gloss: female equivalent of "latino"; a Latina
"""

    expected = {
        'latine': ['n|latine'],
        'latines': ['n|latine'],

        'latina': ['n|latina', 'n|latino'],
        'latinas': ['n|latina', 'n|latino'],

        'latino': ['n|latino'],
        'latinos': ['n|latino'],
    }

    wordlist = Wordlist(wordlist_data.splitlines())
    allforms = AllForms.from_wordlist(wordlist)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v
    allforms = AllForms.from_wordlist(wordlist, resolve_lemmas=False)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v


def test_clientes():

    wordlist_data="""\
_____
clienta
pos: n
  meta: {{es-noun|f|m=cliente}}
  g: f
  gloss: female equivalent of "cliente"
_____
clientas
pos: n
  meta: {{head|es|noun form|g=f-p}}
  g: f-p
  gloss: plural of "clienta"
_____
cliente
pos: n
  meta: {{es-noun|m|f=cliente|f2=clienta}}
  g: m
  gloss: client
"""

    expected = {
        'clienta': ['n|clienta', 'n|cliente'],
        'clientas': ['n|clienta', 'n|cliente'],
        'clientes': ['n|cliente'],
        'cliente': ['n|cliente']
    }

    wordlist = Wordlist(wordlist_data.splitlines())
    allforms = AllForms.from_wordlist(wordlist)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v
    allforms = AllForms.from_wordlist(wordlist, resolve_lemmas=False)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v


def test_nosotres():

    # non binary shouldn't add forms to binary words

    wordlist_data="""\
_____
nosotras
pos: pron
  meta: {{head|es|pronoun|g=f-p|masculine plural|nosotros}}
  g: f-p
  etymology: nos + otras
  gloss: we (feminine plural)
_____
nosotres
pos: pron
  meta: {{head|es|pronoun|masculine|nosotros|feminine|nosotras}}
  gloss: we
    q: hypercorrect, gender-neutral, neologism
_____
nosotros
pos: pron
  meta: {{head|es|pronoun|g=m-p|feminine plural|nosotras}}
  g: m-p
  etymology: From Old Spanish "nos" (us) from Latin "nōs" + otros (others), plural of otro, from Latin "alter". Compare Galician "nosoutros", Catalan "nosaltres", Occitan "nosautre
  gloss: we (masculine plural)
  gloss: inflection of "nosotros"
    q: disjunctive
"""

    expected = {
        'nosotros': ['pron|nosotros'],
        'nosotras': ['pron|nosotras', 'pron|nosotros'],
        'nosotres': ['pron|nosotres']
    }

    wordlist = Wordlist(wordlist_data.splitlines())
    allforms = AllForms.from_wordlist(wordlist)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v
    allforms = AllForms.from_wordlist(wordlist, resolve_lemmas=False)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v


def test_bosniacas():

    wordlist_data="""\
_____
bosníaco
pos: n
  meta: {{es-noun|m|f=bosníaca}}
  g: m
  gloss: Bosniak (native or resident of the region of Bosnia; a descendant of the people from the region of Bosnia)
_____
bosniaca
pos: n
  meta: {{es-noun|f|m=bosniaco}}
  g: f
  gloss: female equivalent of "bosniaco"
_____
bosniaco
pos: n
  meta: {{es-noun|m|f=bosniaca}}
  g: m
  gloss: alternative spelling of "bosníaco"
"""

    expected = {
        'bosníaco': ['n|bosníaco'],
        'bosníacos': ['n|bosníaco'],
        'bosníaca': ['n|bosníaco'],
        'bosníacas': ['n|bosníaco'],
        'bosniaca': ['n|bosniaca', 'n|bosniaco'],
        'bosniacas': ['n|bosniaca', 'n|bosniaco'],
        'bosniaco': ['n|bosniaco'],
        'bosniacos': ['n|bosniaco'],
    }

    wordlist = Wordlist(wordlist_data.splitlines())
    allforms = AllForms.from_wordlist(wordlist)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v

def test_acapulco():

    # non binary shouldn't add forms to binary words

    wordlist_data="""\
_____
Acapulco
pos: prop
  meta: {{es-proper noun}}
  gloss: Acapulco (a city in Guerrero, Mexico)
"""

    expected = {'Acapulco': ['prop|Acapulco']}

    wordlist = Wordlist(wordlist_data.splitlines())
    allforms = AllForms.from_wordlist(wordlist, resolve_lemmas=True)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v

    allforms = AllForms.from_wordlist(wordlist, resolve_lemmas=False)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v

def test_fulana():

    # feminines shouldn't add masculine forms

#pos: prop
#  meta: {{head|es|proper noun|g=f|plural|fulanas|masculine|fulano|maculine plural|fulanos}}
    wordlist_data="""\
_____
fulana
pos: n
  meta: {{es-noun|f|m=+}}
  g: f
  gloss: miss so-and-so
    q: derogatory
  gloss: harlot, slut
    q: derogatory
"""

    expected = {'fulana': ['n|fulana'],
              'fulanas': ['n|fulana'],
              'fulano': ['n|fulana'],
              'fulanos': ['n|fulana']}

    wordlist = Wordlist(wordlist_data.splitlines())
    allforms = AllForms.from_wordlist(wordlist, resolve_lemmas=False)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v
    allforms = AllForms.from_wordlist(wordlist, resolve_lemmas=False)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v


def test_condense_verbs_wrong_existing_form():

    wordlist_data = """\
_____
aborregas
pos: v
  meta: {{head|es|verb form}}
  gloss: pres_2s of "aborregar"
_____
aborregar
pos: v
  meta: {{head|es|verb form}}
  gloss: infinitive of "aborregarse"
_____
aborregarse
pos: v
  meta: {{es-verb}} {{es-conj}}
  gloss: verb
"""

    wordlist = Wordlist(wordlist_data.splitlines())
#    assert "te aborregas" in AllForms.from_wordlist(wordlist).all_forms
    assert "aborregas" in AllForms.from_wordlist(wordlist).all_forms
    assert AllForms.from_wordlist(wordlist).get_lemmas("aborregas") == ['v|aborregar', 'v|aborregarse']
    assert AllForms.from_wordlist(wordlist, resolve_lemmas=False).get_lemmas("aborregas") == ['v|aborregar', 'v|aborregarse'] #, 'v|aborregas']


def test_forms_complex_csv():
    # protectora should be a form of protector even though it has a secondary
    # declaration as a lemma



    wordlist_data = """\
_____
protector
pos: n
  meta: {{es-noun|m|protectores|f=protectora|f2=protectriz}}
  g: m
  gloss: protector
_____
protectora
pos: n
  meta: {{es-noun|f|m=protector}}
  g: f
  gloss: female equivalent of "protector"
pos: n
  meta: {{es-noun|f|+|pl2=protectora_altpl2}}
  g: f
  gloss: another
_____
protectriz
pos: n
  meta: {{es-noun|f|m=protector}}
  g: f
  gloss: alternative form of "protectora"
    q: uncommon
"""

    expected= """\
protector,n,protector
protectora,n,protector,protectora
protectora_altpl2,n,protectora
protectoras,n,protector,protectora
protectores,n,protector
protectrices,n,protector,protectriz
protectriz,n,protector,protectriz\
"""

    wordlist = Wordlist(wordlist_data.splitlines())
    allforms = AllForms.from_wordlist(wordlist)
    print("\n".join(allforms.all_csv))
    assert list(allforms.all_csv) == expected.splitlines()

def test_secondary_lemma_unique_forms_csv():

    wordlist_data = """\
_____
test
pos: n
  meta: {{es-noun|m}}
  g: m
  gloss: test
_____
test2
pos: n
  meta: {{es-noun|m}}
  g: m
  gloss: alternative form of "test"
_____
test3
pos: n
  meta: {{head|es|noun form}}
  g: m
  gloss: alternative form of "test"
_____
test4
pos: n
  meta: {{head|es|noun form}}
  g: m
  gloss: alternative form of "missing_lemma"
_____
test5
pos: n
  meta: {{es-noun|m}}
  g: m
  gloss: test5
_____
test6
pos: n
  meta: {{head|es|noun form}}
  g: m
  gross: this has a definition befor the form of
  gloss: alternative form of "test"
"""


# test2 does not list test as a lemma because
# test does not declare test2 as a form and
# test2 is marked as a lemma and not as a form of

    expected = """\
test,n,test
test2,n,test2
test2s,n,test2
test3,n,test
test4,n,missing_lemma
test5,n,test5
test5s,n,test5
test6,n,test
tests,n,test\
"""

    wordlist = Wordlist(wordlist_data.splitlines())
    allforms = AllForms.from_wordlist(wordlist)
    print("\n".join(allforms.all_csv))
    assert list(allforms.all_csv) == expected.splitlines()


def test_aquellos():

    wordlist_data = """\
_____
aquél
pos: pron
  meta: {{head|es|pronoun|demonstrative||feminine|aquélla|neuter|aquello|masculine plural|aquéllos|feminine plural|aquéllas|g=m}}
  g: m
  gloss: that one (far from speaker and listener)
    q: demonstrative
  gloss: the former
    q: demonstrative
  gloss: anyone/anything
    q: demonstrative
_____
aquéllas
pos: pron
  meta: {{head|es|pronoun form|demonstrative|g=f-p}}
  g: f-p
  gloss: feminine plural of "aquél"; those ones (far from speaker and listener)
_____
aquéllos
pos: pron
  meta: {{head|es|pronoun form|demonstrative|g=m-p}}
  g: m-p
  gloss: plural of "aquél"; those ones (far from speaker and listener)
_____
aquel
pos: determiner
  meta: {{head|es|determiner|feminine|aquella|masculine plural|aquellos|g=m-s}}
  g: m-s
  etymology: From VL "*accum ille", a compound of Latin "eccum" and ille.
  gloss: that (over there; implying some distance)
    q: demonstrative
pos: pron
  meta: {{head|es|pronoun form}}
  usage: The unaccented form can function as a pronoun if it can be unambiguously deduced as such from context.
  etymology: From VL "*accum ille", a compound of Latin "eccum" and ille.
  gloss: alternative spelling of "aquél"
    q: demonstrative
_____
aquella
pos: pron
  meta: {{head|es|pronoun form|demonstrative|g=f}}
  g: f
  usage: The unaccented form can function as a pronoun if it can be unambiguously deduced as such from context.
  etymology: From VL "*accum ille", from Latin "eccum" ille.
  gloss: alternative spelling of "aquélla"; that one
_____
aquellas
pos: determiner
  meta: {{head|es|determiner form|g=f-p}}
  g: f-p
  etymology: From Latin "eccu(m)" illās.
  gloss: feminine plural of "aquel"; those (over there; implying some distance)
pos: pron
  meta: {{head|es|pronoun|demonstrative|g=f-p}}
  g: f-p
  usage: The unaccented form can function as a pronoun if it can be unambiguously deduced as such from context.
  etymology: From Latin "eccu(m)" illās.
  gloss: alternative spelling of "aquéllas"; those ones
_____
aquello
pos: pron
  meta: {{head|es|pronoun form}}
  etymology: From VL "*accum illud", neuter singular of *accum ille.
  gloss: neuter singular of "aquél"; that (over there); it
_____
aquellos
pos: determiner
  meta: {{head|es|determiner form|demonstrative|g=m-p}}
  g: m-p
  etymology: From Latin "eccu(m)" illōs.
  gloss: masculine plural of "aquel"; those (over there; implying some distance)
pos: pron
  meta: {{head|es|pronoun|demonstrative|g=m-p}}
  g: m-p
  etymology: From Latin "eccu(m)" illōs.
  gloss: alternative spelling of "aquéllos"; those ones (over there; implying some distance). The unaccented form can function as a pronoun if it can be unambiguously deduced as su
pos: pron
  meta: {{head|es|pronoun|g=n-p}}
  g: n-p
  etymology: From Latin "eccu(m)" illōs.
  gloss: Those ones. (over there; implying some distance)
"""

    expected = """\
aquel,determiner,aquel
aquel,pron,aquél
aquella,determiner,aquel
aquella,pron,aquélla
aquellas,determiner,aquel
aquellas,pron,aquellas
aquello,pron,aquél
aquellos,determiner,aquel
aquellos,pron,aquellos
aquél,pron,aquél
aquélla,pron,aquél
aquéllas,pron,aquél
aquéllos,pron,aquél
"""

    wordlist = Wordlist(wordlist_data.splitlines())
    allforms = AllForms.from_wordlist(wordlist)
    print("\n".join(allforms.all_csv))
    assert list(allforms.all_csv) == expected.splitlines()


def test_alt_of_form():

    # misspellings count as forms

    data="""\
_____
país
pos: n
  meta: {{es-noun|m|países}}
  g: m
  etymology: Borrowed from French "pays", from Old French "païs", from Malayalam "pagensis", from Latin "pāgus" (“country”). Compare Sicilian "pajisi", Italian "paese".
  gloss: country (the territory of a nation)
  gloss: country, land (a set region of land having particular human occupation or agreed limits)
_____
paises
pos: n
  meta: {{head|es|misspelling}}
  gloss: misspelling of "países"
"""

    expected = """\
paises,n,países
país,n,país
países,n,país\
"""

    wordlist = Wordlist(data.splitlines())
    allforms = AllForms.from_wordlist(wordlist)
    print("\n".join(allforms.all_csv))

    assert allforms.is_lemma(next(wordlist.get_iwords("paises", "n"))) == False
    assert list(allforms.all_csv) == expected.splitlines()
