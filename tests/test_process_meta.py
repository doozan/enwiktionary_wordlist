import process_meta

def test_meta():
    meta = process_meta.Meta("testo {meta-noun} :: pl:'testos' f:'testa' fpl:'testas'")

    assert str(meta) == "testo {meta-noun} :: f:'testa' fpl:'testas' pl:'testos'"

    meta.add_form("old", "tezto")
    assert str(meta) == "testo {meta-noun} :: f:'testa' fpl:'testas' old:'tezto' pl:'testos'"


def test_get_form():
    form,lemma,remainder = process_meta.Word.get_form("feminine of testo")
    assert form == "f"
    assert lemma == "testo"
    assert remainder == ""

    form,lemma,remainder = process_meta.Word.get_form("feminine of abuelo, grandmother")
    assert form == "f"
    assert lemma == "abuelo"
    assert remainder == "grandmother"


def test_word():
    meta = process_meta.Word("testo {m} :: test")
    assert meta.word == "testo"
    assert meta.has_nonform_def == True
    assert meta.lemmas == {}

    meta = process_meta.Word("testa {f} :: feminine of testo")
    assert meta.word == "testa"
    assert meta.has_nonform_def == False
    assert meta.lemmas == {"testo": ["f"]}

    meta = process_meta.Word("testa {f} :: feminine of testo, test")
    assert meta.word == "testa"
    assert meta.has_nonform_def == True
    assert meta.lemmas == {"testo": ["f"]}


def test_process_meta():
    test = """\
testo {meta-noun} :: pl:'testos'
testo {m} :: test
testo {meta-noun} :: pl:'testoz'
testo {m} :: test2
testa {meta-noun} :: pl:'testas'
testa {f} :: feminine noun of testo
testoo {meta-noun} :: pl:'testoos'
testoo {m} :: misspelling of testo
test2 {m} :: misspelling of testo
test2 {m} :: testing
test3 {meta-noun} :: pl:'test3s'
test3 {m} :: test3 one
test3 {meta-noun} :: pl:'test3z'
test3 {m} :: test3 two
"""

    expected = """\
testo {meta-noun} :: f:'testa' fpl:'testas' pl:'testos' pl:'testoz' spell:'testoo' spell:'testoos' spell:'test2'
testo {m} :: test
testo {m} :: test2
test2 {m} :: misspelling of testo
test2 {m} :: testing
test3 {meta-noun} :: pl:'test3s' pl:'test3z'
test3 {m} :: test3 one
test3 {m} :: test3 two
"""

    assert "\n".join(process_meta.process_data(test.splitlines())) == expected.strip()

def test_create_meta():
    test = """\
i {conj} :: obsolete spelling of y
y {conj} :: and
"""

    expected = """\
y {meta-conj} :: old:'i'
y {conj} :: and\
"""

    assert "\n".join(process_meta.process_data(test.splitlines())) == expected.strip()



def test_duplicate_meta():
    test = """\
test {meta-noun} :: pl:'testz'
test {meta-noun} :: pl:'tests'
test {m} :: test
"""

    expected = """\
test {meta-noun} :: pl:'tests'
test {m} :: test\
"""

    assert "\n".join(process_meta.process_data(test.splitlines())) == expected.strip()



