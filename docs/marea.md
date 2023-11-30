# Running marea

<a href="https://github.com/TheJacksonLaboratory/marea/tree/v1.0.2" target="_blank">MAREA</a> (marea adamantly resists egregious acronyms) is a tool for processing PubMed abstracts. See <a href="https://pubmed.ncbi.nlm.nih.gov/34888523/" target="_blank">Ravanmehr et al</a> for additional information.

The README of marea presents details on how to run the scripts. For the current project, we downloaded abstracts from NCBI's FTP site, which makes available gzipped .xml files containing titles, abstracts, and metadata for all PubMed articles. We used the `xml2txt.py` script to extract the required fields from the abstracts. We then chose abstracts published between 2010 and 2020.

## PubTator

Biomedical concept replacement was performed using resources from the <a href="https://www.ncbi.nlm.nih.gov/research/pubtator/" target="_blank">PubTator Central</a> project. The `pubtate.py` script from the marea project was used to process the above files.
