
#from nltk.corpus import wordnet as wn

import os
from collections import defaultdict


class WordNetTransformer:

    def __init__(self, marea_file) -> None:
        """
        Path to the file produced by marea
        """
        if not os.path.exists(marea_file):
            raise FileNotFoundError("Could not find marea file")

        self._marea_file = marea_file
        self._counter = defaultdict(int)
        # Get count of words in corpus
        with open(marea_file) as f:
            for line in f:
                words = line.split()
                for w in words:
                    # TODO skip stop words
                    self._counter[w] += 1
        # Create synonym dictionary with NLTK

    def get_counter(self):
        return self._counter
            

        
            