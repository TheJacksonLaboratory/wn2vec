# wn2vec
Wordnet 2 vector



## Concept sets
The wn2vec scripts require a list of concept sets in order to assess the quality of concept embeddings. The source of gene sets for wn2vec
are selected genesets from MSigDB. The source of clinical concept sets were selected concepts from MeSH. Additionally, we used X 'analogy' sets
TODO describe how we generated these sets.

The format of the wn2vec conceptset file is
```
HAY_BONE_MARROW_NEUTROPHIL	M39203	ncbigene55365;ncbigene23129;ncbigene8935;ncbigene3920;ncbigene221; (...)
```
i.e., name, id, and semicolon-separated list of concept identifiers. For instance, ncbigene55365 refers to TMEM176A (transmembrane protein 176A; Homo sapiens) which
has NCBI Gene ID: 55365.

## Concept replacement

Todo -- summary of concept replacement/marea/source of PubMed data

## Word2vec

Todo -- summary of word2vec and parameters


## Miscellaneous


I have added some skeleton Python code to get us started.

This part of the project serves one purpose -- to substitute texts with one ID per synonym set to reduce the overall number of
vectors that result from Word2vec. Other parts of the project will be developed later on to see if this approach improves
the overall utility of word2vec embedding.

We will create a simple python package to ease testing and use in notebooks or scripts, called ``wn2vec``.


To run this code, we need the NLTK library. To set this up, I recommend the following

```
python3 -m venv mykernel
source mykernel/bin/activate
pip install nltk
```

We can develop the functionality of the code in a notebook by adding the following

```
source mykernel/bin/activate # only needed once per session
pip install jupyter
ipython kernel install --name "mykernel" --user
```

Start with ``jupyter-lab`` or ``jupyter notebook`` and choose ``mykernel``. See the notebook at ``notebook/nltkdemo.ipynb`` for how to use the python package we are creating, ``wn2vec``.


Testing
#######

Use the following to run all tests
```
nosetests tests/
```
.
