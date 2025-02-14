Lines starting with a # are comments and must be ignored
All lines are stripped of all leading and trailing whitespace before being processed

Empty lines are ignored

All entries start with a single line containing 5 underscores
immediately followed by the lemma itself

```
_____
lemma
```

every non-comment, non-empyt line following a lemma must be in "key: value" format
key may contain only alphanumeric plus "_-"
the same key may be used multiple times, values are appended not overwritten
Any '\n' found in value will be converted to a newline unless it is escaped as '\\n'

any values following lemma and before pos: are applied to all pos entries

```
# keys
pos: pos (verb, noun, adj, etc)
# pos designates a new "word" (corresponding with a headword declaration in a pos section)
# There may be multiple pos sections
# Pos order should match the source wiktionary entry
  meta: meta
  # all keys following pos and before the first sense are applied to all senses
  g: (m, f, n, mp, fp) for nouns
  usage: blah
  ety: etymology
  gloss: gloss1
    q: qualifiers
    # Sense order must match the source wiktionary entry
    # sense modifiers are any values following sense until the next sense or pos value
    syn: aoeuaoe
    usage: note
    ex: this in an example sentence
       src: Author, Example Sentences (2025)
       eng: English translation of example sentenc
    _gloss: sub gloss
      usage: sub glosses use the same properties as glosses
  gloss: gloss2
  gloss: gloss3
pos: pos2
...
_____
word2
....
```
