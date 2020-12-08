# Lines starting with a # are comments and must be ignored
  # All lines are stripped of all leading and trailing whitespace before being processed

# Empty lines are ignored
_____
word
# All entries start with a single line containing 5 underscores
# immediately followed by the word itself
# every line following word is in "key: value" format
# key may contain only alphanumeric plus "_-"
# the same key may be used multiple times, values are appended not overwritten
# Any '\n' found in value will be converted to newlines unless it is escaped as '\\n'

# any values following word and before pos: are applied to all pos entries
usenote: unclassed?

pos: pos (verb, noun, adj, etc)
# pos designates a new "word" (corresponding with a headword declaration in a pos section)
# There may me multiple pos sections
# Pos order should match the source wiktionary entry
  meta: meta
  # all keys following pos and before the first sense are applied to all senses
  g: (m, f, n, mp, fp) for nouns
  usenote: blah
  gloss: gloss1
    q: qualifiers
    # Sense order must match the source wiktionary entry
    # sense modifiers are any values following sense until the next sense or pos value
    syn: aoeuaoe
    use: abc
    use: 123
  gloss: gloss2
  gloss: gloss3
pos: pos2
...
_____
word2
....