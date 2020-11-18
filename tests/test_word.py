from ..word import Word

def test_word():
    word = Word("test", "m")
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
    word = Word("test", "m")
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
