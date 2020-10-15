Build dictionary from wiktionary dump

```
./make_dictionary.py --xml enwiktionary-latest-pages-articles.xml.bz2 --lang-id es --lang-section Spanish > es-en.raw.txt
./process_meta.py es-en.raw.txt > es-en.txt
```
