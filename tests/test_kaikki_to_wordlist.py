from enwiktionary_wordlist.kaikki_to_wordlist import KaikkiToWordlist as cls

def test_get_formtype():
    assert cls.get_formtype("plural of blah") == ('plural', 'blah')
    assert cls.get_formtype("simple past tense and past participle of argue") == ("simple past tense and past participle", "argue")
    assert cls.get_formtype("infinitive of hablar combined with me") == ('infinitive combined with me', 'hablar')
    assert cls.get_formtype("Third-person singular simple present indicative form of dictionary") == ('Third-person singular simple present indicative', 'dictionary')

