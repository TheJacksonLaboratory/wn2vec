# Concept Set Evaluation

This stage involves running the `run_word2vec.py` script on two outputs: the filtered marea output (`pubmed_filt_abst.tsv`) and the WordNet replacement output (`pubmed_wn.tsv`), resulting in two sets of metadata and vector files.

The objective here is to assess whether replacing non-medical concepts with synonyms improves the efficiency of medical term embeddings.


## Overview of Concept Sets

Refer to [concept sets](concept_sets.md) for information on how we generated biomedical concept sets for testing. The wn2vec scripts leverage concept sets to evaluate the quality of concept embeddings, drawing gene sets from MSigDB and clinical concept sets from MeSH.

Additionally, we used 965 gene sets. The format of the wn2vec conceptset file is
    ```shell
    HAY_BONE_MARROW_NEUTROPHIL	M39203	ncbigene55365;ncbigene23129;ncbigene8935;ncbigene3920;ncbigene221; (...)
    ```

i.e., name, id, and semicolon-separated list of concept identifiers. 
For instance,  `ncbigene55365` refers to `TMEM176A` (transmembrane protein 176A; Homo sapiens) which has NCBI Gene ID: 55365.


### Gene Set Transformation Script

#### mSigDBgeneSetTransformer.py

**Function**: Converts gene sets from MSigDb into WN2VEC format.

**Usage**:

  - `-i` input directory with gene sets (MSigDb) files.
  - `-o`  output file for a .tsv file with the required format for WN2VEC. Default `../data/gene_sets.tsv` .
  - Example: `python mSigDBgeneSetTransformer.py -i ../data/kegg_canonical_gene_set -o data/gene_sets.tsv`

To test different gene sets, alternate the input directory to a specific gene set directory.


### Mesh Set Importer Script

#### meshImporter.py

**Function**: Downloads and formats mesh sets from <a href="https://meshb.nlm.nih.gov/" target="_blank">Mesh Database</a>.

**Usage**:

  - Reads `data/mesh_target_ids.tsv` for target mesh IDs.
  - Saves formatted data in `../data/mesh_sets.tsv`.
  - Example: `python meshImporter.py`

### Embedding Comparison Script

#### compare_embeddings.py
**Function**: Compares embeddings from `pubmed_filt_abst.tsv` and `pubmed_wn.tsv` using selected MeSH and gene sets.

**Parameters**:

  - `-i`: TensorFlow file directory.
  - `-c`: Concept set directory.
  - `-p`: Prefix for PubTator TensorFlow files.
  - `-w`: Prefix for WordNet TensorFlow files.
  - `-o`: Output file name.
  - Example: `python compare_embeddings.py -i ../data/metadata_threshold -c ../data/bio_geneset.tsv -p pubt -w wn -o comn_concepts.tsv`

## Concise Results Interpretation

- **Objective**: Evaluate the impact of synonym replacement on embedding efficiency.
- **Method**: Compare mean distances in concept clusters between `pubmed_filt_abst.tsv` and `pubmed_wn.tsv`.
- **Criteria**: A true count is recorded if a gene set/mesh set’s mean in `pubmed_wn.tsv` is lower than in `pubmed_filt_abst.tsv`.
- **Threshold**: Consider sets with at least 3 common vocabularies in the metadata files.

The results highlight the effectiveness of synonym replacement in improving the clustering of biomedical concepts.



