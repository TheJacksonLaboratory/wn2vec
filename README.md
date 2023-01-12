# wn2vec
Wordnet 2 vector



## Setup
(TODO install package from PyPI, for now we will do local install)
- create a virtual environment
- pip-install the build package
- do a local build
- then we can use the scripts in the 'scripts' subdirectory with the wn2vec package
```
python3 -m venv venv
source venv/bin/activate
pip install build
python3 -m build .
```



## Part I: Marea : (marea1.0 @ HPC)
Filter PubMed articles for relevance based on year of publication and apply PubTator Central concept recognition to the titles and abstracts of relevant articles. 
### Step 1:  Requirements (step 1 of original Marea)
- Install all required libraries

### Step 2: Download .Xml Files ( step 2 of original Marea)
- NCBI's FTP site makes available gzipped .xml files containing titles, abstracts, and metadata for all PubMed articles.

### Step 3: Extract .txt from .xml (step 3 of original Marea)
- scripts */xml2txt.py* extracts key fields for each article recorded in the gzipped .xml file, eliminates .xml formatting, and writes the result to a text file
- The fields of interest are:
  - PubMed ID
  - Year of publication (the earliest one if the entry has multiple dates with different years)
  - MeSH descriptors (if any)
  - keywords (if any)
  - abstract (if any)

### Step 4: Concept replacement with PubTator Central ( Step 5 of original Marea)
- Download PubMed articles from PubTator Central from the NLM site. bioconcepts2pubtatorcentral.offset.gz from the PubTator Central ftp sit
- *scripts/pubtate.py* applies all the offset file's concept replacements to the title and abstract of each article and writes them to bioconcepts2pubtatorcentral.replaced. 

#### Step 5: Text post processing: (Edited step 6 of original Marea)

- *scripts/post_process.py* takes as input the file produced by pubtate.py and cleans up the text into which pubtate.py has inserted concept identifiers.
- *post_process.py* removes stop words, whether lowercase or capitalized, from the title and abstract. Uppercase acronyms of length ≥ 2, even those that coincide with stop words, are not changed. marea starts with the nltk stop word list for English and adds some new stop words. Any letter of the alphabet that occurs as a single-character token is a stop word. Post-processing also removes all punctuation symbols, including hyphens and underscores within words: the parts of a compound word become separate tokens. To reduce the size of the vocabulary, the remaining tokens are lemmatized with the WordNetLemmatizer from nltk. The last step converts everything to lowercase.
- added an extra urgument of ‘-f’ for filtering or not”, if you want to filter, then you will need  -r : directory of relevant abstracts, if you don’t need to filter, you won’t need -r  directory. 
- Out puts a .tsv file with two columns (pubmed ID & Abstract)  instead of 3 as original Marea

### Step 6: Filtering & Mapping :  
- */filter/newFilter.py* 
- Takes in path to pubmed_txt (year, pubmed ID, abstracts) (from step3)  , path to pubmed_cr (pubmed ID, abstracts ) (from step6) and threshold (year)
- Returns a .tsv file with three columns (pubmed ID, year, abstracts) 

## Part II: WNTransform:(wn2vec1.0 @ HPC) 

- Takes in pubmed_filt.tsv (output of part1) and the output file wordnet.tsv  with three columns: pubmed ID, publication year, abstract
#### Overview:
- */wn2vec/wntransformer.py* 
- Takes in Marea output file (pubmed_filt.tsv) file which has filtered pubmed abstracts by year and it has been cleaned by removing stop words, and other clean ups (refer to step 5, of PartI)
- *wntransformer.py* replaces the vocabulary in pubmed_filt.tsv with their synonyms using wordnet library from nltk. The words are sorted by their frequency of occurrence in the whole file, and all the words whose frequency is less than the threshold, are subjected to be replaced with their synonym word. The threshold is the mean of the frequency of occurrence of all vocabularies in he text. 
- Wordnet provides a list of synonyms of a word: for example 
  - **vocabulary1** : “blood” **has synonym list**: 
  ``` ['blood', 'blood', 'blood', 'rake', 'rakehell', 'profligate', 'rip', 'blood', 'roue', 'lineage', 'line', 'line_of_descent', 'descent', 'bloodline', 'blood_line', 'blood', 'pedigree', 'ancestry', 'origin', 'parentage', 'stemma', 'stock', 'blood', 'blood'] ```
  - **vocabulary2** : “lineage” **has a synonym list** : ``` ['lineage', 'lineage', 'line', 'line_of_descent', 'descent', 'bloodline', 'blood_line', 'blood', 'pedigree', 'ancestry', 'origin', 'parentage', 'stemma', 'stock', 'descent', 'line_of_descent', 'lineage', 'filiation', 'linage', 'lineage', 'linage', 'lineage', 'ancestry', 'lineage', 'derivation', 'filiation'] ```
  - If in order of frequency “blood” occurs more than “lineage” and “lineage”s frequency occurrence is less than threshold, it will be replaced by “blood” even though in the list of synonym of “lineage” there might be a vocabulary “blood”. 
  - If the vocabulary occurs once in the vocabulary or it does not occur in the list of high frequency words’ synonyms, it will stay as it is without being replaced. 

##### Example:
```
Before transformation: '163319 1975     heterogeneity quanitity plasma measure plasma 13 patient thirteen 13 xiii amount  measure bill step quantity'
 ```
 ```
counter = {'heterogeneity': 1, 'quanitity':2,  'plasma':2, 'measure':2, '13':2,  'patient':1, 'thirteen':1 , 'xiii':1, 'amount':1,  'bill':1, 'step':1 }
Vocab_list by frequency =  ['quanitity','plasma','measure','13','heterogeneity','patient','thirteen','xiii','amount','bill', 'step' ]
 ```
 ```
After transformation: 'heterogeneity quantity plasma measure plasma 13 patient 13 13 13 measure measure measure measure quantity'
```

## Part III: Embedding: (word2vec_tf @ HPC) 
- */word2vec_tf/word2vector.py* 
- Parameters: 
  - takes in pubmed_filt.tsv (part I)  or wordnet.tsv (part II) 
  - Names of vectors, (example: pubmed_cr2.0_vectors.tsv) 
  - Name of metadata (example: pubmed_cr2.0_metadata.tsv)
- This step has to be run twice, first for pubmed_filt.tsv and second for wordnet.tsv before going to step 4
- Tensorflow code for word2vector which takes in .tsv file and returns the metadata file and Vector file: https://www.tensorflow.org/tutorials/text/word2vec
- Used 50000 vocabulary size, they are ordered by frequency of occurrence in the large dataset of abstracts in pubmed_filt.tsv(part I)  or wordnet.tsv (part II)
- We used a continuous skip-gram model, where we were predicting words within a certain range before and after the current word in the same sentence. 
- The model is trained on skip-grams, which are n-grams that allow tokens to be skipped. 
- The context of a word can be represented through a set of skip-gram pairs of (target_word, context_word) where context_word appears in the neighboring context of target_word.
- The training objective of the skip-gram model is to maximize the probability of predicting context words given the target word. 
- Link to the code we modified: https://colab.research.google.com/github/tensorflow/docs/blob/master/site/en/tutorials/text/word2vec.ipynb#scrollTo=gK1gN1jwkMpU

## Part IV: Testing : 
##### Concept sets
- The wn2vec scripts require a list of concept sets in order to assess the quality of concept embeddings. The source of gene sets for wn2vec
are selected genesets from MSigDB. The source of clinical concept sets were selected concepts from MeSH. Additionally, we used X 'analogy' sets
The format of the wn2vec conceptset file is
```
HAY_BONE_MARROW_NEUTROPHIL	M39203	ncbigene55365;ncbigene23129;ncbigene8935;ncbigene3920;ncbigene221; (...)
```
i.e., name, id, and semicolon-separated list of concept identifiers. For instance, ncbigene55365 refers to TMEM176A (transmembrane protein 176A; Homo sapiens) which
has NCBI Gene ID: 55365.

- */mSigDBgeneSetTransformer.py* : this file transforms selected gene sets from [MSigDb](https://www.gsea-msigdb.org/gsea/msigdb/) into the format required for WN2VEC. 
    - ‘-i’ : input directory with MSigDb files
    - ‘-0’: output file for a .tsv file with required format for WN2VEC. Default = \‘wn2vec_genesets.tsv'
    - Three columns: geneset name, geneset id, geneset
- */meshImporter.py* : this file downloads he mesh set in the same hierarchy from [link](https://meshb.nlm.nih.gov/?_gl=1*1vw3j9c*_ga*MjA3ODkzNDM1LjE2NTcyOTU2MTg.*_ga_P1FPTH9PL4*MTY2MTQzMzU0MC4xNC4xLjE2NjE0MzM1NTMuMC4wLjA.)
    - Reads a file data/mesh_target_ids.tsv' with target mesh ids 
    - Transforms the meshsets into a required format for WN2VEC 
    - Saves the output in default file “mesh_sets.tsv” 
    - Three columns: meshlabel, mesh id, meshset
- */commonConcepts.py*:  Takes in vectors and metadata files from word2vec (part III) of both pubmed_filt.tsv  (part I) and wordnet.tsv (part II) and either a file with gene sets or meshsets. It uses cosine distance to find the cluster mean distance of each geneset/mesh set in both files pubmed_filt.tsv and wordnet.tsv. Then we compare the mean distance of each geneset in both pubmed_filt.tsv or wordnet.tsv, and test using T-test the difference between both means, and if a particular geneset/mesheset’s  mean of wordnet.tsv is less than the same geneset/meshet’s mean of pubmed_filt.tsv then we count that as a true count.
- In all the geneset/meshset we filter by the threshold of at leat to have 3 common vocabulary with the metadata from pubmed_filt.tsv or worndet.tsv. 
  - I.e if there is a geneset or meshset which only has one gene/meshID in common with the metadata, we disregard that geneset. 
- Parameters: 
    - ‘-i’ : input directory of 4 files (pubmed_filt_metadata.tsv, pubmed_filt_vectors.tsv, wordnet_metadata.tsv, wordnet_vectors.tsv)
    - ‘-o’: input path to wn2vec_genesets.tsv (for genesets) or mesh_sets.tsv (for meshsets) , the default =  default='wn2vec_genesets.tsv'
