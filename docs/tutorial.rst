.. _tutorial:

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
the next step is to perform the wordnet non-biomedical concept replacement (for details see :ref:`wnreplacement`). Run the following script (which is in
the ``scripts`` directory -- note that the example does not show full paths).


.. code-block:: shell
   
   python3  python run_wn_replacement.py -i pubmed_cr.tsv -o pubmed_cr_wn.tsv [--threshold <float>]

the `-i` argument points to the input file. The ``-o`` argument creates a new output file with the result. The ``--threshold`` is a floating number that controls
the minimum (threshold) count of a synonym to be replaced. First, the mean word count of all words (tokens) in the entire corpus is determined. For eaxample, the mean could be 
$\mu = 400$, meaning that the average word occurs 400 times in the entire corpus of texts. For instance, if  the threshold is set to $\tau = 2.0$, then, the minimum count for being replaced 
would be $\tau\cdot \mu = 800$.


The output file has the same overall format as the input file, except that some words are replaced by more common synonyms.

.. admonition:: input text (excerpt)
   :class: tip

   33500803	2020	colloid cyst curtail case report spontaneous colloid cyst regression (...) discover colloid cyst image perform transient meshd009461 ct mri brain reveal 5mm lesion 
   


.. admonition:: Wordnet-replaced text (excerpt)
   :class: tip

   33500803	2020	colloid cyst restrict case report spontaneous colloid cyst regression (...) discover colloid cyst image perform transient meshd009461 ct mri brain reveal 5mm lesion
   
   
Thus, the relatively rare word ``curtail`` was replaced by the more common synonym ``restrict``.


word2vec
^^^^^^^^

The next step is to run word2vec on the replaced input file. If desired, word2vec can be run on both files for comparison purposes; the steps are analogous.







