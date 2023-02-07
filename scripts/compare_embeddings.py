
import os
import argparse
import numpy as np
import pandas as pd
import sys

sys.path.insert(0, os.path.abspath('../src/'))
from wn2vec import TfConceptParser, TfConcept, Ttest, ConceptSetParser2, ConceptSet


import logging
log = logging.getLogger("wn2vec.log")
log.setLevel(logging.INFO)

MINIMUM_CONCEPT_SET_SIZE = 5

ch = logging.StreamHandler() # console handler
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
log.addHandler(ch)



def get_intput_files(pubtator, wordnet):
    pubtator_vector_file = pubtator
    wordnet_vector_file = wordnet
    for f in [pubtator_vector_file, wordnet_vector_file]:
        if not os.path.isfile(f):
            raise FileNotFoundError(f"Could not find input file {f}")
    pubtator_meta_file = pubtator_vector_file.replace("vectors", "metadata")
    wordnet_meta_file = wordnet_vector_file.replace("vectors", "metadata")
    for f in [pubtator_meta_file, wordnet_meta_file]:
        if not os.path.isfile(f):
            raise FileNotFoundError(f"Could not find input file {f}")
    return pubtator_vector_file,  pubtator_meta_file, wordnet_vector_file, wordnet_meta_file


## Input the embedding files with vectors and metadata for the two embeddings (pubtator and wordnet) that we want to compare
parser = argparse.ArgumentParser(description='Process MSigDb genesets into wn2vec concept set format.')
parser.add_argument('-p', '--pubtator',  type=str, required=True, help='vector embedding file for pubtator replaced concepts')
parser.add_argument('-w', '--wordnet',  type=str, required=True, help='vector embedding file for wordnet replaced concepts')
parser.add_argument('-o', type=str, default='comn_concepts.tsv',
                    help='name of output file (default=\'comn_concepts.tsv\'')
args = parser.parse_args()
out_fname = args.o
pubtator_vector_file,  pubtator_meta_file, wordnet_vector_file, wordnet_meta_file = get_intput_files(args.pubtator, args.wordnet)

concept_set_parser = ConceptSetParser2(meta1=pubtator_meta_file, meta2=wordnet_meta_file)


our_mesh_concept_file = '../data/mesh_sets.tsv'

meshs_conceptsets_list = concept_set_parser.get_concept_set_list(concept_file_path=our_mesh_concept_file)
log.info(f"We got {len(meshs_conceptsets_list)} MeSH concepts")

our_gene_concept_file = '../data/gene_sets.tsv'
gene_concept_set_list = concept_set_parser.get_concept_set_list(concept_file_path=our_gene_concept_file)
log.info(f"We got {len(gene_concept_set_list)} gene concepts")

all_concept_sets = set()
all_concept_sets.update(meshs_conceptsets_list)
all_concept_sets.update(gene_concept_set_list)



parser = TfConceptParser(meta_file=pubtator_meta_file, vector_file=pubtator_vector_file, concept_set=all_concept_sets)
concept_set_d_pm = parser.get_active_concept_d()
log.info(f"We got {len(concept_set_d_pm)} PubTator concepts from the TF2 metadata")



parser = TfConceptParser(meta_file=wordnet_meta_file, vector_file=wordnet_vector_file, concept_set=all_concept_sets)
concept_set_d_wn = parser.get_active_concept_d()
log.info(f"We got {len(concept_set_d_wn)} WordNet concepts from the TF2 metadata")


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

for cs in all_concept_sets:
    count = cs.get_concept_count()
    if count < MINIMUM_CONCEPT_SET_SIZE:
        logging.warning(f"Skipping concept {cs.name} because it had only {count} concepts, less than the threshold of {MINIMUM_CONCEPT_SET_SIZE}")
        continue
    print(f"Evaluating {cs.name}: n={cs.get_concept_count()}")
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
> python run_assessment.py  -i /data/metadata_vectors -o /data/comn_concepts.tsv

"""