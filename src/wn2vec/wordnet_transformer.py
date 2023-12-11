import os
import sys
from collections import defaultdict
import nltk
from nltk.corpus import wordnet as wn
from typing import List, Dict
import numpy as np
from tqdm import tqdm


class WordNetTransformer:
    """
    A class designed for transforming abstracts from PubMed by reducing vocabulary size through synonym replacement using WordNet.

    ...

    Attributes
    ----------
    :param marea_file: Path to the .tsv file containing abstracts from marea output.
    :type marea_file: str
    :param output_file: Path to the .tsv file where the transformed abstracts will be written.
    :type output_file: str


    Methods
    -------
    get_word_to_synonyms_d(unique_words_list) -> Dict:
        Creates a dictionary from the whole data set, keys are unique words, and the values are synonyms of keys from synset

    get_highest_occuring_synonym(synonym_list) -> str:
        gets the highest occuring word in the synonym list of the whole dataset (all the bastracts being transformed)

    get_synonym_list(self, word: str) -> List:
        takes a word and returns a list of a word's synonyms using wordnet

    transform(line_abstract: str, _word_to_synonym_d) -> str:
        Replaces the variable in dataset with their synonyms from the dictionary

    calculate_mean_word_count(counter_d) -> int:
        calculates the mean of the frequencies of all the vocabilaries in the datasets

    """

    def __init__(self, marea_file, threshold_multiple=1) -> None:
        """
        Constructs all the necessary attributes for the  WordNetTransformer class

        """
        if not os.path.exists(marea_file):
            raise FileNotFoundError("Could not find marea file")

        self._marea_file = marea_file
        self._counter_d = defaultdict(int)
        self._threshold_multiple = threshold_multiple
        # Get count of words in corpus
        with open(marea_file) as f:
            for line in f:
                columns = line.split("\t")
                if len(columns) != 3:
                    raise ValueError(f"Malformed marea line: {line}")
                payload = columns[2]  # columns[0]: pmid,  columns[1] year, columns[2] abstract text
                words = payload.split()
                for w in words:
                    self._counter_d[w] += 1
        print(f"Got {len(self._counter_d)} words")

        value_at_mean = np.mean(list(self._counter_d.values()))
        self._do_not_replace_threshold = round(value_at_mean * threshold_multiple)

        # Create synonym dictionary with NLTK
        # only downloads if needed
        nltk.download("wordnet", download_dir="../data")

        words_sorted_by_frequency = [
            k for k, v in sorted(self._counter_d.items(), key=lambda item: item[1], reverse=True)
        ]

        self._word_to_synonym_d = self.get_word_to_synonyms_d(words_sorted_by_frequency)

    def get_word_to_synonyms_d(self, unique_words_list) -> Dict:
        """
        Constructs a dictionary of synonyms.

        This method traverses through the list of unique words, and for each word, a list of synonyms is retrieved. The word
        with the highest occurrence from the synonym list is then chosen as the value in the dictionary, ensuring
        that common words are not replaced.

        :param unique_words_list: A list of unique words sorted by frequency.
        :type unique_words_list: List[str]
        :return: A dictionary where keys are unique words and values are the highest occurring synonyms.
        :rtype: Dict[str, str]

        """
        dictionary = {}
        n_words = len(unique_words_list)
        for i in tqdm(range(n_words), "getting unique words"):
            this_word = unique_words_list[i]
            # skip common words not replaced
            this_word_count = self._counter_d.get(this_word, 0)
            if this_word_count > self._do_not_replace_threshold:
                dictionary[this_word] = this_word
            else:
                synonym_list = self.get_synonym_list(this_word)
                dictionary[this_word] = self.get_highest_occuring_synonym(synonym_list)
        """""
        # Remove duplicates
        # if a value is not the same as the key, and there is no pair of the same key & value (based on the value),
                 and then replace the value with the same key
         i.e If a word is replaced by another  a word, it cannot replace another word.
                                Example:  before:
                                                work: study
                                                influence: work
                                                study: study
                                            after:
                                                work: study
                                                influence: influence
                                                study: study
        """ ""

        synonyms_used_for_replacements = set()
        word_to_synonyms_d = {}
        for word, most_frequent_synonym in tqdm(dictionary.items(), "getting most frequent synonym"):
            if word in synonyms_used_for_replacements:
                word_to_synonyms_d[word] = word
            else:
                synonyms_used_for_replacements.add(word)
                word_to_synonyms_d[word] = most_frequent_synonym
        return word_to_synonyms_d

    def get_highest_occuring_synonym(self, synonym_list) -> str:
        """
        gets the highest occuring word in the synonym list of the whole dataset (all the bastracts being transformed)
        @ urgument: synonym_list: a list of a word's syonyms from Wordnet
        @ return: The word (synonym) with the highest count in our dataset

        :param synonym_list: A list of synonyms derived from WordNet for a particular word in the dataset.
        :type synonym_list: List[str]

        :return: The synonym with the highest occurrence in the dataset.
        :rtype: str

        """
        if len(synonym_list) == 0:
            raise ValueError("synonym_list was length zero, should never happen")
        max_count = 0
        most_frequent_synonym = synonym_list[0]
        for s in synonym_list:
            # check frequency of a word in whole dataset
            c = self._counter_d.get(s, 0)
            if c > max_count:
                most_frequent_synonym = s
                max_count = c
        return most_frequent_synonym

    def get_synonym_list(self, word: str) -> List:
        """
        takes a word and returns a list of a word's synonyms using wordnet
        @argument: 'word' A word from the input dataset
        @return: a list of synonyms of the word
        """
        synonym_list = [word]
        for syn in wn.synsets(word):
            for l in syn.lemmas():
                synonym_list.append(l.name())
        return synonym_list

    def transform(self, line_abstract: str) -> str:
        """
        Replaces the variable in dataset with their synonyms from the dictionary
        :param line_abstract: A string representing a line from the marea file,
                            containing the PMID, year, and abstract text separated by tabs.
        :type line_abstract: str

        :return: A string representing the transformed abstract, with words replaced by their synonyms.
        :rtype: str

        """
        columns = line_abstract.split("\t")
        if len(columns) != 3:
            raise ValueError(f"Malformed marea line: {line_abstract}")
        abst_list = columns[2].split()  # columns[0]: pmid, columns[1] year, columns[0] abstract text
        for i in range(len(abst_list)):
            if abst_list[i] in self._word_to_synonym_d:
                abst_list[i] = self._word_to_synonym_d.get(abst_list[i])
            else:
                raise ValueError("the word is not in the dictionary")
            abstract = " ".join([str(item) for item in abst_list])
        # columns[2] = abstract
        # trans_abstract = columns[0] + '\t' + columns[1] + '\t' + columns[2] + '\n'
        return abstract + "\n"

    def output_abstract_only(self, outfilename):
        """
        The marea input file has three fields - PMID - Year - Abstract
        For word2vec, we want to have just the Abstract text
        :return: The third field (abstract) with new line symbol
        """
        fh = open(outfilename, "w")
        file_size = os.path.getsize(self._marea_file)
        pbar = tqdm(total=file_size, unit="MB", desc="output abstracts of input marea file")
        with open(self._marea_file, "r") as f:
            for line in f:
                pbar.update(sys.getsizeof(line) - sys.getsizeof("\n"))
                columns = line.split("\t")
                if len(columns) != 3:
                    raise ValueError(f"Malformed marea line: {line}")
                abstract = columns[2]
                fh.writelines(abstract)
        pbar.close()
        fh.close()

    def get_threshold(self) -> int:
        """
        returns the threshold count
        @return:  an int which is the frequency count at the (mean * multiple) of the unique words' frequencies

        """
        return self._do_not_replace_threshold

    def transform_and_write(self, output_file):
        """
        Transforms each abstract and writes to the specified output file.

        Reads each line from the marea file, transforms the abstract by replacing words with synonyms, and writes
        the new abstract to the specified output file.

        :param output_file: The path to the output file where transformed abstracts will be written.
        :type output_file: str

        """
        fh = open(output_file, "w")
        file_size = os.path.getsize(self._marea_file)
        pbar = tqdm(total=file_size, unit="MB", desc="replacing words in text")
        with open(self._marea_file, "r") as f:
            for line in f:
                pbar.update(sys.getsizeof(line) - sys.getsizeof("\n"))
                new_abstract = self.transform(line)
                fh.writelines(new_abstract)
        pbar.close()
        fh.close()

    def get_total_word_count(self):
        return len(self._word_to_synonym_d)

    def get_replaced_word_count(self):
        """
        Computes the number of words in the dataset that were replaced using WordNet.

        :return: The count of replaced words in the dataset.
        :rtype: int
        """
        replaced = 0
        for k, v in self._word_to_synonym_d.items():
            if k != v:
                replaced += 1
        return replaced
