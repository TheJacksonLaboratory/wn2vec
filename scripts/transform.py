
import nltk
from nltk.corpus import wordnet as wn
from typing import List, Dict
from wntransformer import WordNetTransformer

import os
from collections import defaultdict


class Transformer(WordNetTransformer):

    def __init__(self, marea_file, output_file ) -> None:
        """
        Path to the file produced by marea
        """
        super().__init__(marea_file)
        self._output_file = output_file


        # Get count of words in corpus
        f = open(marea_file, "r")
        y = open(output_file, 'a')
        for line in f:
            columns = line.split('\t')
            if len(columns) != 3:
                raise ValueError(f'Malformed marea line: {line}')
            payload = columns[2]  # columns[0] - year, columns[1]: pmid, columns[2] abstract text
            self.abstract = payload
            columns[2] = self.transform(self, abstract,_dict)
            trans_column = columns[0] + ' ' + columns[1] + '     '+ columns[2]
            y.writelines(trans_column)
        y.close()
        f.close()


    def transform(self, abstract, _dict) ->str:

        """
        Replaces the variable in dataset with their synonyms from the dictionary
        @argument: 'abstract' a string of an abstract
                    "dictionary" a dictionary created with the whole dataset
        @return: 'data_list' a new list with the whole list where the words were replaced by their synonyms

        """
        abst_list = abstract.split()
        for i in range(len(abst_list)):
            if abst_list[i] in self._dict:
                abst_list[i] = self._dict.get(abst_list[i])
            else:
                raise ValueError("the word is not in the dictionary")
            abstract = ' '.join([str(item) for item in abst_list])
        return abstract

