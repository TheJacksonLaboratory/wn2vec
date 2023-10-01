import os
from typing import Set
from .tf_concept import TfConcept
from collections import defaultdict
import numpy as np



class TfConceptParser:
    """
    Parses and manages TensorFlow word2vec output concepts and vectors.

    This class creates a dictionary of concepts (genes or mesh) that we are interested in and are present in the word2vec output.
    The resulting dictionary has the format: {metadata: vector}.

    Attributes
    ----------
    meta_file: str
        Output metadata file from TensorFlow word2vec, containing names of concepts.
    
    vector_file: str
        Output metadata file from TensorFlow word2vec, containing vectors. These vectors follow the same order as the concepts in `meta_file`.
    
    concept_set: set[str]
        A set of concept IDs we are interested in.

    Methods
    -------
    get_active_concept_d() -> dict:
        Creates and returns a dictionary of all concepts used at least once in the `concept_set` passed to the constructor.


    """



    def __init__(self, meta_file, vector_file, concept_set:Set[str]) -> None:
        """
        Initializes the TfConceptParser with provided metadata file, vector file, and set of interested concepts.

        :param meta_file: Output metadata file from TensorFlow word2vec, containing names of concepts.
        :type meta_file: str
        :param vector_file: Output metadata file from TensorFlow word2vec, containing vectors.
        :type vector_file: str
        :param concept_set: A set of concept IDs we are interested in.
        :type concept_set: set[str]
        
        :raises FileNotFoundError: If `meta_file` or `vector_file` paths do not point to valid files.
        :raises ValueError: If `concept_set` is not of type `set`.

        """


        self._d = defaultdict(TfConcept)
        self._vectors = []
        self._concepts = []
        self._common_genes = [] # Keep track of number common genes in both geneset & our metadata
        if not os.path.isfile(meta_file):
            raise FileNotFoundError(f"Could not find meta file {meta_file}")
        if not os.path.isfile(vector_file):
            raise FileNotFoundError(f"Could not find vector file {vector_file}")
        if not isinstance(concept_set, set):
            raise ValueError("concept_set arguments needs to be a set")
        meta_fh = open(meta_file, 'rt')
        vector_fh = open(vector_file, 'rt')
        for meta_line in meta_fh:
            vector_line = vector_fh.readline()
            c = meta_line.rstrip()
            if c in concept_set:
                values = vector_line.rstrip().split('\t')
                fvals = np.array([float(v) for v in values])
                self._d[c] = TfConcept(name=c, vctor=fvals)
            else:
                pass
                #print(f"Could not fine TF concept \"{c}\"")
        meta_fh.close()
        vector_fh.close()

    def get_active_concept_d(self):
        """
        Retrieves the dictionary of active concepts.

        :return: Dictionary containing all concepts used at least once in the `concept_set` passed to the constructor.
        :rtype: dict
        """
        return self._d





        