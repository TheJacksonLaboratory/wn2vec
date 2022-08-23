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

        if not isinstance(pm_common_genes, np.ndarray):
            raise ValueError("Need to be numpy array")
        if not isinstance(wn_common_genes, np.ndarray):
            raise ValueError("Need to be numpy array")

        pw_dist1 = Ttest.get_all_pairwise_distances_in_cluster(pm_common_genes)
        pw_dist2 = Ttest.get_all_pairwise_distances_in_cluster(wn_common_genes)
        self._mean_dist_pubmed = np.mean(pw_dist1)
        self._mean_dist_wordnet = np.mean(pw_dist2)
        n_comparisons_pm = len(pw_dist1)
        #if n_comparisons_pm != len(pw_dist2):
         #   raise ValueError(f"Error - inequal numbeer of concepts: pubemd {n_comparisons_pm} wordnet {len(pw_dist2)}")
        self._n_comparisons = n_comparisons_pm
        self._n_concepts = len(pm_common_genes)
        self._pvalue = stats.ttest_ind(a=pw_dist1, b=pw_dist2, equal_var=True)


    @staticmethod
    def get_all_pairwise_distances_in_cluster(cluster):
        pairwise_distance_list = []
        vec_pair = list(combinations(cluster, 2))
        for pair in vec_pair:
            vec1 = pair[0]
            vec2 = pair[1]
            cosine_similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
            pairwise_distance_list.append(cosine_similarity)
        return pairwise_distance_list

    @property
    def p_value(self):
        return self._pvalue[1]

    @property
    def mean_dist_pubmed(self):
        return self._mean_dist_pubmed

    @property
    def mean_dist_wordnet(self):
        return self._mean_dist_wordnet

    @property
    def n_comparisons(self):
        return self._n_comparisons

    @property
    def n_concepts(self):
        return self._n_concepts