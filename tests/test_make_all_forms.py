from enwiktionary_wordlist.make_all_forms import AllForms

def test_forms_text():

    test = """\
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
    expected = """\
testa,noun,testo
testas,noun,testo
testo,noun,testo
testos,noun,testo
testoz,noun,testo
"""

    assert "\n".join(AllForms(test.splitlines()).export()) == expected.strip()

def test_forms_redirection():

    test = """\
test1 {noun-meta} :: x
test1 {m} :: test
test2 {noun-meta} :: x
test2 {m} :: alternate form of "test1"
test3 {noun-meta} :: x
test3 {m} :: alternate form of "test2"
test4 {noun-meta} :: x
test4 {m} :: alternate form of "test3"
"""
    expected = """\
test1,noun,test1
test2,noun,test1
test3,noun,test1
test4,noun,test1
"""

    assert "\n".join(AllForms(test.splitlines()).export()) == expected.strip()
