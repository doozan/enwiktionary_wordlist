from setuptools import setup

setup(
    name='enwiktionary_wordlist',
    description='Library for handling wordlist data extracted from en.wiktionary.org',
    url='https://github.com/doozan/enwiktionary_wordlist',
    author='Jeff Doozan',
    author_email='github@doozan.com',
    license='GPL 3',
    packages=['enwiktionary_wordlist'],
    scripts=[
        'scripts/dump_lemmas',
        'scripts/make_extract',
        'scripts/make_wordlist',
        'scripts/make_all_forms',
        'scripts/wordlist_to_dictunformat',
        'scripts/kaikki_to_wordlist',
        ],
    install_requires=[
        'pywikibot',
        'enwiktionary_sectionparser @ git+https://github.com/doozan/enwiktionary_sectionparser.git',
        'enwiktionary_templates @ git+https://github.com/doozan/enwiktionary_templates.git',
    ],
)
