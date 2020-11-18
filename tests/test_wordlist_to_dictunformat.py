import enwiktionary_wordlist.wordlist_to_dictunformat as exporter

def test_forms_text():
    exporter.all_pages = {}

    data = """\
asca {noun-meta} :: x
asca {noun-forms} :: pl=ascas
asca {m} [mycology] | teca :: ascus
asco {noun-meta} :: x
asco {noun-forms} :: pl=ascos
asco {m} :: disgust
asco {m} :: nausea
asco {noun-meta} :: x
asco {noun-forms} :: pl=ascos
asco {m} :: alternative form of "asca"
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
asca (m), plural "ascas"
1. (mycology) ascus
      Synonyms: teca
_____
asco|ascos
asca (m), plural "ascas"
1. (mycology) ascus
      Synonyms: teca

asco (m), plural "ascos"
1. disgust
2. nausea

asco (m), plural "ascos"
1. alternative form of "asca"
"""
    assert "\n".join(exporter.export(data.splitlines(), "es", "test")) == expected.strip()


def test_forms_bifurcar():
    exporter.all_pages = {}

    data = """\
bifurcar {verb-meta} :: x
bifurcar {verb-forms} :: 1=bifurcar; 10=bifurca; inf_dat_6=bifurcarse
bifurcar {vt} :: to bifurcate, to cause to fork off
bifurcar {vr} :: To diverge, fork off
bifurcarse {verb-meta} :: x
bifurcarse {verb-forms} :: 1=bifurcarse; 10=bifurca
bifurcarse {v} :: to split, divide, fork, branch off
"""

    expected = """\
_____
00-database-info
##:name:Wiktionary (es-en)
##:url:en.wiktionary.org
##:pagecount:2
##:formcount:3
##:description:test
_____
bifurcar
bifurcar (vt)
1. to bifurcate, to cause to fork off
2. To diverge, fork off
_____
bifurca|bifurcarse
bifurcar (vt)
1. to bifurcate, to cause to fork off
2. To diverge, fork off

bifurcarse (v)
1. to split, divide, fork, branch off
"""
    print("\n".join(exporter.export(data.splitlines(), "es", "test")))
    assert "\n".join(exporter.export(data.splitlines(), "es", "test")) == expected.strip()

