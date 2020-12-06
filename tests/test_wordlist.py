from ..wordlist import Wordlist

def test_wordlist():
    data="""\
amigo {noun-meta} :: x
amigo {noun-forms} :: f=amiga; fpl=amigas; pl=amigos
amigo {m} :: friend
amiga {noun-meta} :: x
amiga {noun-forms} :: m=amigo; mpl=amigos; pl=amigas
amiga {f} :: feminine noun of "amigo", friend
"""

    words = Wordlist(data.splitlines())

    assert words.has_lemma("test", "noun") == False
    assert words.has_lemma("amigo", "noun") == True
    assert words.has_lemma("amiga", "noun") == False


def test_redirection():
    data="""\
test1 {noun-meta} :: x
test1 {m} :: test
test2 {noun-meta} :: x
test2 {m} :: alternate form of "test1"
test3 {noun-meta} :: x
test3 {m} :: alternate form of "test2"
test4 {noun-meta} :: x
test4 {m} :: misspelling of "test3"
test5 {noun-meta} :: x
test5 {m} :: alternate form of "test6"
test6 {noun-meta} :: x
test6 {m} :: alternate form of "test5"
test7 {noun-meta} :: x
test7 {m} :: alternate form of "test-none"
"""

    wlist = Wordlist(data.splitlines())

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


def test_forms_complex():
    # protectora should be a form of protector even though it has a secondary
    # declaration as a lemma

    data = """\
protector {noun-meta} :: x
protector {noun-forms} :: f=protectora; fpl=protectoras; pl=protectores
protector {m} :: protector (someone who protects or guards)
protector {noun-meta} :: x
protector {noun-forms} :: pl=protectores
protector {m} :: protector (a device or mechanism which is designed to protect)
protectora {noun-meta} :: x
protectora {noun-forms} :: m=protector; mpl=protectores; pl=protectoras
protectora {f} :: feminine noun of "protector"
protectora {noun-meta} :: x
protectora {noun-forms} :: pl=protectoras
protectora {f} | protectora de animales :: animal shelter (an organization that provides temporary homes for stray pet animals)
protectriz {noun-meta} :: x
protectriz {noun-forms} :: m=protector; mpl=protectores; pl=protectrices
protectriz {f} [uncommon] :: alternative form of "protectora"
"""
    wlist = Wordlist(data.splitlines())

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

def test_multiple_words():

    data = """\
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
    wlist = Wordlist(data.splitlines())

    assert len(wlist.all_words) == 2
    assert len(wlist.all_words["testo"]) == 1
    assert len(wlist.all_words["testo"]["noun"]) == 2

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
    wlist = Wordlist(data.splitlines())

    diva = wlist.get_words("diva", "noun")[0]
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
    wlist = Wordlist(data.splitlines())

    capitana = wlist.get_words("capitana", "noun")[0]
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
    wlist = Wordlist(data.splitlines())

    capitana = wlist.get_words("bañera", "noun")[0]
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
    wlist = Wordlist(data.splitlines())

    dios =  wlist.get_words("dios", "noun")[0]
    assert dios.is_lemma == True
    assert dios.forms == {'f': ['diosa'], 'fpl': ['diosas'], 'pl': ['dioses']}

    diosa =  wlist.get_words("diosa", "noun")[0]
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
    wlist = Wordlist(data.splitlines())

    word =  wlist.get_words("aquellos", "pron")[0]
    assert word.is_lemma == False
    assert word.form_of == {'aquéllos': ['alt']}
    assert word.forms == {}
    assert wlist.get_lemmas(word) == {'aquél': ['pl']}
