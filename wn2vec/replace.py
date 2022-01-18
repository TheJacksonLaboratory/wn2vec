import nltk

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
def arrangement(list):
    result = sorted(list, key = list.count, reverse = True) # sorting on basis of frequency of elements
    used = set()
    unique = [x for x in result if x not in used and (used.add(x) or True)]  #arrange according to unique characters
    return(unique)

"""
synonym(): Takes a word and prints its synonyms in form of a list (synset) using wordnet 
        @argument: 'word' a string or any variable part of the dataset  
        @return: 'synonyms' a list of synonyms of the words 
"""
def synonym(word):
    synonyms = []
    for syn in wn.synsets(word):
        for l in syn.lemmas():
            synonyms.append(l.name())
    return synonyms

"""
dictCreate(): Creates a dictionary from the whole data set, they keys are in order of their frequency words and the values are synonyms of keys form synset   
        @argument: 'unique' a list of unique variables from the wholed dataset in order of their frequency
        @return: 'diction' a dictionary of all the variables in the dataset, the keys are the unique variables with high frequency, and values are key's synonym
"""
def dictCreate(unique):
  
    list_values = [] #create list of values
    dictionary = {} 
    dictionary[unique[0]]= synonym(unique[0])
    list_values.extend(synonym(unique[0]))
    for x in range(1,len(unique)):
        if(unique[x] in list_values): #check if the variable is the unique list is part of values (synonyms) of already existing dictionary, and skip that word 
            continue
        else:
            list_values.extend(synonym(unique[x])) 
            dictionary[unique[x]] = synonym(unique[x]) # adding a dicitonary 
    #print(diction)
    return dictionary

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

def replace_data_set(data_list):
  for i in range(len(data_list)):
    if data_list[i] in dictionary:
      continue
    else:
      data_list[i]= giveKey(data_list[i], dictionary)
  return(data_list)