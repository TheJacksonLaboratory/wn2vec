import os

from .tf_concept import TfConcept
from collections import defaultdict
import numpy as np



class TfConceptParser:
    def __init__(self, meta_file, vector_file, concept_set) -> None:
        """
        meta_file: output of tensorflow word2vec, metadata file with names of concepts
        vector_file: output of tensorflow word2vec, metadata file with vectors (same order as concepts)
        concept_set: set of concept ids we are interested in
        """
        self._d = defaultdict(TfConcept)
        self._vectors = []
        self._concepts = []
        self._common_genes = [] # Keep track of number common genes in both geneset & our metadata
        if not os.path.isfile(meta_file):
            raise FileNotFoundError(f"Could not find meta file {meta_file}")
        if not os.path.isfile(vector_file):
            raise FileNotFoundError(f"Could not find vector file {vector_file}")
        if not isinstance(concept_set, list):
            raise ValueError("concept_set arguments needs to be a list")
#####
        meta_fh = open(meta_file, 'rt')
        vector_fh = open(vector_file, 'rt')
        for meta_line in meta_fh:
            vector_line = vector_fh.readline()
            c = meta_line.rstrip()

            values = vector_line.rstrip().split('\t')
            fvals = np.array([float(v) for v in values])
            self._vectors.append(fvals)
            self._concepts.append(c)
            self._d[c] = TfConcept(name=c, vctor=fvals)

        meta_fh.close()
        vector_fh.close()

        self._word_to_vec_dict = dict(zip(self._concepts, self._vectors))  # Create a dictionary key: word, value: vector

        # Defining function two check common elements in two lists by converting to sets
        def commonelem_set(list1, list2):
            set_one = set(list1)
            set_two = set(list2)
            no_word = set(['NONE'])
            if (set_one & set_two):
                return (set_one & set_two)
            else:
                return (no_word)

        for geneset in concept_set:
            common = list(commonelem_set(geneset, self._concepts))
            if len(common) > 3:
                self._common_genes.append(common)

        #convert the common_genes from word to vec: Step 1 in  dictionary: word_to_vec_dict
        for com_geneset in self._common_genes:
            for i in range (0, len(com_geneset)):
                com_geneset[i] = self._word_to_vec_dict.get(com_geneset[i])


    def get_active_concept_d(self):
        return self._d

    def get_vector_list(self):
        return self._vectors

    def get_concept_list(self):
        return self._concepts

    def common_genes(self):
        return self._common_genes

    def get_concept_to_vec_d(self):
        return self._word_to_vec_dict



        