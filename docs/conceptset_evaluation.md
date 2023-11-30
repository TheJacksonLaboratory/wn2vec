# Concept Set Evaluation

At this stage, we have run the script `run_word2vec.py` twice: first for the filtered marea output (`pubmed_filt_abst.tsv`) and secondly for the wording output (`pubmed_wn.tsv`). As a result, we have 2 metadata files and 2 vector files.

The goal of this step is to evaluate whether the replacement of non-medical vocabularies with their synonyms would increase the efficiency of embedding of medical terms.

## Concept sets

See [concept sets](concept_sets.md) for background information on how we generated biomedical concept sets for testing.

The wn2vec scripts require a list of concept sets in order to assess the quality of concept embeddings. The source of gene sets for wn2vec are selected gene sets from MSigDB. The source of clinical concept sets were selected concepts from MeSH.

Additionally, we used 965 gene sets. The format of the wn2vec conceptset file is:


i.e., name, id, and semicolon-separated list of concept identifiers. For instance, ncbigene55365 refers to TMEM176A (transmembrane protein 176A; Homo sapiens) which has NCBI Gene ID: 55365.

### scripts/mSigDBgeneSetTransformer.py

- This file transforms selected gene sets from MSigDb into the format required for WN2VEC.

`-i`: input directory with gene sets (MSigDb) files.

`-o`: output file for a .tsv file with the required format for WN2VEC. Default ('../data/gene_sets.tsv').

- The output file has three columns: gene set name, gene set id, gene set.

- To run the script:

    Command: `python mSigDBgeneSetTransformer.py -i [input directory] -o [output file]`

    Example: `python mSigDBgeneSetTransformer.py -i ../data/gene_sets/kegg_canonical_gene_set -o data/gene_sets.tsv`

To test different gene sets, alternate the input directory to a specific gene set directory.


### scripts/meshImporter.py

This file downloads the mesh set in the same hierarchy from [https://meshb.nlm.nih.gov/](https://meshb.nlm.nih.gov/).
- Reads a file `data/mesh_target_ids.tsv` with target mesh ids.

- Transforms the mesh sets into the required format for WN2VEC.

- Saves the output in the default file (`../data/mesh_sets.tsv`).

- The output file has three columns: mesh label, mesh id, mesh set.

- To run the script:

    Command: `python meshImporter.py`

    Example: `python meshImporter.py`

### scripts/compare_embeddings.py

Takes in vectors and metadata files from word2vec of both filtered marea output (`pubmed_filt.tsv`) and WordNet transformed abstracts (`wordnet.tsv`) and assesses using both selected MeSH sets and gene sets from the above steps.

Parameters:

- `-i`: input directory for TensorFlow files (4 files).

- `-c`: input directory for concept sets (MeSH sets / Gene sets).

- `-p`: prefix for PubTator TensorFlow output files, e.g., `pubt`.

- `-w`: prefix for WordNet TensorFlow output files, e.g., `wn`.

- `-o`: name of the output file, e.g., `comn_concepts.tsv`.


- To run the script:
    Example: `python compare_embeddings.py -i ../data/metadata_threshold -c ../data/bio_geneset.tsv -p pubt -w wn -o comn_concepts.tsv`

The process involves using cosine distance to find the cluster mean distance of each gene set/mesh set in both files `pubmed_filt.tsv` and `wordnet.tsv`. We then compare the mean distance of each gene set in both `pubmed_filt.tsv` or `wordnet.tsv`, and test using a T-test the difference between both means. If a particular gene set/mesh set’s mean of `wordnet.tsv` is less than the same gene set/mesh set’s mean of `pubmed_filt.tsv`, then we count that as a true count. In all gene sets/mesh sets, we filter by the threshold of at least having 3 common vocabularies with the metadata from `pubmed_filt.tsv` or `wordnet.tsv`. I.e., if there is a gene set or mesh set which only has one gene/mesh ID in common with the metadata, we disregard that gene set.
