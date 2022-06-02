import nltk
from nltk.corpus import wordnet as wn
from typing import List, Dict
from wntransformer import WordNetTransformer
from transform import Transformer

import os
from collections import defaultdict


output = '/Users/niyone/Documents/GitHub/wn2vec/tests/data/output2abstracts.tsv'
test_marea = '/Users/niyone/Documents/GitHub/wn2vec/tests/data/sample2abstracts.tsv'

test1 = Transformer(test_marea, 2, output)