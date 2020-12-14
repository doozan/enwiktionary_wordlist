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
  g: m
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
  g: f
  gloss: female equivalent of "protector"
pos: n
  meta: {{es-noun|f}}
  forms: pl=protectoras
  g: f
  gloss: animal shelter (an organization that provides temporary homes for stray pet animals)
    syn: protectora de animales
_____
protectoras
pos: n
  meta: {{head|es|noun plural form|g=f-p}}
  g: f-p
  gloss: inflection of "protector"
_____
protectores
pos: n
  meta: {{head|es|noun plural form|g=m-p}}
  g: m-p
  gloss: inflection of "protector"
_____
protectrices
pos: n
  meta: {{head|es|noun plural form|g=f-p}}
  g: f-p
  gloss: inflection of "protector"
_____
protectriz
pos: n
  meta: {{es-noun|f|m=protector}}
  forms: m=protector; mpl=protectores; pl=protectrices
  g: f
  gloss: alternative form of "protectora"
    q: uncommon
"""
    expected = {
'protector': ['n|protector'],
'protectora': ['n|protector', 'n|protectora'],
'protectoras': ['n|protector', 'n|protectora'],
'protectores': ['n|protector'],
'protectrices': ['n|protector'],
'protectriz': ['n|protector'],
}

    wordlist = Wordlist(wordlist_data.splitlines())
    assert AllForms.from_wordlist(wordlist).all_forms == expected


def test_secondary_lemma_unique_forms():
    # test2 should be alt of test, but
    # test2s should only be a form of test2s (since it cannot be an alt of test)

    wordlist_data = """\
_____
test
pos: n
  meta: {{es-noun|m|-}}
  gloss: test
_____
test2
pos: n
  meta: {{es-noun|m|-}}
  gloss: alternative form of "test"
pos: n
  meta: {{es-noun|m|test2s}}
  g: m
  gloss: test2
"""

    expected = {
'test': ['n|test'],
'test2': ['n|test', 'n|test2'],
'test2s': ['n|test2']
}

    wordlist = Wordlist(wordlist_data.splitlines())
    assert AllForms.from_wordlist(wordlist).all_forms == expected


def test_secondary_lemma_no_unique_forms():

    wordlist_data = """\
_____
test
pos: n
  meta: {{es-noun|m|-}}
  gloss: test
_____
test2
pos: n
  meta: {{es-noun|m|test2s}}
  gloss: alternative form of "test"
pos: n
  meta: {{es-noun|m|test2s}}
  g: m
  gloss: test2
"""

    expected = {
'test': ['n|test'],
'test2': ['n|test', 'n|test2'],
'test2s': ['n|test', 'n|test2']
}

    wordlist = Wordlist(wordlist_data.splitlines())
    assert AllForms.from_wordlist(wordlist).all_forms == expected


def test_forms_text():

    wordlist_data = """\
testo {n-meta} :: {{es-noun|m}}
testo {m} :: test
testo {n-meta} :: {{es-noun|m|testoz}}
testo {m} :: test2
testa {n-meta} :: {{es-noun|f}}
testa {f} :: feminine noun of "testo"
"""
    expected = {
'testa': ['n|testo'],
'testas': ['n|testo'],
'testo': ['n|testo'],
'testos': ['n|testo'],
'testoz': ['n|testo'],
}

    wordlist = Wordlist(wordlist_data.splitlines())
    assert AllForms.from_wordlist(wordlist).all_forms == expected

def test_forms_redirection():

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

    wordlist = Wordlist(wordlist_data.splitlines())
    assert AllForms.from_wordlist(wordlist).all_forms == expected


def test_asco_forms():

    wordlist_data = """\
_____
asca
pos: n
  meta: {{es-noun|m}}
  forms: pl=ascas
  g: m
  gloss: ascus
    q: mycology
    syn: teca
_____
asco
pos: n
  meta: {{es-noun|m}}
  forms: pl=ascos
  g: m
  gloss: disgust
  gloss: nausea
  gloss: disgusting person
pos: n
  meta: {{es-noun|m}}
  forms: pl=ascos
  g: m
  gloss: alternative form of "asca"
"""

    expected = {
'asca': ['n|asca'],
'ascas': ['n|asca'],
'asco': ['n|asco', 'n|asca'],
'ascos': ['n|asco', 'n|asca']
}

    wordlist = Wordlist(wordlist_data.splitlines())
    assert AllForms.from_wordlist(wordlist).all_forms == expected


def test_verb_forms():
    wordlist_data = """\
_____
bifurcar
pos: verb
  meta: {{es-verb|bifurc|ar|pret=bifurqué}} {{es-conj-ar|bifur|p=-car|combined=1}}
  forms: 1=bifurcar; 10=bifurca; 11=bifurcamos; 12=bifurcáis; 13=bifurcan; 14=bifurcaba; 15=bifurcabas; 16=bifurcaba; 17=bifurcábamos; 18=bifurcabais; 19=bifurcaban; 2=bifurcando; 20=bifurqué; 21=bifurcaste; 22=bifurcó; 23=bifurcamos; 24=bifurcasteis; 25=bifurcaron; 26=bifurcaré; 27=bifurcarás; 28=bifurcará; 29=bifurcaremos; 3=bifurcado; 30=bifurcaréis; 31=bifurcarán; 32=bifurcaría; 33=bifurcarías; 34=bifurcaría; 35=bifurcaríamos; 36=bifurcaríais; 37=bifurcarían; 38=bifurque; 39=bifurques; 4=bifurcada; 40=bifurqués; 41=bifurque; 42=bifurquemos; 43=bifurquéis; 44=bifurquen; 45=bifurcara; 46=bifurcaras; 47=bifurcara; 48=bifurcáramos; 49=bifurcarais; 5=bifurcados; 50=bifurcaran; 51=bifurcase; 52=bifurcases; 53=bifurcase; 54=bifurcásemos; 55=bifurcaseis; 56=bifurcasen; 57=bifurcare; 58=bifurcares; 59=bifurcare; 6=bifurcadas; 60=bifurcáremos; 61=bifurcareis; 62=bifurcaren; 63=bifurca; 64=bifurcá; 65=bifurque; 66=bifurquemos; 67=bifurcad; 68=bifurquen; 69=bifurques; 7=bifurco; 70=bifurque; 71=bifurquemos; 72=bifurquéis; 73=bifurquen; 8=bifurcas; 9=bifurcás; ger_acc-dat_1=bifurcándómela; ger_acc-dat_1=bifurcándómelas; ger_acc-dat_1=bifurcándómelo; ger_acc-dat_1=bifurcándómelos; ger_acc-dat_2=bifurcándótela; ger_acc-dat_2=bifurcándótelas; ger_acc-dat_2=bifurcándótelo; ger_acc-dat_2=bifurcándótelos; ger_acc-dat_3=bifurcándósela; ger_acc-dat_3=bifurcándóselas; ger_acc-dat_3=bifurcándóselo; ger_acc-dat_3=bifurcándóselos; ger_acc-dat_4=bifurcándónosla; ger_acc-dat_4=bifurcándónoslas; ger_acc-dat_4=bifurcándónoslo; ger_acc-dat_4=bifurcándónoslos; ger_acc-dat_5=bifurcándóosla; ger_acc-dat_5=bifurcándóoslas; ger_acc-dat_5=bifurcándóoslo; ger_acc-dat_5=bifurcándóoslos; ger_acc-dat_6=bifurcándósela; ger_acc-dat_6=bifurcándóselas; ger_acc-dat_6=bifurcándóselo; ger_acc-dat_6=bifurcándóselos; ger_acc-dat_7=bifurcándósela; ger_acc-dat_7=bifurcándóselas; ger_acc-dat_7=bifurcándóselo; ger_acc-dat_7=bifurcándóselos; ger_acc_1=bifurcándome; ger_acc_2=bifurcándote; ger_acc_3=bifurcándola; ger_acc_3=bifurcándolo; ger_acc_3=bifurcándose; ger_acc_4=bifurcándonos; ger_acc_5=bifurcándoos; ger_acc_6=bifurcándolas; ger_acc_6=bifurcándolos; ger_acc_6=bifurcándose; ger_acc_7=bifurcándose; ger_dat_1=bifurcándome; ger_dat_2=bifurcándote; ger_dat_3=bifurcándole; ger_dat_3=bifurcándose; ger_dat_4=bifurcándonos; ger_dat_5=bifurcándoos; ger_dat_6=bifurcándoles; ger_dat_6=bifurcándose; imp_1p_acc-dat_2=bifurquémóstela; imp_1p_acc-dat_2=bifurquémóstelas; imp_1p_acc-dat_2=bifurquémóstelo; imp_1p_acc-dat_2=bifurquémóstelos; imp_1p_acc-dat_4=bifurquémónosla; imp_1p_acc-dat_4=bifurquémónoslas; imp_1p_acc-dat_4=bifurquémónoslo; imp_1p_acc-dat_4=bifurquémónoslos; imp_1p_acc-dat_5=bifurquémóosla; imp_1p_acc-dat_5=bifurquémóoslas; imp_1p_acc-dat_5=bifurquémóoslo; imp_1p_acc-dat_5=bifurquémóoslos; imp_1p_acc_2=bifurquémoste; imp_1p_acc_3=bifurquémosla; imp_1p_acc_3=bifurquémoslo; imp_1p_acc_4=bifurquémonos; imp_1p_acc_5=bifurquémoos; imp_1p_acc_6=bifurquémoslas; imp_1p_acc_6=bifurquémoslos; imp_1p_dat_2=bifurquémoste; imp_1p_dat_3=bifurquémosle; imp_1p_dat_4=bifurquémonos; imp_1p_dat_5=bifurquémoos; imp_1p_dat_6=bifurquémosles; imp_f2p_acc-dat_1=bifúrquénmela; imp_f2p_acc-dat_1=bifúrquénmelas; imp_f2p_acc-dat_1=bifúrquénmelo; imp_f2p_acc-dat_1=bifúrquénmelos; imp_f2p_acc-dat_4=bifúrquénnosla; imp_f2p_acc-dat_4=bifúrquénnoslas; imp_f2p_acc-dat_4=bifúrquénnoslo; imp_f2p_acc-dat_4=bifúrquénnoslos; imp_f2p_acc-dat_6=bifúrquénsela; imp_f2p_acc-dat_6=bifúrquénselas; imp_f2p_acc-dat_6=bifúrquénselo; imp_f2p_acc-dat_6=bifúrquénselos; imp_f2p_acc-dat_7=bifúrquénsela; imp_f2p_acc-dat_7=bifúrquénselas; imp_f2p_acc-dat_7=bifúrquénselo; imp_f2p_acc-dat_7=bifúrquénselos; imp_f2p_acc_1=bifúrquenme; imp_f2p_acc_3=bifúrquenla; imp_f2p_acc_3=bifúrquenlo; imp_f2p_acc_4=bifúrquennos; imp_f2p_acc_6=bifúrquenlas; imp_f2p_acc_6=bifúrquenlos; imp_f2p_acc_6=bifúrquense; imp_f2p_acc_7=bifúrquense; imp_f2p_dat_1=bifúrquenme; imp_f2p_dat_3=bifúrquenle; imp_f2p_dat_4=bifúrquennos; imp_f2p_dat_6=bifúrquenles; imp_f2p_dat_6=bifúrquense; imp_f2s_acc-dat_1=bifúrquémela; imp_f2s_acc-dat_1=bifúrquémelas; imp_f2s_acc-dat_1=bifúrquémelo; imp_f2s_acc-dat_1=bifúrquémelos; imp_f2s_acc-dat_3=bifúrquésela; imp_f2s_acc-dat_3=bifúrquéselas; imp_f2s_acc-dat_3=bifúrquéselo; imp_f2s_acc-dat_3=bifúrquéselos; imp_f2s_acc-dat_4=bifúrquénosla; imp_f2s_acc-dat_4=bifúrquénoslas; imp_f2s_acc-dat_4=bifúrquénoslo; imp_f2s_acc-dat_4=bifúrquénoslos; imp_f2s_acc-dat_7=bifúrquésela; imp_f2s_acc-dat_7=bifúrquéselas; imp_f2s_acc-dat_7=bifúrquéselo; imp_f2s_acc-dat_7=bifúrquéselos; imp_f2s_acc_1=bifúrqueme; imp_f2s_acc_3=bifúrquela; imp_f2s_acc_3=bifúrquelo; imp_f2s_acc_3=bifúrquese; imp_f2s_acc_4=bifúrquenos; imp_f2s_acc_6=bifúrquelas; imp_f2s_acc_6=bifúrquelos; imp_f2s_acc_7=bifúrquese; imp_f2s_dat_1=bifúrqueme; imp_f2s_dat_3=bifúrquele; imp_f2s_dat_3=bifúrquese; imp_f2s_dat_4=bifúrquenos; imp_f2s_dat_6=bifúrqueles; imp_i2p_acc-dat_1=bifurcádmela; imp_i2p_acc-dat_1=bifurcádmelas; imp_i2p_acc-dat_1=bifurcádmelo; imp_i2p_acc-dat_1=bifurcádmelos; imp_i2p_acc-dat_4=bifurcádnosla; imp_i2p_acc-dat_4=bifurcádnoslas; imp_i2p_acc-dat_4=bifurcádnoslo; imp_i2p_acc-dat_4=bifurcádnoslos; imp_i2p_acc-dat_5=bifurcáosla; imp_i2p_acc-dat_5=bifurcáoslas; imp_i2p_acc-dat_5=bifurcáoslo; imp_i2p_acc-dat_5=bifurcáoslos; imp_i2p_acc-dat_7=bifurcádosla; imp_i2p_acc-dat_7=bifurcádoslas; imp_i2p_acc-dat_7=bifurcádoslo; imp_i2p_acc-dat_7=bifurcádoslos; imp_i2p_acc_1=bifurcadme; imp_i2p_acc_3=bifurcadla; imp_i2p_acc_3=bifurcadlo; imp_i2p_acc_4=bifurcadnos; imp_i2p_acc_5=bifurcaos; imp_i2p_acc_6=bifurcadlas; imp_i2p_acc_6=bifurcadlos; imp_i2p_acc_7=bifurcados; imp_i2p_dat_1=bifurcadme; imp_i2p_dat_3=bifurcadle; imp_i2p_dat_4=bifurcadnos; imp_i2p_dat_5=bifurcaos; imp_i2p_dat_6=bifurcadles; imp_i2s_acc-dat_1=bifúrcámela; imp_i2s_acc-dat_1=bifúrcámelas; imp_i2s_acc-dat_1=bifúrcámelo; imp_i2s_acc-dat_1=bifúrcámelos; imp_i2s_acc-dat_2=bifúrcátela; imp_i2s_acc-dat_2=bifúrcátelas; imp_i2s_acc-dat_2=bifúrcátelo; imp_i2s_acc-dat_2=bifúrcátelos; imp_i2s_acc-dat_4=bifúrcánosla; imp_i2s_acc-dat_4=bifúrcánoslas; imp_i2s_acc-dat_4=bifúrcánoslo; imp_i2s_acc-dat_4=bifúrcánoslos; imp_i2s_acc_1=bifúrcame; imp_i2s_acc_2=bifúrcate; imp_i2s_acc_3=bifúrcala; imp_i2s_acc_3=bifúrcalo; imp_i2s_acc_4=bifúrcanos; imp_i2s_acc_6=bifúrcalas; imp_i2s_acc_6=bifúrcalos; imp_i2s_dat_1=bifúrcame; imp_i2s_dat_2=bifúrcate; imp_i2s_dat_3=bifúrcale; imp_i2s_dat_4=bifúrcanos; imp_i2s_dat_6=bifúrcales; inf_acc-dat_1=bifurcármela; inf_acc-dat_1=bifurcármelas; inf_acc-dat_1=bifurcármelo; inf_acc-dat_1=bifurcármelos; inf_acc-dat_2=bifurcártela; inf_acc-dat_2=bifurcártelas; inf_acc-dat_2=bifurcártelo; inf_acc-dat_2=bifurcártelos; inf_acc-dat_3=bifurcársela; inf_acc-dat_3=bifurcárselas; inf_acc-dat_3=bifurcárselo; inf_acc-dat_3=bifurcárselos; inf_acc-dat_4=bifurcárnosla; inf_acc-dat_4=bifurcárnoslas; inf_acc-dat_4=bifurcárnoslo; inf_acc-dat_4=bifurcárnoslos; inf_acc-dat_5=bifurcárosla; inf_acc-dat_5=bifurcároslas; inf_acc-dat_5=bifurcároslo; inf_acc-dat_5=bifurcároslos; inf_acc-dat_6=bifurcársela; inf_acc-dat_6=bifurcárselas; inf_acc-dat_6=bifurcárselo; inf_acc-dat_6=bifurcárselos; inf_acc-dat_7=bifurcársela; inf_acc-dat_7=bifurcárselas; inf_acc-dat_7=bifurcárselo; inf_acc-dat_7=bifurcárselos; inf_acc_1=bifurcarme; inf_acc_2=bifurcarte; inf_acc_3=bifurcarla; inf_acc_3=bifurcarlo; inf_acc_3=bifurcarse; inf_acc_4=bifurcarnos; inf_acc_5=bifurcaros; inf_acc_6=bifurcarlas; inf_acc_6=bifurcarlos; inf_acc_6=bifurcarse; inf_acc_7=bifurcarse; inf_dat_1=bifurcarme; inf_dat_2=bifurcarte; inf_dat_3=bifurcarle; inf_dat_3=bifurcarse; inf_dat_4=bifurcarnos; inf_dat_5=bifurcaros; inf_dat_6=bifurcarles; inf_dat_6=bifurcarse
  gloss: to bifurcate, to cause to fork off
    q: transitive
  gloss: To diverge, fork off
    q: reflexive
_____
bifurcarse
pos: verb
  meta: {{es-verb|bifurc|ar|pret=bifurqué|ref=y}} {{es-conj-ar|bifur|p=-car|ref=1|combined=1}}
  forms: 1=bifurcarse; 10=bifurca; 11=bifurcamos; 12=bifurcáis; 13=bifurcan; 14=bifurcaba; 15=bifurcabas; 16=bifurcaba; 17=bifurcábamos; 18=bifurcabais; 19=bifurcaban; 2=bifurcándose; 20=bifurqué; 21=bifurcaste; 22=bifurcó; 23=bifurcamos; 24=bifurcasteis; 25=bifurcaron; 26=bifurcaré; 27=bifurcarás; 28=bifurcará; 29=bifurcaremos; 3=bifurcado; 30=bifurcaréis; 31=bifurcarán; 32=bifurcaría; 33=bifurcarías; 34=bifurcaría; 35=bifurcaríamos; 36=bifurcaríais; 37=bifurcarían; 38=bifurque; 39=bifurques; 4=bifurcada; 40=bifurqués; 41=bifurque; 42=bifurquemos; 43=bifurquéis; 44=bifurquen; 45=bifurcara; 46=bifurcaras; 47=bifurcara; 48=bifurcáramos; 49=bifurcarais; 5=bifurcados; 50=bifurcaran; 51=bifurcase; 52=bifurcases; 53=bifurcase; 54=bifurcásemos; 55=bifurcaseis; 56=bifurcasen; 57=bifurcare; 58=bifurcares; 59=bifurcare; 6=bifurcadas; 60=bifurcáremos; 61=bifurcareis; 62=bifurcaren; 63=bifurcate; 64=-; 65=bifurque; 66=bifurquemos; 67=bifurcaos; 68=bifurquen; 69=bifurques; 7=bifurco; 70=bifurque; 71=bifurquemos; 72=bifurquéis; 73=bifurquen; 8=bifurcas; 9=bifurcás; ger_acc-dat_1=bifurcándómela; ger_acc-dat_1=bifurcándómelas; ger_acc-dat_1=bifurcándómelo; ger_acc-dat_1=bifurcándómelos; ger_acc-dat_2=bifurcándótela; ger_acc-dat_2=bifurcándótelas; ger_acc-dat_2=bifurcándótelo; ger_acc-dat_2=bifurcándótelos; ger_acc-dat_3=bifurcándósela; ger_acc-dat_3=bifurcándóselas; ger_acc-dat_3=bifurcándóselo; ger_acc-dat_3=bifurcándóselos; ger_acc-dat_4=bifurcándónosla; ger_acc-dat_4=bifurcándónoslas; ger_acc-dat_4=bifurcándónoslo; ger_acc-dat_4=bifurcándónoslos; ger_acc-dat_5=bifurcándóosla; ger_acc-dat_5=bifurcándóoslas; ger_acc-dat_5=bifurcándóoslo; ger_acc-dat_5=bifurcándóoslos; ger_acc-dat_6=bifurcándósela; ger_acc-dat_6=bifurcándóselas; ger_acc-dat_6=bifurcándóselo; ger_acc-dat_6=bifurcándóselos; ger_acc-dat_7=bifurcándósela; ger_acc-dat_7=bifurcándóselas; ger_acc-dat_7=bifurcándóselo; ger_acc-dat_7=bifurcándóselos; ger_acc_1=bifurcándome; ger_acc_2=bifurcándote; ger_acc_3=bifurcándola; ger_acc_3=bifurcándolo; ger_acc_3=bifurcándose; ger_acc_4=bifurcándonos; ger_acc_5=bifurcándoos; ger_acc_6=bifurcándolas; ger_acc_6=bifurcándolos; ger_acc_6=bifurcándose; ger_acc_7=bifurcándose; ger_dat_1=bifurcándome; ger_dat_2=bifurcándote; ger_dat_3=bifurcándole; ger_dat_3=bifurcándose; ger_dat_4=bifurcándonos; ger_dat_5=bifurcándoos; ger_dat_6=bifurcándoles; ger_dat_6=bifurcándose; imp_1p_acc-dat_2=bifurquémóstela; imp_1p_acc-dat_2=bifurquémóstelas; imp_1p_acc-dat_2=bifurquémóstelo; imp_1p_acc-dat_2=bifurquémóstelos; imp_1p_acc-dat_4=bifurquémónosla; imp_1p_acc-dat_4=bifurquémónoslas; imp_1p_acc-dat_4=bifurquémónoslo; imp_1p_acc-dat_4=bifurquémónoslos; imp_1p_acc-dat_5=bifurquémóosla; imp_1p_acc-dat_5=bifurquémóoslas; imp_1p_acc-dat_5=bifurquémóoslo; imp_1p_acc-dat_5=bifurquémóoslos; imp_1p_acc_2=bifurquémoste; imp_1p_acc_3=bifurquémosla; imp_1p_acc_3=bifurquémoslo; imp_1p_acc_4=bifurquémonos; imp_1p_acc_5=bifurquémoos; imp_1p_acc_6=bifurquémoslas; imp_1p_acc_6=bifurquémoslos; imp_1p_dat_2=bifurquémoste; imp_1p_dat_3=bifurquémosle; imp_1p_dat_4=bifurquémonos; imp_1p_dat_5=bifurquémoos; imp_1p_dat_6=bifurquémosles; imp_f2p_acc-dat_1=bifúrquénmela; imp_f2p_acc-dat_1=bifúrquénmelas; imp_f2p_acc-dat_1=bifúrquénmelo; imp_f2p_acc-dat_1=bifúrquénmelos; imp_f2p_acc-dat_4=bifúrquénnosla; imp_f2p_acc-dat_4=bifúrquénnoslas; imp_f2p_acc-dat_4=bifúrquénnoslo; imp_f2p_acc-dat_4=bifúrquénnoslos; imp_f2p_acc-dat_6=bifúrquénsela; imp_f2p_acc-dat_6=bifúrquénselas; imp_f2p_acc-dat_6=bifúrquénselo; imp_f2p_acc-dat_6=bifúrquénselos; imp_f2p_acc-dat_7=bifúrquénsela; imp_f2p_acc-dat_7=bifúrquénselas; imp_f2p_acc-dat_7=bifúrquénselo; imp_f2p_acc-dat_7=bifúrquénselos; imp_f2p_acc_1=bifúrquenme; imp_f2p_acc_3=bifúrquenla; imp_f2p_acc_3=bifúrquenlo; imp_f2p_acc_4=bifúrquennos; imp_f2p_acc_6=bifúrquenlas; imp_f2p_acc_6=bifúrquenlos; imp_f2p_acc_6=bifúrquense; imp_f2p_acc_7=bifúrquense; imp_f2p_dat_1=bifúrquenme; imp_f2p_dat_3=bifúrquenle; imp_f2p_dat_4=bifúrquennos; imp_f2p_dat_6=bifúrquenles; imp_f2p_dat_6=bifúrquense; imp_f2s_acc-dat_1=bifúrquémela; imp_f2s_acc-dat_1=bifúrquémelas; imp_f2s_acc-dat_1=bifúrquémelo; imp_f2s_acc-dat_1=bifúrquémelos; imp_f2s_acc-dat_3=bifúrquésela; imp_f2s_acc-dat_3=bifúrquéselas; imp_f2s_acc-dat_3=bifúrquéselo; imp_f2s_acc-dat_3=bifúrquéselos; imp_f2s_acc-dat_4=bifúrquénosla; imp_f2s_acc-dat_4=bifúrquénoslas; imp_f2s_acc-dat_4=bifúrquénoslo; imp_f2s_acc-dat_4=bifúrquénoslos; imp_f2s_acc-dat_7=bifúrquésela; imp_f2s_acc-dat_7=bifúrquéselas; imp_f2s_acc-dat_7=bifúrquéselo; imp_f2s_acc-dat_7=bifúrquéselos; imp_f2s_acc_1=bifúrqueme; imp_f2s_acc_3=bifúrquela; imp_f2s_acc_3=bifúrquelo; imp_f2s_acc_3=bifúrquese; imp_f2s_acc_4=bifúrquenos; imp_f2s_acc_6=bifúrquelas; imp_f2s_acc_6=bifúrquelos; imp_f2s_acc_7=bifúrquese; imp_f2s_dat_1=bifúrqueme; imp_f2s_dat_3=bifúrquele; imp_f2s_dat_3=bifúrquese; imp_f2s_dat_4=bifúrquenos; imp_f2s_dat_6=bifúrqueles; imp_i2p_acc-dat_1=bifurcaósmela; imp_i2p_acc-dat_1=bifurcaósmelas; imp_i2p_acc-dat_1=bifurcaósmelo; imp_i2p_acc-dat_1=bifurcaósmelos; imp_i2p_acc-dat_4=bifurcaósnosla; imp_i2p_acc-dat_4=bifurcaósnoslas; imp_i2p_acc-dat_4=bifurcaósnoslo; imp_i2p_acc-dat_4=bifurcaósnoslos; imp_i2p_acc-dat_5=bifurcaóosla; imp_i2p_acc-dat_5=bifurcaóoslas; imp_i2p_acc-dat_5=bifurcaóoslo; imp_i2p_acc-dat_5=bifurcaóoslos; imp_i2p_acc-dat_7=bifurcaósosla; imp_i2p_acc-dat_7=bifurcaósoslas; imp_i2p_acc-dat_7=bifurcaósoslo; imp_i2p_acc-dat_7=bifurcaósoslos; imp_i2p_acc_1=bifurcaosme; imp_i2p_acc_3=bifurcaosla; imp_i2p_acc_3=bifurcaoslo; imp_i2p_acc_4=bifurcaosnos; imp_i2p_acc_5=bifurcaoos; imp_i2p_acc_6=bifurcaoslas; imp_i2p_acc_6=bifurcaoslos; imp_i2p_acc_7=bifurcaosos; imp_i2p_dat_1=bifurcaosme; imp_i2p_dat_3=bifurcaosle; imp_i2p_dat_4=bifurcaosnos; imp_i2p_dat_5=bifurcaoos; imp_i2p_dat_6=bifurcaosles; imp_i2s_acc-dat_1=bifurcátémela; imp_i2s_acc-dat_1=bifurcátémelas; imp_i2s_acc-dat_1=bifurcátémelo; imp_i2s_acc-dat_1=bifurcátémelos; imp_i2s_acc-dat_2=bifurcátétela; imp_i2s_acc-dat_2=bifurcátételas; imp_i2s_acc-dat_2=bifurcátételo; imp_i2s_acc-dat_2=bifurcátételos; imp_i2s_acc-dat_4=bifurcáténosla; imp_i2s_acc-dat_4=bifurcáténoslas; imp_i2s_acc-dat_4=bifurcáténoslo; imp_i2s_acc-dat_4=bifurcáténoslos; imp_i2s_acc_1=bifurcáteme; imp_i2s_acc_2=bifurcátete; imp_i2s_acc_3=bifurcátela; imp_i2s_acc_3=bifurcátelo; imp_i2s_acc_4=bifurcátenos; imp_i2s_acc_6=bifurcátelas; imp_i2s_acc_6=bifurcátelos; imp_i2s_dat_1=bifurcáteme; imp_i2s_dat_2=bifurcátete; imp_i2s_dat_3=bifurcátele; imp_i2s_dat_4=bifurcátenos; imp_i2s_dat_6=bifurcáteles; inf_acc-dat_1=bifurcármela; inf_acc-dat_1=bifurcármelas; inf_acc-dat_1=bifurcármelo; inf_acc-dat_1=bifurcármelos; inf_acc-dat_2=bifurcártela; inf_acc-dat_2=bifurcártelas; inf_acc-dat_2=bifurcártelo; inf_acc-dat_2=bifurcártelos; inf_acc-dat_3=bifurcársela; inf_acc-dat_3=bifurcárselas; inf_acc-dat_3=bifurcárselo; inf_acc-dat_3=bifurcárselos; inf_acc-dat_4=bifurcárnosla; inf_acc-dat_4=bifurcárnoslas; inf_acc-dat_4=bifurcárnoslo; inf_acc-dat_4=bifurcárnoslos; inf_acc-dat_5=bifurcárosla; inf_acc-dat_5=bifurcároslas; inf_acc-dat_5=bifurcároslo; inf_acc-dat_5=bifurcároslos; inf_acc-dat_6=bifurcársela; inf_acc-dat_6=bifurcárselas; inf_acc-dat_6=bifurcárselo; inf_acc-dat_6=bifurcárselos; inf_acc-dat_7=bifurcársela; inf_acc-dat_7=bifurcárselas; inf_acc-dat_7=bifurcárselo; inf_acc-dat_7=bifurcárselos; inf_acc_1=bifurcarme; inf_acc_2=bifurcarte; inf_acc_3=bifurcarla; inf_acc_3=bifurcarlo; inf_acc_3=bifurcarse; inf_acc_4=bifurcarnos; inf_acc_5=bifurcaros; inf_acc_6=bifurcarlas; inf_acc_6=bifurcarlos; inf_acc_6=bifurcarse; inf_acc_7=bifurcarse; inf_dat_1=bifurcarme; inf_dat_2=bifurcarte; inf_dat_3=bifurcarle; inf_dat_3=bifurcarse; inf_dat_4=bifurcarnos; inf_dat_5=bifurcaros; inf_dat_6=bifurcarles; inf_dat_6=bifurcarse
  gloss: to split, divide, fork, branch off
"""

    expected = {
'bifurcar': ['verb|bifurcar'],
'bifurca': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcamos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcáis': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcan': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcaba': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcabas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcábamos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcabais': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcaban': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcando': ['verb|bifurcar'],
'bifurqué': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcaste': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcó': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcasteis': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcaron': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcaré': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarás': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcará': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcaremos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcado': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcaréis': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarán': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcaría': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarías': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcaríamos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcaríais': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarían': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurque': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurques': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcada': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurqués': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquemos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquéis': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquen': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcara': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcaras': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcáramos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarais': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcados': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcaran': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcase': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcases': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcásemos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcaseis': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcasen': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcare': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcares': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcadas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcáremos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcareis': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcaren': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcá': ['verb|bifurcar'],
'bifurcad': ['verb|bifurcar'],
'bifurco': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcás': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándómela': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándómelas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándómelo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándómelos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándótela': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándótelas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándótelo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándótelos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándósela': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándóselas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándóselo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándóselos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándónosla': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándónoslas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándónoslo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándónoslos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándóosla': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándóoslas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándóoslo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándóoslos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándome': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándote': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándola': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándolo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándose': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándonos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándoos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándolas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándolos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándole': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcándoles': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémóstela': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémóstelas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémóstelo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémóstelos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémónosla': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémónoslas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémónoslo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémónoslos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémóosla': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémóoslas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémóoslo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémóoslos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémoste': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémosla': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémoslo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémonos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémoos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémoslas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémoslos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémosle': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurquémosles': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquénmela': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquénmelas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquénmelo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquénmelos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquénnosla': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquénnoslas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquénnoslo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquénnoslos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquénsela': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquénselas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquénselo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquénselos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquenme': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquenla': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquenlo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquennos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquenlas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquenlos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquense': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquenle': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquenles': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquémela': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquémelas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquémelo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquémelos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquésela': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquéselas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquéselo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquéselos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquénosla': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquénoslas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquénoslo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquénoslos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrqueme': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquela': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquelo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquese': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquenos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquelas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquelos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrquele': ['verb|bifurcar', 'verb|bifurcarse'],
'bifúrqueles': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcádmela': ['verb|bifurcar'],
'bifurcádmelas': ['verb|bifurcar'],
'bifurcádmelo': ['verb|bifurcar'],
'bifurcádmelos': ['verb|bifurcar'],
'bifurcádnosla': ['verb|bifurcar'],
'bifurcádnoslas': ['verb|bifurcar'],
'bifurcádnoslo': ['verb|bifurcar'],
'bifurcádnoslos': ['verb|bifurcar'],
'bifurcáosla': ['verb|bifurcar'],
'bifurcáoslas': ['verb|bifurcar'],
'bifurcáoslo': ['verb|bifurcar'],
'bifurcáoslos': ['verb|bifurcar'],
'bifurcádosla': ['verb|bifurcar'],
'bifurcádoslas': ['verb|bifurcar'],
'bifurcádoslo': ['verb|bifurcar'],
'bifurcádoslos': ['verb|bifurcar'],
'bifurcadme': ['verb|bifurcar'],
'bifurcadla': ['verb|bifurcar'],
'bifurcadlo': ['verb|bifurcar'],
'bifurcadnos': ['verb|bifurcar'],
'bifurcaos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcadlas': ['verb|bifurcar'],
'bifurcadlos': ['verb|bifurcar'],
'bifurcadle': ['verb|bifurcar'],
'bifurcadles': ['verb|bifurcar'],
'bifúrcámela': ['verb|bifurcar'],
'bifúrcámelas': ['verb|bifurcar'],
'bifúrcámelo': ['verb|bifurcar'],
'bifúrcámelos': ['verb|bifurcar'],
'bifúrcátela': ['verb|bifurcar'],
'bifúrcátelas': ['verb|bifurcar'],
'bifúrcátelo': ['verb|bifurcar'],
'bifúrcátelos': ['verb|bifurcar'],
'bifúrcánosla': ['verb|bifurcar'],
'bifúrcánoslas': ['verb|bifurcar'],
'bifúrcánoslo': ['verb|bifurcar'],
'bifúrcánoslos': ['verb|bifurcar'],
'bifúrcame': ['verb|bifurcar'],
'bifúrcate': ['verb|bifurcar'],
'bifúrcala': ['verb|bifurcar'],
'bifúrcalo': ['verb|bifurcar'],
'bifúrcanos': ['verb|bifurcar'],
'bifúrcalas': ['verb|bifurcar'],
'bifúrcalos': ['verb|bifurcar'],
'bifúrcale': ['verb|bifurcar'],
'bifúrcales': ['verb|bifurcar'],
'bifurcármela': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcármelas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcármelo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcármelos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcártela': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcártelas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcártelo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcártelos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcársela': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcárselas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcárselo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcárselos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcárnosla': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcárnoslas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcárnoslo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcárnoslos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcárosla': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcároslas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcároslo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcároslos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarme': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarte': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarla': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarlo': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarse': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarnos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcaros': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarlas': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarlos': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarle': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcarles': ['verb|bifurcar', 'verb|bifurcarse'],
'bifurcate': ['verb|bifurcarse'],
'bifurcaósmela': ['verb|bifurcarse'],
'bifurcaósmelas': ['verb|bifurcarse'],
'bifurcaósmelo': ['verb|bifurcarse'],
'bifurcaósmelos': ['verb|bifurcarse'],
'bifurcaósnosla': ['verb|bifurcarse'],
'bifurcaósnoslas': ['verb|bifurcarse'],
'bifurcaósnoslo': ['verb|bifurcarse'],
'bifurcaósnoslos': ['verb|bifurcarse'],
'bifurcaóosla': ['verb|bifurcarse'],
'bifurcaóoslas': ['verb|bifurcarse'],
'bifurcaóoslo': ['verb|bifurcarse'],
'bifurcaóoslos': ['verb|bifurcarse'],
'bifurcaósosla': ['verb|bifurcarse'],
'bifurcaósoslas': ['verb|bifurcarse'],
'bifurcaósoslo': ['verb|bifurcarse'],
'bifurcaósoslos': ['verb|bifurcarse'],
'bifurcaosme': ['verb|bifurcarse'],
'bifurcaosla': ['verb|bifurcarse'],
'bifurcaoslo': ['verb|bifurcarse'],
'bifurcaosnos': ['verb|bifurcarse'],
'bifurcaoos': ['verb|bifurcarse'],
'bifurcaoslas': ['verb|bifurcarse'],
'bifurcaoslos': ['verb|bifurcarse'],
'bifurcaosos': ['verb|bifurcarse'],
'bifurcaosle': ['verb|bifurcarse'],
'bifurcaosles': ['verb|bifurcarse'],
'bifurcátémela': ['verb|bifurcarse'],
'bifurcátémelas': ['verb|bifurcarse'],
'bifurcátémelo': ['verb|bifurcarse'],
'bifurcátémelos': ['verb|bifurcarse'],
'bifurcátétela': ['verb|bifurcarse'],
'bifurcátételas': ['verb|bifurcarse'],
'bifurcátételo': ['verb|bifurcarse'],
'bifurcátételos': ['verb|bifurcarse'],
'bifurcáténosla': ['verb|bifurcarse'],
'bifurcáténoslas': ['verb|bifurcarse'],
'bifurcáténoslo': ['verb|bifurcarse'],
'bifurcáténoslos': ['verb|bifurcarse'],
'bifurcáteme': ['verb|bifurcarse'],
'bifurcátete': ['verb|bifurcarse'],
'bifurcátela': ['verb|bifurcarse'],
'bifurcátelo': ['verb|bifurcarse'],
'bifurcátenos': ['verb|bifurcarse'],
'bifurcátelas': ['verb|bifurcarse'],
'bifurcátelos': ['verb|bifurcarse'],
'bifurcátele': ['verb|bifurcarse'],
'bifurcáteles': ['verb|bifurcarse']}

    wordlist = Wordlist(wordlist_data.splitlines())
    assert AllForms.from_wordlist(wordlist).all_forms == expected


def test_afecto():
    wordlist_data = """\
_____
afecto
pos: adj
  meta: {{es-adj|f=afecta}}
  forms: f=afecta; fpl=afectas; pl=afectos
  gloss: test
"""
    expected = {
'afecta': ['adj|afecto'],
'afectas': ['adj|afecto'],
'afectos': ['adj|afecto'],
'afecto': ['adj|afecto']}

    wordlist = Wordlist(wordlist_data.splitlines())
    assert AllForms.from_wordlist(wordlist).all_forms == expected

def test_ninguno():
    wordlist_data = """\
_____
ningún
pos: adj
  meta: {{head|es|adjective form|g=m|apocopate||standard form|ninguno}}
  gloss: test
"""
    expected = {
'ninguno': ['adj|ningún'],
'ningún': ['adj|ningún']
}

    wordlist = Wordlist(wordlist_data.splitlines())
    assert AllForms.from_wordlist(wordlist).all_forms == expected
