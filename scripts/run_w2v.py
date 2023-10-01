import io
import os
import re
import string
import logging
import datetime
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
import argparse
import time
from typing import List

today_date = datetime.date.today().strftime("%b_%d_%Y")
start_time = time.time()
start_time_fmt = time.strftime("%H:%M:%S", time.gmtime(start_time))

logname = f"wn2vec_{today_date}.log"

logging.basicConfig(
    level=logging.INFO,
    filename=logname,
    filemode="w",
    datefmt="%Y-%m-%d %H:%M:%S",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, required=True, help="path to input (marea) file")
parser.add_argument("-v", "--vector", type=str, help="name of output vector file")
parser.add_argument("-m", "--metadata", type=str, help="name of output metadata file")
parser.add_argument("-s", "--vocab_size", type=int, default=100000, help="size of vocabulary for word2vec")
parser.add_argument("--num_epochs", default=10, type=int, help="number of epochs")
args = parser.parse_args()
# the vocabulary size and the number of words in a sequence.
vocab_size = args.vocab_size
input_file_path = args.input
vector_file = args.vector
metadata_file = args.metadata
n_epochs = args.num_epochs

# Other arguments
sequence_length = 10
SEED = 42
AUTOTUNE = tf.data.experimental.AUTOTUNE
num_ns = 4
BATCH_SIZE = 1024
BUFFER_SIZE = 10000
embedding_dim = 128

logging.info(f"Starting word2vec run on {today_date}")
logging.info(f"vocab_size: {vocab_size}")
logging.info(f"sequence_length: {sequence_length}")


def custom_standardization(input_data):
    """
    :param input_data: an input string
    :return: same string, lower-cased with punctuation removed
    """
    lowercase = tf.strings.lower(input_data)
    return tf.strings.regex_replace(lowercase, "[%s]" % re.escape(string.punctuation), "")


def prepare_data(input_file):
    """
    Prepare data for Word2vec by retrieving lines from file and transforming to integers

    :param input_file: Input file for word2vec (a concept/synonym replaced file)
    :return:
    """
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"Could not find word2vec input file at {input_file}")
    text_ds = tf.data.TextLineDataset(input_file).filter(lambda x: tf.cast(tf.strings.length(x), bool))
    # Define the vocabulary size and the number of words in a sequence.
    sequence_length = 5000

    # Use the `TextVectorization` layer to normalize, split, and map strings to
    # integers. Set the `output_sequence_length` length to pad all samples to the
    # same length.
    vectorize_layer = layers.TextVectorization(
        standardize=custom_standardization,
        max_tokens=vocab_size,
        output_mode='int',
        output_sequence_length=sequence_length)

    vectorize_layer.adapt(text_ds.batch(1024))

    # Save the created vocabulary for reference.
    inverse_vocab = vectorize_layer.get_vocabulary()

    # Vectorize the data in text_ds.
    text_vector_ds = text_ds.batch(1024).prefetch(AUTOTUNE).map(vectorize_layer).unbatch()

    return inverse_vocab, text_vector_ds


if __name__ == "__main__":
    inverse_vocab, text_vector_ds = prepare_data(input_file=input_file_path)
    logging.info(f"size of inverse vocabulary {len(inverse_vocab)}")
    sequences = list(text_vector_ds.as_numpy_iterator())
    print(f"n sequeces {len(sequences)}")
    print(f"seqience len {len(sequences[0])}")
    for s in sequences[0]:
        print(s, end=" ")
