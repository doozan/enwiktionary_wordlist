import wordlist

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

    word.add_sense("m", None, "alternative form of testz", None)
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

    word.add_meta("pl=test4s; f=test2a")
    assert word.forms == { "pl": ["tests", "test2s", "test3s", "test4s"], "f": ["testa", "test2a"] }

def test_verb():
    verb = wordlist.Verb("obrir")
    verb.add_meta("pattern=-brir; stem=o")
    verb.add_meta("old=abrir")

    assert verb.paradigms == [ ("-brir", ["o"]) ]
    assert verb.forms == { "old": ["abrir"] }

def test_wordlist():
    data="""\
amigo {meta-noun} :: f=amiga; fpl=amigas; pl=amigos
amigo {m} :: friend
amiga {meta-noun} :: m=amigo; mpl=amigos; pl=amigas
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

    test1 = wlist.all_words["test1"][0]
    test2 = wlist.all_words["test2"][0]
    test3 = wlist.all_words["test3"][0]
    test4 = wlist.all_words["test4"][0]
    test5 = wlist.all_words["test5"][0]
    test6 = wlist.all_words["test6"][0]
    test7 = wlist.all_words["test7"][0]

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
'test1': {'noun': {'m': ['test1']}},
'test2': {'noun': {'alt': ['test1']}},
'test3': {'noun': {'alt': ['test1']}},
'test4': {'noun': {'alt': ['test1']}}
}

    assert wlist.all_lemmas ==  {
'test1': {'noun': {'alt': ['test2', 'test3', 'test4'], 'm': ['test1']}}
}
