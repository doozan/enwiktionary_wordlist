import re

from enwiktionary_templates import expand_templates
import enwiktionary_parser as wtparser

verb_qualifiers = {
    "transitive": "t",
    "reflexive": "r",
    "intransitive": "i",
    "pronominal": "p",
    "ambitransitive": "it",
}

def extract_verb_qualifiers(all_qualifiers):
    """ Removes verb usage qualifiers from list of provided qualifers
    Returns a tuple (verb_type, [remaining_qualifiers])
    where verb type is an abbreviation generated from the qualifiers """

    qualifiers = []
    usage = "v"

    for q in all_qualifiers:
        if q in verb_qualifiers:
             usage += verb_qualifiers[q]
        else:
            qualifiers.append(q)

    return (usage, qualifiers)

def make_qualification(lang_id, title, qualifiers, strip_verb_qualifiers=False):
    """ Convert a list of qualifiers to label """

    if strip_verb_qualifiers:
        print("extracting", title, qualifiers, strip_verb_qualifiers)
        pos, qualifiers = extract_verb_qualifiers(qualifiers)

    template_str = "{{lb|" + lang_id + "|" + "|".join(qualifiers) + "}}"
    qualified = wiki_to_text(template_str, title)
    if not qualified:
        return ""

    # Strip ()
    return qualified[1:-1]

def make_gendertag(all_genders):
    genders = []
    for gender in all_genders:
        gender = gender.replace("-", "")
        if gender not in genders:
            genders.append(gender)
    return "".join(genders)

def make_pos_tag(word, qualifiers):
    pos = word.shortpos
    gendertag = make_gendertag(word.genders)

    if pos in ["n","prop"] and gendertag:
        return "{" + gendertag + "}"
    if pos == "v":
        pos, _ = extract_verb_qualifiers(qualifiers)

    return "{" + pos + "}"

def wiki_to_text( wikitext, title):
    wikt = wtparser.parse(wikitext)

    expand_templates(wikt, title)

    # Reparse and expand links
    wikt = wtparser.parse(str(wikt))
    for wikilink in wikt.ifilter_wikilinks():
        display = wikilink.text if wikilink.text else wikilink.title
        wikt.replace(wikilink, display)


    # Remove comments
    for comment in wikt.ifilter_comments():
        wikt.remove(comment)
    # Also remove any unterminated comments
    res = re.sub(r"<!--.*", "", str(wikt))

    res = re.sub("''+", "", res)
    res = re.sub(r"<sup>(.*?)</sup>", r"^\1", res)
    res = re.sub(r"<sub>(.*?)</sub>", r"\1", res)
    res = re.sub(r"<ref(.*?)</ref>", "", res)
    res = re.sub(r"<ref [^>]*/>", "", res)
    res = re.sub(r"<ref>.*", "", res)
    res = re.sub(r"&nbsp;", " ", res)
    res = re.sub(r"&ndash;", "-", res)
    return res

