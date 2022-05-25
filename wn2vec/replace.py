import nltk

nltk.download("wordnet")
from nltk.corpus import wordnet as wn # Import Wordnet
from collections import Counter  # Import Counter
import numpy as np
import csv





"""
giveKey(): Takes a word and dictionary and returns the key of the word in the dictionary  
        @argument: 'word' a string or any variable part of the dataset to be replaced with the dictionary key if it is not a key itself
                    "dictList" a dictionary created with the whole dataset   
        @return: 'Key_lis[x]' a string of a unique key of the word in the dictionary 
"""
def giveKey(word, dictList):
    key_list = []
    val_list = []
    key_list.extend(dictList.keys())
    val_list.extend(dictList.values())
    for x in range(len(val_list)):
        for j in range(len(val_list[x])):
            if(val_list[x][j] == word):
                return(key_list[x])

"""
replace_data_set(): Replaces the variable in dataset with their synonyms from the dictionary  
        @argument: 'data_list' a list of all the data_set in form of a list 
                    "dictionary" a dictionary created with the whole dataset   
        @return: 'data_list' a new list with the whole list where the words were replaced by their synonyms 

"""

def replace_data_set(data_list,dictionary):
  for i in range(len(data_list)):
    if data_list[i] in dictionary:
      continue
    else:
      data_list[i]= giveKey(data_list[i], dictionary)
  return(data_list)