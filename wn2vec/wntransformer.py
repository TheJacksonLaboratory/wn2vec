## when the pubmed_cr has 3 columns
import nltk
from nltk.corpus import wordnet as wn
from typing import List, Dict
import os
import pandas as pd
import numpy as np
import math

import os
from collections import defaultdict

#nltk.download('omw-1.4')
# nltk.download()

class WordNetTransformer:
    #_do_not_replace_threshold: int = 2

    def __init__(self, marea_file, output_file) -> None:
        """
        Path to the file produced by marea
        """
        if not os.path.exists(marea_file):
            raise FileNotFoundError("Could not find marea file")
        if not os.path.exists(output_file):
            raise FileNotFoundError("Could not find output file")

        self._marea_file = marea_file
        self._output_file = output_file
        self._counter = defaultdict(int)
        # Get count of words in corpus
        with open(marea_file) as f:
            for line in f:
                columns = line.split('\t')
                if len(columns) != 3:
                    raise ValueError(f'Malformed marea line: {line}')
                payload = columns[2]  #columns[0]: pmid,  columns[1] year, columns[2] abstract text
                words = payload.split()
                for w in words:
                    self._counter[w] += 1

        # Create synonym dictionary with NLTK
        # if needed, install wordnet
        nltk.download("wordnet")

        words_sorted_by_frequency = [k for k, v in
                                     sorted(self._counter.items(), key=lambda item: item[1], reverse=True)]
        self._do_not_replace_threshold = self.best_threshold(self._counter)
        self._dict = self.dictCreate(words_sorted_by_frequency)

        f = open(marea_file, "r")
        y = open(output_file, 'w')
        dictionary = self.dictCreate(words_sorted_by_frequency)
        for line in f:
            new_abstract = self.transform(line, dictionary)
            y.writelines(new_abstract)
        y.close()
        f.close()

    def dictCreate(self, word_list) -> Dict:
        """
        Creates a dictionary from the whole data set, they keys are in order of their frequency words
        and the values are synonyms of keys from synset
        @argument: 'word_list' a list of unique words from the whole dataset in order of frequency
        @return: a dictionary of all the variables in the dataset, the keys are the unique variables
                   with high frequency, and values are key's synonym
        """
        dictionary = {}
        for i in range(len(word_list)):
            this_word = word_list[i]
            # skip common words
            this_word_count = self._counter.get(this_word, 0)
            if this_word_count > self._do_not_replace_threshold:
                dictionary[this_word] = this_word
            else:
                synonym_list = self.synonym(this_word)
                dictionary[this_word] = self._highest_count_synonym(synonym_list)
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
        """""
        # dictionary to tuple
        dict_tuple = [(k, v) for k, v in dictionary.items()]

        # tuple to list
        size = len(dict_tuple)
        key_list = []
        value_list = []
        for i in range(0, size):
            key_list.append(dict_tuple[i][0])
            value_list.append(dict_tuple[i][1])

        #check if there is a pair of the unique value with a smiliar key
        def same_key_value(word, dict_tuple):
            same = True
            for i in range(len(dict_tuple)):
                if (dict_tuple[i][0] == word) and (dict_tuple[i][0] == dict_tuple[i][1]):
                    same = False
            return same

        for i in range(len(value_list)):
            if (value_list[i] != key_list[i]):
                if (same_key_value(value_list[i], dict_tuple) == True):
                    value_list[i] = key_list[i]

        # list to dictionary
        new_dictionary = {}
        for key in key_list:
            for value in value_list:
                new_dictionary[key] = value
                value_list.remove(value)
                break

        return new_dictionary


    def _highest_count_synonym(self, synonym_list) -> str:
        """
        :param synonym_list: a list of a word and its synonyms in Wordnet
        :return: The word (synonym) with the highest count in our dataset
        """
        if len(synonym_list) == 0:
            raise ValueError("synonym_list was length zero, should never happen")
        max_count = 0
        max_word = synonym_list[0]
        for s in synonym_list:
            c = self._counter.get(s, 0)
            if c > max_count:
                max_word = s
                max_count = c
        return max_word

    def synonym(self, word: str) -> List:
        """
        @argument: 'word' A word from the input dataset
        @return: a list of synonyms of the words
        """
        synonyms = [word]
        for syn in wn.synsets(word):
            for l in syn.lemmas():
                synonyms.append(l.name())
        return synonyms

    def transform(self, line_abstract: str, _dict) -> str:
        """
        Replaces the variable in dataset with their synonyms from the dictionary
        @argument: 'line_abstract' a string of line abstract including pubmed id and year
                   "_dict" a dictionary created with the whole dataset
        @return: 'trans_abstract'  a string of transformed abstract

        """
        columns = line_abstract.split('\t')
        if len(columns) != 3:
            raise ValueError(f'Malformed marea line: {line}')
        abst_list = columns[2].split()  # columns[0]: pmid, columns[1] year, columns[0] abstract text
        for i in range(len(abst_list)):
            if abst_list[i] in self._dict:
                abst_list[i] = self._dict.get(abst_list[i])
            else:
                raise ValueError("the word is not in the dictionary")
            abstract = ' '.join([str(item) for item in abst_list])
        columns[2] = abstract
        trans_abstract = columns[0] + '\t' + columns[1] + '\t' + columns[2] + '\n'
        return (trans_abstract)


    def best_threshold(self,_counter) -> int:
        """

        @argument: '_counter' a dictionary created from whole dataset with the unique work as the key and frequency as the value
        @return: 'mean_frequency'  an int which is mean of the unique words' frequencies

        """
        # convert a dictionary into a tuple
        counter_dict = _counter
        dict_tuple = [(k, v) for k, v in counter_dict.items()]
        sorted_dict_tup = dict_tuple
        # convert a tuple into a panda dataframe
        dict_words = []
        words_count = []
        for i in range(0, len(sorted_dict_tup)):
            dict_words.append(sorted_dict_tup[i][0])
            words_count.append(sorted_dict_tup[i][1])

        unique_words = pd.Series(dict_words)
        words_frequency = pd.Series(words_count)

        dict_df = pd.concat([unique_words, words_frequency], axis=1)

        # Rename Columns
        dict_df.columns = ['Words', 'Counts']

        # print mean of the word frequency
        mean_frequency = dict_df['Counts'].mean()

        mean_frequency = round(mean_frequency)
        return mean_frequency



if __name__ == "__main__":

    #running code using command line
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str) #address of the marea file
    parser.add_argument('output', type=str) #address of output file
    args = parser.parse_args()


    def all_replaced_words(dict):
        replaced = []
        for i in dict:
            if dict.get(i) != i:
                replaced.append(i)
        return replaced

    app = WordNetTransformer(args.input, args.output)

    threshold = app._do_not_replace_threshold
    print('Threshold: ', threshold)

    dictionary = app._dict
    replaced_words = all_replaced_words(dictionary)
    print("Number of replaced words: ", len(replaced_words))
    #print('All replaced words: \n', replaced_words)

    # sample way of running the code using arparse:
    """
    locate the file you are running + python + wntransformer.py + address of marea_file + address of output_file
    example: 
    > python wntransformer.py 'marea_file location' 'output_file location'

    """
