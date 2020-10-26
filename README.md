Tools for creating, reading, and converting a wordlist from en.wiktionary.org


### Build a Spanish-English wordlist
```
./make_wordlist.py --xml enwiktionary-latest-pages-articles.xml.bz2 --lang-id es --lang-section Spanish > es-en.raw.txt
sort -s -d -k 1,1 -t"{" es-en.raw.txt > es-en.txt
```

### Convert Spanish-English wordlist to StarDict dictionary (requires [pyglossary](https://github.com/ilius/pyglossary))
```
wordlist_to_dictunformat.py es-en.txt --lang-id es > es-en.dictunformat
pyglossary es-en.dictunformat es-en.ifo -w merge_syns=1
```
