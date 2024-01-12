from enwiktionary_wordlist.wordlist import Wordlist
from enwiktionary_wordlist.all_forms import AllForms

import enwiktionary_templates
cachedb = enwiktionary_templates.cache.get_default_cachedb()

def test_mf_noun():

    # generate implied feminine lemmas

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
'protectora': ['n|protector', 'n|protectora'],
'protectoras': ['n|protector', 'n|protectora'],
'protectores': ['n|protector'],
'protectriz': ['n|protector', 'n|protectriz'],
'protectrices': ['n|protector', 'n|protectriz'],
}

    wordlist = Wordlist(wordlist_data.splitlines(), template_cachedb=cachedb)
    allforms = AllForms.from_wordlist(wordlist)
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
'protectriz': ['n|protector', 'n|protectriz'],
'protectrices': ['n|protector', 'n|protectriz'],
'protectora_altpl': ['n|protectora'],
'protectora_altpl2': ['n|protectora'],
}

    wordlist = Wordlist(wordlist_data.splitlines(), template_cachedb=cachedb)
    allforms = AllForms.from_wordlist(wordlist)
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

    wordlist = Wordlist(wordlist_data.splitlines(), template_cachedb=cachedb)
    allforms = AllForms.from_wordlist(wordlist)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v
    allforms = AllForms.from_wordlist(wordlist)
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
'protectora': ['n|protector', 'n|protectora'],
'protectoras': ['n|protector', 'n|protectora'],
'protectores': ['n|protector'],
'protectriz': ['n|protector', 'n|protectriz'],
'protectrices': ['n|protector', 'n|protectriz'],
'alt_protectora': ['n|alt_protectora'],
'alt_protectora_pl': ['n|alt_protectora'],
}

    wordlist = Wordlist(wordlist_data.splitlines(), template_cachedb=cachedb)
    allforms = AllForms.from_wordlist(wordlist)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v
    allforms = AllForms.from_wordlist(wordlist)
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

    wordlist = Wordlist(wordlist_data.splitlines(), template_cachedb=cachedb)

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

    wordlist = Wordlist(wordlist_data.splitlines(), template_cachedb=cachedb)
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

    wordlist = Wordlist(wordlist_data.splitlines(), template_cachedb=cachedb)
    allforms = AllForms.from_wordlist(wordlist)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v
    allforms = AllForms.from_wordlist(wordlist)
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

    wordlist = Wordlist(wordlist_data.splitlines(), template_cachedb=cachedb)
    allforms = AllForms.from_wordlist(wordlist)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v

    # this should be different
    allforms = AllForms.from_wordlist(wordlist)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v


def test_asco_forms():

    wordlist_data = """\
_____
asca
pos: n
  meta: {{es-noun|m}}
  g: m
  gloss: ascus
    q: mycology
    syn: teca
_____
asco
pos: n
  meta: {{es-noun|m}}
  g: m
  gloss: disgust
  gloss: nausea
  gloss: disgusting person
pos: n
  meta: {{es-noun|m}}
  g: m
  gloss: alternative form of "asca"
"""

    expected = {
'asca': ['n|asca'],
'ascas': ['n|asca'],
'asco': ['n|asco'],
'ascos': ['n|asco']
}

    wordlist = Wordlist(wordlist_data.splitlines(), template_cachedb=cachedb)
    allforms = AllForms.from_wordlist(wordlist)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v
    allforms = AllForms.from_wordlist(wordlist)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v


def test_afecto():
    wordlist_data = """\
_____
afecto
pos: adj
  meta: {{es-adj|f=afecta}}
  gloss: test
"""
    expected = {
'afecta': ['adj|afecto'],
'afectas': ['adj|afecto'],
'afectos': ['adj|afecto'],
'afecto': ['adj|afecto']}

    wordlist = Wordlist(wordlist_data.splitlines(), template_cachedb=cachedb)
    allforms = AllForms.from_wordlist(wordlist)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v
    allforms = AllForms.from_wordlist(wordlist)
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
    wordlist = Wordlist(wordlist_data.splitlines(), template_cachedb=cachedb)
    allforms = AllForms.from_wordlist(wordlist)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v
    allforms = AllForms.from_wordlist(wordlist)
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
    wordlist = Wordlist(wordlist_data.splitlines(), template_cachedb=cachedb)
    allforms = AllForms.from_wordlist(wordlist)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v
    allforms = AllForms.from_wordlist(wordlist)
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
    wordlist = Wordlist(wordlist_data.splitlines(), template_cachedb=cachedb)
    allforms = AllForms.from_wordlist(wordlist)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v
    allforms = AllForms.from_wordlist(wordlist)
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
    assert allforms.get_lemmas('test', 'adj') == ['adj|a1', 'adj|a2', 'adj|a3']
    assert allforms.get_lemmas('test', ['adj']) == ['adj|a1', 'adj|a2', 'adj|a3']
    assert allforms.get_lemmas('test', ['adj','noun']) == ['adj|a1', 'adj|a2', 'adj|a3', 'noun|n1', 'noun|n2', 'noun|n3']
    assert allforms.get_lemmas('test1,test2') == ['noun|test1', 'noun|test2', 'noun|test3']

    assert list(allforms.all_lemmas) == ['a1', 'a2', 'a3', 'n1', 'n2', 'n3', 'test1', 'test2', 'test3']

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

    wordlist = Wordlist(wordlist_data.splitlines(), template_cachedb=cachedb)
    allforms = AllForms.from_wordlist(wordlist)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v
    allforms = AllForms.from_wordlist(wordlist)
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

    wordlist = Wordlist(wordlist_data.splitlines(), template_cachedb=cachedb)
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

    wordlist = Wordlist(wordlist_data.splitlines(), template_cachedb=cachedb)
    allforms = AllForms.from_wordlist(wordlist)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v
    allforms = AllForms.from_wordlist(wordlist)
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

    wordlist = Wordlist(wordlist_data.splitlines(), template_cachedb=cachedb)
    allforms = AllForms.from_wordlist(wordlist)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v
    allforms = AllForms.from_wordlist(wordlist)
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

    wordlist = Wordlist(wordlist_data.splitlines(), template_cachedb=cachedb)
    allforms = AllForms.from_wordlist(wordlist)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v
    allforms = AllForms.from_wordlist(wordlist)
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

    wordlist = Wordlist(wordlist_data.splitlines(), template_cachedb=cachedb)
    allforms = AllForms.from_wordlist(wordlist)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v
    allforms = AllForms.from_wordlist(wordlist)
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
        'bosníaca': ['n|bosníaca', 'n|bosníaco'],
        'bosníacas': ['n|bosníaca', 'n|bosníaco'],
        'bosniaca': ['n|bosniaca', 'n|bosniaco'],
        'bosniacas': ['n|bosniaca', 'n|bosniaco'],
        'bosniaco': ['n|bosniaco'],
        'bosniacos': ['n|bosniaco'],
    }

    wordlist = Wordlist(wordlist_data.splitlines(), template_cachedb=cachedb)
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

    wordlist = Wordlist(wordlist_data.splitlines(), template_cachedb=cachedb)
    allforms = AllForms.from_wordlist(wordlist)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v

    allforms = AllForms.from_wordlist(wordlist)
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

    wordlist = Wordlist(wordlist_data.splitlines(), template_cachedb=cachedb)
    allforms = AllForms.from_wordlist(wordlist)
    for k,v in expected.items():
        print(k,v)
        assert allforms.get_lemmas(k) == v
    allforms = AllForms.from_wordlist(wordlist)
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

    wordlist = Wordlist(wordlist_data.splitlines(), template_cachedb=cachedb)
#    assert "te aborregas" in AllForms.from_wordlist(wordlist).all_forms
    assert "aborregas" in AllForms.from_wordlist(wordlist).all_forms
    assert AllForms.from_wordlist(wordlist).get_lemmas("aborregas") == ['v|aborregar', 'v|aborregarse']
    assert AllForms.from_wordlist(wordlist).get_lemmas("aborregas") == ['v|aborregar', 'v|aborregarse'] #, 'v|aborregas']


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

    wordlist = Wordlist(wordlist_data.splitlines(), template_cachedb=cachedb)
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

    wordlist = Wordlist(wordlist_data.splitlines(), template_cachedb=cachedb)
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

    wordlist = Wordlist(wordlist_data.splitlines(), template_cachedb=cachedb)
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

    wordlist = Wordlist(data.splitlines(), template_cachedb=cachedb)
    allforms = AllForms.from_wordlist(wordlist)
    print("\n".join(allforms.all_csv))

    assert allforms.is_lemma(next(wordlist.get_iwords("paises", "n"))) == False
    assert list(allforms.all_csv) == expected.splitlines()


def test_part():

    # Verbs should only generate verb forms
    # "part" identification, etc is handled elsewhere

    data="""\
_____
brincar
pos: v
  meta: {{es-verb}} {{es-conj}}
  gloss: to jump around
"""

    wordlist = Wordlist(data.splitlines(), template_cachedb=cachedb)
    allforms = AllForms.from_wordlist(wordlist)
    print("\n".join([x for x in allforms.all_csv if x.startswith("brincada,")]))

    for line in allforms.all_csv:
        assert ",part," not in line
        assert ",v," in line


def test_proscribir():

    # Verbs should only generate verb forms
    # "part" identification, etc is handled elsewhere

    data="""\
_____
proscribir
pos: v
  meta: {{es-verb}} {{es-conj}}
  gloss: to have
"""

    wordlist = Wordlist(data.splitlines(), template_cachedb=cachedb)
    allforms = AllForms.from_wordlist(wordlist)

    csv = "\n".join(allforms.all_csv)

    assert csv == """\
proscriba,v,proscribir
proscribamos,v,proscribir
proscriban,v,proscribir
proscribas,v,proscribir
proscribe,v,proscribir
proscriben,v,proscribir
proscribes,v,proscribir
proscribid,v,proscribir
proscribidla,v,proscribir
proscribidlas,v,proscribir
proscribidle,v,proscribir
proscribidles,v,proscribir
proscribidlo,v,proscribir
proscribidlos,v,proscribir
proscribidme,v,proscribir
proscribidnos,v,proscribir
proscribiendo,v,proscribir
proscribiera,v,proscribir
proscribierais,v,proscribir
proscribieran,v,proscribir
proscribieras,v,proscribir
proscribiere,v,proscribir
proscribiereis,v,proscribir
proscribieren,v,proscribir
proscribieres,v,proscribir
proscribieron,v,proscribir
proscribiese,v,proscribir
proscribieseis,v,proscribir
proscribiesen,v,proscribir
proscribieses,v,proscribir
proscribila,v,proscribir
proscribilas,v,proscribir
proscribile,v,proscribir
proscribiles,v,proscribir
proscribilo,v,proscribir
proscribilos,v,proscribir
proscribime,v,proscribir
proscribimos,v,proscribir
proscribinos,v,proscribir
proscribir,v,proscribir
proscribiremos,v,proscribir
proscribirla,v,proscribir
proscribirlas,v,proscribir
proscribirle,v,proscribir
proscribirles,v,proscribir
proscribirlo,v,proscribir
proscribirlos,v,proscribir
proscribirme,v,proscribir
proscribirnos,v,proscribir
proscribiros,v,proscribir
proscribirse,v,proscribir
proscribirte,v,proscribir
proscribirá,v,proscribir
proscribirán,v,proscribir
proscribirás,v,proscribir
proscribiré,v,proscribir
proscribiréis,v,proscribir
proscribiría,v,proscribir
proscribiríais,v,proscribir
proscribiríamos,v,proscribir
proscribirían,v,proscribir
proscribirías,v,proscribir
proscribiste,v,proscribir
proscribisteis,v,proscribir
proscribite,v,proscribir
proscribiéndola,v,proscribir
proscribiéndolas,v,proscribir
proscribiéndole,v,proscribir
proscribiéndoles,v,proscribir
proscribiéndolo,v,proscribir
proscribiéndolos,v,proscribir
proscribiéndome,v,proscribir
proscribiéndomela,v,proscribir
proscribiéndomelas,v,proscribir
proscribiéndomele,v,proscribir
proscribiéndomeles,v,proscribir
proscribiéndomelo,v,proscribir
proscribiéndomelos,v,proscribir
proscribiéndonos,v,proscribir
proscribiéndonosla,v,proscribir
proscribiéndonoslas,v,proscribir
proscribiéndonosle,v,proscribir
proscribiéndonosles,v,proscribir
proscribiéndonoslo,v,proscribir
proscribiéndonoslos,v,proscribir
proscribiéndoos,v,proscribir
proscribiéndoosla,v,proscribir
proscribiéndooslas,v,proscribir
proscribiéndoosle,v,proscribir
proscribiéndoosles,v,proscribir
proscribiéndooslo,v,proscribir
proscribiéndooslos,v,proscribir
proscribiéndose,v,proscribir
proscribiéndosela,v,proscribir
proscribiéndoselas,v,proscribir
proscribiéndosele,v,proscribir
proscribiéndoseles,v,proscribir
proscribiéndoselo,v,proscribir
proscribiéndoselos,v,proscribir
proscribiéndote,v,proscribir
proscribiéndotela,v,proscribir
proscribiéndotelas,v,proscribir
proscribiéndotele,v,proscribir
proscribiéndoteles,v,proscribir
proscribiéndotelo,v,proscribir
proscribiéndotelos,v,proscribir
proscribiéramos,v,proscribir
proscribiéremos,v,proscribir
proscribiésemos,v,proscribir
proscribió,v,proscribir
proscribo,v,proscribir
proscribáis,v,proscribir
proscribámonos,v,proscribir
proscribámonosla,v,proscribir
proscribámonoslas,v,proscribir
proscribámonosle,v,proscribir
proscribámonosles,v,proscribir
proscribámonoslo,v,proscribir
proscribámonoslos,v,proscribir
proscribámoos,v,proscribir
proscribámoosla,v,proscribir
proscribámooslas,v,proscribir
proscribámoosle,v,proscribir
proscribámoosles,v,proscribir
proscribámooslo,v,proscribir
proscribámooslos,v,proscribir
proscribámosla,v,proscribir
proscribámoslas,v,proscribir
proscribámosle,v,proscribir
proscribámosles,v,proscribir
proscribámoslo,v,proscribir
proscribámoslos,v,proscribir
proscribámoste,v,proscribir
proscribámostela,v,proscribir
proscribámostelas,v,proscribir
proscribámostele,v,proscribir
proscribámosteles,v,proscribir
proscribámostelo,v,proscribir
proscribámostelos,v,proscribir
proscribás,v,proscribir
proscribí,v,proscribir
proscribía,v,proscribir
proscribíais,v,proscribir
proscribíamos,v,proscribir
proscribían,v,proscribir
proscribías,v,proscribir
proscribídmela,v,proscribir
proscribídmelas,v,proscribir
proscribídmele,v,proscribir
proscribídmeles,v,proscribir
proscribídmelo,v,proscribir
proscribídmelos,v,proscribir
proscribídnosla,v,proscribir
proscribídnoslas,v,proscribir
proscribídnosle,v,proscribir
proscribídnosles,v,proscribir
proscribídnoslo,v,proscribir
proscribídnoslos,v,proscribir
proscribímela,v,proscribir
proscribímelas,v,proscribir
proscribímele,v,proscribir
proscribímeles,v,proscribir
proscribímelo,v,proscribir
proscribímelos,v,proscribir
proscribínosla,v,proscribir
proscribínoslas,v,proscribir
proscribínosle,v,proscribir
proscribínosles,v,proscribir
proscribínoslo,v,proscribir
proscribínoslos,v,proscribir
proscribíos,v,proscribir
proscribíosla,v,proscribir
proscribíoslas,v,proscribir
proscribíosle,v,proscribir
proscribíosles,v,proscribir
proscribíoslo,v,proscribir
proscribíoslos,v,proscribir
proscribírmela,v,proscribir
proscribírmelas,v,proscribir
proscribírmele,v,proscribir
proscribírmeles,v,proscribir
proscribírmelo,v,proscribir
proscribírmelos,v,proscribir
proscribírnosla,v,proscribir
proscribírnoslas,v,proscribir
proscribírnosle,v,proscribir
proscribírnosles,v,proscribir
proscribírnoslo,v,proscribir
proscribírnoslos,v,proscribir
proscribírosla,v,proscribir
proscribíroslas,v,proscribir
proscribírosle,v,proscribir
proscribírosles,v,proscribir
proscribíroslo,v,proscribir
proscribíroslos,v,proscribir
proscribírsela,v,proscribir
proscribírselas,v,proscribir
proscribírsele,v,proscribir
proscribírseles,v,proscribir
proscribírselo,v,proscribir
proscribírselos,v,proscribir
proscribírtela,v,proscribir
proscribírtelas,v,proscribir
proscribírtele,v,proscribir
proscribírteles,v,proscribir
proscribírtelo,v,proscribir
proscribírtelos,v,proscribir
proscribís,v,proscribir
proscribítela,v,proscribir
proscribítelas,v,proscribir
proscribítele,v,proscribir
proscribíteles,v,proscribir
proscribítelo,v,proscribir
proscribítelos,v,proscribir
proscripta,v,proscribir
proscriptas,v,proscribir
proscripto,v,proscribir
proscriptos,v,proscribir
proscrita,v,proscribir
proscritas,v,proscribir
proscrito,v,proscribir
proscritos,v,proscribir
proscríbala,v,proscribir
proscríbalas,v,proscribir
proscríbale,v,proscribir
proscríbales,v,proscribir
proscríbalo,v,proscribir
proscríbalos,v,proscribir
proscríbame,v,proscribir
proscríbamela,v,proscribir
proscríbamelas,v,proscribir
proscríbamele,v,proscribir
proscríbameles,v,proscribir
proscríbamelo,v,proscribir
proscríbamelos,v,proscribir
proscríbanla,v,proscribir
proscríbanlas,v,proscribir
proscríbanle,v,proscribir
proscríbanles,v,proscribir
proscríbanlo,v,proscribir
proscríbanlos,v,proscribir
proscríbanme,v,proscribir
proscríbanmela,v,proscribir
proscríbanmelas,v,proscribir
proscríbanmele,v,proscribir
proscríbanmeles,v,proscribir
proscríbanmelo,v,proscribir
proscríbanmelos,v,proscribir
proscríbannos,v,proscribir
proscríbannosla,v,proscribir
proscríbannoslas,v,proscribir
proscríbannosle,v,proscribir
proscríbannosles,v,proscribir
proscríbannoslo,v,proscribir
proscríbannoslos,v,proscribir
proscríbanos,v,proscribir
proscríbanosla,v,proscribir
proscríbanoslas,v,proscribir
proscríbanosle,v,proscribir
proscríbanosles,v,proscribir
proscríbanoslo,v,proscribir
proscríbanoslos,v,proscribir
proscríbanse,v,proscribir
proscríbansela,v,proscribir
proscríbanselas,v,proscribir
proscríbansele,v,proscribir
proscríbanseles,v,proscribir
proscríbanselo,v,proscribir
proscríbanselos,v,proscribir
proscríbase,v,proscribir
proscríbasela,v,proscribir
proscríbaselas,v,proscribir
proscríbasele,v,proscribir
proscríbaseles,v,proscribir
proscríbaselo,v,proscribir
proscríbaselos,v,proscribir
proscríbela,v,proscribir
proscríbelas,v,proscribir
proscríbele,v,proscribir
proscríbeles,v,proscribir
proscríbelo,v,proscribir
proscríbelos,v,proscribir
proscríbeme,v,proscribir
proscríbemela,v,proscribir
proscríbemelas,v,proscribir
proscríbemele,v,proscribir
proscríbemeles,v,proscribir
proscríbemelo,v,proscribir
proscríbemelos,v,proscribir
proscríbenos,v,proscribir
proscríbenosla,v,proscribir
proscríbenoslas,v,proscribir
proscríbenosle,v,proscribir
proscríbenosles,v,proscribir
proscríbenoslo,v,proscribir
proscríbenoslos,v,proscribir
proscríbete,v,proscribir
proscríbetela,v,proscribir
proscríbetelas,v,proscribir
proscríbetele,v,proscribir
proscríbeteles,v,proscribir
proscríbetelo,v,proscribir
proscríbetelos,v,proscribir"""

#    wordlist = Wordlist(wordlist_data.splitlines(), template_cachedb=cachedb)
#    allforms = AllForms.from_wordlist(wordlist)
#    for k,v in expected.items():
#        print(k,v)
#        assert allforms.get_lemmas(k) == v
#    allforms = AllForms.from_wordlist(wordlist)
#    for k,v in expected.items():
#        print(k,v)
#        assert allforms.get_lemmas(k) == v



