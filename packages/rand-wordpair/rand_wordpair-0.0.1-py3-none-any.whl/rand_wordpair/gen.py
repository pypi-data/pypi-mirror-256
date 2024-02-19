import re
import random
import hashlib
import secrets
import getpass
import nltk
from typing import Callable

is_setup = False
nouns : list[str] = []
adjs : list[str] = []

def setup() -> None:
    global is_setup, nouns, adjs
    if not is_setup:
        nltk.download('wordnet', quiet=True)
        from nltk.corpus import wordnet

        all_lower = re.compile(r'[a-z]+')
        nouns = sorted(w for s in wordnet.all_synsets(wordnet.NOUN)
                         for w in s.lemma_names()
                         if all_lower.fullmatch(w))
        adjs = sorted(w for s in wordnet.all_synsets(wordnet.ADJ)
                        for w in s.lemma_names()
                        if all_lower.fullmatch(w))
    is_setup = True

def gen_pair(sep: str = '-', choicer: Callable[[list[str]], str] = secrets.choice) -> str:
    """Generates a random adjective/noun pair, separated by sep."""
    setup()
    return f"{choicer(adjs)}{sep}{choicer(nouns)}"

def get_code(s: str) -> str:
    """Gets a code (random adj/noun pair) for the given source string."""
    old_seed = random.getstate()
    random.seed(hashlib.sha3_256(s.encode('utf8')).digest(), version=2)
    res = gen_pair(sep='_', choicer=random.choice)
    random.setstate(old_seed)
    return res

def show_user_code() -> None:
    """Displays the codeword pair for the current username."""
    user = getpass.getuser()
    code = get_code(user)
    print(f"code for {user}: {code}")
