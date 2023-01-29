.. _w2v:

========
Word2Vec
========

* Now we have two files to campare. We have the marea output  which was filtered by year (pubmed_filt.tsv) and word net transformed text (pubmed_wn.tsv).
* This step has to be run twice, first for pubmed_filt.tsv and second for wordnet.tsv before going to the following step 
* Word2vec converts the texts from abstracts to build word embedding using Skip-gram and negative sampling. 
* We used a continuous skip-gram model, where we were predicting words within a certain range before and after the current word in the same sentence.
* The model is trained on skip-grams, which are n-grams that allow tokens to be skipped.
* The context of a word can be represented through a set of skip-gram pairs of (target_word, context_word) where context_word appears in the neighboring context of target_word.
* The training objective of the skip-gram model is to maximize the probability of predicting context words given the target word.

    * /run_word2vec.py takes three command line options:
        * -i : address of a .tsv file with abstracts (either pubmed_filt.tsv or pubmed_cr.tsv) 
        * -v : name of vector file output
        * -m : name of metadata file
        * -w : size of embedding window 
        * --embedding_dim: the desired dimension of vectors
        * --vocab_size: the size of vocabulary to be produced  
    * To run the script:
        * locate the file you are running + python + run_word2vec.py +vector_file name + metadata_file name
        * Example: python run_word2vec.py -i ../data/pubmed_filt.tsv -v filt_vector_file -m filt_metatada_file 
            * To run the script on the HPC, you can run the singularity file  singularity/run_word2vec.py as “sbatch -q batch run_word2vec.py”
The output files: vector file: has the list of vectors equals to the number of vocab size and the meta data, the vector file has 100 diminsions of each vocabulary while meta data file has a list of vocabularies. 
One this step is related twice for both the filtered abstracts and the corresponding word net transformed file, we have 2 metadata files, and 2 vector files which Will be used in the evaluation
