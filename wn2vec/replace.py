import nltk

#nltk.download("wordnet")
from nltk.corpus import wordnet as wn # Import Wordnet
from collections import Counter  # Import Counter
import numpy as np


class Replace:
    def __init__(self, list):
        self.list = list

    """
    Arragnement(): takes a list and returns list of sorted unique variables according to frequency 
                urgument: 'list' a list of data set 
                return: 'unique' a list of sorted variables in order of frequency  
                i.e the first element is a unique word which as a high frequency
    """
    def arrangement(list):
        result = sorted(list, key = list.count, reverse = True) # sorting on basis of frequency of elements
        used = set()
        unique = [x for x in result if x not in used and (used.add(x) or True)]  #arrange according to unique characters
        return(unique)


    """
    synonym(): Takes a word and prints its synonyms in form of a list (synset) using wordnet 
            @urgument: 'word' a string or any variable part of the dataset  
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
            @urgument: 'unique' a list of unique variables from the wholed dataset in order of their frequency
            @return: 'diction' a dictionary of all the variables in the dataset, the keys are the unique variables with high frequency, and values are key's synonym
    """
    def dictCreate(unique):
        valueSynm = [] #create list of values
        keys = [unique[0]] #enter the first word from the list and its synonym
        values = [synonym(unique[0])]
        diction = dict(zip(keys, values)) 
        valueSynm.extend(synonym(unique[0]))
        for x in range(1,len(unique)):
            if(unique[x] in valueSynm): #check if the variable is the unique list is part of values (synonyms) of already existing dictionary, and skip that word 
                continue
            else:
                valueSynm.extend(synonym(unique[x])) 
                diction[unique[x]] = synonym(unique[x]) # adding a dicitonary 
        return diction
