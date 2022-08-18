import os
import numpy as np
from itertools import combinations
import scipy.stats as stats
import numpy as np
from scipy.stats import ttest_ind

from .tf_concept import TfConcept
from collections import defaultdict




class Ttest:
    def __init__(self, pm_common_genes, wn_common_genes) -> None:
        # -->  Pre_Step 2: Finding average cosine distance of a cluster

        self._p_values = []
        self._trueCounts = 0

        def distanceVectors(vector1, vector2):
            cosine_similarity = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
            return cosine_similarity

        # cosine_distance between 2 vectors
        # Average cosine distance of vectors in a cluster

        def cluster_distance(cluster):
            clust_dist = []
            vec_pair = list(combinations(cluster, 2))
            for pair in vec_pair:
                dist = distanceVectors(pair[0], pair[1])
                clust_dist.append(dist)
            return clust_dist

        def t_test(cluster1, cluster2):
            list1 = cluster_distance(cluster1)
            list2 = cluster_distance(cluster2)
            p_value = stats.ttest_ind(a=list1, b=list2, equal_var=True)
            return (p_value[1])


        for i in range (0,len(pm_common_genes)):
            self._p_values.append(t_test(pm_common_genes[i], wn_common_genes[i]))

        for pValue in self._p_values:
            if pValue < 0.05:
                self._trueCounts += 1




    def get_pValues_list(self):
        return self._p_values
    def get_True_counts(self):
        return self._trueCounts