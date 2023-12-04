# Concept Sets

New users of this software can create concept sets for testing in any way that is appropriate to their use case.
Here, we describe how we generated concepts sets in case it is useful for others. 

## Medical Subject Headings (MeSH)

We manually reviewed MeSH entries using the <a href="https://meshb.nlm.nih.gov/" target="_blank">MeSH Browser</a> and chose identifiers of entries that describe a group of related medical concepts. We selected 105 concepts in this way, and the following table shows the first four of them (the entire list can be found in the file <a href="https://github.com/TheJacksonLaboratory/wn2vec/blob/main/data/mesh_target_ids.tsv" target="_blank">mesh_target_ids.tsv</a>).


| mesh.id  | label                |
|----------|----------------------|
| D001145  | Arrhythmias, Cardiac |
| D007674  | Kidney Diseases      |
| D009202  | Cardiomyopathies     |
| D001523  | Mental Disorders     |

The Python script `meshImporter.py` was used to retrieve all of the descendant terms of each of these identifiers.
For instance, Arrhythmias, Cardiac has 40 descendant terms including Adams-Stokes Syndrome (D000219) and
Arrhythmia, Sinus (D001146). The `meshImporter.py` script retrieves these terms and writes them in a file with the following structure

| Arrhythmias, Cardiac | D001145 | meshd016170;meshd000219; (...)             |
|----------------------|---------|--------------------------------------------|
| Kidney Diseases      | D007674 | meshd016263;meshd000141;meshd058186; (...) |
| Cardiomyopathies     | D009202 | meshd000092183;meshd019571; (...)          |
| Mental Disorders     | D001523 | meshd015526;meshd000275; (...)             |

For convenience, the output of this script is stored in the file <a href="https://github.com/TheJacksonLaboratory/wn2vec/blob/main/data/mesh_sets.tsv" target="_blank">mesh_sets.tsv</a> and does not need to be recreated to run the other scripts.
