import re

from enwiktionary_templates import expand_templates
import enwiktionary_parser as wtparser

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
