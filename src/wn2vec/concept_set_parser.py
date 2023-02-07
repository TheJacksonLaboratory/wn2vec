import os
from .concept_set import ConceptSet


import logging
log = logging.getLogger("wn2vec.log")
log.setLevel(logging.INFO)

MINIMUM_CONCEPT_SET_SIZE = 5

ch = logging.StreamHandler() # console handler
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)


class ConceptSetParser:
    """
    creates an object of concept set from the .tsv files from their path of both geneset or meshset
    ...

    Attributes
    ----------
        concept_file_path: str
                a path to a .tsv  file with all the concpets (either mesh sets or gene sets)

    Methods
    -------
    def get_all_concepts(self):
        returns all the concepts sets in a file (with 3 clolumns: name, id, concept list )
    def get_concept_set_list(self):
        returns all the concept lists in a file (with 1 column: concept list)

    """


    def __init__(self, concept_file_path):

        """
        Constructs all the necessary attributes for the  ConceptSetParser class
        
        Parameters
        ----------
        concept_file_path: str
                    a path to a .tsv  file with all the concpets (either meshets or genesets)
       
        """

        if not os.path.isfile(concept_file_path):
            raise FileNotFoundError(f"Could not find concept file at {concept_file_path}")
        self._concept_set_list = []
        with open(concept_file_path) as f:
            for line in f:
                fields = line.rstrip().split('\t')
                if len(fields) != 3:
                    raise ValueError(f"Malformed concept line {line}")
                name = fields[0]
                id = fields[1]
                concept_list = fields[2].split(";")
                cs = ConceptSet(name=name, id=id, concept_list=concept_list)
                self._concept_set_list.append(cs)

    def get_all_concepts(self, meta1, meta2):
        """
        returns all the concepts sets in a file (with 3 clolumns: name, id, concept list )
        """
        return self._all_concepts

    def get_concept_set_list(self):
        """
        returns all the concept lists in a file (with 1 column: concept list)
        """
        return self._concept_set_list