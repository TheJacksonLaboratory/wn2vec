import nltk
import ssl
from typing import List
from collections import Counter
# to disable SSL to be able to download worldnet
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download("wordnet")

from nltk.corpus import wordnet as wn # Import Wordnet
from collections import Counter  # Import Counter
import numpy as np
import csv

"""
Arragnement(): takes a list and returns list of sorted unique variables according to frequency 
            @argument: 'list' a list of data set 
            @return: 'unique' a list of sorted variables in order of frequency  
            i.e the first element is a unique word which as a high frequency
"""
def sort_words_by_count(list: List[str]) -> List[str]:
    result = sorted(list, key = list.count, reverse = True) # sorting on basis of frequency of elements
    used = set()
    unique = [x for x in result if x not in used and (used.add(x) or True)]  #arrange according to unique characters
    return(unique)


def sort_words_by_count2(list: List[str]) -> List[str]:
    counter = Counter(list)
    # sort words (keys) by their frequency in 'list' (value)
    sorted_keys = [pair[0] for pair in sorted(counter.items(), key=lambda item: item[1], reverse=True)]
    return sorted_keys



"""
synonym(): Takes a word and prints its synonyms in form of a list (synset) using wordnet 
        @argument: 'word' a string or any variable part of the dataset  
        @return: 'synonyms' a list of synonyms of the words 
"""
def synonym(word):
    synonyms = []
    for syn in wn.synsets(word):
        #for l in syn.lemmas():
        #    synonyms.append(l.name())
        synonyms.extend([l.name() for l in syn.lemmas()])
    return synonyms

"""
dictCreate(): Creates a dictionary from the whole data set, 
they keys are in order of their frequency words and the values 
are synonyms of keys form synset   
        @argument: 'unique' a list of unique variables from the wholed dataset in order of their frequency
        @return: 'dictionary' a dictionary of all the variables in the dataset, the keys are the unique variables with high frequency, and values are key's synonym
"""
def dictCreate(unique: List[str]):
    dictionary = {} 
    synonym2keyword_d = {}
    for word in unique:
        #synonym2keyword_d[word] = word
        for syn in synonym(word):
            if syn in synonym2keyword_d : continue
            synonym2keyword_d[syn] = word
    return synonym2keyword_d
   # i = 0
    #while i < len(unique):
     # if unique[i] in dictionary:
      #  i = i+1
      #else:
      #  for x in range(0, len(synonym(unique[i]))):
      #    dictionary[synonym(unique[i])[x]] = unique[i]
      #  i = i+1
    #return dictionary

"""
giveValue(): Takes a word and dictionary and returns the value of the word in the dictionary  
        @argument: 'word' a string or any variable part of the dataset to be replaced with the dictionary key if it is not a key itself
                    "dictList" a dictionary created with the whole dataset   
        @return: 'Key_lis[x]' a string of a unique value of the word in the dictionary 
"""
def giveValue(word, dictList):
    return dictList[word]

"""
replace_data_set(): Replaces the variable in dataset with their synonyms from the dictionary  
        @argument: 'data_list' a list of all the data_set in form of a list 
                    "dictionary" a dictionary created with the whole dataset   
        @return: 'data_list' a new list with the whole list where the words were replaced by their synonyms 

"""

def replace_data_set(data_list,dictionary):
  for i in range(len(data_list)):
    if data_list[i] in dictionary:
        data_list[i]= giveValue(data_list[i], dictionary)
    else:
        continue
      
  return(data_list)