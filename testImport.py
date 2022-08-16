from wn2vec import TfConceptParser, TfConcept
import os


dir = '/home/robinp/data/wn2vec'
pm_meta = os.path.join(dir, 'pubmed_cr2.0_metadata.tsv')
pm_vectors = os.path.join(dir, 'pubmed_cr2.0_vectors.tsv')

wn_meta = os.path.join(dir, 'wn2vec2.0_metadata.tsv')
wn_vectors = os.path.join(dir, 'wn2vec2.0_vectors.tsv')

our_concept_file = 'wn2vec_genesets.tsv'

concept_set = set()

with open (our_concept_file) as f:
    for line in f:
        fields = line.rstrip().split('\t')
        if len(fields) != 3:
            raise ValueError(f"Malformed concept line {line}")
        concepts = fields[2].split(";")
        for c in concepts:
            concept_set.add(c)
print(f"Concepts: n={len(concept_set)}")



parser = TfConceptParser(meta_file=pm_meta, vector_file=pm_vectors, concept_set=concept_set)

concept_dict_pm = parser.get_active_concept_d()
print(f"PM Concept objects: n={len(concept_dict_pm)}")

parser = TfConceptParser(meta_file=wn_meta, vector_file=wn_vectors, concept_set=concept_set)

concept_dict_wn = parser.get_active_concept_d()
print(f"WN Concept objects: n={len(concept_dict_wn)}")


## Get all of the concepts for a concept set
## compare the pairwise distances using a t test
## report when marea or WN was better and if the t test was signifant
  
