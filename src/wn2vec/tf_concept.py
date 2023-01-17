import numpy as np

class TfConcept:

    """
    creates an object of concept with name and vector 
    ...

    Attributes
    ----------
        name: str
            a name of a concept in the metadata (output of word2vector)
        
        vctor: list
            a list of vectors corresponding to the concept (out put of word2vector)

    Methods
    -------
    def name(self):
        returns the name of a concept

    def vector(self):
        returns the vector corresponding to a concept
    def __str__(self):
        returns a string of a name of a concept and dimension of its vector
    """
    def __init__(self, name, vctor) -> None:
        """
        Constructs all the necessary attributes for the  TfConcept class
        
        Parameters
        ----------
        name: str
            a name of a concept in the metadata (output of word2vector)
        
        vctor: list
            a list of vectors corresponding to the concept (out put of word2vector)
        
        """

        self._name = name
        if not isinstance(vctor, np.ndarray):
            raise ValueError("input vector needs to be numpy array")
        self._vector = vctor

    @property
    def name(self):
        """
        returns the name of a concept
        """
        return self._name

    @property
    def vector(self):
        """
        returns the vector corresponding to a concept
        """
        return self._vector

    def __str__(self):
        """
        returns a string of a name of a concept and dimension of its vector
        """
        return f"{self._name} with vector of {len(self._vector)} dimensions"

