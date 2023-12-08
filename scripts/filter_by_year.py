import os, glob
import argparse
import pandas as pd


class FilterAbstracts:
    """
    Filter Marea Output by Year

    The class is designed to filter the output of Marea by a threshold year. It initializes with paths to the
    input and output files and a threshold year and processes the input file, writing the lines that meet
    the threshold to the output file.

    :param path_to_pubmed_cr: Path to .tsv file with abstracts from Marea output.
    :type path_to_pubmed_cr: str
    :param path_to_output_file: Path to .tsv file that will contain the output after abstracts are filtered.
    :type path_to_output_file: str
    :param threshold_year: A year to be used to filter all the abstracts published below that year.
    :type threshold_year: int

    Methods
    -------
    def check_abstract_above_threshold (line_abstract, _threshold_year):
        check if the abstract of the article was published after the threshold yearwords, and the values are synonyms of keys from synset
    """

    def __init__(self, path_to_pubmed_cr, path_to_output_file, threshold_year) -> None:
        """

        Initializes the FilterAbstracts object and processes the input file immediately to filter out abstracts
        published below the specified threshold year.

        :param path_to_pubmed_cr: Path to the .tsv file containing abstracts from Marea output.
        :type path_to_pubmed_cr: str
        :param path_to_output_file: Path to the .tsv file where the filtered abstracts will be written.
        :type path_to_output_file: str
        :param threshold_year: Abstracts published below this year will be filtered out.
        :type threshold_year: int

        :raises FileNotFoundError: if either path_to_pubmed_cr or path_to_output_file do not exist.
        """

        if not os.path.exists(path_to_pubmed_cr):
            raise FileNotFoundError("Could not find marea file")

        self._marea_file = path_to_pubmed_cr
        self._output_file = path_to_output_file
        self._threshold_year = threshold_year

        f = open(path_to_pubmed_cr, "r")
        y = open(path_to_output_file, "w")
        for line in f:
            if self.check_abstract_above_threshold(line, self._threshold_year):
                y.writelines(line)
        y.close()
        f.close()

    def check_abstract_above_threshold(self, line_abstract, _threshold_year):
        """
        Check if the abstract of the article was published after the threshold year.

        :param line_abstract: a tsv row from the whole dataset with 3 columns (pubmedID, publication year, abstract)
        :type line_abstract: str
        :param _threshold_year: a year to be used for selecting all abstracts published above that year
        :type _threshold_year: int

        :returns: above_threshold_year: whether the article was published after the threshold year
        :rtype: bool

        :raises ValueError: if the line_abstract does not have exactly 3 columns
        """
        above_threshold_year = False
        columns = line_abstract.split("\t")
        if len(columns) != 3:
            raise ValueError(f"Malformed marea line: {line_abstract}")
        if columns[1] > str(_threshold_year):
            above_threshold_year = True
        return above_threshold_year


if __name__ == "__main__":
    # running code using command line
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", type=str, help="address of marea_file", required=True)  # name of pubmed_cr file
    parser.add_argument("-o", type=str, help="address of output_file", required=True)  # address of output file
    parser.add_argument("-y", type=int, help="threshold year of filter", required=True)  # year threshold
    args = parser.parse_args()


FilterAbstracts(args.i, args.o, args.y)

"""

Sample way of running the code:

python filter_by_year.py 'path_to_pubmed_cr' 'path_to_output_file' 'threshold_year'

ex:  python  /scripts/filter_by_year.py  -i ../data/pubmed_cr.tsv  -o ../data/pubmed_filt.tsv  -y 2015

"""
