import nltk
from nltk.corpus import wordnet as wn
from typing import List, Dict
#from wn_transformer import WordNetTransformer
import os
from collections import defaultdict
#nltk.download()

import os
import pandas as pd
import numpy as np
import math

def replaced_words_position(input, output):
  input_split = input.split('\t')
  output_split = output.split('\t')
  if (len(input_split) != 3) or (len(output_split) != 3):
    raise ValueError(f'Malformed marea line: {output}')
  input_abst_list = input_split[2].split()
  output_abst_list = output_split[2].split()

  if len(input_abst_list) != len(output_abst_list):
    raise ValueError(f'a word missing: {output}')

  for i in range(len(input_abst_list)):
    if input_abst_list[i] != output_abst_list[i]:
      print('Before: ', input_abst_list[i-1: i+2])
      print('After: ' ,output_abst_list[i-1: i+2])



input = '/Users/niyone/Documents/GitHub/wn2vec/tests/data/sample2abstracts.tsv'
output = '/Users/niyone/Documents/GitHub/wn2vec/tests/data/output2abstracts.tsv'



f = open(input)
y = open(output)

content = y.readlines()
count = 0
# print(content[1])
for input_line in f:
    word_replaced = replaced_words_position(input_line , content[count])
    count = count + 1
    print(word_replaced)
y.close()
f.close()