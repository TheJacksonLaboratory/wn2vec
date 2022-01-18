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
        expected_dicitonary = {'cadre': ['cell', 'cadre', 'cadre'],'cider': ['cider', 'cyder'], 'tissue': ['tissue', 'tissue', 'tissue_paper', 'weave', 'tissue']}
        self.assertEqual(expected_dictionary,dictCreate(test_list), 'Dictionary created do not match expected.')
    
    def test_giveKey(self):
        test_dictionary = {'cadre': ['cell', 'cadre', 'cadre'],'cider': ['cider', 'cyder'],'tissue': ['tissue', 'tissue', 'tissue_paper', 'weave', 'tissue']}
        test5 = 'cell'
        expected5 = 'cadre'
        test6 = 'cider' 
        expected6 = 'cider'
        self.assertEqual(expected5,synonym(test5,test_dictionary), 'Key do not match expected.')
        self.assertEqual(expected6,synonym(test6,test_dictionary), 'Key do not match expected.')       
    
    def test_replace_data_set(self):
        test_set = ['cell', 'cadre', 'cell', 'dyestuff', 'dye', 'dye']
        #test_dictionary = dictCreate(arrangement(test_set))
        test_dictionary = {'cell': ['cell', 'cell', 'cell', 'electric_cell', 'cell', 'cadre', 'cellular_telephone', 'cellular_phone', 'cellphone', 'cell', 'mobile_phone', 'cell', 'cubicle', 'cell', 'jail_cell', 'prison_cell'], 'dye': ['dye', 'dyestuff', 'dye']}
        expected_set =['cell', 'cell', 'cell', 'dye', 'dye', 'dye']
        self.assertEqual(expected_set,synonym(test_set,test_dictionary), 'Key do not match expected.')

if __name__ == '__main__':
    unittest.main()