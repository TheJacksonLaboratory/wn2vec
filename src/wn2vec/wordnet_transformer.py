import os
from collections import defaultdict
import nltk
from nltk.corpus import wordnet as wn
from typing import List, Dict
import numpy as np


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

    def __init__(self, marea_file, percentile=50) -> None:
        """
        Constructs all the necessary attributes for the  WordNetTransformer class
        
        Parameters
        ----------
        marea_file: str
                    path to .tsv file with abstracts from marea output
        output_file: str
                    path to .tsv file that will contain the output after abstracts are transformed
        percentile: float
                    percentile for threshold frequency. Default is 0.5 (i.e. 50%), the median
        """
        if not os.path.exists(marea_file):
            raise FileNotFoundError("Could not find marea file")

        self._marea_file = marea_file
        self._counter_d = defaultdict(int)
        self._percentile = percentile
        # Get count of words in corpus
        with open(marea_file) as f:
            for line in f:
                columns = line.split('\t')
                if len(columns) != 3:
                    raise ValueError(f'Malformed marea line: {line}')
                payload = columns[2]  # columns[0]: pmid,  columns[1] year, columns[2] abstract text
                words = payload.split()
                for w in words:
                    self._counter_d[w] += 1
        print(f"Got {len(self._counter_d)} words")
        value_at_percentile = np.percentile(list(self._counter_d.values()), percentile)

        # Create synonym dictionary with NLTK
        # only downloads if needed
        nltk.download("wordnet", download_dir='../data')

        words_sorted_by_frequency = [k for k, v in
                                     sorted(self._counter_d.items(), key=lambda item: item[1], reverse=True)]

        self._do_not_replace_threshold = round(value_at_percentile)

        self._word_to_synonym_d = self.get_word_to_synonyms_d(words_sorted_by_frequency)

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
            this_word_count = self._counter_d.get(this_word, 0)
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

        # TEST THIS
        synonyms_used_for_replacements = set()
        word_to_synonyms_d = {}
        for word, most_frequent_synonym in dictionary.items():
            if word in synonyms_used_for_replacements:
                word_to_synonyms_d[word] = word
            else:
                synonyms_used_for_replacements.add(word)
                word_to_synonyms_d[word] = most_frequent_synonym
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
        most_frequent_synonym = synonym_list[0]
        for s in synonym_list:
            # check frequency of a word in whole dataset
            c = self._counter_d.get(s, 0)
            if c > max_count:
                most_frequent_synonym = s
                max_count = c
        return most_frequent_synonym

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

    def transform(self, line_abstract: str) -> str:
        """
        Replaces the variable in dataset with their synonyms from the dictionary
        @argument: 'line_abstract' a string of line abstract including pubmed id and year
        @return: 'trans_abstract'  a string of transformed abstract

        """
        columns = line_abstract.split('\t')
        if len(columns) != 3:
            raise ValueError(f'Malformed marea line: {line_abstract}')
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

    def get_threshold(self) -> int:
        """
        returns the threshold count 
        @return:  an int which is at the percentile of the unique words' frequencies

        """
        return self._do_not_replace_threshold

    def transform_and_write(self, output_file):
        fh = open(output_file, 'w')
        with open(self._marea_file, "r") as f:
            for line in f:
                new_abstract = self.transform(line)
                fh.writelines(new_abstract)
        fh.close()

    def get_total_word_count(self):
        return len(self._word_to_synonym_d)

    def get_replaced_word_count(self):
        """
        return the number of words in our corpus that we replaced using WordNet
        """
        replaced = 0
        for k, v in self._word_to_synonym_d.items():
            if k != v:
                replaced += 1
        return replaced
