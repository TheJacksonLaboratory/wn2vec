import os

from .tf_concept import TfConcept
from collections import defaultdict
import numpy as np



class TfConceptParser:
    """
    creates a dictionary of concepts that are both  we are interested in (genes or mesh) and are present in the word2vec output (key: metadata, value: vector)
    ...

    Attributes
    ----------
        meta_file: str
                   output of tensorflow word2vec, metadata file with names of concepts
        
        vector_file: str
                    output of tensorflow word2vec, metadata file with vectors (same order as concepts)
        
        concept_set: str
                   set of concept ids we are interested in

    Methods
    -------
    def get_active_concept_d(self):
        Dictionary of all concepts used at least once in the concept_set passed to the constructor

    """



    def __init__(self, meta_file, vector_file, concept_set) -> None:
        """
        Constructs all the necessary attributes for the  TfConceptParser class
        
        Parameters
        ----------
        meta_file: str
                   output of tensorflow word2vec, metadata file with names of concepts
        
        vector_file: str
                    output of tensorflow word2vec, metadata file with vectors (same order as concepts)
        
        concept_set: str
                   set of concept ids we are interested in
       
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
                #self._d[c] = fvals
                self._d[c] = TfConcept(name=c, vctor=fvals)
        meta_fh.close()
        vector_fh.close()

    def get_active_concept_d(self):
        """
        creates a dictionary of all concepts used at least once in the concept_set passed to the constructor
        """
        return self._d





        