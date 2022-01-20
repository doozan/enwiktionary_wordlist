from ..word import Word

def test_word():
    word = Word("test", [ ("pos", "n"), ("g","m") ])
    assert word.pos == "n"
    assert word.genders == "m"

    word.add_sense([("gloss","a test word"),("q","rare")])
    assert len(word.senses) == 1
    assert word.forms == {}
    assert word.form_of == {}

    # Adding form of in a secondary def should have no effect
    word.add_sense([("gloss", 'alternative form of "testz"')])
    assert len(word.senses) == 2
    assert word.forms == {}
    assert word.form_of == {}

    # But form of in the first def does
    word = Word("test", [("pos", "n")])
    assert word.pos == "n"
    word.add_sense([("gloss", 'alternative form of "testz"')])
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

    word = Word("test", [ ("pos", "prop"), ("g","m"), ("meta", "{{head|es|proper noun|g=m|plural|Fulanos|feminine|Fulana|feminine plural|Fulanas}}") ])
    assert word.pos == "prop"
    assert word.genders == "m"
    assert word.forms == {'f': ['Fulana'], 'fpl': ['Fulanas'], 'pl': ['Fulanos']}
    assert list(word.get_formtypes("Fulanas")) == ["fpl"]
    assert list(word.get_formtypes("Fulana")) == ["f"]
    assert list(word.get_formtypes("none")) == []

    word = Word("-ito", [ ("pos", "suffix"), ("meta", "{{es-suffix|m|f=-ita}}") ])
    assert word.pos == "suffix"
    assert word.forms == {'f': ['-ita']}
