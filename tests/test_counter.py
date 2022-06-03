from script.wntransformer import WordNetTransformer

import os
from unittest import TestCase


class TestWn2vecCounter(TestCase):

    @classmethod
    def setUpClass(cls):
        current_dir = os.path.dirname(__file__)
        sample_abstracts_file = os.path.join(current_dir, 'data', "sample2abstracts.tsv")
        transformer = WordNetTransformer(sample_abstracts_file)
        cls.counter = transformer.get_counter()

    
    def test_evaluation(self):
        expected_count = 1
        self.assertEquals(expected_count, self.counter['evaluation'])

# import unittest
# from scripts.wntransformer import *
# from scripts import wntransformer
#
# import nltk
# import pytest
# # nltk.download("wordnet")
# from nltk.corpus import wordnet as wn  # Import Wordnet
# from collections import Counter  # Import Counter
# import numpy as np
# import csv
#
#
# class ReplaceTestCase(unittest.TestCase):
#
#     @classmethod
#     def setUpClass(cls):
#         """
#         Set up small fake dataset for testing
#         """
#         current_dir = os.path.dirname(__file__)
#         test_marea_file = os.path.join(current_dir, 'data', 'sample2abstracts.tsv')
#         cls.wnt = WordNetTransformer(marea_file=test_marea_file)
#
#
#     def test_transormer(self):
#
#
# if __name__ == '__main__':
#     unittest.main()