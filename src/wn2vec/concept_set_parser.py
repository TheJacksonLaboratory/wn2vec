import os
import typing
from .concept_set import ConceptSet


import logging

log = logging.getLogger("wn2vec.log")
log.setLevel(logging.INFO)


MINIMUM_CONCEPT_SET_SIZE = 5

ch = logging.StreamHandler()  # console handler
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
log.addHandler(ch)


class ConceptSetParser:
    """
    Parses concept sets and restricts comparison to identical sets of vectors.

    This class is initialized with paths to two metadata files and parses concept sets contained in both.
    This ensures that comparisons are restricted to identical sets of vectors when performing t-tests for pairwise distances,
    allowing for accurate comparison between PubTator and WordNet concept replacement strategies.

    :param meta1: A path to the first metadata file from TensorFlow with concepts from one of the embeddings (PubTator or WordNet).
    :type meta1: str
    :param meta2: A path to the second metadata file from TensorFlow with concepts from one of the embeddings (PubTator or WordNet).
    :type meta2: str
    """

    def __init__(self, meta1: str, meta2: str):
        """
        Constructs all the necessary attributes for the ConceptSetParser class.

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
        Parses the specified file and returns all the concept sets contained within.

        :param concept_file_path: Path to a .tsv file with all the concepts.
        :type concept_file_path: str

        :returns: A set containing all the concept sets in the file, each with 3 columns: name, id, concept list.
        :rtype: typing.Set[ConceptSet]


        """

        if not os.path.isfile(concept_file_path):
            raise FileNotFoundError(f"Could not find concept file {concept_file_path}")

        # Initialize concept set list and parse the specified file.
        concept_set_list = []
        with open(concept_file_path) as f:
            for line in f:
                fields = line.rstrip().split("\t")
                if len(fields) != 3:
                    raise ValueError(f"Malformed concept line {line}")
                name = fields[0]
                id = fields[1]
                concept_list = fields[2].split(";")
                # Discard concepts that are not contained in both metadata lists.
                filtered_cs_list = [c for c in concept_list if c in self._common_concepts]
                cs = ConceptSet(name=name, id=id, concept_list=filtered_cs_list)
                concept_set_list.append(cs)
        return concept_set_list
