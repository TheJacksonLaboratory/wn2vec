import os
from .concept_set import ConceptSet


class ConceptSetParser:

    def __init__(self, concept_file_path):
        if not os.path.isfile(concept_file_path):
            raise FileNotFoundError(f"Could not find concept file at {concept_file_path}")
        self._concept_set_list = []
        self._all_concepts = set()
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
                self._all_concepts.update(concept_list)

    def get_all_concepts(self):
        return self._all_concepts

    def get_concept_set_list(self):
        return self._concept_set_list