import unittest
from scripts.wntransformer import *

import nltk
import pytest
# nltk.download("wordnet")
from nltk.corpus import wordnet as wn  # Import Wordnet
from collections import Counter  # Import Counter
import numpy as np
import csv


class ReplaceTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Set up small fake dataset for testing
        """
        current_dir = os.path.dirname(__file__)
        test_marea_file = os.path.join(current_dir, 'data', 'sample2abstracts.tsv')
        cls.wnt = WordNetTransformer(marea_file=test_marea_file)


    def test_synonym(self):
        expected = ['colony', 'colony', 'settlement', 'colony', 'Colony', 'colony', 'colony', 'dependency', 'colony']
        result = self.wnt.synonym('colony')
        self.assertEqual(expected, result, 'Synonym do not match expected.')

    def _highest_count_synonym(self):
        test1 = ['inhibition', 'inhibition', 'suppression', 'inhibition', 'inhibition', 'prohibition', 'inhibition',
                 'forbiddance']
        counter = {'evaluation': 2, 'dye': 2, 'exclusion': 2, 'colony': 8, 'settlement': 15, 'inhibition': 17,
                   'prohibition': 50}
        result = wntransformer._highest_count_synonym(test1)
        expected = ['prohibition']

    def test_transormer(self):

if __name__ == '__main__':
    unittest.main()