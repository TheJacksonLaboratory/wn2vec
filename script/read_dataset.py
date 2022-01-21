

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


#Create a dictionary using all the data set
tsv_file = open(marea_file)
read_tsv = csv.reader(tsv_file, delimiter="\t")
temp = []
for row in read_tsv:
    #corpus_raw = row
    raw_sentences = row[2].split('.')
    sentences = []
    for sentence in raw_sentences:
        temp.extend(sentence.split())
dictionary = dictCreate(sort_words_by_count(temp))
tsv_file.close()
print(dictionary)



#Replace the dictionary variables 

tsv_file = open(marea_file)
read_tsv = csv.reader(tsv_file, delimiter="\t")
for row in read_tsv:
    raw_sentences = row[2].split('.')
    sentences = []
    for sentence in raw_sentences:
        sentences.append(sentence.split())
        print(replace_data_set(sentences[0], dictionary)) #used sentences[0] because the dataset gives us a nested list 
tsv_file.close()