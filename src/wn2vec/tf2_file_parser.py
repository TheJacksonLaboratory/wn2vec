from typing import List
import os


class Tf2FileParser:
    
    def __init__(self, indir, pubtator_prefix, wordnet_prefix):
        if not os.path.isdir(indir):
            raise FileNotFoundError(f"Could not find input directory {indir}")
        self._pubtator_vector_file = os.path.join(indir, f"{pubtator_prefix}_vector.tsv")
        if not os.path.isfile(self._pubtator_vector_file):
            raise FileNotFoundError(f"Could not find pubtator vector file {self._pubtator_vector_file}")
        self._pubtator_meta_file = os.path.join(indir, f"{pubtator_prefix}_metadata.tsv")
        if not os.path.isfile(self._pubtator_meta_file):
            raise FileNotFoundError(f"Could not find pubtator metadata file {self._pubtator_meta_file}")
        self._wordnet_vector_file = os.path.join(indir, f"{wordnet_prefix}_vector.tsv")
        if not os.path.isfile(self._pubtator_vector_file):
            raise FileNotFoundError(f"Could not find wordnet vector file {self._wordnet_vector_file}")
        self._wordnet_meta_file = os.path.join(indir, f"{wordnet_prefix}_metadata.tsv")
        if not os.path.isfile(self._pubtator_meta_file):
            raise FileNotFoundError(f"Could not find wordnet metadata file {self._wordnet_meta_file}")
        
    @property
    def pubtator_vector(self):
        return self._pubtator_vector_file
    
    @property
    def pubtator_metadata(self):
        return self._pubtator_meta_file
    
    @property
    def wordnet_vector(self):
        return self._wordnet_vector_file
    
    @property
    def wordnet_metadata(self):
        return self._wordnet_meta_file
    
    def get_files(self):
        """return all four files needed for the comparison

        Returns:
            [str]: pubtator_vector_file,  pubtator_meta_file, wordnet_vector_file, wordnet_meta_file 
        """
        return self._pubtator_vector_file,  self._pubtator_meta_file, self._wordnet_vector_file, self._wordnet_meta_file 