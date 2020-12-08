from ..wordlist import Wordlist

def test_simple():
    data="""\
_____
amiga
pos: noun
  meta: {{es-noun|f|m=amigo}}
  forms: m=amigo; mpl=amigos; pl=amigas
  form: f
  gloss: female equivalent of "amigo", friend
_____
amigo
pos: noun
  meta: {{es-noun|m|f=amiga}}
  forms: f=amiga; fpl=amigas; pl=amigos
  form: m
  gloss: friend
"""

    wordlist = Wordlist(data.splitlines())
    assert len(wordlist.all_entries) == 2

    assert wordlist.has_lemma("test", "noun") == False
    assert wordlist.has_lemma("amigo", "noun") == True
    assert wordlist.has_lemma("amiga", "noun") == False

def test_mbformat():
    data="""\
amiga {noun-meta} :: {{es-noun|f}}
amiga {noun-forms} :: m=amigo; mpl=amigos; pl=amigas
amiga {f} :: female equivalent of "amigo", friend
amigo {noun-meta} :: {{es-noun|m}}
amigo {noun-forms} :: f=amiga; fpl=amigas; pl=amigos
amigo {f} :: friend
"""

    wordlist = Wordlist(data.splitlines(), mbformat=True)
    assert len(wordlist.all_entries) == 2

    assert wordlist.has_lemma("test", "noun") == False
    assert wordlist.has_lemma("amigo", "noun") == True
    assert wordlist.has_lemma("amiga", "noun") == False


def test_cache():
    data="""\
_____
amiga
pos: noun
  meta: {{es-noun|f|m=amigo}}
  forms: m=amigo; mpl=amigos; pl=amigas
  form: f
  gloss: female equivalent of "amigo", friend
_____
amigo
pos: noun
  meta: {{es-noun|m|f=amiga}}
  forms: f=amiga; fpl=amigas; pl=amigos
  form: m
  gloss: friend
"""

    words = Wordlist(data.splitlines())

    assert len(words._cached) == 0

    assert words.has_lemma("test", "noun") == False
    assert len(words._cached) == 0

    assert words.has_lemma("amigo", "noun") == True
    assert len(words._cached) == 1

    assert words.has_lemma("amiga", "noun") == False
    assert len(words._cached) == 2


def test_nocache():
    data="""\
_____
amiga
pos: noun
  meta: {{es-noun|f|m=amigo}}
  forms: m=amigo; mpl=amigos; pl=amigas
  form: f
  gloss: female equivalent of "amigo", friend
_____
amigo
pos: noun
  meta: {{es-noun|m|f=amiga}}
  forms: f=amiga; fpl=amigas; pl=amigos
  form: m
  gloss: friend
"""

    words = Wordlist(data.splitlines(), cache_words=False)

    assert len(words._cached) == 0

    assert words.has_lemma("test", "noun") == False
    assert len(words._cached) == 0

    assert words.has_lemma("amigo", "noun") == True
    assert len(words._cached) == 0

    assert words.has_lemma("amiga", "noun") == False
    assert len(words._cached) == 0


def test_redirection():
    data="""\
_____
test1
pos: noun
  form: m
  gloss: test
_____
test2
pos: noun
  gloss: alternate form of "test1"
_____
test3
pos: noun
  gloss: alternate form of "test2"
_____
test4
pos: noun
  gloss: misspelling of "test3"
_____
test5
pos: noun
  gloss: alternative form of "test6"
_____
test6
pos: noun
  gloss: alternative form of "test5"
_____
test7
pos: noun
  gloss: alternative form of "test-none"
"""

    wlist = Wordlist(data.splitlines())

    assert wlist.has_lemma("test1", "noun") == True
    assert wlist.has_lemma("test2", "noun") == False

    test1 = next(wlist.get_words("test1", "noun"))
    test2 = next(wlist.get_words("test2", "noun"))
    test3 = next(wlist.get_words("test3", "noun"))
    test4 = next(wlist.get_words("test4", "noun"))
    test5 = next(wlist.get_words("test5", "noun"))
    test6 = next(wlist.get_words("test6", "noun"))
    test7 = next(wlist.get_words("test7", "noun"))

    assert test1.word == "test1"
    assert test1.common_pos == "noun"
    assert test1.pos == "m"

    assert wlist.get_lemmas(test1) == {'test1': ['m']}
    assert wlist.get_lemmas(test2) == {'test1': ['alt']}
    assert wlist.get_lemmas(test3) == {'test1': ['alt']}
    assert wlist.get_lemmas(test4) == {'test1': ['alt']}
    assert wlist.get_lemmas(test5) == {}
    assert wlist.get_lemmas(test6) == {}
    assert wlist.get_lemmas(test7) == {}

def test_forms_complex():
    # protectora should be a form of protector even though it has a secondary
    # declaration as a lemma

    wordlist_data = """\
_____
protector
pos: noun
  meta: {{es-noun|m|protectores|f=protectora|f2=protectriz}}
  forms: f=protectora; f=protectriz; fpl=protectoras; fpl=protectrices; pl=protectores
  form: m
  gloss: protector (someone who protects or guards)
pos: noun
  meta: {{es-noun|m}}
  forms: pl=protectores
  g: m
  gloss: protector (a device or mechanism which is designed to protect)
_____
protectora
pos: noun
  meta: {{es-noun|f|m=protector}}
  forms: m=protector; mpl=protectores; pl=protectoras
  form: f
  gloss: female equivalent of "protector"
pos: noun
  meta: {{es-noun|f}}
  forms: pl=protectoras
  form: f
  gloss: animal shelter (an organization that provides temporary homes for stray pet animals)
    syn: protectora de animales
_____
protectoras
pos: noun
  meta: {{head|es|noun plural form|g=f-p}}
  form: f-p
  gloss: inflection of "protector"
_____
protectores
pos: noun
  meta: {{head|es|noun plural form|g=m-p}}
  form: m-p
  gloss: inflection of "protector"
_____
protectrices
pos: noun
  meta: {{head|es|noun plural form|g=f-p}}
  form: f-p
  gloss: inflection of "protector"
_____
protectriz
pos: noun
  meta: {{es-noun|f|m=protector}}
  forms: m=protector; mpl=protectores; pl=protectrices
  form: f
  gloss: alternative form of "protectora"
    q: uncommon
"""
    wlist = Wordlist(wordlist_data.splitlines())

    assert wlist.has_lemma("protector", "noun") == True
    assert wlist.has_lemma("protectora", "noun") == False
    assert wlist.has_lemma("protectriz", "noun") == False

    protector = next(wlist.get_words("protector", "noun"))
    protectora = next(wlist.get_words("protectora", "noun"))
    protectriz = next(wlist.get_words("protectriz", "noun"))

    assert protector.is_lemma == True
    assert protectora.is_lemma == False
    assert protectriz.is_lemma == False

    assert wlist.get_lemmas(protector) == {'protector': ['m']}
    assert wlist.get_lemmas(protectora) == {'protector': ['f']}
    assert wlist.get_lemmas(protectriz) == {'protector': ['f']}

def test_diva():

    data = """\
diva {noun-meta} :: x
diva {noun-forms} :: m=divo; mpl=divos; pl=divas
diva {f} :: diva
divo {adj-meta} :: x
divo {adj-forms} :: f=diva; fpl=divas; pl=divos
divo {adj} :: star (famous)
divo {noun-meta} :: x
divo {noun-forms} :: f=diva; fpl=divas; pl=divos
divo {m} :: star, celeb\
"""
    wlist = Wordlist(data.splitlines(), mbformat=True)

    diva = next(wlist.get_words("diva", "noun"))
    assert diva.is_lemma == False
    assert wlist.get_lemmas(diva) == {'divo': ['f']}

def test_capitana():

    data = """\
capitana {noun-meta} :: x
capitana {noun-forms} :: pl=capitanas
capitana {f} :: female equivalent of "capitán"
capitán {noun-meta} :: x
capitán {noun-forms} :: f=capitana; fpl=capitanas; pl=capitanes
capitán {m} :: captain\
"""
    wlist = Wordlist(data.splitlines(), mbformat=True)

    capitana = next(wlist.get_words("capitana", "noun"))
    assert capitana.is_lemma == False
    assert wlist.get_lemmas(capitana) == {'capitán': ['f']}

# Ignore "form of" if it's not in the primary sense
def test_banera():

    data = """\
bañera {noun-meta} :: x
bañera {noun-forms} :: pl=bañeras
bañera {f} :: bathtub
bañera {f} [nautical] :: cockpit
bañera {f} [Argentina, Chile, Uruguay] :: female equivalent of "bañero"
bañero {noun-meta} :: x
bañero {noun-forms} :: f=bañera; fpl=bañeras; pl=bañeros
bañero {m} [Argentina, Chile, Uruguay] :: lifeguard
"""
    wlist = Wordlist(data.splitlines(), mbformat=True)

    capitana = next(wlist.get_words("bañera", "noun"))
    assert capitana.is_lemma == True



def test_dios():

    data = """\
dios {noun-meta} :: {{es-noun|m|dioses|f=diosa}}
dios {noun-forms} :: f=diosa; fpl=diosas; pl=dioses
dios {m} :: god
diosa {noun-meta} :: {{es-noun|f|m=dios}}
diosa {noun-forms} :: m=dios; mpl=dios; pl=diosas
diosa {f} :: goddess
diosa {noun-meta} :: {{es-noun|f}}
diosa {noun-forms} :: pl=diosas
diosa {f} [biochemistry] :: diose
"""
    wlist = Wordlist(data.splitlines(), mbformat=True)

    dios =  next(wlist.get_words("dios", "noun"))
    assert dios.is_lemma == True
    assert dios.forms == {'f': ['diosa'], 'fpl': ['diosas'], 'pl': ['dioses']}

    diosa =  next(wlist.get_words("diosa", "noun"))
    assert diosa.is_lemma == False

def test_aquellos():

    data = """\
aquél {pron-meta} :: {{head|es|pronoun|demonstrative, feminine|aquélla|neuter|aquello|masculine plural|aquéllos|feminine plural|aquéllas|g=m}}
aquél {pron-forms} :: demonstrative_feminine=aquélla; feminine_plural=aquéllas; masculine_plural=aquéllos; neuter=aquello
aquél {pron} [demonstrative] :: that one (far from speaker and listener)
aquéllos {pron-meta} :: {{head|es|pronoun|demonstrative|g=m-p}}
aquéllos {pron} :: plural of "aquél"; those ones (far from speaker and listener)
aquel {pron-meta} :: {{head|es|pronoun|g=m|feminine|aquella|neutrum|aquello|masculine plural|aquellos|neutrum plural|aquellos|feminine plural|aquellas}}
aquel {pron-forms} :: feminine=aquella; feminine_plural=aquellas; masculine_plural=aquellos; neutrum=aquello; neutrum_plural=aquellos
aquel {pron} [demonstrative] :: alternative spelling of "aquél"
aquellos {pron-meta} :: {{head|es|pronoun|demonstrative|g=m-p}}
aquellos {pron} :: alternative spelling of "aquéllos"; those ones (over there; implying some distance). The unaccented form can function as a pronoun if it can be unambiguously deduced as such from context.
aquellos {pron-meta} :: {{head|es|pronoun|g=n-p}}
aquellos {pron} :: Those ones. (over there; implying some distance)
"""

    wlist = Wordlist(data.splitlines(), mbformat=True)

    word =  next(wlist.get_words("aquellos", "pron"))
    assert word.is_lemma == False
    assert word.form_of == {'aquéllos': ['alt']}
    assert word.forms == {}
    assert wlist.get_lemmas(word) == {'aquél': ['pl']}


