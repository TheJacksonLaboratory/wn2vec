import itertools
import collections
from typing import List
import numpy as np
import tensorflow as tf

# also defined in dataset.py, needs to be in synch
OOV_ID = -1

class WordTokenizer(object):
    """Vanilla word tokenizer

    Tokenizer that spits out space-separated tokens from raw text
    string. Note for non-space separated languages, the corpus must be
    pre-tokenized such that tokens are space-delimited.

    :param max_vocab_size: maximum vocabulary size. If > 0, only the top  `max_vocab_size` most frequent words will be kept in vocabulary.
    :type max_vocab_size: int
    :param min_count: words whose counts < `min_count` will not be included in the vocabulary.
    :type min_count: int
    :param sample: subsampling rate, default 1e-3
    :type sample: float
    """

    def __init__(self, max_vocab_size=0, min_count=10, sample=1e-3):
        """Constructor.
        """
        self._max_vocab_size = max_vocab_size
        self._min_count = min_count
        self._sample = sample
        self._vocab = None
        self._table_words = None
        self._unigram_counts = None
        self._keep_probs = None

    @property
    def unigram_counts(self):
        return self._unigram_counts

    @property
    def table_words(self):
        return self._table_words

    def _build_raw_vocab(self, filenames):
        """Builds raw vocabulary by iterate through the corpus once and count the unique words.

        :param filenames: names of text files.
        :type filenames: List[str]
        :returns: raw_vocab: a list of 2-tuples holding the word (string) and count (int), sorted in descending order of word count.
        :rtype: collections.Counter
        """
        lines = []
        for fn in filenames:
            with tf.io.gfile.GFile(fn) as f:
                lines.append(f)
        lines = itertools.chain(*lines)

        raw_vocab = collections.Counter()
        for line in lines:
            raw_vocab.update(line.strip().split())
        raw_vocab = raw_vocab.most_common()
        # truncate to have at most `max_vocab_size` vocab words
        if self._max_vocab_size > 0:
            raw_vocab = raw_vocab[:self._max_vocab_size]
        return raw_vocab

    def build_vocab(self, filenames):
        """Builds the vocabulary.

        Sets the following attributes: for each word `word` we have
        vocab[word] = index
        table_words[index] = word `word`
        unigram_counts[index] = count of `word` in vocab
        keep_probs[index] = keep prob of `word` for subsampling

        :param filenames: names of text files.
        :type filenames: List[str]
        """
        raw_vocab = self._build_raw_vocab(filenames)
        raw_vocab = [(w, c) for w, c in raw_vocab if c >= self._min_count]
        self._corpus_size = sum(list(zip(*raw_vocab))[1])

        self._vocab = {}
        self._table_words = []
        self._unigram_counts = []
        self._keep_probs = []
        for index, (word, count) in enumerate(raw_vocab):
            frac = count / float(self._corpus_size)
            keep_prob = (np.sqrt(frac / self._sample) + 1) * (self._sample / frac)
            keep_prob = np.minimum(keep_prob, 1.0)
            self._vocab[word] = index
            self._table_words.append(word)
            self._unigram_counts.append(count)
            self._keep_probs.append(keep_prob)

    def encode(self, string):
        """Split raw text string into tokens (space-separated) and translate to token ids.

        :param string: the raw text string to be tokenized.
        :type string: str
        :returns:a list of ints, the token ids of the tokenized string.
        :rtype: List[int]
        """
        tokens = string.strip().split()
        ids = [self._vocab[token] if token in self._vocab else OOV_ID
               for token in tokens]
        return ids
