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

To use the wn2vec pipeline, you may need to use a script to reformat your input data to have an analogous format.

wordnet replacement
^^^^^^^^^^^^^^^^^^^

After you have downloaded the pubmed_cr.tsv file (or prepared your own input file to have the same format),
the next step is to perform the wondnet non-biomedical concept replacement.


TODO describe