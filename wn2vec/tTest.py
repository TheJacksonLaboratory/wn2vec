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

        def t_test(list1, list2):
            p_value = stats.ttest_ind(a=list1, b=list2, equal_var=True)
            return (p_value[1])

        p_values = []
        def all_in_one(pm , wn)

        def all_in_one(pm_common_genes, )
            for cluster in pm_common_genes:
                cluster_distance(cluster)
                mean = average_dist_cluster(cluster)
                clusters_mean.append(mean)
            return clusters_mean

