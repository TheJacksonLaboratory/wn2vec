import numpy as np

class TfConcept:
    def __init__(self, name, vctor) -> None:
        self._name = name
        if not isinstance(vctor, np.ndarray):
            raise ValueError("input vector needs to be numpy array")
        self._vector = vctor

    @property
    def name(self):
        return self._name

    @property
    def vector(self):
        return self._vector

    def __str__(self):
     return f"{self._name} with vector of {len(self._vector)} dimensions"

