import unittest
from scripts.wntransformer import WordNetTransformer
import nltk

#nltk.download("wordnet")
from nltk.corpus import wordnet as wn # Import Wordnet
from collections import Counter  # Import Counter
import numpy as np
import csv

class WordNetTransformerTestCase(unittest.TestCase):
    # def test_synonym(self):
    #     test1 = 'adam'
    #     expected = ['adam', 'Adam', 'Adam', 'Robert_Adam', 'Adam', 'ecstasy', 'XTC', 'go', 'disco_biscuit', 'cristal', 'X', 'hug_drug']
    #     self.assertEqual(expected, WordNetTransformer.synonym(test1), 'Synonym do not match expected.')

    def test_dictCreate(self):
        test_list = ['prohibition', 'inhibition', 'settlement', 'colony', 'exclusion', 'dye', 'evaluation']
        expected1 = {'prohibition': 'inhibition', 'inhibition': 'inhibition', 'settlement': 'colony', 'colony': 'colony', 'exclusion': 'exclusion', 'dye': 'dye', 'evaluation': 'evaluation'}
        self.assertEqual(expected1,WordNetTransformer.dictCreate(test_list))