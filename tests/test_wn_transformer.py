import unittest
from scripts.wn_transformer import WordNetTransformer
import os
#import pytest
from unittest import TestCase
from collections import defaultdict

nltk.download("wordnet")
from nltk.corpus import wordnet as wn # Import Wordnet
from collections import Counter  # Import Counter
import numpy as np
import csv

class TransformerTestCase(unittest.TestCase):
    class WordNetTransformerTestCase(unittest.TestCase):
        def test_synonym(self):
            test1 = 'adam'
            expected = ['adam', 'Adam', 'Adam', 'Robert_Adam', 'Adam', 'ecstasy', 'XTC', 'go', 'disco_biscuit',
                        'cristal', 'X', 'hug_drug']
            self.assertEqual(expected, WordNetTransformer.synonym(test1), 'Synonym do not match expected.')
