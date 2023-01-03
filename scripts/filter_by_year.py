import os, glob
import argparse
import pandas as pd 

class FilterAbstracts:
    """
    A class that filter marea output by year
    ...

    Attributes
    ----------
    path_to_pubmed_cr: str
                        path to .tsv file with abstracts from marea output
    path_to_output_file: str
                        path to .tsv file that will contain the output after abstracts are filtered
    threshold_year: int 
                        a year to be used to filter all the abstracts published below that year

    Methods
    -------
    def check_abstract_above_threshold (line_abstract, _threshold_year):
        check if the abstract of the article was published after the threshold yearwords, and the values are synonyms of keys from synset
    """

    def __init__(self, path_to_pubmed_cr, path_to_output_file, threshold_year) -> None:
            """
            Constructs all the necessary attributes for the  WordNetTransformer class
            
            Parameters
            ----------
            path_to_pubmed_cr: str
                        path to .tsv file with abstracts from marea output
            path_to_output_file: str
                        path to .tsv file that will contain the output after abstracts are filtered
            threshold_year: int 
                        a year to be used to filter all the abstracts published below that year

            """
            if not os.path.exists(path_to_pubmed_cr):
                raise FileNotFoundError("Could not find marea file")
            if not os.path.exists(path_to_output_file):
                raise FileNotFoundError("Could not find output file")

            self._marea_file = path_to_pubmed_cr
            self._output_file = path_to_output_file
            self._threshold_year = threshold_year


            f = open(path_to_pubmed_cr, "r")
            y = open(path_to_output_file, 'w')
            for line in f:
                if self.check_abstract_above_threshold(line,self._threshold_year):
                    y.writelines(line)
            y.close()
            f.close()


    def check_abstract_above_threshold (self,line_abstract, _threshold_year):
        """
        check if the abstract of the article was published after the threshold year
        @ parameter: line_abstract: string
            a tsv row from the whole dataset with 3 columns (pubmedID, publication year, abstract)
        @ parameter: _threshold_year: int
            a year to be used for selecting all abstracts published above that year

        @ return: above_threshold_year: Boolean
            returns true if the article was published above that year, false otherwise
        """
        above_threshold_year = False
        columns = line_abstract.split('\t')
        if len(columns) != 3:
            raise ValueError(f'Malformed marea line: {line_abstract}')
        if columns[1] > str(_threshold_year):
            above_threshold_year = True
        return above_threshold_year




if __name__ == "__main__":

#running code using command line
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('pubmed_cr', type=str) #name of pubmed_cr file
    parser.add_argument('output', type=str) #address of output file
    parser.add_argument('threshold', type=int) #year threshold
    args = parser.parse_args()


FilterAbstracts(args.pubmed_cr, args.output,  args.threshold)

"""

Sample way of running the code:

python filter_by_year.py 'path_to_pubmed_cr' 'path_to_output_file' 'threshold_year' 

ex:  python filter_by_year.py /Users/niyone/Documents/GitHub/wn2vec/data/wntransform_sample/100Pubmed_cr_3.tsv /Users/niyone/Documents/GitHub/wn2vec/scripts/pubmed_filter.tsv 1974

"""