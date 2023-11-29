.. _home:

======
WN2Vec
======

The original word2vec method operates on individual words (tokens). However, many biomedical concepts span multiple tokens. 
For instance, *Myocardial Infarction* would be treated by word2vec as two words, but it represents a 
single medical concept. For this reason, recent approaches collapse multiword concepts into a single token prior to 
embedding by replacing the multiword concepts with a single concept id (e.g., MeSH:D009203).

In this project,  we reasoned that replacing synonyms of non-biomedical concepts with the same identifier would 
additionally improve the performance of word2vec. WordNet is a  database of synonyms, hyponyms, and meronyms that 
groups synonyms from the same lexical category (nouns, verbs, adjectives, and adverbs) into synsets. 

---------------------------
Running the WN2Vec pipeline
---------------------------

To reproduce the results in the manuscript, the following steps should be performed. Additionally,
a detailed start to finish:ref:`tutorial` is provided
with a relatively small input dataset.

1. Installation & Download data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
See :ref:`installation` for instructions on how to set up the package. 

PubMed abstracts
^^^^^^^^^^^^^^^^

To obtain PubMed abstracts, following the instructions
of the NCBI `Download PubMed Data <https://pubmed.ncbi.nlm.nih.gov/download/>`_ website. 

2. Replacement of biomedical concepts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We use the `marea <https://github.com/TheJacksonLaboratory/marea>`_ package to replace 
single- or multi-word biomedical concepts with concept identifiers.

See :ref:`rst_marea` for instructions on how to run marea to perform biomedical concept replacement.


3. WordNet-based synonym Replacement
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Next we performed non-biomedical synonyms replacement using WordNet identifers from WordNet library. 

See :ref:`wordnetreplacement` for details and instructions to perform wordNet-based synonym replacement.


4. word2vec embedding
^^^^^^^^^^^^^^^^^^^^^

We perform word2vec embedding using Gensim word2vec model. In order to compare the results of embedding with and without WordNet replacement, embedding is performed on both datasets separately.

See :ref:`word2vec` for details and instructions to perform word2vec embedding.

This step has to be run twice, first for marea output (pubtator) and second for step3 output, where concepts were replaced by their synonyms, before going to the following step 


5. Evaluating concept sets 
^^^^^^^^^^^^^^^^^^^^^^^^^^

Our hypothesis is that non-biomedical concept synonym replacement will improve embeddings as judged by a smaller distance of related 
concepts to each other. 

To assess this, we defined 5 different biomedical concept sets representing genetic and genomic functions (gene sets) and biomedical concepts taken from MeSH  (4 gene sets of sets and 1 MeSH set of sets): 
* biocarta_canonical_gene_set
* kegg_canonical_gene_set
* bp_gene_ontology_gene_set 
* pid_canonical_gene_set 

We used the word2vec embeddings of each concepts in the sets to evaluate the impact of WordNet-based synonym replacemnt using the mean cluster coside distance of the corresponding concepts.

See :ref:`conceptset_evaluation` for details.





.. toctree::
    :caption: wn2vec
    :name: wn2vec
    :maxdepth: 1

    install
    marea
    wordnetreplacement
    word2vec
    concept_sets
    conceptset_evaluation
    tutorial
    contributing
    authors
    history
    LICENSE

 

--------
Feedback
--------

The best place to leave feedback, ask questions, and report bugs is the `WN2vec Issue Tracker <https://github.com/TheJacksonLaboratory/wn2vec/issues>`_.

