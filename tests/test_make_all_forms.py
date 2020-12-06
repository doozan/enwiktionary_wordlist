import enwiktionary_wordlist.make_all_forms as exporter

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
testa {noun} f=testo
testas {noun} fpl=testo
testo {noun} m=testo
testos {noun} pl=testo
testoz {noun} pl=testo
"""
    assert "\n".join(exporter.export(test.splitlines(), json=False)) == expected.strip()

def notest_forms_json():

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
{
"testa": {"noun": {"f": ["testo"]}},
"testas": {"noun": {"fpl": ["testo"]}},
"testo": {"noun": {"m": ["testo"]}},
"testos": {"noun": {"pl": ["testo"]}},
"testoz": {"noun": {"pl": ["testo"]}}
}
"""
    assert "\n".join(exporter.export(test.splitlines(), json=True)) == expected.strip()

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
test1 {noun} m=test1
test2 {noun} alt=test1
test3 {noun} alt=test1
test4 {noun} alt=test1
"""
    assert "\n".join(exporter.export(test.splitlines(), json=False)) == expected.strip()


