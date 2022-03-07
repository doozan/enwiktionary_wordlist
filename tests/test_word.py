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


    assert word.has_form("tests") == False

    word.add_form("pl", "tests")
    assert word.forms == { "pl": ["tests"] }

    assert word.has_form("tests") == True
    assert word.has_form("tests", "xx") == False
    assert word.has_form("tests", "pl") == True

    word.add_form("pl", "test2s")
    assert word.forms == { "pl": ["tests", "test2s"] }

    # dup should not do anything
    word.add_form("pl", "tests")
    assert word.forms == { "pl": ["tests", "test2s"] }

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


    word = Word("protectriz", [ ("pos", "n"), ("meta", "{{es-noun|f|m=protector}}") ])
    word.add_sense([("gloss",'alternative form of "protectora"'),("q","uncommon")])
    assert word.forms == {'m': ['protector'], 'mpl': ['protectores'], 'pl': ['protectrices']}
    assert word.form_of == {'protectora': ['alt']}


    word = Word("aquellos", [ ("pos", "m-p"), ("meta", "{{head|es|pronoun|demonstrative|g=m-p}}") ])
    word.add_sense([("gloss",'alternative spelling of "aquéllos"')])
    assert word.form_of == {'aquéllos': ['alt']}

    # Assure form_of parses senses
    word = Word("aquellos", [
        ("pos", "m-p"),
        ("meta", "{{head|es|pronoun|demonstrative|g=m-p}}"),
        ("gloss",'alternative spelling of "aquéllos"'),
        ])
    assert word.form_of == {'aquéllos': ['alt']}

    word = Word("asco", [
        ('pos', 'n'),
        ('meta', '{{es-noun|m}}'),
        ('g', 'm'),
        ('gloss', 'alternative form of "asca"'),
        ])
    assert len(word.senses) == 1
