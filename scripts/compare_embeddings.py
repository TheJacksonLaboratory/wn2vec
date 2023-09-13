
import os
import argparse
import numpy as np
import pandas as pd
import sys

sys.path.insert(0, os.path.abspath('../src/'))
from wn2vec import Tf2FileParser,TfConceptParser, TfConcept, Ttest, ConceptSetParser, ConceptSet


import logging
log = logging.getLogger("wn2vec.log")
log.setLevel(logging.INFO)

MINIMUM_CONCEPT_SET_SIZE = 5

#ch = logging.StreamHandler() # console handler
#ch.setLevel(logging.DEBUG)
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#ch.setFormatter(formatter)
#log.addHandler(ch)



## Input the embedding files with vectors and metadata for the two embeddings (pubtator and wordnet) that we want to compare
parser = argparse.ArgumentParser(description='Process MSigDb genesets into wn2vec concept set format.')
parser.add_argument('-i', '--indir', type=str, required=True, help='input directory for tensorflow files')
parser.add_argument('-c', '--concepts', type=str, required=True, help='input directory for concept sets (MeSH sets / Gene sets)')
parser.add_argument('-p', '--pubtator',  type=str, required=True, help='prefix for pubtator tensorflow output files, e.g., pubt')
parser.add_argument('-w', '--wordnet',  type=str, required=True, help='prefix for wornet transform tensorflow output files, e.g., wn')
parser.add_argument('-o', type=str, default='comn_concepts.tsv',
                    help='name of output file (default=\'comn_concepts.tsv\'')
args = parser.parse_args()
out_fname = args.o

tf2parser = Tf2FileParser(indir=args.indir, pubtator_prefix=args.pubtator, wordnet_prefix=args.wordnet)
pubtator_vector_file,  pubtator_meta_file, wordnet_vector_file, wordnet_meta_file = tf2parser.get_files()

log.info(f"pubtator_vector_file: {pubtator_vector_file}")
log.info(f"pubtator_meta_file: {pubtator_meta_file}")
log.info(f"wordnet_vector_file: {wordnet_vector_file}")
log.info(f"wordnet_meta_file: {wordnet_meta_file}")



concept_set_parser = ConceptSetParser(meta1=pubtator_meta_file, meta2=wordnet_meta_file)


# Pass in the concept set directory, 4 gene sets & 1 meshset 

our_concept_file = args.concepts

conceptsets_list = concept_set_parser.get_concept_set_list(concept_file_path=our_concept_file)
log.info(f"We got {len(conceptsets_list)} concepts")

all_concept_sets = set()
all_concept_set_objects = set()
for cs in conceptsets_list:
    all_concept_sets.update(cs.concepts)
    all_concept_set_objects.add(cs)



log.info(f"All concepts {len(all_concept_sets)}")


parser = TfConceptParser(meta_file=pubtator_meta_file, vector_file=pubtator_vector_file, concept_set=all_concept_sets)
pubtator_concept_set_d = parser.get_active_concept_d()
log.info(f"We got {len(pubtator_concept_set_d)} PubTator concepts from the TF2 metadata")

parser = TfConceptParser(meta_file=wordnet_meta_file, vector_file=wordnet_vector_file, concept_set=all_concept_sets)
wordnet_concept_set_d = parser.get_active_concept_d()
log.info(f"We got {len(wordnet_concept_set_d)} WordNet concepts from the TF2 metadata")


pubtator_relevant_concepts = list(pubtator_concept_set_d.keys())
wn_relevant_concepts = list(wordnet_concept_set_d.keys())

pm_relevant_concepts_length= len(pubtator_relevant_concepts)
wn_relevant_concepts_length = len(wn_relevant_concepts)



pm_mean_distance = []
wn_mean_distance = []
p_values = []
relevant_sets_count = 0

comparison_dictionary_list = []


sig_wn = 0
sig_pm = 0
wn_less = 0
pm_less = 0

for cs in all_concept_set_objects:
    count = cs.get_concept_count()
    if count < MINIMUM_CONCEPT_SET_SIZE:
        #logging.warning(f"Skipping concept {cs.name} because it had only {count} concepts, less than the threshold of {MINIMUM_CONCEPT_SET_SIZE}")
        continue
    print(f"Evaluating {cs.name}: n={cs.get_concept_count()}")
    pm_vecs = np.array([pubtator_concept_set_d.get(c).vector for c in cs.concepts if c in pubtator_concept_set_d])
    wn_vecs = np.array([wordnet_concept_set_d.get(c).vector for c in cs.concepts if c in wordnet_concept_set_d])
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
df.set_index('name', inplace=True)
log.info(f"Outputting results to {out_fname}")

df.to_csv(out_fname, sep='\t')

# sample way of running the code using arparse:
"""

python compare_embeddings.py -i ../data/metadata_vectors -c ../data/bio_geneset.tsv -p pubt -w wn -o comn_concepts.tsv


"""