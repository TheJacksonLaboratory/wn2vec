
import nltk
from typing import List
from collections import Counter
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

class Replace:

    def __init__(self, list):
        self.list = list


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
        synonym2keyword_d = {}
        for word in unique:
            synonym2keyword_d[word] = word
            for syn in synonym(word):
                if syn in synonym2keyword_d : continue
                synonym2keyword_d[syn] = word
        return synonym2keyword_d

    def replace_data_set(data_list: List[str],dictionary: dict[str,str]) -> List[str]:
        """
        Replaces the variable in dataset with their synonyms from the dictionary  
        :param data_list: a list of all the data_set in form of a list 
        :param dictionary: a dictionary created with the whole dataset   
        :return: 'data_list' a new list with the whole list where the words were replaced by their synonyms 

        """
        for i in range(len(data_list)):
            if data_list[i] in dictionary:
               data_list[i]= dictionary[data_list[i]]
        return(data_list)
