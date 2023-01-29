
import logging
import datetime

import argparse
import time
import io

import wn2vec 
from wn2vec import Word2VecRunner


today_date = datetime.date.today().strftime("%b_%d_%Y")
logname = f"wn2vec_{today_date}.log"

logging.basicConfig(level=logging.INFO, filename=logname, filemode='w', datefmt='%Y-%m-%d %H:%M:%S', 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# record start time
start_time = time.time()

parser = argparse.ArgumentParser()
parser.add_argument('-i', type=str, default='../data/pubmed_filt.tsv', help ='address of the .tsv file with abstracts') 
parser.add_argument('-v', type=str, default='vector_file', help='name of vector file output')
parser.add_argument('-m', type=str, default='metadata_file', help='name of metadata file')
parser.add_argument('-w', '--window_size', type=int, default=2, help='size of embedding window')

parser.add_argument('--embedding_dim', type=int, default=128)
parser.add_argument('--vocab_size', type=int, default=100000)
args = parser.parse_args()



input_file_path = args.i
vector_name = args.v
metadata_name = args.m
vocab_size = args.vocab_size
embed_dim = args.embedding_dim
window_size = args.window_size
num_ns = 4
sequence_length = 10
BATCH_SIZE = 128
BUFFER_SIZE= 10000
SEED = 42


runner = Word2VecRunner(input_file=input_file_path, vector=vector_name, metadata=metadata_name, vocab_size=5000, 
                             embedding_dim=embed_dim, sequence_length = sequence_length, window_size = window_size, 
                              BATCH_SIZE = 128, BUFFER_SIZE= 10000, num_ns = 4, SEED = 42 )

logging.info("starting run_word2vec.py")
logging.info(f"input_file_path: {input_file_path}")
logging.info(f"vector_name: {vector_name}")
logging.info(f"metadata_name: {metadata_name}")
logging.info(f"embed_dim: {embed_dim}")
logging.info(f"sequence_length: {sequence_length}")
logging.info(f"BATCH_SIZE: {BATCH_SIZE}")
logging.info(f"BUFFER_SIZE: {BUFFER_SIZE}")
logging.info(f"SEED: {SEED}")

      
runner.input_file()

vectorize_layer, text_ds, inverse_vocab = runner.get_vecotrized_layer()
targets, contexts, labels = runner.get_sequences(vectorize_layer, text_ds, inverse_vocab)

dataset = runner.get_dataset(targets, contexts, labels )

runner.get_embedding(dataset,vectorize_layer )


# record end time
end_time = time.time()
duration_time = time.strftime("%H:%M:%S", time.gmtime(end_time - start_time))
logging.info(f"Execution time: {duration_time} ")

