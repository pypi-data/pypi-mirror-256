import numpy as np
import itertools as itt

class diNucMat:
    def __init__(self, values, colnames) -> None:
        #- check if colnames is a 1-D array with 16 elements, each a dinucleotide in the correct order
        assert colnames == ["".join(i) for i in itt.product(["A","C","G","T"], repeat=2)]
        self.values   = values
        self.colnames = colnames
        
    @property
    def values(self):
        return self._values 
    
    @values.setter
    def values(self, values):
        #- check if probs is a 2-D array with 16 columns
        assert len(values.shape) == 2
        assert values.shape[1] == 16
        assert values.shape[0] > 0
        self._values = values
        #- make the column matrices, rely on correct column order
        #  therefore need the assert in init...
        self._colMats = np.reshape(self.values, newshape=(values.shape[0], 4, 4))

    @property
    def colMats(self):
        return self._colMats    
    
    @property
    def colnames(self):
        return self._colnames
    
    @colnames.setter
    def colnames(self, colnames):
        self._colnames = colnames
    

 #- specifically for probabiltity matricees   
class diNucProbMat(diNucMat):
    #- override the values setter for extra checks
    @diNucMat.values.setter
    def values(self, values):
        #- check if probs is a 2-D array with 16 columns
        assert len(values.shape) == 2
        assert values.shape[1] == 16
        assert values.shape[0] > 0
        #- check if all values are between 0 and 1
        assert np.all(values >= 0)
        assert np.all(values <= 1)
        #- check if the rows sum to 1
        assert np.all(np.isclose(np.sum(values, axis=1), 1))
        self._values = values
        #- make the column matrices, rely on correct column order
        #  therefore need the assert in init...
        self._colMats = np.reshape(self.values, newshape=(self.values.shape[0], 4, 4))
        #- make the transition matrices (row normalized column matrices)
        self._trnMats = self._colMats / np.sum(self._colMats, axis=2, keepdims=True)
    
    @property
    def trnMats(self) -> np.array:
        return self._trnMats
        
