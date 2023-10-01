from script.wntransformer import WordNetTransformer

import os
from unittest import TestCase


class TestWn2vecCounter(TestCase):
    @classmethod
    def setUpClass(cls):
        current_dir = os.path.dirname(__file__)
        sample_abstracts_file = os.path.join(current_dir, "data", "sample2abstracts.tsv")
        transformer = WordNetTransformer(sample_abstracts_file)
        cls.counter = transformer.get_counter()

    def test_evaluation(self):
        expected_count = 1
        self.assertEquals(expected_count, self.counter["evaluation"])
