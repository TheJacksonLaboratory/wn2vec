import nltk
from typing import List
from collections import Counter
import ssl
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


def sort_words_by_count(list: List[str]) -> List[str]:
    """
    takes a list and returns list of sorted unique variables according to frequency 
    sort words (keys) by their frequency in 'list' (value)
    :param list: a list of data set 
    :return: a list of sorted variables in order of frequency  
   
    """
    counter = Counter(list)
    sorted_keys = [pair[0] for pair in sorted(counter.items(), key=lambda item: item[1], reverse=True)]
    return sorted_keys


def synonym(word:str) -> List[str]:
    """
    Takes a word and prints its synonyms in form of a list (synset) using wordnet 
    :param word: a string or any variable part of the dataset  
    :return: 'synonyms' a list of synonyms of the words 

    """
    synonyms = []
    for syn in wn.synsets(word):
        synonyms.extend([l.name() for l in syn.lemmas()])
    return synonyms


def dictCreate(unique:List[str]) -> dict[str, str]:
    """
    Creates a dictionary from the whole data set, they keys are in order of their frequency words and the values are synonyms of keys form synset   
    :param unique: a list of unique variables from the wholed dataset in order of their frequency
    :return: 'dictionary' a dictionary of all the variables in the dataset, the keys are the unique variables with high frequency, and values are key's synonym
    
    """

    dictionary = {} 
    i = 0
    while i < len(unique):
      if unique[i] in dictionary:
        i = i+1
      else:
        for x in range(0, len(synonym(unique[i]))):
          dictionary[synonym(unique[i])[x]] = unique[i]
        i = i+1
    return dictionary


def giveValue(word: str, dictList: dict[str,str]) -> str:
    """
    Takes a word and dictionary and returns the value of the word in the dictionary  
    :param word: a string or any variable part of the dataset to be replaced with the dictionary key if it is not a key itself
    :param dictList: a dictionary created with the whole dataset   
    :return: 'Key_lis[x]' a string of a unique value of the word in the dictionary 

    """
    return dictList[word]



def replace_data_set(data_list: List[str],dictionary: dict[str,str]) -> List[str]:
    """
    Replaces the variable in dataset with their synonyms from the dictionary  
    :param data_list: a list of all the data_set in form of a list 
    :param dictionary: a dictionary created with the whole dataset   
    :return: 'data_list' a new list with the whole list where the words were replaced by their synonyms 

    """
    for i in range(len(data_list)):
        if data_list[i] in dictionary:
            data_list[i]= giveValue(data_list[i], dictionary)
    return(data_list)
