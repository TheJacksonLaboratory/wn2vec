from wn2vec import TfConceptParser, TfConcept, Ttest, ConceptSetParser, ConceptSet
import os
import argparse
import numpy as np
import typing

parser = argparse.ArgumentParser(description='Process MSigDb genesets into wn2vec concept set format.')
parser.add_argument('-i',  type=str, default='data/tf_wn2vec', required=False, help='input directory')
parser.add_argument('-o', type=str, default='wn2vec_genesets.tsv',
                    help='name of output file (default=\'wn2vec_genesets.tsv\'')
args = parser.parse_args()
input_dir = args.i
out_fname = args.o




dir = args.i

# pm_meta = os.path.join(dir, 'pubmed_cr0.0_metadata.tsv')
# pm_vectors = os.path.join(dir, 'pubmed_cr0.0_vectors.tsv')
#
# wn_meta = os.path.join(dir, 'wn2vec0.0_metadata.tsv')
# wn_vectors = os.path.join(dir, 'wn2vec0.0_vectors.tsv')



# pm_meta = os.path.join(dir, 'pubmed_cr2.0_metadata.tsv')
# pm_vectors = os.path.join(dir, 'pubmed_cr2.0_vectors.tsv')
#
# wn_meta = os.path.join(dir, 'wn2vec2.0_metadata.tsv')
# wn_vectors = os.path.join(dir, 'wn2vec2.0_vectors.tsv')



# pm_meta = os.path.join(dir, 'marea_0.1_metadata.tsv')
# pm_vectors = os.path.join(dir, 'marea_0.1_vectors.tsv')
#
# wn_meta = os.path.join(dir, 'wn2vec_0.1_metadata.tsv')
# wn_vectors = os.path.join(dir, 'wn2vec_0.1_vectors.tsv')



pm_meta = os.path.join(dir, 'marea_4.0_metadata.tsv')
pm_vectors = os.path.join(dir, 'marea_4.0_vectors.tsv')

wn_meta = os.path.join(dir, 'wn2vec_4.0_metadata.tsv')
wn_vectors = os.path.join(dir, 'wn2vec_4.0_vectors.tsv')


# Intended purpose -- file with ALL of gene sets we are interested in
# our_concept_file = 'wn2vec_genesets.tsv'
our_concept_file = 'mesh_sets.tsv'
concept_set_parser = ConceptSetParser(concept_file_path=our_concept_file)
all_concept_sets = concept_set_parser.get_all_concepts()
concept_set_list = concept_set_parser.get_concept_set_list()



parser = TfConceptParser(meta_file=pm_meta, vector_file=pm_vectors, concept_set=all_concept_sets)
concept_set_d_pm = parser.get_active_concept_d()

parser = TfConceptParser(meta_file=wn_meta, vector_file=wn_vectors, concept_set=all_concept_sets)
concept_set_d_wn = parser.get_active_concept_d()


pm_mean_distance = []
wn_mean_distance = []
p_values = []
relevant_sets_count = 0
for cs in concept_set_list:
    pm_vecs = np.array([concept_set_d_pm.get(c).vector for c in cs.concepts if c in concept_set_d_pm])
    wn_vecs = np.array([concept_set_d_wn.get(c).vector for c in cs.concepts if c in concept_set_d_wn])
    pm_concept = TfConcept(name=cs.name, vctor=pm_vecs)
    wn_concept = TfConcept(name=cs.name, vctor=wn_vecs)

    #comparison = Ttest(pm_concept, wn_concept)
    comparison = Ttest(pm_vecs, wn_vecs)
    pm_mean = comparison._mean_dist
    if comparison.n_concepts > 3:
        relevant_sets_count +=1
        #print(
            #f'P-val: {comparison.p_value}; n comparisons {comparison.n_comparisons}; pubmed mean distance {comparison.mean_dist_pubmed}; wordnet mean dist {comparison.mean_dist_wordnet}')
        p_values.append(comparison.p_value)
        pm_mean_distance.append(comparison.mean_dist_pubmed)
        wn_mean_distance.append(comparison.mean_dist_wordnet)
        #print(f'concepts {comparison.n_concepts}')



true_counts = 0
index_true_counts = []
for i in range (0, len(p_values)):
    if p_values[i] <= 0.05:
        true_counts +=1
        index_true_counts.append(i)


# Code to see which value (pm or wn) is significant in either direction
wn_less_pm = 0
pm_less_wn = 0
for index in index_true_counts:
    if wn_mean_distance[index] < pm_mean_distance[index]:
        wn_less_pm +=1
    else:
        pm_less_wn +=1


print('P_Values for all sets: ', p_values)
print(f'Mean distance for pubmed:', pm_mean_distance)
print(f'Mean distance for wordnet:', wn_mean_distance)
# print(f'Index True Counts:', index_true_counts, "\n")
print(f'In : {relevant_sets_count}, relevant gene sets {true_counts}, are the significant difference ')
print(f'Tally of when wn is less than pm: {wn_less_pm}')
print(f'Tally of when pm is less than wn: {pm_less_wn}')






