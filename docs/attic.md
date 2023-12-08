# ATTIC

Move these texts somewhere else


Before running the two files in word2vec, ensure that they have the same format. Run the following bash script through the terminal to remove the PubMed identifier and publication year columns, leaving only the abstract from  `pubmed_filt.tsv`:

For Unix-like shell (like Mac) use:
    ```shell
    awk -F'\t' '{print $3}' pubmed_filt.tsv > pubmed_filt_abst.tsv
    ```
For Windows use:
    ```shell
    Get-Content pubmed_filt.tsv | ForEach-Object { ($_ -split "`t")[2] } | Set-Content pubmed_filt_abst.tsv
    ```
