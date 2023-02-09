import numpy as np
from itertools import combinations
import scipy.stats as stats
import numpy as np



class Ttest:
    """
    Using Ttest to measure the singnificance between cluster mean distance of concepts of the same set
    comparing those transformed with wordnet (wn_common_genes) vs the concepts without transformation of wornet (pm_common_genes)
    ...

    Attributes
    ----------
        pm_common_genes: np.ndarray
                    an array of concept vectors without wordnet transformation (marea output)
        wn_common_genes: np.ndarray
                    an array of transformed concept vectors which were transformed through wordnet
                   
    Methods
    -------
    def get_all_pairwise_distances_in_cluster(cluster):
        Creates a dictionary from the whole data set, keys are unique words, and the values are synonyms of keys from synset
    def wn_distance_smaller_than_pm(self):
        checks whether mean cosine distance between worndet transformed cluster's concept  is smaller than untranformend  cluster's concepts
    def pm_distance_smaller_than_wn(self):
        checks whether mean cosine distance between untranformend cluster's concept  is smaller than worndet transformed cluster's concepts
    def is_significant(self, alpha_threshold=0.05):
         checks whether p_value from statistical ttest is ginificant differece for the distance between transromed vs untransformed through wordnet
    """

    def __init__(self, pm_common_genes, wn_common_genes) -> None:
        """
        Constructs all the necessary attributes for the  Ttest class
        
        Parameters
        ----------
        pm_common_genes: np.ndarray
                    an array of concept vectors without wordnet transformation (marea output)
        wn_common_genes: np.ndarray
                    an array of transformed concept vectors which were transformed through wordnet
                   
        """

        if not isinstance(pm_common_genes, np.ndarray):
            raise ValueError("Need to be numpy array")
        if not isinstance(wn_common_genes, np.ndarray):
            raise ValueError("Need to be numpy array")

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
        Creates a dictionary from the whole data set, keys are unique words, and the values are synonyms of keys from synset
        @parameter: 
            cluster: np.ndarray
             an array of vectors of conncepts of the same genesets or meshsets
        @return: returns a pair wise distance list from the vectors of the same cluster using cosine similarity 

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

    def wn_distance_smaller_than_pm(self):
        """
        checks whether mean cosine distance between worndet transformed cluster's concept  is smaller than untranformend  cluster's concepts
        """
        return self.mean_dist_wordnet  < self._mean_dist_pubmed

    def pm_distance_smaller_than_wn(self):
        """
        checks whether mean cosine distance between untranformend cluster's concept  is smaller than worndet transformed cluster's concepts
        """
        return self._mean_dist_pubmed < self._mean_dist_wordnet

    def is_significant(self, alpha_threshold=0.05):
        """
         checks whether p_value from statistical ttest is ginificant differece for the distance between transromed vs untransformed through wordnet
        """
        return self._pvalue[1] <= alpha_threshold