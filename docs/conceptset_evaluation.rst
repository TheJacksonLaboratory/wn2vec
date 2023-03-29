.. _conceptseteval:

======================
Concept Set Evaluation
======================

At this stage we have runed the script run_word2vec.py twice first for the filtered marea output (pubmed_filt.tsv) and secondly for the wording output (pubmed_wn.tsv)  and we have 2 metadata files and 2 vector files.

The goal of this step is to evaluate whether the replacement of non-medical vocabularies with their synonyms would increase the efficiency of embedding of medical terms.

Concept sets
^^^^^^^^^^^^
See :ref"`concept_sets`_ for background information on how we generated biomedical concept sets for testing.

The wn2vec scripts require a list of concept sets in order to assess the quality of concept embeddings. The source of gene sets for wn2vec are selected genesets from MSigDB. The source of clinical concept sets were selected concepts from MeSH

Additionally, we used X 'analogy' sets The format of the wn2vec conceptset file is

HAY_BONE_MARROW_NEUTROPHIL	M39203	ncbigene55365;ncbigene23129;ncbigene8935;ncbigene3920;ncbigene221; (...)

i.e., name, id, and semicolon-separated list of concept identifiers. For instance, ncbigene55365 refers to TMEM176A (transmembrane protein 176A; Homo sapiens) which has NCBI Gene ID: 55365.

* scripts/mSigDBgeneSetTransformer.py: this file transforms selected gene sets from MSigDb into the format required for WN2VEC.
    * ‘-i’ : input directory with genesetts (MSigDb) files from  
    * ‘-0’: output file for a .tsv file with required format for WN2VEC. Default ('../data/gene_sets.tsv') 
    * The output file has three columns: geneset name, geneset id, geneset
    * To run the script:
        * locate the file you are running + python + mSigDBgeneSetTransformer.py  + '-i' +  address of gene sets files  + '-o' + address of output_file (optional)
        * example: python mSigDBgeneSetTransformer.py -i ../data/gene_sets/kegg_canonical_gene_set -o data/gene_sets.tsv
    * To test different genesets, alternate the input directory to a specific geneset directory
* scripts/meshImporter.py : this file downloads he mesh set in the same hierarchy from https://meshb.nlm.nih.gov/ 
    * Reads a file data/mesh_target_ids.tsv' with target mesh ids
    * Transforms the meshsets into a required format for WN2VEC
    * Saves the output in default file '../data/mesh_sets.tsv’) 
    * The output file has three columns: meshlabel, mesh id, meshset
    * To run the script:
        * locate the file you are running + python + meshImporter.py 
        * example:  python meshImporter.py 

* cripts/compare_embeddings.py: Takes in vectors and metadata files from word2vec  of both filtered marea output (pubmed_filt.tsv) and word net transformed abstracts (wordnet.tsv)  and assess using both selected Mesh sets and gene sets from the above steps. 


* Parameters:
    * ‘-i’ : input directory for tensorflow files (4 files) 
    * '-c' : input directory for concept sets (MeSH sets / Gene sets)
    * ‘-p’ : prefix for pubtator tensorflow output files, e.g., pubt
    * '-w' : prefix for pubtator tensorflow output files, e.g., wn'
    * '-o' : name of output file, e.g comn_concepts.tsv
* To run the script:
    * example: python compare_embeddings.py -i ../data/metadata_threshold -c ../data/bio_geneset.tsv -p pubt -w wn -o comn_concepts.tsv




* either a file with gene sets or meshsets. It uses cosine distance to find the cluster mean distance of each geneset/mesh set in both files pubmed_filt.tsv and wordnet.tsv. Then we compare the mean distance of each geneset in both pubmed_filt.tsv or wordnet.tsv, and test using T-test the difference between both means, and if a particular geneset/mesheset’s mean of wordnet.tsv is less than the same geneset/meshet’s mean of pubmed_filt.tsv then we count that as a true count.
* In all the geneset/meshset we filter by the threshold of at leat to have 3 common vocabulary with the metadata from pubmed_filt.tsv or worndet.tsv.
    * I.e if there is a geneset or meshset which only has one gene/meshID in common with the metadata, we disregard that geneset.


