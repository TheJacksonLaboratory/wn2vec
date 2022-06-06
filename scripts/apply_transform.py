import nltk
from nltk.corpus import wordnet as wn
from typing import List, Dict
from wntransformer import WordNetTransformer
from transform import Transformer

import os
from collections import defaultdict


output = '/Users/niyone/Documents/GitHub/wn2vec/tests/data/output2abstracts.tsv'
test_marea = '/Users/niyone/Documents/GitHub/wn2vec/tests/data/sample2abstracts.tsv'


f = open(test_marea, "r")
y = open(output, 'a')
for line in f:
    print(line)
    #new_abstract = self.transform(line)
    y.writelines(line)
y.close()
f.close()
