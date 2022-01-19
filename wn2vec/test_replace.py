import unittest

from replace import*
import nltk

#nltk.download("wordnet")
from nltk.corpus import wordnet as wn # Import Wordnet
from collections import Counter  # Import Counter
import numpy as np
import csv

class ReplaceTestCase(unittest.TestCase):
    def test_arrangement(self):
        test1 = ['cancer', 'disease', 'caused', 'cell', 'crab', 'simple', 'cadre', 'cell', 'cancer', 'disease', 'cell', 'cancer', 'cell']
        expected = ['cell', 'cancer', 'disease', 'caused', 'crab', 'simple', 'cadre']
        self.assertEqual(expected,arrangement(test1), 'Arrangement do not match expected.')

    def test_synonym(self):
        test2 = 'tissue'
        expected = ['tissue', 'tissue', 'tissue_paper', 'weave', 'tissue']
        self.assertEqual(expected,synonym(test2), 'Synonym do not match expected.')
    
    def test_dictCreate(self):
        test_list = ['cadre', 'tissue', 'cell', 'weave', 'cider']
        expected_dictionary = {'cell': 'cadre', 'cadre': 'cadre', 'tissue': 'tissue', 'tissue_paper': 'tissue', 'weave': 'tissue', 'cider': 'cider', 'cyder': 'cider'}
        self.assertEqual(expected_dictionary,dictCreate(test_list), 'Dictionary created do not match expected.')
    
    def test_giveValue(self):
        test_dictionary = {'cell': 'cadre', 'cadre': 'cadre', 'tissue': 'tissue', 'tissue_paper': 'tissue', 'weave': 'tissue', 'cider': 'cider', 'cyder': 'cider'}
        test5 = 'cell'
        expected5 = 'cadre'
        test6 = 'cider' 
        expected6 = 'cider'
        self.assertEqual(expected5,giveValue(test5,test_dictionary), 'Key do not match expected.')
        self.assertEqual(expected6,giveValue(test6,test_dictionary), 'Key do not match expected.')       
    
    def test_replace_data_set(self):
        test_set = ['cell', 'cadre', 'cell', 'dyestuff', 'dye', 'dye']
        test_dictionary = dictCreate(arrangement(test_set))
        expected_set =['cell', 'cell', 'cell', 'dye', 'dye', 'dye']
        self.assertEqual(expected_set,replace_data_set(test_set,test_dictionary), 'Key do not match expected.')

if __name__ == '__main__':
    unittest.main()