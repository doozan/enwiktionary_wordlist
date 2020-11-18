from ..sense import Sense

def run_test_sense_form(gloss, formtype, lemma, nonform):
    sense = Sense("x",None,gloss,None)
    assert sense.formtype == formtype
    assert sense.lemma == lemma
    assert sense.nonform == nonform

def test_sense():
    sense = Sense("m","rare","(mostly) obsolete form of fuego","syn1; syn2")
    assert sense.pos == "m"
    assert sense.qualifier == "rare"
    assert sense.synonyms == ["syn1", "syn2"]
    assert sense.formtype == "old"
    assert sense.lemma == "fuego"
    assert sense.nonform == "(mostly"

    run_test_sense_form("An alternative form of centollo", "alt", "centollo", "")
    run_test_sense_form("feminine noun of test word, testing", "f", "test word", "testing")
    run_test_sense_form("testing, alternative form of test word", "alt", "test word", "testing")
    run_test_sense_form("alternative spelling of test", "alt", "test", "")
    run_test_sense_form("nonstandard form of 1.ª", "alt", "1.ª", "")
    run_test_sense_form("alternative form of EE. UU", "alt", "EE. UU", "")
    run_test_sense_form("to defend. (obsolete spelling of defender)", "old", "defender", "to defend.")
    run_test_sense_form("given name: alternative spelling of Carina", "alt", "Carina", "given name")
    run_test_sense_form("obsolete form of se (as a dative pronoun)", "old", "se", "as a dative pronoun)")
