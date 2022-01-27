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
        expected = ['cell', 'cancer', 'disease', 'caused', 'crab', 'simple', 'cadre']
        self.assertEqual(expected,sort_words_by_count(test1), 'Arrangement do not match expected.')
        # 'cancer', 'disease', 'caused', 'cell', 'crab', 'simple', 'cadre']

    def test_synonym(self):
        test2 = 'tissue'
        expected = ['tissue', 'tissue', 'tissue_paper', 'weave', 'tissue']
        print(synonym(test2))
        self.assertEqual(expected,synonym(test2), 'Synonym do not match expected.')
    
    def test_dictCreate(self):
        test_list = ['cadre', 'tissue', 'cell', 'weave', 'cider']
        expected_dictionary = {'cell': 'cadre', 'cadre': 'cadre', 'tissue': 'tissue', 'tissue_paper': 'tissue', 'weave': 'tissue', 'cider': 'cider', 'cyder': 'cider'}
        self.assertEqual(expected_dictionary,dictCreate(test_list), 'Dictionary created do not match expected.')
      
    
    def test_replace_data_set(self):
        test_set = ['cell', 'cadre', 'cell', 'dyestuff', 'dye', 'dye']
        test_dictionary = dictCreate(sort_words_by_count(test_set))
        test_d = {'cell': 'cell', 'dye': 'dye', 'cadre': 'cell', 'dyestuff': 'dye'}
        expected_set =['cell', 'cell', 'cell', 'dye', 'dye', 'dye']
        res = replace_data_set(test_set,test_d)
        print("DICTIONARY")
        print(test_dictionary)
        print("RESULT")
        print(res)
        self.assertEqual(expected_set,replace_data_set(test_set,test_d), 'Key do not match expected.')

if __name__ == '__main__':
    unittest.main()