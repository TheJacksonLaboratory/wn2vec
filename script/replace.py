
from readline import replace_history_item
from turtle import st
import nltk
from typing import List, Dict
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
        sorted_words = Replace.sort_words_by_count(list)
        print(f"[INFO] {len(sorted_words)} sorted words")
        self._word_dict = Replace.dictCreate(sorted_words)
        self._replaced = self.replace_data_set(list)
        print("[INFO] Created word dictionary")

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def dictCreate(unique:List[str]) -> Dict[str, str]:
        """
        Creates a dictionary from the whole data set, they keys are in order of their frequency words and the values are synonyms of keys form synset   
        :param unique: a list of unique variables from the wholed dataset in order of their frequency
        :return: 'dictionary' a dictionary of all the variables in the dataset, the keys are the unique variables with high frequency, and values are key's synonym
        
        """
        dictionary = {} 
        for word in unique:
            if word in dictionary: continue
            else:
                for syn in Replace.synonym(word):
                    dictionary[syn] = word
        return dictionary 


    def replace_data_set(self, data_list: List[str]) -> List[str]:
        """
        Replaces the variable in dataset with their synonyms from the dictionary  
        :param data_list: a list of all the data_set in form of a list 
        :param dictionary: a dictionary created with the whole dataset   
        :return: 'data_list' a new list with the whole list where the words were replaced by their synonyms
        """
        if not isinstance(data_list, list):
            raise ValueError("replace_data_set accepts a list of strings")
        for i in range(len(data_list)):
            if data_list[i] in self._word_dict:
               data_list[i]= self._word_dict[data_list[i]]
        return(data_list)

    def get_word_dictionary(self) -> Dict:
        return self._word_dict

    def get_replaced_data(self):
        return self._replaced
