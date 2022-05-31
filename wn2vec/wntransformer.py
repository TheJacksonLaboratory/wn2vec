import nltk
from nltk.corpus import wordnet as wn
from typing import List, Dict

import os
from collections import defaultdict


class WordNetTransformer:

    def __init__(self, marea_file, do_not_replace_threshold: int = 20) -> None:
        """
        Path to the file produced by marea
        """
        if not os.path.exists(marea_file):
            raise FileNotFoundError("Could not find marea file")

        self._marea_file = marea_file
        self._counter = defaultdict(int)
        # Get count of words in corpus

        with open(marea_file) as f:
            data_list = []  # contains string of all the words in dataset
            for line in f:
                words = line.split()
                for w in words:
                    # TODO skip stop words
                    self._counter[w] += 1
                    #add each word to the data_list
                    data_list.append(w)
        # Create synonym dictionary with NLTK
        # if needed, install wordnet
        nltk.download("wordnet")

        words_sorted_by_frequency = [k for k, v in
                                     sorted(self._counter.items(), key=lambda item: item[1], reverse=True)]

        self._do_not_replace_threshold = do_not_replace_threshold
        self._dict = self.dictCreate(words_sorted_by_frequency)
        self._data_list = data_list

    def dictCreate(self, word_list) -> Dict:
        """
        Creates a dictionary from the whole data set, they keys are in order of their frequency words
        and the values are synonyms of keys from synset
        @argument: 'word_list' a list of unique words from the whole dataset in order of frequency
        @return: a dictionary of all the variables in the dataset, the keys are the unique variables
                   with high frequency, and values are key's synonym
        """
        dictionary = {}
        for i in range(len(word_list)):
            this_word = word_list[i]
            # skip common words
            this_word_count = self._counter.get(this_word, 0)
            if this_word_count > self._do_not_replace_threshold:
                continue
            synonym_list = self.synonym(this_word)
            dictionary[this_word] = self._highest_count_synonym(synonym_list)
        return dictionary

    def _highest_count_synonym(self, synonym_list):
        """
        :param synonym_list: a list of a word and its synonyms in Wordnet
        :return: The word (synonym) with the highest count in our dataset
        """
        if len(synonym_list) == 0:
            raise ValueError("synonym_list was length zero, should never happen")
        max_count = 0
        max_word = synonym_list[0]
        for s in synonym_list:
            c = self._counter.get(s, 0)
            if c > max_count:
                max_word = s
                max_count = c
        return max_word

    def synonym(self, word: str) -> List:
        """
        @argument: 'word' A word from the input dataset
        @return: a list of synonyms of the words
        """
        synonyms = [word]
        for syn in wn.synsets(word):
            for l in syn.lemmas():
                synonyms.append(l.name())
        return synonyms

    def replace_data_set(self, _data_list, _dict) ->List:

        """
        Replaces the variable in dataset with their synonyms from the dictionary
        @argument: 'data_list' a list of all the dataset  in form of a list
                    '_dict' a dictionary created from the unique words from the whole dataset
        @return: 'data_list' a new list with the whole list where the words were replaced by their synonyms

        """

        for i in range(len(self._data_list)):
            if self._data_list[i] in self._dict:
                self._data_list[i] = self._dict.get(self._data_list[i])
            else:
                raise ValueError("the word is not in the dictionary")
        return (self._data_list)

    def transform(self, sentence: str) -> str:
        pass