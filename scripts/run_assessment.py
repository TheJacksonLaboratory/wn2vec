
import os
import argparse
import numpy as np
import pandas as pd
import typing

import wn2vec 
from wn2vec import TfConceptParser, TfConcept, Ttest, ConceptSetParser, ConceptSet


import logging
log = logging.getLogger("wn2vec.log")
log.setLevel(logging.INFO)

MINIMUM_CONCEPT_SET_SIZE = 5

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
# add the handlers to the logger
log.addHandler(ch)



parser = argparse.ArgumentParser(description='Process MSigDb genesets into wn2vec concept set format.')
parser.add_argument('-i',  type=str, required=True, help='input directory with word2vector.py output files')
parser.add_argument('-o', type=str, default='../data/comn_concepts.tsv',
                    help='name of output file (default=\'comn_concepts.tsv\'')
args = parser.parse_args()
input_dir = args.i
out_fname = args.o

dir = args.i


"""
pm_meta = os.path.join(dir, '2018_filt_metadata.tsv')
pm_vectors = os.path.join(dir, '2018_filt_vector.tsv')

wn_meta = os.path.join(dir, '2018_wn_metadata.tsv')
wn_vectors = os.path.join(dir, '2018_wn_vector.tsv')


#100000
pm_meta = os.path.join(dir, '100000_filt_metadata.tsv')
pm_vectors = os.path.join(dir, '100000_filt_vector.tsv')

wn_meta = os.path.join(dir, '100000_wn_metadata.tsv')
wn_vectors = os.path.join(dir, '100000_wn_vector.tsv')
"""
#2015
pm_meta = os.path.join(dir, '2015_filt_sumner_metadata.tsv')
pm_vectors = os.path.join(dir, '2015_filt_sumner_vector.tsv')

wn_meta = os.path.join(dir, '2015_wn_sumner_metadata.tsv')
wn_vectors = os.path.join(dir, '2015_wn_sumner_vector.tsv')
"""

#2010
pm_meta = os.path.join(dir, '2010_filt_sumner_metadata.tsv')
pm_vectors = os.path.join(dir, '2010_filt_sumner_vector.tsv')

wn_meta = os.path.join(dir, '2010_wn_sumner_metadata.tsv')
wn_vectors = os.path.join(dir, '2010_wn_sumner_vector.tsv')
"""

# Intended purpose -- file with ALL of gene sets we are interested in


#our_mesh_concept_file = '../data/0_mesh_sets.tsv'
our_mesh_concept_file = '../data/mesh_sets.tsv'
mesh_concept_set_parser = ConceptSetParser(concept_file_path=our_mesh_concept_file)
all_concept_sets = mesh_concept_set_parser.get_all_concepts()
concept_set_list = mesh_concept_set_parser.get_concept_set_list()
log.info(f"We got {len(concept_set_list)} MeSH concepts")

our_gene_concept_file = '../data/gene_sets_100.tsv'
#our_gene_concept_file = '../data/gene_sets_biocarta.tsv'
#our_gene_concept_file = '../data/gene_sets_kegg.tsv'
#our_gene_concept_file = '../data/gene_sets_bp.tsv'
#our_gene_concept_file = '../data/gene_sets_pid.tsv'

#our_gene_concept_file = 'data/gene_sets.tsv'
gene_concept_set_parser = ConceptSetParser(concept_file_path=our_gene_concept_file)
gene_concept_sets = gene_concept_set_parser.get_all_concepts()
gene_concept_set_list = gene_concept_set_parser.get_concept_set_list()
log.info(f"We got {len(gene_concept_set_list)} gene concepts")

all_concept_sets.update(gene_concept_sets)
concept_set_list.extend(gene_concept_set_list)


parser = TfConceptParser(meta_file=pm_meta, vector_file=pm_vectors, concept_set=all_concept_sets)
concept_set_d_pm = parser.get_active_concept_d()


parser = TfConceptParser(meta_file=wn_meta, vector_file=wn_vectors, concept_set=all_concept_sets)
concept_set_d_wn = parser.get_active_concept_d()

pm_relevant_concepts = list(concept_set_d_pm.keys())
wn_relevant_concepts = list(concept_set_d_wn.keys())

pm_relevant_concepts_length= len(pm_relevant_concepts)
wn_relevant_concepts_length = len(wn_relevant_concepts)


for  concept in wn_relevant_concepts:
    if concept in pm_relevant_concepts:
        continue
    else:
        del concept_set_d_wn[concept]



pm_mean_distance = []
wn_mean_distance = []
p_values = []
relevant_sets_count = 0

comparison_dictionary_list = []


sig_wn = 0
sig_pm = 0
wn_less = 0
pm_less = 0

for cs in concept_set_list:
    
    print(cs)
    pm_vecs = np.array([concept_set_d_pm.get(c).vector for c in cs.concepts if c in concept_set_d_pm])
    
    wn_vecs = np.array([concept_set_d_wn.get(c).vector for c in cs.concepts if c in concept_set_d_wn])
    pm_concept = TfConcept(name=cs.name, vctor=pm_vecs)
    wn_concept = TfConcept(name=cs.name, vctor=wn_vecs)
    comparison = Ttest(pm_common_genes=pm_vecs, wn_common_genes=wn_vecs)

     
    if comparison.n_concepts > MINIMUM_CONCEPT_SET_SIZE:
        d  = {'name': cs.name, 
        'comparisons': comparison.n_comparisons,
        'concepts': comparison.n_concepts,
        'mean_distance_pm': comparison.mean_dist_pubmed,
        'mean_distance_wn': comparison.mean_dist_wordnet,
        'pval': comparison.p_value}
        comparison_dictionary_list.append(d)
        if comparison.is_significant():
            if comparison.wn_distance_smaller_than_pm():
                sig_wn += 1
            elif comparison.pm_distance_smaller_than_wn():
                sig_pm += 1
        if comparison.wn_distance_smaller_than_pm():
            wn_less += 1
        else:
            pm_less += 1

log.info(f"WN relevant concepts {wn_relevant_concepts_length} and PM relevant concepts {pm_relevant_concepts_length}")

log.info(f"WN sig {sig_wn} and PM sig {sig_pm}")
log.info(f"WN LESS  {wn_less} and PM LESS {pm_less} (irregardless of pvalue)")

df = pd.DataFrame(comparison_dictionary_list) 

log.info(f"Outputting results to {out_fname}")

df.to_csv(out_fname, sep='\t')

# sample way of running the code using arparse:
"""
locate the file you are running + python + run_assessment.py  + '-i' +  address of word2vector output (metadata & vectors) + address of output_file (optional)
example: 
> python run_assessment.py  -i /Users/niyone/Desktop/testing/metadata_vectors -o comn_concepts.tsv

"""