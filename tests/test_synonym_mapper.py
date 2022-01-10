

from wn2vec.synonym_mapper import SynonymMapper

import os
from collections import defaultdict
from unittest import TestCase



class SynonymMapperTester(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.counter = defaultdict(int)
        cls.counter['examination'] = 16
        cls.counter['test'] = 2
        cls.counter['pneumonia]'] = 10
        ## etc, whatever you need for tests
    
    def test_setup(self):
        self.assertEquals(16, self.counter.get('examination'))
