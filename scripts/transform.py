
import nltk
from nltk.corpus import wordnet as wn
from typing import List, Dict
from wntransformer import WordNetTransformer

import os
from collections import defaultdict


class Transformer:

    def __init__(self,marea_file ) -> None:
        """
        Path to the file produced by marea
        """
        if not os.path.exists(marea_file):
            raise FileNotFoundError("Could not find marea file")

        self._marea_file = marea_file
        self._counter = defaultdict(int)
        # Get count of words in corpus

        with open(marea_file) as f:
            for line in f:
                columns = line.split('\t')
                if len(columns) != 3:
                    raise ValueError(f'Malformed marea line: {line}')
                payload = columns[2] # columns[0] - year, columns[1]: pmid, columns[2] abstract text
                words = payload.split()
                for w in words:
                    self._counter[w] += 1

        # Create synonym dictionary with NLTK
        # if needed, install wordnet
        nltk.download("wordnet")

        words_sorted_by_frequency = [k for k, v in
                                     sorted(self._counter.items(), key=lambda item: item[1], reverse=True)]

        self._do_not_replace_threshold = do_not_replace_threshold
        self._dict = self.dictCreate(words_sorted_by_frequency)


def replace_data_set(self, _data_list, _dict) -> List:
    """
    Replaces the variable in dataset with their synonyms from the dictionary
    @argument: '_data_list' a list of all the dataset  in form of a list
                '_dict' a dictionary created from the unique words from the whole dataset
    @return: 'data_list' a new list with the whole list where the words were replaced by their synonyms

    """
    # gh = open('outputfilename.tsv', 'wt')
    # with open('input.tsv') as f:
    # as above
    # gh.close()
    for i in range(len(self._data_list)):
        if self._data_list[i] in self._dict:
            self._data_list[i] = self._dict.get(self._data_list[i])
        else:
            raise ValueError("the word is not in the dictionary")
    return (self._data_list)