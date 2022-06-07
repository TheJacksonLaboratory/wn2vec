import unittest
from scripts.wn_transformer import WordNetTransformer
import os
import pytest
from unittest import TestCase
from collections import defaultdict

#nltk.download()
from nltk.corpus import wordnet as wn # Import Wordnet
from collections import Counter  # Import Counter
import numpy as np
import csv

test_output = '/Users/niyone/Documents/GitHub/wn2vec/tests/data/output2abstracts.tsv'
test_marea = '/Users/niyone/Documents/GitHub/wn2vec/tests/data/sample2abstracts.tsv'
tp = WordNetTransformer(test_marea, test_output)

class WordNetTransformerTestCase(unittest.TestCase):

    def test_synonym(self):
        #synonym1
        expected1 = ['plasma', 'plasma', 'plasm', 'blood_plasma', 'plasma', 'plasma']
        self.assertEqual(expected1, tp.synonym('plasma'))
        #synonym2
        expected2 = ['quantity', 'measure', 'quantity', 'amount', 'quantity', 'quantity']
        self.assertEqual(expected2, tp.synonym('quantity'))
        #synonym3
        expected3 = ['measure', 'measure', 'step', 'measure', 'quantity', 'amount', 'bill', 'measure', 'measurement', 'measuring', 'measure', 'mensuration', 'standard', 'criterion', 'measure', 'touchstone', 'meter', 'metre', 'measure', 'beat', 'cadence', 'measure', 'bar', 'measuring_stick', 'measure', 'measuring_rod', 'measure', 'measure', 'mensurate', 'measure_out', 'quantify', 'measure', 'measure', 'measure', 'evaluate', 'valuate', 'assess', 'appraise', 'value']
        self.assertEqual(expected3, tp.synonym('measure'))
