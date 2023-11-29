## tutorial

========
Tutorial
========

Here, we demonstrate all the steps required to run the wn2vec pipeline on a small input dataset consisting of
100000 abstracts from pubmed. The pipeline can be run similarly with all PubMed abstracts or any other input source.

Preparing the data
^^^^^^^^^^^^^^^^^^

The input data for this tutorial consists of a 100,000 file with 100,000 abstracts from PubMed that have been already
processed using the marea pipeline for medical concept replacement. See :ref:`rst_marea` for details on how to 
run marea.

The file can be downloaded from zenodo: `https://zenodo.org/record/7588919/files/pubmed_cr.tsv <https://zenodo.org/record/7588919/files/pubmed_cr.tsv?download=1>`_.


.. csv-table:: Input file (PubMed Abstracts following Pubtator Concept Replacement)
   :file: _files/sample_pubmed.csv
   :header-rows: 1
   :widths: 20, 20, 260



Using your own data 
^^^^^^^^^^^^^^^^^^^

For our experiments, we used `PubTator <https://pubmed.ncbi.nlm.nih.gov/31114887/>`_ to perform concept replacement, and the above file already 
has been processed with PubTator. You can use any analogous file and perform concept replacement by any method. To use the scripts in this tutorial,
make sure the output is formated in three tab-separated columns with column 1 being the PubMed identifier, column 2 being the year of publication, and column 3 being the 
abstract text with concept replacements. 

Setting up the environment
^^^^^^^^^^^^^^^^^^^^^^^^^^

There are several ways to run the code but the simplest is to set up a virtual environment. For this example, we call the environment ``wn2v_env`` but you can use any name you like.

.. code-block:: shell

   python3 -m venv wn2v_env
   source wn2v_env/bin/activate
   pip install .



wordnet replacement
^^^^^^^^^^^^^^^^^^^

After you have downloaded the pubmed_cr.tsv file (or prepared your own input file to have the same format),
the next step is to perform the wordnet non-biomedical concept replacement (for details see :ref:`wordnetreplacement`). Run the following script (which is in
the ``scripts`` directory -- note that the example does not show full paths).


.. code-block:: shell
   
   python3  python run_wn_replacement.py -i pubmed_cr.tsv -o pubmed_cr_wn.tsv [--threshold <float>]

the `-i` argument points to the input file. The ``-o`` argument creates a new output file with the result. The ``--threshold`` is a floating number that controls
the minimum (threshold) count of a synonym to be replaced. First, the mean word count of all words (tokens) in the entire corpus is determined. For eaxample, the mean could be 
$\mu = 400$, meaning that the average word occurs 400 times in the entire corpus of texts. For instance, if  the threshold is set to $\tau = 2.0$, then, the minimum count for being replaced 
would be $\tau\cdot \mu = 800$.

The output file has the same number of abstracts as the input file, except that some words are replaced by more common synonyms, and the formart changed to be just one column which is the abstracts only. 



.. admonition:: input text (excerpt)
   :class: tip

   33500803	2020	colloid cyst curtail case report spontaneous colloid cyst regression (...) discover colloid cyst image perform transient meshd009461 ct mri brain reveal 5mm lesion 
   


.. admonition:: Wordnet-replaced text (excerpt)
   :class: tip

   colloid cyst restrict case report spontaneous colloid cyst regression (...) discover colloid cyst image perform transient meshd009461 ct mri brain reveal 5mm lesion
   
   
Thus, the relatively rare word ``curtail`` was replaced by the more common synonym ``restrict``.


word2vec
^^^^^^^^

The next step is to run word2vec on the replaced input file. If desired, word2vec can be run on both files for comparison purposes; the steps are analogous.

Note, before running the two files in word2vec, ensure that they have the same formart. 
Run through the terminal the following bash script to remove column 1 being the PubMed identifier, column 2 being the year of publication and stay with the abstract on pubmed_cr.tsv 

.. code-block:: shell
   awk -F'\t' '{print $3}' pubmed_cr.tsv > pubmed_cr_filt.tsv

Now you are going to run each file with abstracts through word2vec. If you want to compare both files to test the impact of wordnet-based synonym replacement, 
then you will have to run the following code twice. 


.. code-block:: shell

   python3  python run_word2vec.py -i pubmed_cr_filt.tsv ['input file'] -v pm_vector ['vectors name']-m pm_metadata ['metadata name']
   python3  python run_word2vec.py -i pubmed_cr_filt.tsv  -v wn_vector -m wn_metadata 


Remember to run this code twice with separate paths of the input and differnt names of vectors and metadata if you want to compare two separate files.
Note: all the custom vector names should end with '_vector' and metadata should end '_metadata'.


Compare embedding
^^^^^^^^^^^^^^^^^

This step comes after you have 2 vector files and 2 metadata files for two separate corups generated form the step above.
This step is to evaluate the impact of wordnet-based synonym replacement on the corup. 
The test will be done on different biomedical sets as detailed in :ref:`conceptset_evaluation`


.. code-block:: shell

   python  compare_embeddings.py -i metadata_vectors/ ['path to embedding output directory'] -c data/bio_geneset.tsv ['path to concept set'] -p filt  -w wn -o dump/comn_concepts.tsv


Repeat this step for multiple concept sets to check how different concepts' embeddings behave. 

Sample of the results you will be in this formart: 
.. admonition:: Results interpretation 
   :class: tip

   WN: refers to wornet replaced corpus
   PM: refers to marea output (none of concepts were replaced using wordnet)

   WN relevant concepts 1302 and PM relevant concepts 1302 : means there were 1302 genes both in corpus and biocarta_canonical_gene_set (concept set)
   WN sig 22 and PM sig 3: means 22 (WN) concept sets using cluster mean distance comparision were significantly less than PM, and 3 other wise. 
   WN LESS  165 and PM LESS 117 (irregardless of pvalue): There were 165 concept sets whose cluster mean distance were less in WN compared to PM, and 117 otherwise.
   WN sig PairTest 106249 and PM sig PairTest 90127
   WN LESS PairTest 130706 and PM LESS PairTest 113559 (irregardless of pvalue)

