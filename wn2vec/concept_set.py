



class ConceptSet:
    """
    Each concept set is constructed from a line of the wn2vec_genesets/mesh file
    HAY_BONE_MARROW_ERYTHROBLAST	M39197	ncbigene8813;ncbigene2729;ncbigene81887;
    """

    def __init__(self, name, id, concept_list):
        self._name = name
        self._id = id
        self._concepts = concept_list


    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    @property
    def concepts(self):
        return self._concepts