import enwiktionary_wordlist as wordlist

def run_test_sense_form(gloss, formtype, lemma, nonform):
    sense = wordlist.Sense("x",None,gloss,None)
    assert sense.formtype == formtype
    assert sense.lemma == lemma
    assert sense.nonform == nonform

def test_sense():
    sense = wordlist.Sense("m","rare","(mostly) obsolete form of fuego","syn1; syn2")
    assert sense.pos == "m"
    assert sense.qualifier == "rare"
    assert sense.synonyms == ["syn1", "syn2"]
    assert sense.formtype == "old"
    assert sense.lemma == "fuego"
    assert sense.nonform == "(mostly"

    run_test_sense_form("An alternative form of centollo", "alt", "centollo", "")
    run_test_sense_form("feminine noun of test word, testing", "f", "test word", "testing")
    run_test_sense_form("testing, alternative form of test word", "alt", "test word", "testing")
    run_test_sense_form("alternative spelling of test", "alt", "test", "")
    run_test_sense_form("nonstandard form of 1.ª", "alt", "1.ª", "")
    run_test_sense_form("alternative form of EE. UU", "alt", "EE. UU", "")
    run_test_sense_form("to defend. (obsolete spelling of defender)", "old", "defender", "to defend.")
    run_test_sense_form("given name: alternative spelling of Carina", "alt", "Carina", "given name")
    run_test_sense_form("obsolete form of se (as a dative pronoun)", "old", "se", "as a dative pronoun)")


def test_word():
    word = wordlist.Word("test", "m")
    assert word.common_pos == "noun"

    word.add_sense("m", "rare", "a test word", None)
    assert len(word.senses) == 1
    assert word.forms == {}
    assert word.form_of == {}

    # Adding form of in a secondary def should have effect
    word.add_sense("m", None, 'alternative form of "testz"', None)
    assert word.forms == {}
    assert word.form_of == {}

    # But form of in the first def does
    word = wordlist.Word("test", "m")
    assert word.common_pos == "noun"
    word.add_sense("m", None, 'alternative form of "testz"', None)
    assert word.forms == {}
    assert word.form_of == { "testz": ["alt"] }

    word.add_form("pl", "tests")
    assert word.forms == { "pl": ["tests"] }

    word.add_form("pl", "test2s")
    assert word.forms == { "pl": ["tests", "test2s"] }

    # dup should not do anything
    word.add_form("pl", "tests")
    assert word.forms == { "pl": ["tests", "test2s"] }

    word.add_forms( {"pl": ["test3s"], "f": ["testa"] } )
    assert word.forms == { "pl": ["tests", "test2s", "test3s"], "f": ["testa"] }

    word.parse_forms("pl=test4s; f=test2a")
    assert word.forms == { "pl": ["tests", "test2s", "test3s", "test4s"], "f": ["testa", "test2a"] }

#def test_verb():
#    verb = wordlist.Verb("obrir")
##    verb.add_meta("pattern=-brir; stem=o")
#    verb.add_meta("old=abrir")
#
#    assert verb.paradigms == [ ("-brir", ["o"]) ]
#    assert verb.forms == { "old": ["abrir"] }

def test_wordlist():
    data="""\
amigo {noun-forms} :: f=amiga; fpl=amigas; pl=amigos
amigo {m} :: friend
amiga {noun-forms} :: m=amigo; mpl=amigos; pl=amigas
amiga {f} :: feminine noun of "amigo", friend
"""

    words = wordlist.Wordlist(data.splitlines())

    assert words.has_lemma("test", "noun") == False
    assert words.has_lemma("amigo", "noun") == True
    assert words.has_lemma("amiga", "noun") == False


def test_redirection():
    data="""\
test1 {m} :: test
test2 {m} :: alternate form of "test1"
test3 {m} :: alternate form of "test2"
test4 {m} :: misspelling of "test3"
test5 {m} :: alternate form of "test6"
test6 {m} :: alternate form of "test5"
test7 {m} :: alternate form of "test-none"
"""

    wlist = wordlist.Wordlist(data.splitlines())

    assert wlist.has_lemma("test1", "noun") == True
    assert wlist.has_lemma("test2", "noun") == False

    test1 = wlist.all_words["test1"]["noun"][0]
    test2 = wlist.all_words["test2"]["noun"][0]
    test3 = wlist.all_words["test3"]["noun"][0]
    test4 = wlist.all_words["test4"]["noun"][0]
    test5 = wlist.all_words["test5"]["noun"][0]
    test6 = wlist.all_words["test6"]["noun"][0]
    test7 = wlist.all_words["test7"]["noun"][0]

    assert test1.word == "test1"
    assert test1.pos == "m"
    assert test1.common_pos == "noun"

    assert wlist.get_lemmas(test1) == {'test1': ['m']}
    assert wlist.get_lemmas(test2) == {'test1': ['alt']}
    assert wlist.get_lemmas(test3) == {'test1': ['alt']}
    assert wlist.get_lemmas(test4) == {'test1': ['alt']}
    assert wlist.get_lemmas(test5) == {}
    assert wlist.get_lemmas(test6) == {}
    assert wlist.get_lemmas(test7) == {}


def test_forms_redirection():

    data = """\
test1 {m} :: test
test2 {m} :: alternate form of "test1"
test3 {m} :: alternate form of "test2"
test4 {m} :: alternate form of "test3"
"""
    wlist = wordlist.Wordlist(data.splitlines())

    assert wlist.all_forms == {
        'test1': ['noun:test1:m'],
        'test2': ['noun:test1:alt'],
        'test3': ['noun:test1:alt'],
        'test4': ['noun:test1:alt']
        }

def test_forms_complex():
    # protectora should be a form of protector even though it has a secondary
    # declaration as a lemma

    data = """\
protector {noun-forms} :: f=protectora; fpl=protectoras; pl=protectores
protector {m} :: protector (someone who protects or guards)
protector {noun-forms} :: pl=protectores
protector {m} :: protector (a device or mechanism which is designed to protect)
protectora {noun-forms} :: m=protector; mpl=protectores; pl=protectoras
protectora {f} :: feminine noun of "protector"
protectora {noun-forms} :: pl=protectoras
protectora {f} | protectora de animales :: animal shelter (an organization that provides temporary homes for stray pet animals)
protectriz {noun-forms} :: m=protector; mpl=protectores; pl=protectrices
protectriz {f} [uncommon] :: alternative form of "protectora"
"""
    wlist = wordlist.Wordlist(data.splitlines())

    assert wlist.has_lemma("protector", "noun") == True
    assert wlist.has_lemma("protectora", "noun") == False
    assert wlist.has_lemma("protectriz", "noun") == False

    protector = wlist.get_words("protector", "noun")[0]
    protectora = wlist.get_words("protectora", "noun")[0]
    protectriz = wlist.get_words("protectriz", "noun")[0]

    assert protector.is_lemma == True
    assert protectora.is_lemma == False
    assert protectriz.is_lemma == False

    assert wlist.get_lemmas(protector) == {'protector': ['m']}
    assert wlist.get_lemmas(protectora) == {'protector': ['f']}
    assert wlist.get_lemmas(protectriz) == {'protector': ['f']}

    print(wlist.all_forms)
    assert wlist.all_forms == {
        'protector': ['noun:protector:m'],
        'protectora': ['noun:protector:f', 'noun:protectora:f'],
        'protectoras': ['noun:protector:fpl', 'noun:protectora:pl'],
        'protectores': ['noun:protector:pl'],
        'protectriz': ['noun:protector:f'],
        'protectrices': ['noun:protector:fpl']
        }


def test_secondary_lemma_unique_forms():
    # Renfe should be alt of RENFE, but
    # Renfes should be a form of Renfe (since it cannot be an alt of RENFE)

    data = """\
RENFE {prop} :: A state owned company that runs the Spanish railway network
Renfe {m} :: alternative form of "RENFE"
Renfe {noun-forms} :: pl=Renfes
Renfe {m} [Spain] :: train station
"""
    wlist = wordlist.Wordlist(data.splitlines())

    assert wlist.has_lemma("RENFE", "noun") == True
    assert wlist.has_lemma("Renfe", "noun") == False

    RENFE = wlist.get_words("RENFE", "noun")[0]
    Renfe1 = wlist.get_words("Renfe", "noun")[0]
    Renfe2 = wlist.get_words("Renfe", "noun")[1]

    assert RENFE.is_lemma == True
    assert Renfe1.is_lemma == False
    assert Renfe2.is_lemma == True

    assert wlist.get_lemmas(RENFE) == {'RENFE': ['prop']}
    assert wlist.get_lemmas(Renfe1) == {'RENFE': ['alt']}
    assert wlist.get_lemmas(Renfe2) == {'Renfe': ['m']}

    assert wlist.all_forms == {
        'RENFE': ['noun:RENFE:prop'],
        'Renfe': ['noun:RENFE:alt', 'noun:Renfe:m'],
        'Renfes': ['noun:Renfe:pl']
        }


def test_secondary_lemma_no_unique_forms():
    # Renfe and Renfes should be alts of RENFE

    data = """\
RENFE {prop} :: A state owned company that runs the Spanish railway network
Renfe {noun-forms} :: pl=Renfes
Renfe {m} :: alternative form of "RENFE"
Renfe {noun-forms} :: pl=Renfes
Renfe {m} [Spain] :: train station
"""
    wlist = wordlist.Wordlist(data.splitlines())

    assert wlist.has_lemma("RENFE", "noun") == True
    assert wlist.has_lemma("Renfe", "noun") == False

    RENFE = wlist.get_words("RENFE", "noun")[0]
    Renfe1 = wlist.get_words("Renfe", "noun")[0]
    Renfe2 = wlist.get_words("Renfe", "noun")[1]

    assert RENFE.is_lemma == True
    assert Renfe1.is_lemma == False
    assert Renfe2.is_lemma == True

    assert wlist.get_lemmas(RENFE) == {'RENFE': ['prop']}
    assert wlist.get_lemmas(Renfe1) == {'RENFE': ['alt']}
    assert wlist.get_lemmas(Renfe2) == {'Renfe': ['m']}

    assert wlist.all_forms == {
        'RENFE': ['noun:RENFE:prop'],
        'Renfe': ['noun:RENFE:alt', 'noun:Renfe:m'],
        'Renfes': ['noun:RENFE:pl', 'noun:Renfe:pl']
        }

def test_asco_forms():

    data = """\
asca {noun-forms} :: pl=ascas
asca {m} [mycology] | teca :: ascus
asco {noun-forms} :: pl=ascos
asco {m} :: disgust
asco {m} :: nausea
asco {noun-forms} :: pl=ascos
asco {m} :: alternative form of "asca"
"""
    wlist = wordlist.Wordlist(data.splitlines())

    print(wlist.all_forms)

    assert wlist.all_forms == {
        'asca': ['noun:asca:m'],
        'ascas': ['noun:asca:pl'],
        'asco': ['noun:asco:m', 'noun:asca:alt'],
        'ascos': ['noun:asco:pl', 'noun:asca:pl']
    }


def test_multiple_words():

    data = """\
testo {noun-forms} :: pl=testos
testo {m} :: test
testo {noun-forms} :: pl=testoz
testo {m} :: test2
testa {noun-forms} :: pl=testas
testa {f} :: feminine noun of "testo"
"""
    wlist = wordlist.Wordlist(data.splitlines())

    assert len(wlist.all_words) == 2
    assert len(wlist.all_words["testo"]) == 1
    assert len(wlist.all_words["testo"]["noun"]) == 2

def test_diva():

    data = """\
diva {noun-forms} :: m=divo; mpl=divos; pl=divas
diva {f} :: diva
divo {adj-forms} :: f=diva; fpl=divas; pl=divos
divo {adj} :: star (famous)
divo {noun-forms} :: f=diva; fpl=divas; pl=divos
divo {m} :: star, celeb\
"""
    wlist = wordlist.Wordlist(data.splitlines())

    diva = wlist.get_words("diva", "noun")[0]
    assert diva.is_lemma == False
    assert wlist.get_lemmas(diva) == {'divo': ['f']}

def test_capitana():

    data = """\
capitana {noun-forms} :: pl=capitanas
capitana {f} :: female equivalent of "capitán"
capitán {noun-forms} :: f=capitana; fpl=capitanas; pl=capitanes
capitán {m} :: captain\
"""
    wlist = wordlist.Wordlist(data.splitlines())

    capitana = wlist.get_words("capitana", "noun")[0]
    assert capitana.is_lemma == False
    assert wlist.get_lemmas(capitana) == {'capitán': ['f']}

# Ignore "form of" if it's not in the primary sense
def test_banera():

    data = """\
bañera {noun-forms} :: pl=bañeras
bañera {f} :: bathtub
bañera {f} [nautical] :: cockpit
bañera {f} [Argentina, Chile, Uruguay] :: female equivalent of "bañero"
bañero {noun-forms} :: f=bañera; fpl=bañeras; pl=bañeros
bañero {m} [Argentina, Chile, Uruguay] :: lifeguard
"""
    wlist = wordlist.Wordlist(data.splitlines())

    capitana = wlist.get_words("bañera", "noun")[0]
    assert capitana.is_lemma == True
