# Running marea

[MAREA](https://github.com/TheJacksonLaboratory/marea){:target="_blank"} (marea adamantly resists egregious acronyms) is a tool for processing PubMed abstracts. [Ravanmehr et al](https://pubmed.ncbi.nlm.nih.gov/34888523){:target="_blank"} for additional information.

The README of marea presents details on how to run the scripts. For the current project, we downloaded abstracts from NCBI's FTP site, which makes available gzipped .xml files containing titles, abstracts, and metadata for all PubMed articles. We used the `xml2txt.py` script to extract the required fields from the abstracts. We then chose abstracts published between 2010 and 2020.

### Using Your Own Data and Concept Replacement Tool.

For our experiments, we used [PubTator](https://pubmed.ncbi.nlm.nih.gov/31114887/) to perform concept replacement, and the above file has already been processed with PubTator. You can use any analogous file and perform concept replacement by any method. Ensure the output is formatted in three tab-separated columns with column 1 being the PubMed identifier, column 2 being the year of publication, and column 3 being the abstract text with concept replacements. The following table shows an example.

| Column 1 |Column 2 |Column 3 |
|:---------|:--------|:--------|
| 35509584	| 2022	 | endoscope control extend ... meshd009369 frontal convexity technical note ....
| 35444774	| 2022	| meshd008223 ncbigene4609 ncbigene4609 ncbigene596 ncbigene596 ncbigene604 ncbigene604 rearrangement review diagnosis treatment modern era classification meshd009369 depends immunomorphological |
| 34433723 | 2021	|  unusual meshd006471 mimic rupture solitary gastric varix due meshd046152 exogenous growth meshd046152 lead meshd006471 usual |


## PubTator

Biomedical concept replacement was performed using resources from the <a href="https://www.ncbi.nlm.nih.gov/research/pubtator/" target="_blank">PubTator Central</a> project. The `pubtate.py` script from the marea project was used to process the above files.


