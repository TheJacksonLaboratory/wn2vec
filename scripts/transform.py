
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
            new_abstract = self.transform(line)
            y.writelines(new_abstract)
        y.close()
        f.close()

    def transform(self, line_abstract,_dict):

          """
          Replaces the variable in dataset with their synonyms from the dictionary
          @argument: 'line_abstract' a string of line abstract including pubmed id and year
                     "_dict" a dictionary created with the whole dataset
          @return: 'trans_abstract'  a string of transformed abstract

          """
          columns = line_abstract.split('\t')
          if len(columns) != 3:
            raise ValueError(f'Malformed marea line: {line}')
          abst_list = columns[2].split()  # columns[0] - year, columns[1]: pmid, columns[2] abstract text
          #abst_list = abstract.split()
          for i in range(len(abst_list)):
            if abst_list[i] in self._dict:
              abst_list[i]= self._dict.get(abst_list[i])
            else:
              raise ValueError("the word is not in the dictionary")
            abstract = ' '.join([str(item) for item in abst_list])
          columns[2] = abstract
          trans_abstract = columns[0] + ' ' + columns[1] + '     '+ columns[2]
          return(trans_abstract)
