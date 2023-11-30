# Word2Vec
Now we have two files to compare. We have the marea output which was filtered by year (`pubmed_filt.tsv`) and WordNet-transformed text (`pubmed_wn.tsv`).

## Transforming input text

To ensure that we have fair results after embedding, the input text should be in the same formart. Currently `pubmed_wn.tsv` have only one column which is abstracts, we are going to remove extra columns from  `pubmed_filt.tsv` to have same formart. 

Run the following comand in your terminal

For Unix-like shell (like Mac) use: 
    ```shell
    awk -F'\t' '{print $3}' pubmed_filt.tsv > pubmed_filt_abst.tsv
    ```
For Windows use:
    ```shell
    Get-Content pubmed_filt.tsv | ForEach-Object { ($_ -split "`t")[2] } | Set-Content pubmed_filt_abst.tsv
    ```

## Word2Vec Embedding 

- This step has to be run twice, first for `pubmed_filt_abst.tsv` and second for `pubmed_wn.tsv` before going to the following step.

- Word2vec converts the texts from abstracts to build word embedding using Skip-gram and negative sampling using <a href="https://radimrehurek.com/gensim/models/word2vec.html" target="_blank">Gensim Word2vec model</a>.


- We used a continuous skip-gram model, where we were predicting words within a certain range before and after the current word in the same sentence.

- The model is trained on skip-grams, which are n-grams that allow tokens to be skipped.

- The context of a word can be represented through a set of skip-gram pairs of (target_word, context_word) where context_word appears in the neighboring context of target_word.

- The training objective of the skip-gram model is to maximize the probability of predicting context words given the target word.

## Running the Word2Vec Script

`run_word2vec.py` takes three command-line options:

- `-i`: Path to a .tsv file with abstracts (either `pubmed_filt_abst.tsv` or `pubmed_cr.tsv`).

- `-v`: Name of output vector file (ex. `wn_vector`).

- `-m`: Name of output metadata file (ex. `wn_metadata`).

Remember to run this code twice with separate paths for the input and different names for vectors and metadata if you want to compare two separate files. 

**Note**: all custom vector names should end with `_vector` and metadata should end `_metadata`.

To run the code:

1. On local laptop:
    - Locate the file you are running, then use Python to execute `run_word2vec.py` with the appropriate arguments.
    - Example: `python run_word2vec.py -i pubmed_wn.tsv -v wn_vector -m wn_metadata`

2. On High Performance Computing (HPC):
    - Run the  singularity file `singularity/word2vector.sh` as `sbatch -q batch word2vector.sh`.

The output files consist of:

- A vector file: contains a list of vectors equal to the number of vocab size and the metadata. The vector file has 128 dimensions for each vocabulary.
- A metadata file: contains a list of vocabularies.

Once this step is repeated twice for both the filtered abstracts and the corresponding WordNet transformed file, we have 2 metadata files and 2 vector files which will be used in the evaluation.
