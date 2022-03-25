import bz2
from enwiktionary_wordlist.wikiextract import *

sample_data = """\
_____page1:test:@12345_____
page1 text
_____page2_____
page2 text
page2 text
page2 text
"""

def test_iter_articles(tmp_path):

    items = list(WikiExtract.iter_articles(sample_data.splitlines(keepends=True)))
    assert items[0] == ("page1:test:@12345", "page1 text")
    assert items[0].title == "page1:test:@12345"
    assert items[0].text == "page1 text"

    assert items[1].title == "page2"
    assert items[1].text == "page2 text\npage2 text\npage2 text"


def test_iter_articles_from_bz2(tmp_path):

    testfile = f"{tmp_path}/test.bz2"
    with bz2.open(testfile, mode='wt', compresslevel=9) as outfile:
        outfile.write(sample_data)

    items = list(WikiExtract.iter_articles_from_bz2(testfile))
    assert items[0] == ("page1:test:@12345", "page1 text")
    assert items[0].title == "page1:test:@12345"
    assert items[0].text == "page1 text"

    assert items[1].title == "page2"
    assert items[1].text == "page2 text\npage2 text\npage2 text"

def test_iter_articles_from_txt(tmp_path):

    testfile = f"{tmp_path}/test.txt"
    with open(testfile, mode='w') as outfile:
        outfile.write(sample_data)

    items = list(WikiExtract.iter_articles_from_txt(testfile))
    assert items[0] == ("page1:test:@12345", "page1 text")
    assert items[0].title == "page1:test:@12345"
    assert items[0].text == "page1 text"

    assert items[1].title == "page2"
    assert items[1].text == "page2 text\npage2 text\npage2 text"


def test_iter_articles_with_revision_from_bz2(tmp_path):

    testfile = f"{tmp_path}/test.bz2"
    with bz2.open(testfile, mode='wt', compresslevel=9) as outfile:
        outfile.write(sample_data)

    items = list(WikiExtractWithRev.iter_articles_from_bz2(testfile))
    assert items[0] == ("page1:test", "page1 text", "12345")
    assert items[0].title == "page1:test"
    assert items[0].text == "page1 text"
    assert items[0].revision == "12345"

    assert items[1].title == "page2"
    assert items[1].text == "page2 text\npage2 text\npage2 text"
    assert items[1].revision == ""
