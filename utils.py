import re

from enwiktionary_templates import expand_templates
import mwparserfromhell as mwparser

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

    if pos == "n" and gendertag:
        return "{" + gendertag + "}"
    if pos == "prop" and gendertag:
        return "{prop} {" + gendertag + "}"
    if pos == "v":
        pos, _ = extract_verb_qualifiers(qualifiers)

    return "{" + pos + "}"

def wiki_to_text( wikitext, title, transclude_senses={}, template_cachedb=None, redirects={}):
    wiki = mwparser.parse(wikitext)

    expand_templates(wiki, title, transclude_senses, template_cachedb, redirects)

    # Reparse and expand links
    wiki = mwparser.parse(str(wiki))
    replacements = []
    for wikilink in wiki.ifilter_wikilinks():
        if any(wikilink.title.startswith(p) for p in ["File:", "Image:", "Category:"]):
            display = ""
        else:
            display = wikilink.text if wikilink.text else wikilink.title

        replacements.append((str(wikilink), str(display)))

    # Remove comments
    for comment in wiki.ifilter_comments():
        wiki.remove(comment)
    # Also remove any unterminated comments
    res = re.sub(r"<!--.*", "", str(wiki))

    for old, new in replacements:
        res = res.replace(old, new)

    res = re.sub("''+", "", res)
    res = re.sub(r"<sup>(.*?)</sup>", r"^\1", res, flags=re.DOTALL)
    res = re.sub(r"<sub>(.*?)</sub>", r"\1", res, flags=re.DOTALL)
    res = re.sub(r"<\s*blockquote.*?>(.*?)<\s*/\s*blockquote\s*>", r"\1", res, flags=re.DOTALL)
    res = re.sub(r"<ref [^>]*/>", "", res, flags=re.DOTALL)
    res = re.sub(r"<ref(.*?)</ref>", "", res, flags=re.DOTALL)
    res = re.sub(r"<br\s*(/)?\s*>", "\n", res, flags=re.DOTALL)
    res = re.sub(r"<ref>.*", "", res, flags=re.DOTALL)
    res = re.sub(r"&nbsp;", " ", res)
    res = re.sub(r"&ndash;", "-", res)
    return res


def make_language_pattern(lang_sections):
    """ Returns a regex pattern for matching given L2 sections
    lang_sections may be a list of section titles or a single string to match just one section
    """
    section_titles = lang_sections if isinstance(lang_sections, str) else "|".join(map(re.escape, lang_sections))
    start = fr"(^|\n)==\s*(?P<section_title>{section_titles})\s*==\s*\n"
    endings = r"==[^=]+==|----"
    newlines = r"(\n\s*)+"
    pattern = fr"{start}.*?(?={newlines}({endings})|$)"
    return re.compile(pattern, re.DOTALL)
