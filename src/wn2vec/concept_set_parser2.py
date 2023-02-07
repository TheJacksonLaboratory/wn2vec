import os
import typing
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


class ConceptSetParser2:
    """
    Parsers the concept sets and creates sets of concepts that are contained in both the metadata files. The reason is that we want to 
    restrict the comparison to identical sets of vectors when we do the t test for pairwaise distances to compare PubTator and Wordnet
    concept replacements strategies. If we did not do this, then we would tend to have more concepts in some WordNet clusters because
    the fact that we replace non-biomedical concepts with WordNet means that more biomedical concepts are included within the vocabulary
    size (typically 100,000) used for word2vec embedding.
    ...

    Attributes
    ----------
        meta1: str
                a path to the metadata file from tensforflow with all concepts from one of the two embeddings (PubTator or Wordnet)
        meta2: str
                a path to the metadata file from tensforflow with all concepts from one of the two embeddings (PubTator or Wordnet)

    Methods
    -------
    def get_all_concepts(self):
        returns all the concepts sets in a file (with 3 clolumns: name, id, concept list )
    def get_concept_set_list(self):
        returns all the concept lists in a file (with 1 column: concept list)

    """


    def __init__(self, meta1:str, meta2:str):

        """
        Constructs all the necessary attributes for the  ConceptSetParser class
        
        Parameters
        ----------
        concept_file_path: str
                    a path to a .tsv  file with all the concpets (either meshets or genesets)
       
        """

        if not os.path.isfile(meta1):
            raise FileNotFoundError(f"Could not find metadata file at {meta1}")
        if not os.path.isfile(meta2):
            raise FileNotFoundError(f"Could not find metadata file at {meta2}")
        meta1_set = set()
        meta2_set = set()
        with open(meta1) as f:
            for line in f:
                meta1_set.add(line.strip())
        with open(meta2) as f:
            for line in f:
                meta2_set.add(line.strip())
        self._common_concepts = meta1_set.intersection(meta2_set)
        

    def get_concept_set_list(self, concept_file_path) -> typing.Set[ConceptSet]:
        """
        returns all the concepts sets in a file (with 3 clolumns: name, id, concept list )
        """
        if not os.path.isfile(concept_file_path):
            raise FileNotFoundError(f"Could not find concept file {concept_file_path}")
        concept_set_list = []
        with open(concept_file_path) as f:
            for line in f:
                fields = line.rstrip().split('\t')
                if len(fields) != 3:
                    raise ValueError(f"Malformed concept line {line}")
                name = fields[0]
                id = fields[1]
                concept_list = fields[2].split(";")
                # The following line discards concepts that are not contained in both metadata lists
                filtered_cs_list = [c for c in concept_list if c in self._common_concepts]
                cs = ConceptSet(name=name, id=id, concept_list=filtered_cs_list)
                concept_set_list.append(cs)
        return concept_set_list
