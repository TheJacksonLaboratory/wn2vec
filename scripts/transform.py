
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
        self._dict = WordNetTransformer.__dict__

        # Get count of words in corpus

        with open(marea_file) as f:
            for line in f:
                columns = line.split('\t')
                if len(columns) != 3:
                    raise ValueError(f'Malformed marea line: {line}')
                abstract = columns[2] # columns[0] - year, columns[1]: pmid, columns[2] abstract text
                columns[2] = transform(abstract,self._dict)


def transform(self, abstract, _dict) ->str:

    """
    Replaces the variable in dataset with their synonyms from the dictionary
    @argument: 'abstract' a string of an abstract
                "dictionary" a dictionary created with the whole dataset
    @return: 'data_list' a new list with the whole list where the words were replaced by their synonyms

    """
    abst_list = abstract.split()
    for i in range(len(abst_list)):
        if abst_list[i] in dictionary:
            abst_list[i] = dictionary.get(abst_list[i])
        else:
            raise ValueError("the word is not in the dictionary")
        abstract = ' '.join([str(item) for item in abst_list])
    return abstract