
class ConceptSet:
    """
    Creates a class of a concept set with name, id, and concept list
    Each concept set is constructed from a line of the data/mesh_sets  or data/gene_sets files
    HAY_BONE_MARROW_ERYTHROBLAST	M39197	ncbigene8813;ncbigene2729;ncbigene81887;

    ...

    Attributes
    ----------
        name: str
                name of a gene or mesh set (ex:HAY_BONE_MARROW_ERYTHROBLAST )
        id: str
                id of a gene or mesh set (ex: M39197)
        concept_list: list
                a list of concepts in a set (either genes or mesh) 

    Methods
    -------
    def name(self):
        returns name of a concept set
    def id(self):
        returns id of a concept set
    def concepts(self):
        returns a list of concepts in a  concept set

    """

    def __init__(self, name, id, concept_list):
        """
        Constructs all the necessary attributes for the  ConceptSet class
        
        Parameters
        ----------
        name: str
                    name of a gene or mesh set (ex:HAY_BONE_MARROW_ERYTHROBLAST )
        id: str
                    id of a gene or mesh set (ex: M39197)
        concept_list: list
                    a list of concepts in a set (either genes or mesh) 
        """
        self._name = name
        self._id = id
        self._concepts = concept_list


    @property
    def name(self):
        """
        returns name of a concept set
        """
        return self._name

    @property
    def id(self):
        """
        returns id of a concept set
        """
        return self._id

    @property
    def concepts(self):
        """
        returns a list of concepts in a  concept set
        """
        return self._concepts