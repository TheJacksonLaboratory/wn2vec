import unittest
from wn2vec.wntransformer import *

import nltk

# nltk.download("wordnet")
from nltk.corpus import wordnet as wn  # Import Wordnet
from collections import Counter  # Import Counter
import numpy as np
import csv


class ReplaceTestCase(unittest.TestCase):
    def test_synonym(self):
        expected = ['colony', 'colony', 'settlement', 'colony', 'Colony', 'colony', 'colony', 'dependency', 'colony']
        result = wntransformer.synonym('colony')
        self.assertEqual(expected, result, 'Synonym do not match expected.')

    def _highest_count_synonym(self):
        test1 = ['inhibition', 'inhibition', 'suppression', 'inhibition', 'inhibition', 'prohibition', 'inhibition',
                 'forbiddance']
        counter = {'evaluation': 2, 'dye': 2, 'exclusion': 2, 'colony': 8, 'settlement': 15, 'inhibition': 17,
                   'prohibition': 50}
        result = wntransformer._highest_count_synonym(test1)
        expected = ['prohibition']
        self.assertEqual(expected, result, 'Arrangement do not match expected.')

    def test_dictCreate(self):
        test_list = ['prohibition', 'inhibition', 'settlement', 'colony', 'exclusion', 'dye', 'evaluation']
        counter = {'evaluation': 2, 'dye': 2, 'exclusion': 2, 'colony': 8, 'settlement': 15, 'inhibition': 17,
                   'prohibition': 50}
        expected_dictionary = {'inhibition': 'prohibition', 'settlement': 'settlement', 'colony': 'settlement',
                               'exclusion': 'exclusion',
                               'dye': 'dye', 'evaluation': 'evaluation'}
        results = wntransformer.dictCreate(test_list)
        self.assertEqual(expected_dictionary, results, 'Dictionary created do not match expected.')

    def test_replace_data_set(self):
        test_set = ['evaluation', 'add', 'exclusion', 'total', 'basis', 'base', 'indicates', 'polyoma']
        dictionary = {'inhibition': 'prohibition', 'settlement': 'settlement', 'colony': 'settlement',
                      'exclusion': 'exclusion', 'dye': 'dye', 'evaluation': 'evaluation'}
        result = wntransformer.replace_data_set(test_set, dictionary)
        expected_set = ['evaluation', 'total', 'exclusion', 'total', 'base', 'found', 'show', 'polyoma']
        self.assertEqual(expected_set, result, 'Key do not match expected.')


if __name__ == '__main__':
    unittest.main()