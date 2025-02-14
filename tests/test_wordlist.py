from enwiktionary_wordlist.wordlist import Wordlist

def test_simple():
    data="""\
_____
amiga
pos: n
  meta: {{es-noun|f|m=amigo}}
  g: f
  gloss: female equivalent of "amigo", friend
  gloss: friend
_____
amigo
pos: n
  meta: {{es-noun|m|f=amiga}}
  g: m
  gloss: friend
"""

    wordlist = Wordlist(data.splitlines())
    assert len(wordlist.all_entries) == 2

    assert wordlist.has_word("test", "n") == False
    assert wordlist.has_word("amigo", "n") == True
    assert wordlist.has_word("amiga", "n") == True

def test_mbformat():
    data="""\
amiga {n-meta} :: {{es-noun|f}}
amiga {f} :: female equivalent of "amigo", friend
amiga {f} :: friend2
amigo {n-meta} :: {{es-noun|m}}
amigo {m} :: friend
amigo {m} :: friend2
"""

    wordlist = Wordlist(data.splitlines())

    assert wordlist.all_entries == {
'amiga': [
    'pos: n',
    'meta: {{es-noun|f}}',
    'g: f',
    'gloss: female equivalent of "amigo", friend',
    'gloss: friend2'],
'amigo': [
    'pos: n',
    'meta: {{es-noun|m}}',
    'g: m',
    'gloss: friend',
    'gloss: friend2']}

    assert wordlist.has_word("test", "n") == False
    assert wordlist.has_word("amigo", "n") == True
    assert wordlist.has_word("amiga", "n") == True


    data = """\
test {n-meta} :: x
test {m} :: masculine
test {n-meta} :: x
test {f} :: feminine
"""
    wordlist = Wordlist(data.splitlines())
    print(wordlist.all_entries)
    assert wordlist.all_entries == {
'test': [
    'pos: n',
    'meta: x',
    'g: m',
    'gloss: masculine',
    'pos: n',
    'meta: x',
    'g: f',
    'gloss: feminine']
}

def test_cache():
    data="""\
_____
amiga
pos: n
  meta: {{es-noun|f|m=amigo}}
  g: f
  gloss: female equivalent of "amigo", friend
_____
amigo
pos: n
  meta: {{es-noun|m|f=amiga}}
  g: m
  gloss: friend
"""

    words = Wordlist(data.splitlines())

    assert len(words._cached) == 0

    assert words.has_word("test", "n") == False
    assert len(words._cached) == 0

    assert words.has_word("amigo", "n") == True
    assert len(words._cached) == 1

    assert words.has_word("amiga", "n") == True
    assert len(words._cached) == 2


def test_nocache():
    data="""\
_____
amiga
pos: n
  meta: {{es-noun|f|m=amigo}}
  g: f
  gloss: female equivalent of "amigo", friend
_____
amigo
pos: n
  meta: {{es-noun|m|f=amiga}}
  g: m
  gloss: friend
"""

    words = Wordlist(data.splitlines(), cache_words=False)

    assert len(words._cached) == 0

    assert words.has_word("test", "n") == False
    assert len(words._cached) == 0

    assert words.has_word("amigo", "n") == True
    assert len(words._cached) == 0

    assert words.has_word("amiga", "n") == True
    assert len(words._cached) == 0


def test_dios():

    data = """\
dios {n-meta} :: {{es-noun|m|dioses|f=diosa}}
dios {m} :: god
diosa {n-meta} :: {{es-noun|f|m=dios}}
diosa {f} :: goddess
diosa {n-meta} :: {{es-noun|f}}
diosa {f} [biochemistry] :: diose
"""
    wlist = Wordlist(data.splitlines())

    dios =  next(wlist.get_iwords("dios", "n"))
    assert dios.forms == {'f': ['diosa'], 'fpl': ['diosas'], 'pl': ['dioses']}

    assert list(wlist.get_formtypes("dios", "n", "diosa")) == ["f"]
    diosa =  next(wlist.get_iwords("diosa", "n"))
    assert diosa.forms == {'m': ['dios'], 'mpl': ['dioses'], 'pl': ['diosas']}
    assert diosa.form_of == {}

def test_aquellos():

    data = """\
aquél {pron-meta} :: {{head|es|pronoun|demonstrative, feminine|aquélla|neuter|aquello|masculine plural|aquéllos|feminine plural|aquéllas|g=m}}
aquél {pron} [demonstrative] :: that one (far from speaker and listener)
aquéllos {pron-meta} :: {{head|es|pronoun|demonstrative|g=m-p}}
aquéllos {pron} :: plural of "aquél"; those ones (far from speaker and listener)
aquel {pron-meta} :: {{head|es|pronoun|g=m|feminine|aquella|neutrum|aquello|masculine plural|aquellos|neutrum plural|aquellos|feminine plural|aquellas}}
aquel {pron} [demonstrative] :: alternative spelling of "aquél"
aquellos {pron-meta} :: {{head|es|pronoun|demonstrative|g=m-p}}
aquellos {pron} :: alternative spelling of "aquéllos"; those ones (over there; implying some distance). The unaccented form can function as a pronoun if it can be unambiguously deduced as such from context.
aquellos {pron-meta} :: {{head|es|pronoun|g=n-p}}
aquellos {pron} :: Those ones. (over there; implying some distance)
"""

    wlist = Wordlist(data.splitlines())

    word =  next(wlist.get_iwords("aquel", "pron"))
    assert word.forms == {'f': ['aquella'], 'fpl': ['aquellas'], 'mpl': ['aquellos'], 'neutrum': ['aquello'], 'neutrum_plural': ['aquellos']}

    word =  next(wlist.get_iwords("aquellos", "pron"))
#    for sense in word.senses:
#        print(sense.gloss)
    assert word.form_of == {'aquéllos': ['alt']}
    assert word.forms == {}
