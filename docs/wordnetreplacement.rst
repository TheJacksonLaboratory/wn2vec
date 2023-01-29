.. _wnreplacement:

=================================
WordNet-based synonym Replacement
=================================


After getting the pre-processed data where biomedical concepts has been replaced as the results of Marea (pubmed_cr). 

* The pubmed_cr.tsv file will have 3 columns, Pubmed ID, Publication Year, and abstract.
* First step: Filtering by year
    * Use the script scripts/filter_by_year.py to filter the whole data set with a certain year you would want to use. For example if you want all published pubmed aricle’s abstracts from 2010  up to the latest, you will use 2010 as a threshold year.
    * /filter_by_year.py takes three command line options:
        * -i : address of a .tsv marea_file output (pubmed_cr.tsv)
        * -o : address to .tsv output file where the output will go (pubmed_filt)
        * -y : threshold year, all pubmed published above the year will be saved in output file 
    * To run the code: 
        * locate the file you are running + python + filter_by_year.py + address of marea_file + address of output_file + threshold year of filter
        * example:  python  /scripts/filter_by_year.py  -i   ../data/pubmed_cr  -o ../data/pubmed_filt.tsv  -y 2010
        * To run the script on the HPC, you can run the singularity file  singularity/filter_by_year.sh as “sbatch -q batch filter_by_year.sh”
* Second step: WN Replacement 
    * This step  we replace non-medical concepts with their synonyms using wordnet library from nltk . This means that words with the same synonyms are replaced by one synonym id. For example: good, well, better, best, effective , can be replaced with one single word  like “good”
    * The words are sorted by their frequency of occurrence in the whole file, and all the words whose frequency is less than the threshold, are subjected to be replaced with their synonym word. The threshold is the mean of the frequency of occurrence of all vocabularies in he text.
    * /run_wn_replacement.py takes two command line options:
        * -i : address of a .tsv filtered marea_file output (pubmed_filt.tsv)
        * -o : address to .tsv output file where the output will go (pubmed_wn.tsv)

    * To run the script:
        * locate the file you are running + python + run_wn_replacement.py + address of filtered marea_file + address of output_file
        * example:  python ../scripts/run_wn_replacement.py -i ../data/pubmed_filt/100pubmed_filt.tsv -o ../data/pubmed_wn/100pubmed_wn.tsv
            * To run the script on the HPC, you can run the singularity file  singularity/wntransformer.sh as “sbatch -q batch wntransformer.sh”
    * The output of this step is a .tsv file with 3 columns: pubmed id, publication year, abstract. The wn transformed file has the same number of abstracts as filtered marea output. 



