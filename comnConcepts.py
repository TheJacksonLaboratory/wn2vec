from wn2vec import TfConceptParser, TfConcept, Ttest
import os

dir = '/Users/niyone/Documents/GitHub/wn2vec/data/tf_wn2vec'
pm_meta = os.path.join(dir, 'pubmed_cr2.0_metadata.tsv')
pm_vectors = os.path.join(dir, 'pubmed_cr2.0_vectors.tsv')

wn_meta = os.path.join(dir, 'wn2vec2.0_metadata.tsv')
wn_vectors = os.path.join(dir, 'wn2vec2.0_vectors.tsv')

our_concept_file = 'wn2vec_genesets.tsv'

list_gene_sets = []

with open (our_concept_file) as f:
    for line in f:
        fields = line.rstrip().split('\t')
        if len(fields) != 3:
            raise ValueError(f"Malformed concept line {line}")
        concept_list = set(fields[2].split(";"))
        list_gene_sets.append(concept_list)

parser = TfConceptParser(meta_file=pm_meta, vector_file=pm_vectors, concept_set=list_gene_sets)

concept_dict_pm = parser.get_active_concept_d()
pm_vectors = parser.get_vector_list()
pm_concepts = parser.get_concept_list()
word_to_vec_dict = parser.get_concept_to_vec_d()
pm_common_genes = parser.common_genes()
print('pm', len(pm_common_genes))

parser = TfConceptParser(meta_file=wn_meta, vector_file=wn_vectors, concept_set=list_gene_sets)

wn_common_genes = parser.common_genes()
print('wn',len(wn_common_genes))


comparison = Ttest(pm_common_genes,wn_common_genes)
t_test = comparison.get_pValues_list()
print(t_test)