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
  form: m
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
  form: f
  gloss: female equivalent of "protector"
pos: n
  meta: {{es-noun|f}}
  forms: pl=protectoras
  form: f
  gloss: animal shelter (an organization that provides temporary homes for stray pet animals)
    syn: protectora de animales
_____
protectoras
pos: n
  meta: {{head|es|noun plural form|g=f-p}}
  form: f-p
  gloss: inflection of "protector"
_____
protectores
pos: n
  meta: {{head|es|noun plural form|g=m-p}}
  form: m-p
  gloss: inflection of "protector"
_____
protectrices
pos: n
  meta: {{head|es|noun plural form|g=f-p}}
  form: f-p
  gloss: inflection of "protector"
_____
protectriz
pos: n
  meta: {{es-noun|f|m=protector}}
  forms: m=protector; mpl=protectores; pl=protectrices
  form: f
  gloss: alternative form of "protectora"
    q: uncommon
"""
    expected = {
'protector': ['noun|protector'],
'protectora': ['noun|protector', 'noun|protectora'],
'protectoras': ['noun|protector', 'noun|protectora'],
'protectores': ['noun|protector'],
'protectrices': ['noun|protector'],
'protectriz': ['noun|protector'],
}

    wordlist = Wordlist(wordlist_data.splitlines())
    print(AllForms.from_wordlist(wordlist).all_forms)
    assert AllForms.from_wordlist(wordlist).all_forms == expected


def test_secondary_lemma_unique_forms():
    # Renfe should be alt of RENFE, but
    # Renfes should be a form of Renfe (since it cannot be an alt of RENFE)

    wordlist_data = """\
_____
test
pos: n
  gloss: test
_____
test2
pos: n
#  forms: pl=test2s
  gloss: alternative form of "test"
pos: n
  forms: pl=test2s
  form: m
  gloss: test2
"""

    expected = {
'test': ['noun|test'],
#'test2': ['noun|test'], ??
'test2': ['noun|test', 'noun|test2'],
'test2s': ['noun|test2']
}

    wordlist = Wordlist(wordlist_data.splitlines())
    assert AllForms.from_wordlist(wordlist).all_forms == expected


def test_secondary_lemma_no_unique_forms():

    wordlist_data = """\
_____
test
pos: n
  gloss: test
_____
test2
pos: n
  forms: pl=test2s
  gloss: alternative form of "test"
pos: n
  forms: pl=test2s
  form: m
  gloss: test2
"""

    expected = {
'test': ['noun|test'],
#'test2': ['noun|test'], ??
'test2': ['noun|test', 'noun|test2'],
'test2s': ['noun|test', 'noun|test2']
}

    wordlist = Wordlist(wordlist_data.splitlines())
    assert AllForms.from_wordlist(wordlist).all_forms == expected


def test_forms_text():

    wordlist_data = """\
testo {noun-meta} :: x
testo {noun-forms} :: pl=testos
testo {m} :: test
testo {noun-meta} :: x
testo {noun-forms} :: pl=testoz
testo {m} :: test2
testa {noun-meta} :: x
testa {noun-forms} :: pl=testas
testa {f} :: feminine noun of "testo"
"""
    expected = {
'testa': ['noun|testo'],
'testas': ['noun|testo'],
'testo': ['noun|testo'],
'testos': ['noun|testo'],
'testoz': ['noun|testo'],
}

    wordlist = Wordlist(wordlist_data.splitlines(), mbformat=True)
    assert AllForms.from_wordlist(wordlist).all_forms == expected

def test_forms_redirection():

    wordlist_data = """\
test1 {noun-meta} :: x
test1 {m} :: test
test2 {noun-meta} :: x
test2 {m} :: alternate form of "test1"
test3 {noun-meta} :: x
test3 {m} :: alternate form of "test2"
test4 {noun-meta} :: x
test4 {m} :: alternate form of "test3"
"""

    expected = {
'test1': ['noun|test1'],
'test2': ['noun|test1'],
'test3': ['noun|test1'],
'test4': ['noun|test1']
}

    wordlist = Wordlist(wordlist_data.splitlines(), mbformat=True)
    assert AllForms.from_wordlist(wordlist).all_forms == expected


def test_asco_forms():

    wordlist_data = """\
asca {noun-meta} :: x
asca {noun-forms} :: pl=ascas
asca {m} [mycology] | teca :: ascus
asco {noun-meta} :: x
asco {noun-forms} :: pl=ascos
asco {m} :: disgust
asco {m} :: nausea
asco {noun-meta} :: x
asco {noun-forms} :: pl=ascos
asco {m} :: alternative form of "asca"
"""

    expected = {
'asca': ['noun|asca'],
'ascas': ['noun|asca'],
'asco': ['noun|asco', 'noun|asca'],
'ascos': ['noun|asco', 'noun|asca']
}

    wordlist = Wordlist(wordlist_data.splitlines(), mbformat=True)
    assert AllForms.from_wordlist(wordlist).all_forms == expected
