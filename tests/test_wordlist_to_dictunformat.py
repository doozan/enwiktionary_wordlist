import enwiktionary_wordlist.wordlist_to_dictunformat as exporter

def test_forms_text():
    exporter.all_pages = {}

    data = """\
_____
asca
pos: n
  meta: {{es-noun|m}}
  forms: pl=ascas
  form: m
  gloss: ascus
    q: mycology
    syn: teca
_____
asco
pos: n
  meta: {{es-noun|m}}
  forms: pl=ascos
  form: m
  gloss: disgust
  gloss: nausea
  gloss: disgusting person
pos: n
  meta: {{es-noun|m}}
  forms: pl=ascos
  form: m
  gloss: alternative form of "asca"
"""

    expected = """\
_____
00-database-info
##:name:Wiktionary (es-en)
##:url:en.wiktionary.org
##:pagecount:2
##:formcount:4
##:description:test
_____
asca|ascas
asca (n, m), plural "ascas"
1. (mycology) ascus
      Synonyms: teca
_____
asco|ascos
asca (n, m), plural "ascas"
1. (mycology) ascus
      Synonyms: teca

asco (n, m), plural "ascos"
1. disgust
2. nausea
3. disgusting person

asco (n, m), plural "ascos"
1. alternative form of "asca"
"""
    print("\n".join(exporter.export(data.splitlines(), None, "es", "test")))
    assert "\n".join(exporter.export(data.splitlines(), None, "es", "test")) == expected.strip()


def test_forms_bifurcar():
    exporter.all_pages = {}

    wordlist_data = """\
_____
bifurcar
pos: v
  meta: {{es-verb|bifurc|ar|pret=bifurqué}} {{es-conj-ar|bifur|p=-car|combined=1}}
  forms: 1=bifurcar; 10=bifurca; 11=bifurcamos; 12=bifurcáis; 13=bifurcan; 14=bifurcaba; 15=bifurcabas; 16=bifurcaba; 17=bifurcábamos; 18=bifurcabais; 19=bifurcaban; 2=bifurcando; 20=bifurqué; 21=bifurcaste; 22=bifurcó; 23=bifurcamos; 24=bifurcasteis; 25=bifurcaron; 26=bifurcaré; 27=bifurcarás; 28=bifurcará; 29=bifurcaremos; 3=bifurcado; 30=bifurcaréis; 31=bifurcarán; 32=bifurcaría; 33=bifurcarías; 34=bifurcaría; 35=bifurcaríamos; 36=bifurcaríais; 37=bifurcarían; 38=bifurque; 39=bifurques; 4=bifurcada; 40=bifurqués; 41=bifurque; 42=bifurquemos; 43=bifurquéis; 44=bifurquen; 45=bifurcara; 46=bifurcaras; 47=bifurcara; 48=bifurcáramos; 49=bifurcarais; 5=bifurcados; 50=bifurcaran; 51=bifurcase; 52=bifurcases; 53=bifurcase; 54=bifurcásemos; 55=bifurcaseis; 56=bifurcasen; 57=bifurcare; 58=bifurcares; 59=bifurcare; 6=bifurcadas; 60=bifurcáremos; 61=bifurcareis; 62=bifurcaren; 63=bifurca; 64=bifurcá; 65=bifurque; 66=bifurquemos; 67=bifurcad; 68=bifurquen; 69=bifurques; 7=bifurco; 70=bifurque; 71=bifurquemos; 72=bifurquéis; 73=bifurquen; 8=bifurcas; 9=bifurcás; ger_acc-dat_1=bifurcándómela; ger_acc-dat_1=bifurcándómelas; ger_acc-dat_1=bifurcándómelo; ger_acc-dat_1=bifurcándómelos; ger_acc-dat_2=bifurcándótela; ger_acc-dat_2=bifurcándótelas; ger_acc-dat_2=bifurcándótelo; ger_acc-dat_2=bifurcándótelos; ger_acc-dat_3=bifurcándósela; ger_acc-dat_3=bifurcándóselas; ger_acc-dat_3=bifurcándóselo; ger_acc-dat_3=bifurcándóselos; ger_acc-dat_4=bifurcándónosla; ger_acc-dat_4=bifurcándónoslas; ger_acc-dat_4=bifurcándónoslo; ger_acc-dat_4=bifurcándónoslos; ger_acc-dat_5=bifurcándóosla; ger_acc-dat_5=bifurcándóoslas; ger_acc-dat_5=bifurcándóoslo; ger_acc-dat_5=bifurcándóoslos; ger_acc-dat_6=bifurcándósela; ger_acc-dat_6=bifurcándóselas; ger_acc-dat_6=bifurcándóselo; ger_acc-dat_6=bifurcándóselos; ger_acc-dat_7=bifurcándósela; ger_acc-dat_7=bifurcándóselas; ger_acc-dat_7=bifurcándóselo; ger_acc-dat_7=bifurcándóselos; ger_acc_1=bifurcándome; ger_acc_2=bifurcándote; ger_acc_3=bifurcándola; ger_acc_3=bifurcándolo; ger_acc_3=bifurcándose; ger_acc_4=bifurcándonos; ger_acc_5=bifurcándoos; ger_acc_6=bifurcándolas; ger_acc_6=bifurcándolos; ger_acc_6=bifurcándose; ger_acc_7=bifurcándose; ger_dat_1=bifurcándome; ger_dat_2=bifurcándote; ger_dat_3=bifurcándole; ger_dat_3=bifurcándose; ger_dat_4=bifurcándonos; ger_dat_5=bifurcándoos; ger_dat_6=bifurcándoles; ger_dat_6=bifurcándose; imp_1p_acc-dat_2=bifurquémóstela; imp_1p_acc-dat_2=bifurquémóstelas; imp_1p_acc-dat_2=bifurquémóstelo; imp_1p_acc-dat_2=bifurquémóstelos; imp_1p_acc-dat_4=bifurquémónosla; imp_1p_acc-dat_4=bifurquémónoslas; imp_1p_acc-dat_4=bifurquémónoslo; imp_1p_acc-dat_4=bifurquémónoslos; imp_1p_acc-dat_5=bifurquémóosla; imp_1p_acc-dat_5=bifurquémóoslas; imp_1p_acc-dat_5=bifurquémóoslo; imp_1p_acc-dat_5=bifurquémóoslos; imp_1p_acc_2=bifurquémoste; imp_1p_acc_3=bifurquémosla; imp_1p_acc_3=bifurquémoslo; imp_1p_acc_4=bifurquémonos; imp_1p_acc_5=bifurquémoos; imp_1p_acc_6=bifurquémoslas; imp_1p_acc_6=bifurquémoslos; imp_1p_dat_2=bifurquémoste; imp_1p_dat_3=bifurquémosle; imp_1p_dat_4=bifurquémonos; imp_1p_dat_5=bifurquémoos; imp_1p_dat_6=bifurquémosles; imp_f2p_acc-dat_1=bifúrquénmela; imp_f2p_acc-dat_1=bifúrquénmelas; imp_f2p_acc-dat_1=bifúrquénmelo; imp_f2p_acc-dat_1=bifúrquénmelos; imp_f2p_acc-dat_4=bifúrquénnosla; imp_f2p_acc-dat_4=bifúrquénnoslas; imp_f2p_acc-dat_4=bifúrquénnoslo; imp_f2p_acc-dat_4=bifúrquénnoslos; imp_f2p_acc-dat_6=bifúrquénsela; imp_f2p_acc-dat_6=bifúrquénselas; imp_f2p_acc-dat_6=bifúrquénselo; imp_f2p_acc-dat_6=bifúrquénselos; imp_f2p_acc-dat_7=bifúrquénsela; imp_f2p_acc-dat_7=bifúrquénselas; imp_f2p_acc-dat_7=bifúrquénselo; imp_f2p_acc-dat_7=bifúrquénselos; imp_f2p_acc_1=bifúrquenme; imp_f2p_acc_3=bifúrquenla; imp_f2p_acc_3=bifúrquenlo; imp_f2p_acc_4=bifúrquennos; imp_f2p_acc_6=bifúrquenlas; imp_f2p_acc_6=bifúrquenlos; imp_f2p_acc_6=bifúrquense; imp_f2p_acc_7=bifúrquense; imp_f2p_dat_1=bifúrquenme; imp_f2p_dat_3=bifúrquenle; imp_f2p_dat_4=bifúrquennos; imp_f2p_dat_6=bifúrquenles; imp_f2p_dat_6=bifúrquense; imp_f2s_acc-dat_1=bifúrquémela; imp_f2s_acc-dat_1=bifúrquémelas; imp_f2s_acc-dat_1=bifúrquémelo; imp_f2s_acc-dat_1=bifúrquémelos; imp_f2s_acc-dat_3=bifúrquésela; imp_f2s_acc-dat_3=bifúrquéselas; imp_f2s_acc-dat_3=bifúrquéselo; imp_f2s_acc-dat_3=bifúrquéselos; imp_f2s_acc-dat_4=bifúrquénosla; imp_f2s_acc-dat_4=bifúrquénoslas; imp_f2s_acc-dat_4=bifúrquénoslo; imp_f2s_acc-dat_4=bifúrquénoslos; imp_f2s_acc-dat_7=bifúrquésela; imp_f2s_acc-dat_7=bifúrquéselas; imp_f2s_acc-dat_7=bifúrquéselo; imp_f2s_acc-dat_7=bifúrquéselos; imp_f2s_acc_1=bifúrqueme; imp_f2s_acc_3=bifúrquela; imp_f2s_acc_3=bifúrquelo; imp_f2s_acc_3=bifúrquese; imp_f2s_acc_4=bifúrquenos; imp_f2s_acc_6=bifúrquelas; imp_f2s_acc_6=bifúrquelos; imp_f2s_acc_7=bifúrquese; imp_f2s_dat_1=bifúrqueme; imp_f2s_dat_3=bifúrquele; imp_f2s_dat_3=bifúrquese; imp_f2s_dat_4=bifúrquenos; imp_f2s_dat_6=bifúrqueles; imp_i2p_acc-dat_1=bifurcádmela; imp_i2p_acc-dat_1=bifurcádmelas; imp_i2p_acc-dat_1=bifurcádmelo; imp_i2p_acc-dat_1=bifurcádmelos; imp_i2p_acc-dat_4=bifurcádnosla; imp_i2p_acc-dat_4=bifurcádnoslas; imp_i2p_acc-dat_4=bifurcádnoslo; imp_i2p_acc-dat_4=bifurcádnoslos; imp_i2p_acc-dat_5=bifurcáosla; imp_i2p_acc-dat_5=bifurcáoslas; imp_i2p_acc-dat_5=bifurcáoslo; imp_i2p_acc-dat_5=bifurcáoslos; imp_i2p_acc-dat_7=bifurcádosla; imp_i2p_acc-dat_7=bifurcádoslas; imp_i2p_acc-dat_7=bifurcádoslo; imp_i2p_acc-dat_7=bifurcádoslos; imp_i2p_acc_1=bifurcadme; imp_i2p_acc_3=bifurcadla; imp_i2p_acc_3=bifurcadlo; imp_i2p_acc_4=bifurcadnos; imp_i2p_acc_5=bifurcaos; imp_i2p_acc_6=bifurcadlas; imp_i2p_acc_6=bifurcadlos; imp_i2p_acc_7=bifurcados; imp_i2p_dat_1=bifurcadme; imp_i2p_dat_3=bifurcadle; imp_i2p_dat_4=bifurcadnos; imp_i2p_dat_5=bifurcaos; imp_i2p_dat_6=bifurcadles; imp_i2s_acc-dat_1=bifúrcámela; imp_i2s_acc-dat_1=bifúrcámelas; imp_i2s_acc-dat_1=bifúrcámelo; imp_i2s_acc-dat_1=bifúrcámelos; imp_i2s_acc-dat_2=bifúrcátela; imp_i2s_acc-dat_2=bifúrcátelas; imp_i2s_acc-dat_2=bifúrcátelo; imp_i2s_acc-dat_2=bifúrcátelos; imp_i2s_acc-dat_4=bifúrcánosla; imp_i2s_acc-dat_4=bifúrcánoslas; imp_i2s_acc-dat_4=bifúrcánoslo; imp_i2s_acc-dat_4=bifúrcánoslos; imp_i2s_acc_1=bifúrcame; imp_i2s_acc_2=bifúrcate; imp_i2s_acc_3=bifúrcala; imp_i2s_acc_3=bifúrcalo; imp_i2s_acc_4=bifúrcanos; imp_i2s_acc_6=bifúrcalas; imp_i2s_acc_6=bifúrcalos; imp_i2s_dat_1=bifúrcame; imp_i2s_dat_2=bifúrcate; imp_i2s_dat_3=bifúrcale; imp_i2s_dat_4=bifúrcanos; imp_i2s_dat_6=bifúrcales; inf_acc-dat_1=bifurcármela; inf_acc-dat_1=bifurcármelas; inf_acc-dat_1=bifurcármelo; inf_acc-dat_1=bifurcármelos; inf_acc-dat_2=bifurcártela; inf_acc-dat_2=bifurcártelas; inf_acc-dat_2=bifurcártelo; inf_acc-dat_2=bifurcártelos; inf_acc-dat_3=bifurcársela; inf_acc-dat_3=bifurcárselas; inf_acc-dat_3=bifurcárselo; inf_acc-dat_3=bifurcárselos; inf_acc-dat_4=bifurcárnosla; inf_acc-dat_4=bifurcárnoslas; inf_acc-dat_4=bifurcárnoslo; inf_acc-dat_4=bifurcárnoslos; inf_acc-dat_5=bifurcárosla; inf_acc-dat_5=bifurcároslas; inf_acc-dat_5=bifurcároslo; inf_acc-dat_5=bifurcároslos; inf_acc-dat_6=bifurcársela; inf_acc-dat_6=bifurcárselas; inf_acc-dat_6=bifurcárselo; inf_acc-dat_6=bifurcárselos; inf_acc-dat_7=bifurcársela; inf_acc-dat_7=bifurcárselas; inf_acc-dat_7=bifurcárselo; inf_acc-dat_7=bifurcárselos; inf_acc_1=bifurcarme; inf_acc_2=bifurcarte; inf_acc_3=bifurcarla; inf_acc_3=bifurcarlo; inf_acc_3=bifurcarse; inf_acc_4=bifurcarnos; inf_acc_5=bifurcaros; inf_acc_6=bifurcarlas; inf_acc_6=bifurcarlos; inf_acc_6=bifurcarse; inf_acc_7=bifurcarse; inf_dat_1=bifurcarme; inf_dat_2=bifurcarte; inf_dat_3=bifurcarle; inf_dat_3=bifurcarse; inf_dat_4=bifurcarnos; inf_dat_5=bifurcaros; inf_dat_6=bifurcarles; inf_dat_6=bifurcarse
  gloss: to bifurcate, to cause to fork off
    q: transitive
  gloss: To diverge, fork off
    q: reflexive
_____
bifurcarse
pos: v
  meta: {{es-verb|bifurc|ar|pret=bifurqué|ref=y}} {{es-conj-ar|bifur|p=-car|ref=1|combined=1}}
  forms: 1=bifurcarse; 10=bifurca; 11=bifurcamos; 12=bifurcáis; 13=bifurcan; 14=bifurcaba; 15=bifurcabas; 16=bifurcaba; 17=bifurcábamos; 18=bifurcabais; 19=bifurcaban; 2=bifurcándose; 20=bifurqué; 21=bifurcaste; 22=bifurcó; 23=bifurcamos; 24=bifurcasteis; 25=bifurcaron; 26=bifurcaré; 27=bifurcarás; 28=bifurcará; 29=bifurcaremos; 3=bifurcado; 30=bifurcaréis; 31=bifurcarán; 32=bifurcaría; 33=bifurcarías; 34=bifurcaría; 35=bifurcaríamos; 36=bifurcaríais; 37=bifurcarían; 38=bifurque; 39=bifurques; 4=bifurcada; 40=bifurqués; 41=bifurque; 42=bifurquemos; 43=bifurquéis; 44=bifurquen; 45=bifurcara; 46=bifurcaras; 47=bifurcara; 48=bifurcáramos; 49=bifurcarais; 5=bifurcados; 50=bifurcaran; 51=bifurcase; 52=bifurcases; 53=bifurcase; 54=bifurcásemos; 55=bifurcaseis; 56=bifurcasen; 57=bifurcare; 58=bifurcares; 59=bifurcare; 6=bifurcadas; 60=bifurcáremos; 61=bifurcareis; 62=bifurcaren; 63=bifurcate; 64=-; 65=bifurque; 66=bifurquemos; 67=bifurcaos; 68=bifurquen; 69=bifurques; 7=bifurco; 70=bifurque; 71=bifurquemos; 72=bifurquéis; 73=bifurquen; 8=bifurcas; 9=bifurcás; ger_acc-dat_1=bifurcándómela; ger_acc-dat_1=bifurcándómelas; ger_acc-dat_1=bifurcándómelo; ger_acc-dat_1=bifurcándómelos; ger_acc-dat_2=bifurcándótela; ger_acc-dat_2=bifurcándótelas; ger_acc-dat_2=bifurcándótelo; ger_acc-dat_2=bifurcándótelos; ger_acc-dat_3=bifurcándósela; ger_acc-dat_3=bifurcándóselas; ger_acc-dat_3=bifurcándóselo; ger_acc-dat_3=bifurcándóselos; ger_acc-dat_4=bifurcándónosla; ger_acc-dat_4=bifurcándónoslas; ger_acc-dat_4=bifurcándónoslo; ger_acc-dat_4=bifurcándónoslos; ger_acc-dat_5=bifurcándóosla; ger_acc-dat_5=bifurcándóoslas; ger_acc-dat_5=bifurcándóoslo; ger_acc-dat_5=bifurcándóoslos; ger_acc-dat_6=bifurcándósela; ger_acc-dat_6=bifurcándóselas; ger_acc-dat_6=bifurcándóselo; ger_acc-dat_6=bifurcándóselos; ger_acc-dat_7=bifurcándósela; ger_acc-dat_7=bifurcándóselas; ger_acc-dat_7=bifurcándóselo; ger_acc-dat_7=bifurcándóselos; ger_acc_1=bifurcándome; ger_acc_2=bifurcándote; ger_acc_3=bifurcándola; ger_acc_3=bifurcándolo; ger_acc_3=bifurcándose; ger_acc_4=bifurcándonos; ger_acc_5=bifurcándoos; ger_acc_6=bifurcándolas; ger_acc_6=bifurcándolos; ger_acc_6=bifurcándose; ger_acc_7=bifurcándose; ger_dat_1=bifurcándome; ger_dat_2=bifurcándote; ger_dat_3=bifurcándole; ger_dat_3=bifurcándose; ger_dat_4=bifurcándonos; ger_dat_5=bifurcándoos; ger_dat_6=bifurcándoles; ger_dat_6=bifurcándose; imp_1p_acc-dat_2=bifurquémóstela; imp_1p_acc-dat_2=bifurquémóstelas; imp_1p_acc-dat_2=bifurquémóstelo; imp_1p_acc-dat_2=bifurquémóstelos; imp_1p_acc-dat_4=bifurquémónosla; imp_1p_acc-dat_4=bifurquémónoslas; imp_1p_acc-dat_4=bifurquémónoslo; imp_1p_acc-dat_4=bifurquémónoslos; imp_1p_acc-dat_5=bifurquémóosla; imp_1p_acc-dat_5=bifurquémóoslas; imp_1p_acc-dat_5=bifurquémóoslo; imp_1p_acc-dat_5=bifurquémóoslos; imp_1p_acc_2=bifurquémoste; imp_1p_acc_3=bifurquémosla; imp_1p_acc_3=bifurquémoslo; imp_1p_acc_4=bifurquémonos; imp_1p_acc_5=bifurquémoos; imp_1p_acc_6=bifurquémoslas; imp_1p_acc_6=bifurquémoslos; imp_1p_dat_2=bifurquémoste; imp_1p_dat_3=bifurquémosle; imp_1p_dat_4=bifurquémonos; imp_1p_dat_5=bifurquémoos; imp_1p_dat_6=bifurquémosles; imp_f2p_acc-dat_1=bifúrquénmela; imp_f2p_acc-dat_1=bifúrquénmelas; imp_f2p_acc-dat_1=bifúrquénmelo; imp_f2p_acc-dat_1=bifúrquénmelos; imp_f2p_acc-dat_4=bifúrquénnosla; imp_f2p_acc-dat_4=bifúrquénnoslas; imp_f2p_acc-dat_4=bifúrquénnoslo; imp_f2p_acc-dat_4=bifúrquénnoslos; imp_f2p_acc-dat_6=bifúrquénsela; imp_f2p_acc-dat_6=bifúrquénselas; imp_f2p_acc-dat_6=bifúrquénselo; imp_f2p_acc-dat_6=bifúrquénselos; imp_f2p_acc-dat_7=bifúrquénsela; imp_f2p_acc-dat_7=bifúrquénselas; imp_f2p_acc-dat_7=bifúrquénselo; imp_f2p_acc-dat_7=bifúrquénselos; imp_f2p_acc_1=bifúrquenme; imp_f2p_acc_3=bifúrquenla; imp_f2p_acc_3=bifúrquenlo; imp_f2p_acc_4=bifúrquennos; imp_f2p_acc_6=bifúrquenlas; imp_f2p_acc_6=bifúrquenlos; imp_f2p_acc_6=bifúrquense; imp_f2p_acc_7=bifúrquense; imp_f2p_dat_1=bifúrquenme; imp_f2p_dat_3=bifúrquenle; imp_f2p_dat_4=bifúrquennos; imp_f2p_dat_6=bifúrquenles; imp_f2p_dat_6=bifúrquense; imp_f2s_acc-dat_1=bifúrquémela; imp_f2s_acc-dat_1=bifúrquémelas; imp_f2s_acc-dat_1=bifúrquémelo; imp_f2s_acc-dat_1=bifúrquémelos; imp_f2s_acc-dat_3=bifúrquésela; imp_f2s_acc-dat_3=bifúrquéselas; imp_f2s_acc-dat_3=bifúrquéselo; imp_f2s_acc-dat_3=bifúrquéselos; imp_f2s_acc-dat_4=bifúrquénosla; imp_f2s_acc-dat_4=bifúrquénoslas; imp_f2s_acc-dat_4=bifúrquénoslo; imp_f2s_acc-dat_4=bifúrquénoslos; imp_f2s_acc-dat_7=bifúrquésela; imp_f2s_acc-dat_7=bifúrquéselas; imp_f2s_acc-dat_7=bifúrquéselo; imp_f2s_acc-dat_7=bifúrquéselos; imp_f2s_acc_1=bifúrqueme; imp_f2s_acc_3=bifúrquela; imp_f2s_acc_3=bifúrquelo; imp_f2s_acc_3=bifúrquese; imp_f2s_acc_4=bifúrquenos; imp_f2s_acc_6=bifúrquelas; imp_f2s_acc_6=bifúrquelos; imp_f2s_acc_7=bifúrquese; imp_f2s_dat_1=bifúrqueme; imp_f2s_dat_3=bifúrquele; imp_f2s_dat_3=bifúrquese; imp_f2s_dat_4=bifúrquenos; imp_f2s_dat_6=bifúrqueles; imp_i2p_acc-dat_1=bifurcaósmela; imp_i2p_acc-dat_1=bifurcaósmelas; imp_i2p_acc-dat_1=bifurcaósmelo; imp_i2p_acc-dat_1=bifurcaósmelos; imp_i2p_acc-dat_4=bifurcaósnosla; imp_i2p_acc-dat_4=bifurcaósnoslas; imp_i2p_acc-dat_4=bifurcaósnoslo; imp_i2p_acc-dat_4=bifurcaósnoslos; imp_i2p_acc-dat_5=bifurcaóosla; imp_i2p_acc-dat_5=bifurcaóoslas; imp_i2p_acc-dat_5=bifurcaóoslo; imp_i2p_acc-dat_5=bifurcaóoslos; imp_i2p_acc-dat_7=bifurcaósosla; imp_i2p_acc-dat_7=bifurcaósoslas; imp_i2p_acc-dat_7=bifurcaósoslo; imp_i2p_acc-dat_7=bifurcaósoslos; imp_i2p_acc_1=bifurcaosme; imp_i2p_acc_3=bifurcaosla; imp_i2p_acc_3=bifurcaoslo; imp_i2p_acc_4=bifurcaosnos; imp_i2p_acc_5=bifurcaoos; imp_i2p_acc_6=bifurcaoslas; imp_i2p_acc_6=bifurcaoslos; imp_i2p_acc_7=bifurcaosos; imp_i2p_dat_1=bifurcaosme; imp_i2p_dat_3=bifurcaosle; imp_i2p_dat_4=bifurcaosnos; imp_i2p_dat_5=bifurcaoos; imp_i2p_dat_6=bifurcaosles; imp_i2s_acc-dat_1=bifurcátémela; imp_i2s_acc-dat_1=bifurcátémelas; imp_i2s_acc-dat_1=bifurcátémelo; imp_i2s_acc-dat_1=bifurcátémelos; imp_i2s_acc-dat_2=bifurcátétela; imp_i2s_acc-dat_2=bifurcátételas; imp_i2s_acc-dat_2=bifurcátételo; imp_i2s_acc-dat_2=bifurcátételos; imp_i2s_acc-dat_4=bifurcáténosla; imp_i2s_acc-dat_4=bifurcáténoslas; imp_i2s_acc-dat_4=bifurcáténoslo; imp_i2s_acc-dat_4=bifurcáténoslos; imp_i2s_acc_1=bifurcáteme; imp_i2s_acc_2=bifurcátete; imp_i2s_acc_3=bifurcátela; imp_i2s_acc_3=bifurcátelo; imp_i2s_acc_4=bifurcátenos; imp_i2s_acc_6=bifurcátelas; imp_i2s_acc_6=bifurcátelos; imp_i2s_dat_1=bifurcáteme; imp_i2s_dat_2=bifurcátete; imp_i2s_dat_3=bifurcátele; imp_i2s_dat_4=bifurcátenos; imp_i2s_dat_6=bifurcáteles; inf_acc-dat_1=bifurcármela; inf_acc-dat_1=bifurcármelas; inf_acc-dat_1=bifurcármelo; inf_acc-dat_1=bifurcármelos; inf_acc-dat_2=bifurcártela; inf_acc-dat_2=bifurcártelas; inf_acc-dat_2=bifurcártelo; inf_acc-dat_2=bifurcártelos; inf_acc-dat_3=bifurcársela; inf_acc-dat_3=bifurcárselas; inf_acc-dat_3=bifurcárselo; inf_acc-dat_3=bifurcárselos; inf_acc-dat_4=bifurcárnosla; inf_acc-dat_4=bifurcárnoslas; inf_acc-dat_4=bifurcárnoslo; inf_acc-dat_4=bifurcárnoslos; inf_acc-dat_5=bifurcárosla; inf_acc-dat_5=bifurcároslas; inf_acc-dat_5=bifurcároslo; inf_acc-dat_5=bifurcároslos; inf_acc-dat_6=bifurcársela; inf_acc-dat_6=bifurcárselas; inf_acc-dat_6=bifurcárselo; inf_acc-dat_6=bifurcárselos; inf_acc-dat_7=bifurcársela; inf_acc-dat_7=bifurcárselas; inf_acc-dat_7=bifurcárselo; inf_acc-dat_7=bifurcárselos; inf_acc_1=bifurcarme; inf_acc_2=bifurcarte; inf_acc_3=bifurcarla; inf_acc_3=bifurcarlo; inf_acc_3=bifurcarse; inf_acc_4=bifurcarnos; inf_acc_5=bifurcaros; inf_acc_6=bifurcarlas; inf_acc_6=bifurcarlos; inf_acc_6=bifurcarse; inf_acc_7=bifurcarse; inf_dat_1=bifurcarme; inf_dat_2=bifurcarte; inf_dat_3=bifurcarle; inf_dat_3=bifurcarse; inf_dat_4=bifurcarnos; inf_dat_5=bifurcaros; inf_dat_6=bifurcarles; inf_dat_6=bifurcarse
  gloss: to split, divide, fork, branch off
"""

    expected = """\
_____
00-database-info
##:name:Wiktionary (es-en)
##:url:en.wiktionary.org
##:pagecount:3
##:formcount:276
##:description:test
_____
bifurcad|bifurcadla|bifurcadlas|bifurcadle|bifurcadles|bifurcadlo|bifurcadlos|bifurcadme|bifurcadnos|bifurcando|bifurcar|bifurcá|bifurcádmela|bifurcádmelas|bifurcádmelo|bifurcádmelos|bifurcádnosla|bifurcádnoslas|bifurcádnoslo|bifurcádnoslos|bifurcádosla|bifurcádoslas|bifurcádoslo|bifurcádoslos|bifurcáosla|bifurcáoslas|bifurcáoslo|bifurcáoslos|bifúrcala|bifúrcalas|bifúrcale|bifúrcales|bifúrcalo|bifúrcalos|bifúrcame|bifúrcanos|bifúrcate|bifúrcámela|bifúrcámelas|bifúrcámelo|bifúrcámelos|bifúrcánosla|bifúrcánoslas|bifúrcánoslo|bifúrcánoslos|bifúrcátela|bifúrcátelas|bifúrcátelo|bifúrcátelos
bifurcar (v)
1. (transitive) to bifurcate, to cause to fork off
2. (reflexive) To diverge, fork off
_____
bifurca|bifurcaba|bifurcabais|bifurcaban|bifurcabas|bifurcada|bifurcadas|bifurcado|bifurcados|bifurcamos|bifurcan|bifurcaos|bifurcara|bifurcarais|bifurcaran|bifurcaras|bifurcare|bifurcareis|bifurcaremos|bifurcaren|bifurcares|bifurcarla|bifurcarlas|bifurcarle|bifurcarles|bifurcarlo|bifurcarlos|bifurcarme|bifurcarnos|bifurcaron|bifurcaros|bifurcarse|bifurcarte|bifurcará|bifurcarán|bifurcarás|bifurcaré|bifurcaréis|bifurcaría|bifurcaríais|bifurcaríamos|bifurcarían|bifurcarías|bifurcas|bifurcase|bifurcaseis|bifurcasen|bifurcases|bifurcaste|bifurcasteis|bifurco|bifurcábamos|bifurcáis|bifurcándola|bifurcándolas|bifurcándole|bifurcándoles|bifurcándolo|bifurcándolos|bifurcándome|bifurcándonos|bifurcándoos|bifurcándose|bifurcándote|bifurcándómela|bifurcándómelas|bifurcándómelo|bifurcándómelos|bifurcándónosla|bifurcándónoslas|bifurcándónoslo|bifurcándónoslos|bifurcándóosla|bifurcándóoslas|bifurcándóoslo|bifurcándóoslos|bifurcándósela|bifurcándóselas|bifurcándóselo|bifurcándóselos|bifurcándótela|bifurcándótelas|bifurcándótelo|bifurcándótelos|bifurcáramos|bifurcáremos|bifurcármela|bifurcármelas|bifurcármelo|bifurcármelos|bifurcárnosla|bifurcárnoslas|bifurcárnoslo|bifurcárnoslos|bifurcárosla|bifurcároslas|bifurcároslo|bifurcároslos|bifurcársela|bifurcárselas|bifurcárselo|bifurcárselos|bifurcártela|bifurcártelas|bifurcártelo|bifurcártelos|bifurcás|bifurcásemos|bifurcó|bifurque|bifurquemos|bifurquen|bifurques|bifurqué|bifurquéis|bifurquémonos|bifurquémoos|bifurquémosla|bifurquémoslas|bifurquémosle|bifurquémosles|bifurquémoslo|bifurquémoslos|bifurquémoste|bifurquémónosla|bifurquémónoslas|bifurquémónoslo|bifurquémónoslos|bifurquémóosla|bifurquémóoslas|bifurquémóoslo|bifurquémóoslos|bifurquémóstela|bifurquémóstelas|bifurquémóstelo|bifurquémóstelos|bifurqués|bifúrquela|bifúrquelas|bifúrquele|bifúrqueles|bifúrquelo|bifúrquelos|bifúrqueme|bifúrquenla|bifúrquenlas|bifúrquenle|bifúrquenles|bifúrquenlo|bifúrquenlos|bifúrquenme|bifúrquennos|bifúrquenos|bifúrquense|bifúrquese|bifúrquémela|bifúrquémelas|bifúrquémelo|bifúrquémelos|bifúrquénmela|bifúrquénmelas|bifúrquénmelo|bifúrquénmelos|bifúrquénnosla|bifúrquénnoslas|bifúrquénnoslo|bifúrquénnoslos|bifúrquénosla|bifúrquénoslas|bifúrquénoslo|bifúrquénoslos|bifúrquénsela|bifúrquénselas|bifúrquénselo|bifúrquénselos|bifúrquésela|bifúrquéselas|bifúrquéselo|bifúrquéselos
bifurcar (v)
1. (transitive) to bifurcate, to cause to fork off
2. (reflexive) To diverge, fork off

bifurcarse (v)
1. to split, divide, fork, branch off
_____
bifurcaoos|bifurcaosla|bifurcaoslas|bifurcaosle|bifurcaosles|bifurcaoslo|bifurcaoslos|bifurcaosme|bifurcaosnos|bifurcaosos|bifurcate|bifurcaóosla|bifurcaóoslas|bifurcaóoslo|bifurcaóoslos|bifurcaósmela|bifurcaósmelas|bifurcaósmelo|bifurcaósmelos|bifurcaósnosla|bifurcaósnoslas|bifurcaósnoslo|bifurcaósnoslos|bifurcaósosla|bifurcaósoslas|bifurcaósoslo|bifurcaósoslos|bifurcátela|bifurcátelas|bifurcátele|bifurcáteles|bifurcátelo|bifurcátelos|bifurcáteme|bifurcátenos|bifurcátete|bifurcátémela|bifurcátémelas|bifurcátémelo|bifurcátémelos|bifurcáténosla|bifurcáténoslas|bifurcáténoslo|bifurcáténoslos|bifurcátétela|bifurcátételas|bifurcátételo|bifurcátételos
bifurcarse (v)
1. to split, divide, fork, branch off
"""
    print("\n".join(exporter.export(wordlist_data.splitlines(), None, "es", "test")))
    assert "\n".join(exporter.export(wordlist_data.splitlines(), None, "es", "test")) == expected.strip()

