
# Read ten first ten lines of the data set and prints them 

from collections import defaultdict
import csv


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
  corpus_raw = row
  raw_sentences = row[2].split('.')
  sentences = []
  for sentence in raw_sentences:
    temp.extend(sentence.split())
dictionary = dictCreate(arrangement(temp)) 
tsv_file.close()

#Replace the variables in data set with the synonyms (synset ID) from the dictionary

tsv_file = open(marea_file)
read_tsv = csv.reader(tsv_file, delimiter="\t")
for row in read_tsv:
  corpus_raw = row
  raw_sentences = row[2].split('.')
  sentences = []
  for sentence in raw_sentences:
    sentences.append(sentence.split())
    for i in range(len(sentences)):
      if sentences[0][i] in dictionary:
        continue
      else:
        x = giveKey(sentences[i], dictionary)
        sentences[i] = x
  print(sentences[0])
tsv_file.close()