# WN2Vec

The original word2vec method operates on individual words (tokens). However, many biomedical concepts span multiple tokens.
For instance, *Myocardial Infarction* would be treated by word2vec as two words, but it represents a single medical concept. For this reason, recent approaches collapse multiword concepts into a single token prior to
embedding by replacing the multiword concepts with a single concept id (e.g., [MeSH:D009203](https://meshb.nlm.nih.gov/record/ui?ui=D009203){:target="_blank"}).

In this project, we reasoned that replacing synonyms of non-biomedical concepts with the same identifier would additionally improve the performance of word2vec. [WordNet](https://wordnet.princeton.edu/){:target="_blank"} is a database of synonyms, hyponyms, and meronyms that
groups synonyms from the same lexical category (nouns, verbs, adjectives, and adverbs) into synsets.

## Running the WN2Vec pipeline

To reproduce the results in the manuscript, the following steps should be performed. Additionally,
a detailed start to finish [tutorial](tutorial.md) is provided
with a relatively small input dataset.

### 1. Installation & Download data

See [installation](install.md) for instructions on how to set up the package.

#### PubMed abstracts

To obtain PubMed abstracts, follow the instructions of the NCBI <a href="https://pubmed.ncbi.nlm.nih.gov/download/" target="_blank">Download PubMed Data</a> website.


### 2. Replacement of biomedical concepts

We use the <a href="https://github.com/TheJacksonLaboratory/marea" target="_blank">marea</a> package to replace single- or multi-word biomedical concepts with concept identifiers.


See [marea](marea.md) for instructions on how to run marea to perform biomedical concept replacement.

### 3. WordNet-based synonym Replacement

Next we performed non-biomedical synonyms replacement using WordNet identifiers from the WordNet library.

See [wordnetreplacement](wordnetreplacement.md) for details and instructions to perform WordNet-based synonym replacement.

### 4. word2vec embedding

We perform word2vec embedding using the Gensim word2vec model. In order to compare the results of embedding with and without WordNet replacement, embedding is performed on both datasets separately.

See [word2vec](word2vec.md) for details and instructions to perform word2vec embedding.

This step has to be run twice, first for marea output (pubtator) and second for step 3 output, where concepts were replaced by their synonyms, before going to the following step.

### 5. Evaluating concept sets

Our hypothesis is that non-biomedical concept synonym replacement will improve embeddings as judged by a smaller distance of related
concepts to each other.

To assess this, we defined 5 different biomedical concept sets representing genetic and genomic functions (gene sets) and biomedical concepts taken from MeSH  (four  sets of gene concept sets and one set of MeSH concept sets):

- biocarta_canonical_gene_set

- kegg_canonical_gene_set

- bp_gene_ontology_gene_set

- pid_canonical_gene_set


We used the word2vec embeddings of each concept in the sets to evaluate the impact of WordNet-based synonym replacement using the mean cluster cosine distance of the corresponding concepts.

See [conceptset_evaluation](conceptset_evaluation.md) for details.

---

## Feedback

The best place to leave feedback, ask questions, and report bugs is the <a href="https://github.com/TheJacksonLaboratory/wn2vec/issues" target="_blank">WN2vec Issue Tracker</a>.
