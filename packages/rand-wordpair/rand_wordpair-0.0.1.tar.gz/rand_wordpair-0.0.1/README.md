# rand\_wordpair
Python module to generate a random pair of English words

# Usage

To get a random pair of words:

    from rand_wordpair import gen_pair
    print(gen_pair()) # different every time, e.g. sudsy-pickup

To get a username-based code (e.g. for SD212 homework):

    from rand_wordpair import show_user_code
    show_user_code() # prints code wordpair to the screen

# Dependencies

Uses [nltk](https://www.nltk.org/) for and the
[WordNet database](https://wordnet.princeton.edu/).

# Build instructions

Follow [this tutorial on packaging](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
and [this quickstart for setuptools](https://setuptools.pypa.io/en/latest/userguide/quickstart.html).

Pip/conda/mamba packages needed:

    build twine

To test:

    python3 test.py

To build:

    python3 -m build

To publish on pypi (requires account setup and
[api token](https://test.pypi.org/manage/account/token/)):

    python3 -m twine upload --repository testpypi dist/*
