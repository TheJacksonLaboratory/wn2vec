from typing import List
import os


class Tf2FileParser:
    """
    Responsible for managing and validating the existence of PubTator and WordNet files within a specified directory.
    
    :param indir: Directory containing the expected files.
    :type indir: str
    :param pubtator_prefix: Prefix identifying PubTator files within the directory.
    :type pubtator_prefix: str
    :param wordnet_prefix: Prefix identifying WordNet files within the directory.
    :type wordnet_prefix: str
    """

    def __init__(self, indir, pubtator_prefix, wordnet_prefix):
        """
        Initializes the Tf2FileParser object and validates the existence of specific files within the given directory.
        
        """
        
        if not os.path.isdir(indir):
            raise FileNotFoundError(f"Could not find input directory {indir}")
        self._pubtator_vector_file = os.path.join(indir, f"{pubtator_prefix}_vector.tsv")
        if not os.path.isfile(self._pubtator_vector_file):
            raise FileNotFoundError(f"Could not find pubtator vector file {self._pubtator_vector_file}")
        self._pubtator_meta_file = os.path.join(indir, f"{pubtator_prefix}_metadata.tsv")
        if not os.path.isfile(self._pubtator_meta_file):
            raise FileNotFoundError(f"Could not find pubtator metadata file {self._pubtator_meta_file}")
        self._wordnet_vector_file = os.path.join(indir, f"{wordnet_prefix}_vector.tsv")
        if not os.path.isfile(self._wordnet_vector_file):
            raise FileNotFoundError(f"Could not find wordnet vector file {self._wordnet_vector_file}")
        self._wordnet_meta_file = os.path.join(indir, f"{wordnet_prefix}_metadata.tsv")
        if not os.path.isfile(self._wordnet_meta_file):
            raise FileNotFoundError(f"Could not find wordnet metadata file {self._wordnet_meta_file}")

    @property
    def pubtator_vector(self):
        """
        :return: Path to the PubTator vector file.
        :rtype: str
        """
        return self._pubtator_vector_file

    @property
    def pubtator_metadata(self):
        """
        :return: Path to the PubTator metadata file.
        :rtype: str
        """
        return self._pubtator_meta_file

    @property
    def wordnet_vector(self):
        """
        :return: Path to the WordNet vector file.
        :rtype: str
        """
        return self._wordnet_vector_file

    @property
    def wordnet_metadata(self):
        """
        :return: Path to the WordNet metadata file.
        :rtype: str
        """
        return self._wordnet_meta_file

    def get_files(self):
        """
        Retrieves the paths to all managed files.
        
        :return: Tuple containing paths to the PubTator vector file, PubTator metadata file, WordNet vector file, and WordNet metadata file, in that order.
        :rtype: Tuple[str, str, str, str]
        """
        return self._pubtator_vector_file, self._pubtator_meta_file, self._wordnet_vector_file, self._wordnet_meta_file
