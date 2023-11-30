# WordNet replacement 

## WordNet-based synonym Replacement

After getting the pre-processed data where biomedical concepts have been replaced as the results of Marea (pubmed_cr), the following steps are taken:

#### Input Data

The `pubmed_cr.tsv` file will have 3 columns: PubMed ID, Publication Year, and abstract.

### First Step: Filtering by Year

Use the script `scripts/filter_by_year.py` to filter the whole dataset with a certain year you want to use. For example, if you want all published PubMed article’s abstracts from 2010 up to the latest, you will use 2010 as a threshold year.

`filter_by_year.py` takes three command-line options:

- `-i`: Path of a .tsv Marea file output (`pubmed_cr.tsv`)

- `-o`: Path to .tsv output file where the output will go (`pubmed_filt`)

- `-y`: Threshold year, all PubMed published above the year will be saved in the output file


To run the code:

1. On local laptop:
    - Locate the file you are running, then use Python to execute `filter_by_year.py` with the appropriate arguments.
    - Example: `python /filter_by_year.py -i ../pubmed_cr.tsv -o ../pubmed_filt.tsv -y 2010`

2. On High Performance Computing (HPC):
    - Run the singularity file `singularity/filter_by_year.sh` as `sbatch -q batch filter_by_year.sh`.

### Second Step: WN Replacement

In this step, we replace non-medical concepts with their synonyms using the WordNet library from NLTK. This means that words with the same synonyms are replaced by one synonym ID.  For example, *good,* *well,* *better,* *best,* *effective* can be replaced with a single word like *good.*


The words are sorted by their frequency of occurrence in the whole file, and all the words whose frequency is less than the threshold, are subjected to be replaced with their synonym word. The threshold is the mean of the frequency of occurrence of all vocabularies in the text.

`run_wn_replacement.py` takes two command-line options:

- `-i`: Path of a .tsv filtered Marea file output (`pubmed_filt.tsv`)

- `-o`: Path to .tsv output file where the output will go (`pubmed_wn.tsv`)

- `--threshold`: This is a floating number that controls the minimum (threshold) count of a synonym to be replaced (default `--threshold 1`).  

To run the code:

1. On local laptop:
    - Locate the file you are running, then use Python to execute `run_wn_replacement.py` with the appropriate arguments.
    - Example: `python3 run_wn_replacement.py -i pubmed_filt.tsv -o pubmed_cr.tsv [--threshold <float>]`
2. On High Performance Computing (HPC):
    - Run the  singularity file `singularity/wntransformer.sh` as `sbatch -q batch wntransformer.sh`.


The output of this step is a .tsv file with 1 column which is the abstract of each article. The WN transformed file has the same number of abstracts as the filtered Marea output.
