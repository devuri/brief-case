import numpy as np
from nltk.stem.porter import *
porter = PorterStemmer()

def unique_by_stem(keywords):
    '''
    Input a list of keywords and remove repeated keywords based on common stems.
    '''

    kwords_stems = [porter.stem(kw) for kw in keywords]

    kw_uniques_idx = []
    matched_word = ""

    for i, stem in enumerate(kwords_stems):
        if i == (len(kwords_stems) - 1):
            break

        if kwords_stems[i] == kwords_stems[i+1] and kwords_stems[i] == matched_word:
            next
        elif kwords_stems[i] == kwords_stems[i+1] and kwords_stems[i] != matched_word:
            matched_word = kwords_stems[i]
        else:
            kw_uniques_idx.append(i)

    keywords = [kw.upper() for kw in keywords[kw_uniques_idx]]

    return "    ||    ".join(keywords)
