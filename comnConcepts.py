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
pm_meta = os.path.join(dir, 'pubmed_cr2.0_metadata.tsv')
pm_vectors = os.path.join(dir, 'pubmed_cr2.0_vectors.tsv')

wn_meta = os.path.join(dir, 'wn2vec2.0_metadata.tsv')
wn_vectors = os.path.join(dir, 'wn2vec2.0_vectors.tsv')

# Intended purpose -- file with ALL of gene sets we are interested in
our_concept_file = 'wn2vec_genesets.tsv'
concept_set_parser = ConceptSetParser(concept_file_path=our_concept_file)
all_concept_sets = concept_set_parser.get_all_concepts()
concept_set_list = concept_set_parser.get_concept_set_list()



parser = TfConceptParser(meta_file=pm_meta, vector_file=pm_vectors, concept_set=all_concept_sets)
concept_set_d_pm = parser.get_active_concept_d()
parser = TfConceptParser(meta_file=wn_meta, vector_file=wn_vectors, concept_set=all_concept_sets)
concept_set_d_wn = parser.get_active_concept_d()

for cs in concept_set_list:
    pm_vecs = np.array([concept_set_d_pm.get(c).vector for c in cs.concepts if c in concept_set_d_pm])
    wn_vecs = np.array([concept_set_d_wn.get(c).vector for c in cs.concepts if c in concept_set_d_wn])
    pm_concept = TfConcept(name=cs.name, vctor=pm_vecs)
    wn_concept = TfConcept(name=cs.name, vctor=wn_vecs)
    comparison = Ttest(pm_concept, wn_concept)
    print(
        f'P-val: {comparison.p_value}; n comparisons {comparison.n_comparisons}; pubmed mean distance {comparison.mean_dist_pubmed}; wordnet mean dist {comparison.mean_dist_wordnet}')
    print(f'concepts {comparison.n_concepts}')








