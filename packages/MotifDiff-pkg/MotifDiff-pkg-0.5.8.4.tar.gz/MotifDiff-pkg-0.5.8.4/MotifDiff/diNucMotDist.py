import numpy as np
import diNucMat as dn
from collections import namedtuple


def score_dist(pssm, prob, gran=None, size=1000):
#==============================================================================
    #- assert pssm  is a ov class diNucMat and 
    #  prob is of class diNucProbMat
    assert isinstance(pssm, dn.diNucMat)    
    assert isinstance(prob, dn.diNucProbMat)

    if gran is None:
        if size is None:
            raise ValueError("provide either gran or size. Both missing.")
        gran = (np.max(pssm) - np.min(pssm))/(size - 1)  
        
    # utility function for converting a score to an index (of the distribution)
    def vals2inds(vals, mnscore, gran):
        return np.rint(((vals - mnscore)/gran)).astype(int)
    
    # discretization and score range
    mnscore = np.floor(np.sum(np.min(pssm.values, axis=1))) #- lower bound
    mxscore = np.ceil(np.sum(np.max(pssm.values, axis=1))) #- upper bound
    if mxscore<0: mxscore=0
    nscores = int(np.rint((mxscore - mnscore) / gran) + 1) #- shouldn't really need to round
    
    # make the score distribution
    #- INITIALIZATION
    SD = np.zeros((4, nscores))
    #- FIRST POSITION
    for i in range(4):
        #- update SD at the right indices
        for j in range(4):
            SD[i, vals2inds(pssm.colMats[0, j, i], mnscore, gran)] += prob.colMats[0, j, i]

    #- need a copy of SD for updating
    SD_tmp = SD.copy()
    #- ITERATE through rest of the motif
    for pos in range(1, pssm.values.shape[0]):
        #- nuc is ending nucleotide (second of the two)
        for nuc in range(4):
            tvec   = np.zeros(nscores)
            scores = pssm.colMats[pos, :, nuc]
            shifts = np.rint(scores / gran).astype(int)
            #- i is the starting nucleotide
            for i in range(4):
                tvec += np.roll(SD_tmp[i, :], shifts[i]) * prob.trnMats[pos, i, nuc] 
            #- overwriteing SD here, so thats why we need to use SD_tmp above
            SD[nuc, :] = tvec
        #- need to update SD_tmp for the next iteration
        SD_tmp = SD.copy()

    # RETURN final motif distribution

    x = np.arange(mnscore, mxscore + gran, gran)
    y = np.sum(SD, axis=0)
    ii = np.where(y > 0)[0]
    support = mnscore + (ii) * gran
    
    x = support
    y = y[ii]
    
    #- results as a named tuple
    Dist = namedtuple('Dist', ['x', 'y'])
    return Dist(x, y)
