import os, glob
import argparse
import csv
import pandas as pd 

class FilterAbstracts:
    """
    A class to represent a transofrmation of Pubmed Abstracts by reducing vocabulary size through replacing words with their synonyms from Wordnet.

    ...

    Attributes
    ----------
    marea_file: str
                path to .tsv file with abstracts from marea output
    output_file: str
                path to .tsv file that will contain the output after abstracts are transformed

    Methods
    -------
    get_word_to_synonyms_d(unique_words_list) -> Dict:
        Creates a dictionary from the whole data set, keys are unique words, and the values are synonyms of keys from synset
    """

    def __init__(self, path_to_pubmed_cr, output_file, threshold_year) -> None:
            """
            Constructs all the necessary attributes for the  WordNetTransformer class
            
            Parameters
            ----------
            marea_file: str
                        path to .tsv file with abstracts from marea output
            output_file: str
                        path to .tsv file that will contain the output after abstracts are transformed
            """
            if not os.path.exists(path_to_pubmed_cr):
                raise FileNotFoundError("Could not find marea file")
            if not os.path.exists(output_file):
                raise FileNotFoundError("Could not find output file")

            self._marea_file = path_to_pubmed_cr
            self._output_file = output_file
            self._threshold_year = threshold_year


            f = open(path_to_pubmed_cr, "r")
            y = open(output_file, 'w')
            for line in f:
                if self.check_abstract_above_threshold(line,self._threshold_year):
                    y.writelines(line)
            y.close()
            f.close()


    def check_abstract_above_threshold (self,line_abstract, _threshold_year):
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

python newFilter.py 'path_to_pubmed_txt' 'path_to_pubmed_cr' 'threshold' 

ex:  python newFilter.py /Users/niyone/Desktop/wn2vc_marea/test_filter/test_pubmed_txt /Users/niyone/Desktop/wn2vc_marea/test_filter/test_pubmed_cr/100000_test_marea.tsv 2000


"""
