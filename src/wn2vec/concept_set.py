class ConceptSet:
    """
    Represents a concept set with a name, id, and concept list.

    Concept sets are typically constructed from lines of the data/mesh_sets or data/gene_sets files, 
    for example: HAY_BONE_MARROW_ERYTHROBLAST    M39197    ncbigene8813;ncbigene2729;ncbigene81887;

    Attributes
    ----------
    name: str
        Name of a gene or mesh set (ex: HAY_BONE_MARROW_ERYTHROBLAST).
    id: str
        ID of a gene or mesh set (ex: M39197).
    concept_list: list
        A list of concepts in a set (either genes or mesh). 

    Methods
    -------
    name() -> str:
        Return the name of a concept set.
    id() -> str:
        Return the ID of a concept set.
    concepts() -> list:
        Return a list of concepts in a concept set.
    get_concept_count() -> int:
        Return the number of concepts in the set.
    """

    def __init__(self, name:str, id:str, concept_list:list):
        """
        Initialize the ConceptSet object with its name, id, and list of concepts.

        :param name: Name of the gene or mesh set.
        :type name: str
        :param id: ID of the gene or mesh set.
        :type id: str
        :param concept_list: List of concepts in the set.
        :type concept_list: list
        """
        self._name = name
        self._id = id
        self._concepts = concept_list

    @property
    def name(self) -> str:
        """
        Get the name of the concept set.

        :return: Name of the concept set.
        :rtype: str
        """
        return self._name

    @property
    def id(self) -> str:
        """
        Get the ID of the concept set.

        :return: ID of the concept set.
        :rtype: str
        """
        return self._id

    @property
    def concepts(self) -> list:
        """
        Get the list of concepts in the concept set.

        :return: List of concepts.
        :rtype: list
        """
        return self._concepts

    def get_concept_count(self) -> int:
        """
        Get the count of concepts in the set.

        :return: Number of concepts in the set.
        :rtype: int
        """
        return len(self._concepts)
