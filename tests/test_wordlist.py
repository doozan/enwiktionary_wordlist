import wordlist

def test_sense_parse_form_of():
    parse_form_of = wordlist.Sense.parse_form_of

    assert parse_form_of("grandmother, feminine noun of abuelo") == ("f", "abuelo", "grandmother,")
    assert parse_form_of("Son of a gun, alternative form of hijo de la gran puta") == ("alt", "hijo de la gran puta", "Son of a gun,")
    assert parse_form_of("alternative spelling of hijo de puta") == ("alt", "hijo de la gran puta", "Son of a gun,")

    #assert
    #assert parse_form_of("grandmother, feminine noun of abuelo") == ("f", "abuelo", "grandmother")
    #assert parse_form_of("Son of a gun, alternative form of hijo de la gran puta") == ("alt", "hijo de la gran puta", "Son of a gun")
    #assert parse_form_of("nonstandard form of 1.ª") == ("alt", "1.ª", "")
    #assert parse_form_of("alternative form of EE. UU") == ("alt", "EE. UU", "")
