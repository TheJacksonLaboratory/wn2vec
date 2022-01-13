

# Read ten first ten lines of the data set and prints them 
from replace import*
from collections import defaultdict
import csv
from nltk.corpus import wordnet as wn # Import Wordnet
from collections import Counter  # Import Counter
import numpy as np

marea_file = "data/sample100abstracts.tsv"
counter = defaultdict(int)
tsv_file = open(marea_file)
read_tsv = csv.reader(tsv_file, delimiter="\t")
i = 0
for row in read_tsv:
  print(row)
  i+=1
  if i>10:
    break



dictionary_from_list(marea_file)
replace_dataSet(marea_file)