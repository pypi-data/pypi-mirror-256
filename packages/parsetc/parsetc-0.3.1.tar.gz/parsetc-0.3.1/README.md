Parsing tools for Teochew phonetic spelling
===========================================

[![PyPI version shields.io](https://img.shields.io/pypi/v/parsetc.svg)](https://pypi.python.org/pypi/parsetc/)
![GitHub License](https://img.shields.io/github/license/learn-teochew/parsetc)

Parse and convert between different Teochew phonetic spelling schemes.


Input formats
-------------

 * Geng'dang Pêng'im 廣東拼音 (`gdpi`)
 * Gaginang Peng'im 家己儂拼音 (`ggn`)
 * Gaginang Peng'im with coda `-n` allowed (nasalization written with `ñ`
   instead) (`ggnn`)
 * Dieghv 潮語 (`dieghv`);
   [(source)](https://kahaani.github.io/gatian/appendix1/index.html)
 * Tie-tsiann-hue 潮正會, also known as Tie-lo 潮羅 (`tlo`);
   [(source)](http://library.hiteo.pw/book/wagpzbkv.html)
 * Duffus system (`duffus`), also known as Pe̍h-ūe-jī (PUJ);
   [(source)](https://archive.org/details/englishchinesev00duffgoog)


Output formats
--------------

`gdpi`, `ggnn`, `tlo`, `duffus`, plus:

 * Teochew Sinwenz (`sinwz`);
   [(source)](http://eresources.nlb.gov.sg/newspapers/Digitised/Page/nysp19391115-1.1.22)
 * Traditional initial-final categories (`15`) from 《彙集雅俗通十五音》 also
   known as 《擊木知音》, based on the analysis by 徐宇航
   「《擊木知音》音系之再研究」 (2014)


Orthographic conventions for input text
---------------------------------------

 * Text must be in lower case
 * Syllables may be written with or without tone numbers
 * Syllables may be combined into words for legibility, i.e. [word-segmented
   writing](https://en.wikipedia.org/wiki/Chinese_word-segmented_writing)
 * If syllables are combined into words, they must either have tone numbers
   (e.g. `diê5ziu1`), or use a syllable separator character (e.g. `diê-ziu` or
   `pêng'im`, or `diê5-ziu1`). The separator character is either a hyphen or
   single apostrophe. This is because of ambiguous parsings, e.g. `pê-ngi-m`
   instead of `pêng-im`, which in general can only be dealt with by usage
   frequency, which is not available.
 * If syllable separator characters are used, they must be used consistently.
   Mixing conventions may cause unexpected parsing errors.


Running the script
------------------

`parsetc` requires Python 3 and [`lark`](https://lark-parser.readthedocs.io/en/latest/) v1.1.

Install latest release with `pip` from PyPI:

```bash
pip install parsetc
```

If you are interested in latest development version, you can clone this
repository and checkout the `dev` branch, then install with `pip` from source
code:

```bash
pip install .
```

See help message:

```bash
parsetc --help
```

Input text is read from STDIN, no line breaks.

```bash
# output in Tie-lo
echo 'ua2 ain3 oh8 diê5ghe2, ain3 dan3 diê5ziu1 uê7.' | parsetc -i gdpi -o tlo
# all available output romanizations
echo 'ua2 ain3 oh8 diê5ghe2, ain3 dan3 diê5ziu1 uê7.' | parsetc -i gdpi --all
```

Testing with provided example text:

```bash
# Example with tone numbers but no syllable separators
cat examples/dieghv.tones.txt | parsetc -i dieghv --all
# Example with hyphens as syllable separators
cat examples/dieghv.sep.txt | parsetc -i dieghv --all
```
