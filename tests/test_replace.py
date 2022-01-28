import unittest
from script.replace import*

import nltk

#nltk.download("wordnet")
from nltk.corpus import wordnet as wn # Import Wordnet
from collections import Counter  # Import Counter
import numpy as np
import csv

class ReplaceTestCase(unittest.TestCase):
    def test_sort_words_by_count(self):
        test1 = ['cancer', 'disease', 'caused', 'cell', 'crab', 'simple', 'cadre', 'cell', 'cancer', 'disease', 'cell', 'cancer', 'cell']
        result = Replace.sort_words_by_count(test1)
        expected = ['cell', 'cancer', 'disease', 'caused', 'crab', 'simple', 'cadre']
        self.assertEqual(expected, result, 'Arrangement do not match expected.')
        # 'cancer', 'disease', 'caused', 'cell', 'crab', 'simple', 'cadre']

    def test_synonym(self):
        expected = ['tissue', 'tissue', 'tissue_paper', 'weave', 'tissue']
        result = Replace.synonym('tissue')
        self.assertEqual(expected, result, 'Synonym do not match expected.')
    
    def test_dictCreate(self):
        test_list = ['cadre', 'tissue', 'cell', 'weave', 'cider']
        expected_dictionary = {'cell': 'cadre', 'cadre': 'cadre', 'tissue': 'tissue', 'tissue_paper': 'tissue', 'weave': 'tissue', 'cider': 'cider', 'cyder': 'cider'}
        rep = Replace(test_list)
        d = rep.get_word_dictionary()
        self.assertEqual(expected_dictionary, d, 'Dictionary created do not match expected.')
      
    
    def test_replace_data_set(self):
        test_set = ['cell', 'cadre', 'cell', 'dyestuff', 'dye', 'dye']
        replace = Replace(list=test_set)
        result = replace.get_replaced_data()
        expected_set =['cell', 'cell', 'cell', 'dye', 'dye', 'dye']
        self.assertEqual(expected_set, result, 'Key do not match expected.')

if __name__ == '__main__':
    unittest.main()