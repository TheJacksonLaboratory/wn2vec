import numpy as np
from itertools import combinations
import scipy.stats as stats
from scipy.stats import ttest_rel
import numpy as np


class Ttest:
    """
    Performs T-test on clusters to compare distances of concepts, considering wordnet-transformed and non-transformed clusters.

    This class calculates the mean cosine distances between transformed and non-transformed clusters and performs a T-test 
    to determine the significance of the difference between them.

    Attributes
    ----------
    :param pm_common_genes: Concept vectors without wordnet transformation (marea output).
    :type pm_common_genes: np.ndarray
    :param wn_common_genes: Transformed concept vectors through wordnet.
    :type wn_common_genes: np.ndarray
    """

    def __init__(self, pm_common_genes, wn_common_genes) -> None:
        """
        Initializes the Ttest object and computes mean distances for clusters.

        """

        if not isinstance(pm_common_genes, np.ndarray):
            raise ValueError("Need to be numpy array")
        if not isinstance(wn_common_genes, np.ndarray):
            raise ValueError("Need to be numpy array")
        self._pm_common_genes = pm_common_genes
        self._wn_common_genes = wn_common_genes
        pw_dist1 = Ttest.get_all_pairwise_distances_in_cluster(pm_common_genes)
        pw_dist2 = Ttest.get_all_pairwise_distances_in_cluster(wn_common_genes)

        self._mean_dist_pubmed = np.mean(pw_dist1)
        self._mean_dist_wordnet = np.mean(pw_dist2)
        n_comparisons_pm = len(pw_dist1)
        if n_comparisons_pm != len(pw_dist2):
            raise ValueError(f"Error - inequal number of concepts: pubemd {n_comparisons_pm} wordnet {len(pw_dist2)}")
        self._n_comparisons = n_comparisons_pm
        self._n_concepts = len(pm_common_genes)
        self._pvalue = stats.ttest_ind(a=pw_dist1, b=pw_dist2, equal_var=True)

    @staticmethod
    def get_all_pairwise_distances_in_cluster(cluster):
        """
        Computes pairwise cosine distances for a given cluster.

        :param cluster: An array of vectors representing concepts within a cluster (either genesets or meshsets).
        :type cluster: np.ndarray
        :return: A list of pairwise distances within the cluster using cosine similarity.
        :rtype: List[float]

        """

        pairwise_distance_list = []
        vec_pair = list(combinations(cluster, 2))
        for pair in vec_pair:
            vec1 = pair[0]
            vec2 = pair[1]
            cosine_similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
            pairwise_distance_list.append(cosine_similarity)
        return pairwise_distance_list
    
    @property
    def p_value(self) -> float:
        """ 
        :return: The p-value from the T-test.
        :rtype: float
        """
        return self._pvalue[1]

    @property
    def mean_dist_pubmed(self) -> float:
        """ 
        :return: Mean distance of non-transformed cluster's concepts.
        :rtype: float
        """
        return self._mean_dist_pubmed

    @property
    def mean_dist_wordnet(self) -> float:
        """ 
        :return: Mean distance of wordnet-transformed cluster's concepts.
        :rtype: float
        """
        return self._mean_dist_wordnet

    @property
    def n_comparisons(self) -> int:
        """ 
        :return: Number of pairwise comparisons performed.
        :rtype: int
        """
        return self._n_comparisons

    @property
    def n_concepts(self) -> int:
        """ 
        :return: Number of concepts in the cluster.
        :rtype: int
        """
        return self._n_concepts

    def wn_distance_smaller_than_pm(self) -> bool:
        """
        Determines if mean cosine distance between wordnet-transformed cluster's concepts is smaller than that of the non-transformed cluster's concepts.
        
        :return: True if wordnet-transformed distance is smaller, otherwise False.
        :rtype: bool
        """
        return self.mean_dist_wordnet < self._mean_dist_pubmed

    def pm_distance_smaller_than_wn(self) -> bool:
        """
        Determines if mean cosine distance between non-transformed cluster's concepts is smaller than that of the wordnet-transformed cluster's concepts.
        
        :return: True if non-transformed distance is smaller, otherwise False.
        :rtype: bool
        """
        return self._mean_dist_pubmed < self._mean_dist_wordnet

    def is_significant(self, alpha_threshold=0.05) -> bool:
        """
        Checks if the difference in distances between transformed and non-transformed clusters is statistically significant.
        
        :param alpha_threshold: The significance level for the T-test.
        :type alpha_threshold: float
        :return: True if the p-value is less than or equal to the alpha threshold, otherwise False.
        :rtype: bool
        """
        return self._pvalue[1] <= alpha_threshold
    
    # PAIR WISE COMPARISON 
    def compare_gene_modifications(self):
        # Compute pairwise cosine similarities
        pw_dist1 = Ttest.get_all_pairwise_distances_in_cluster(self._pm_common_genes)
        pw_dist2 = Ttest.get_all_pairwise_distances_in_cluster(self._wn_common_genes)

        # Compute the differences between the cosine similarities
        differences = [a - b for a, b in zip(pw_dist1, pw_dist2)]

        # Perform paired sample t-test
        t_stat, p_value = ttest_rel(pw_dist1, pw_dist2)

        # Count how many times wn_common_genes is smaller than pm_common_genes
        wn_smaller_count = sum(1 for a, b in zip(pw_dist1, pw_dist2) if b < a)

        # Count how many times pm_common_genes is smaller than wn_common_genes
        pm_smaller_count = sum(1 for a, b in zip(pw_dist1, pw_dist2) if a < b)

        # Check statistical significance
        is_significant = p_value < 0.05

        # Results
        results = {
            "wn_smaller_count": wn_smaller_count,
            "pm_smaller_count": pm_smaller_count,
            "wn_smaller_count_significant": wn_smaller_count if is_significant else 0,
            "pm_smaller_count_significant": pm_smaller_count if is_significant else 0
        }

        return results  
