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
pip install .
```


## Set up documentation

Enter the following code to install mkdocs and run a server locally. The GitHub action will create a comparable site online.

```
python3 -m venv venv
source venv/bin/activate
pip install mkdocs-material
pip install mkdocs-material[imaging]
pip install mkdocs-material-extensions
pip install pillow cairosvg
pip install mkdocstrings[python]
mkdocs serve
```

# To navigate the tutorials:
Please follow the instructions in
- *docs/index.rst*

## Part I: Marea :
Tutorial to run this step:
- *docs/marea.rst*

## Part II: WNTransform:

Tutorial to run this step:
- *docs/wordnetreplacement.rst*

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

## Part III: Embedding:
Tutorial to run this step:
- */docs/word2vec.rst*

## Part IV: Testing :
Tutorial to run this step:
- */docs/conceptset_evaluation.rst*
