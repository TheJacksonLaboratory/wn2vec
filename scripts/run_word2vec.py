
import logging
import datetime

import argparse
import time

import wn2vec
from wn2vec import Word2VecRunner


today_date = datetime.date.today().strftime("%b_%d_%Y")
start_time = time.time()
start_time_fmt= time.strftime("%H:%M:%S", time.gmtime(start_time))

logname = f"wn2vec_{today_date} {start_time_fmt}.log"

logging.basicConfig(level=logging.INFO, filename=logname, filemode='w', datefmt='%Y-%m-%d %H:%M:%S', 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


parser = argparse.ArgumentParser()
parser.add_argument('-i', type=str, required=True, help ='address of the .tsv file with abstracts') 
parser.add_argument('-v', type=str, default='vector', help='name of vector file output')
parser.add_argument('-m', type=str, default='metadata', help='name of metadata file')
parser.add_argument('--embedding_dim', type=int, default=128)
parser.add_argument('--vocab_size', type=int, default=50000)
args = parser.parse_args()



input_file_path = args.i
vector_name = args.v
metadata_name = args.m
vocab_size = args.vocab_size
embed_dim = args.embedding_dim

runner = Word2VecRunner(input_file=input_file_path, vector=vector_name, metadata=metadata_name, vocab_size=5000, 
                             embedding_dim=embed_dim, sequence_length = 10, window_size = 2, 
                              BATCH_SIZE = 128, BUFFER_SIZE= 10000, num_ns = 4, SEED = 42 )


runner.input_file()

runner.get_vecotrized_layer()

runner.get_embedding()



# record end time
end_time = time.time()
duration_time = time.strftime("%H:%M:%S", time.gmtime(end_time - start_time))
logging.info(f"Execution time: {duration_time} ")
