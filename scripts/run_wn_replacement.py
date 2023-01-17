
import nltk
from nltk.corpus import wordnet as wn
from typing import List, Dict
import os
import pandas as pd
import numpy as np
import statistics
import math

import os
from collections import defaultdict


class WordNetTransformer:
    
    """
    A class to represent a transofrmation of Pubmed Abstracts by reducing vocabulary size through replacing words with their synonyms from Wordnet.

    ...

    Attributes
    ----------
    marea_file: str
                path to .tsv file with abstracts from marea output
    output_file: str
                path to .tsv file that will contain the output after abstracts are transformed

    Methods
    -------
    get_word_to_synonyms_d(unique_words_list) -> Dict:
        Creates a dictionary from the whole data set, keys are unique words, and the values are synonyms of keys from synset

    get_highest_occuring_synonym(synonym_list) -> str:
        gets the highest occuring word in the synonym list of the whole dataset (all the bastracts being transformed)

    get_synonym_list(self, word: str) -> List:
        takes a word and returns a list of a word's synonyms using wordnet

    transform(line_abstract: str, _word_to_synonym_d) -> str:
        Replaces the variable in dataset with their synonyms from the dictionary
    
    calculate_mean_word_count(counter_d) -> int:
        calculates the mean of the frequencies of all the vocabilaries in the datasets

    """



    def __init__(self, marea_file, output_file) -> None:
        """
        Constructs all the necessary attributes for the  WordNetTransformer class
        
        Parameters
        ----------
        marea_file: str
                    path to .tsv file with abstracts from marea output
        output_file: str
                    path to .tsv file that will contain the output after abstracts are transformed
        """
        if not os.path.exists(marea_file):
            raise FileNotFoundError("Could not find marea file")
        if not os.path.exists(output_file):
            raise FileNotFoundError("Could not find output file")

        self._marea_file = marea_file
        self._output_file = output_file
        self._counter = defaultdict(int)
        # Get count of words in corpus
        with open(marea_file) as f:
            for line in f:
                columns = line.split('\t')
                if len(columns) != 3:
                    raise ValueError(f'Malformed marea line: {line}')
                payload = columns[2]  #columns[0]: pmid,  columns[1] year, columns[2] abstract text
                words = payload.split()
                for w in words:
                    self._counter[w] += 1

        # Create synonym dictionary with NLTK
        nltk.download("wordnet", download_dir = '../data')

        words_sorted_by_frequency = [k for k, v in
                                     sorted(self._counter.items(), key=lambda item: item[1], reverse=True)]
        self._do_not_replace_threshold = self.calculate_mean_word_count(self._counter)
        self._word_to_synonym_d = self.get_word_to_synonyms_d(words_sorted_by_frequency)

        f = open(marea_file, "r")
        y = open(output_file, 'w')
        word_to_synonym_d= self.get_word_to_synonyms_d(words_sorted_by_frequency)
        for line in f:
            new_abstract = self.transform(line, word_to_synonym_d)
            y.writelines(new_abstract)
        y.close()
        f.close()

    def get_word_to_synonyms_d(self, unique_words_list) -> Dict:
        """
        Creates a dictionary from the whole data set, keys are unique words, and the values are synonyms of keys from synset
        @parameter: 
            unique_words_list: list
             a list of unique words from the whole dataset in order of frequency
        @return: a dictionary of all the variables in the dataset, the keys are the unique variables
                   with high frequency, and values are key's synonyms list
        Methods
        -------
        def check_same_key_value(word, dict_tuple):
            check if there is a pair of the unique value with a smiliar key

        """
        dictionary = {}
        for i in range(len(unique_words_list)):
            this_word = unique_words_list[i]
            # skip common words not replaced 
            this_word_count = self._counter.get(this_word, 0)
            if this_word_count > self._do_not_replace_threshold:
                dictionary[this_word] = this_word
            else:
                synonym_list = self.get_synonym_list(this_word)
                dictionary[this_word] = self.get_highest_occuring_synonym(synonym_list)
        """""
        # Remove duplicates
        # if a value is not the same as the key, and there is no pair of the same key & value (based on the value), 
                 and then replace the value with the same key
         i.e If a word is replaced by another  a word, it cannot replace another word. 
                                Example:  before: 
                                                work: study
                                                influence: work
                                                study: study 
                                            after: 
                                                work: study
                                                influence: influence
                                                study: study 
        """""
        # dictionary to tuple
        dict_tuple = [(k, v) for k, v in dictionary.items()]

        # tuple to list
        size = len(dict_tuple)
        key_list = []
        value_list = []
        for i in range(0, size):
            key_list.append(dict_tuple[i][0])
            value_list.append(dict_tuple[i][1])

        
        def check_same_key_value(word, dict_tuple):
            """
            check if there is a pair of the unique value with a smiliar key
            @ parameter: dict_tuple: tuple
                a dictionary maped to a tuple, where the key is a word and the value is a list of a word's synonym
            
            @ return: status: Boolean
                returns false if the key and the values are not the same, true otherwise
            """
            status = True
            for i in range(len(dict_tuple)):
                if (dict_tuple[i][0] == word) and (dict_tuple[i][0] == dict_tuple[i][1]):
                    status = False
            return status

        for i in range(len(value_list)):
            if (value_list[i] != key_list[i]):
                if (check_same_key_value(value_list[i], dict_tuple) == True):
                    value_list[i] = key_list[i]

        # list to dictionary
        word_to_synonyms_d = {}
        for key in key_list:
            for value in value_list:
                word_to_synonyms_d[key] = value
                value_list.remove(value)
                break

        return word_to_synonyms_d


    def get_highest_occuring_synonym(self, synonym_list) -> str:
        """
        gets the highest occuring word in the synonym list of the whole dataset (all the bastracts being transformed)
        @ urgument: synonym_list: a list of a word's syonyms from Wordnet
        @ return: The word (synonym) with the highest count in our dataset
        """
        if len(synonym_list) == 0:
            raise ValueError("synonym_list was length zero, should never happen")
        max_count = 0
        highest_occuring_synonym = synonym_list[0]
        for s in synonym_list:
            #check frequency of a word in whole dataset
            c = self._counter.get(s, 0)
            if c > max_count:
                highest_occuring_synonym = s
                max_count = c
        return highest_occuring_synonym

    def get_synonym_list(self, word: str) -> List:
        """
        takes a word and returns a list of a word's synonyms using wordnet
        @argument: 'word' A word from the input dataset
        @return: a list of synonyms of the word
        """
        synonym_list = [word]
        for syn in wn.synsets(word):
            for l in syn.lemmas():
                synonym_list.append(l.name())
        return synonym_list

    def transform(self, line_abstract: str, _word_to_synonym_d) -> str:
        """
        Replaces the variable in dataset with their synonyms from the dictionary
        @argument: 'line_abstract' a string of line abstract including pubmed id and year
                   "_word_to_synonym_d" a dictionary created with the whole dataset
        @return: 'trans_abstract'  a string of transformed abstract

        """
        columns = line_abstract.split('\t')
        if len(columns) != 3:
            raise ValueError(f'Malformed marea line: {line}')
        abst_list = columns[2].split()  # columns[0]: pmid, columns[1] year, columns[0] abstract text
        for i in range(len(abst_list)):
            if abst_list[i] in self._word_to_synonym_d:
                abst_list[i] = self._word_to_synonym_d.get(abst_list[i])
            else:
                raise ValueError("the word is not in the dictionary")
            abstract = ' '.join([str(item) for item in abst_list])
        columns[2] = abstract
        trans_abstract = columns[0] + '\t' + columns[1] + '\t' + columns[2] + '\n'
        return (trans_abstract)


    def calculate_mean_word_count(self,counter_d) -> int:

        """
        calculates the mean of the frequencies of all the vocabilaries in the datasets
        @argument: 'counter_d' a dictionary created from whole dataset with the unique word as the key and frequency as the value
        @return:  an int which is mean of the unique words' frequencies

        """
        return round(statistics.mean(list(counter_d.values())))



if __name__ == "__main__":

    #running code using command line
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str) #address of the marea file
    parser.add_argument('output', type=str) #address of output file
    args = parser.parse_args()


    def all_replaced_words(dict):
        replaced = []
        for i in dict:
            if dict.get(i) != i:
                replaced.append(i)
        return replaced

    app = WordNetTransformer(args.input, args.output)

    threshold = app._do_not_replace_threshold
    print('Threshold: ', threshold)

    dictionary = app._word_to_synonym_d
    replaced_words = all_replaced_words(dictionary)
    print("Number of replaced words: ", len(replaced_words))
    print('All replaced words: \n', replaced_words)

    # sample way of running the code using arparse:
    """
    locate the file you are running + python + run_wn_replacement.py + address of marea_file + address of output_file
    example: 
    > python run_wn_replacement.py 'marea_file location' 'output_file location'

    """
