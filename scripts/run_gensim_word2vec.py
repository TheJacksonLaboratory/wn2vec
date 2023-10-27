import io
import re
import string
import tqdm
import logging
import datetime
import argparse
import time

########

import multiprocessing
from gensim.models import Word2Vec
from gensim.models.callbacks import CallbackAny2Vec

class epoch_loss_callback(CallbackAny2Vec):
    def __init__(self):
        self.epoch = 1
        self.losses = []
        self.cumu_losses = []
        self.previous_epoch_time = time.time()

    def on_epoch_end(self, model):
        cumu_loss = model.get_latest_training_loss()
        loss = cumu_loss if self.epoch <= 1 else cumu_loss - self.cumu_losses[-1]
        now = time.time()
        epoch_seconds = now - self.previous_epoch_time
        self.previous_epoch_time = now
        print(f"Loss after epoch {self.epoch}: {loss} / cumulative loss: {cumu_loss} "+\
              f" -> epoch took {round(epoch_seconds, 2)} s")
        self.epoch += 1
        self.losses.append(loss)
        self.cumu_losses.append(cumu_loss)        
########


today_date = datetime.date.today().strftime("%b_%d_%Y")
start_time = time.time()
start_time_fmt = time.strftime("%H:%M:%S", time.gmtime(start_time))

logname = f"wn2vec_{today_date} {start_time_fmt}.log"

logging.basicConfig(
    level=logging.INFO,
    filename=logname,
    filemode="w",
    datefmt="%Y-%m-%d %H:%M:%S",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, help="path to input (marea) file")
parser.add_argument("-v", "--vector", type=str, help="name of output vector file")
parser.add_argument("-m", "--metadata", type=str, help="name of output metadata file")
parser.add_argument("-s", "--vocab_size", type=int, default=100000, help="size of vocabulary for word2vec")
args = parser.parse_args()
# the vocabulary size and the number of words in a sequence.
vocab_size = args.vocab_size
path_to_file = args.input
vector_file = args.vector
metadata_file = args.metadata

# Other arguments
BUFFER_SIZE = 10000
embedding_dim = 128

cores = multiprocessing.cpu_count() # Count the number of cores in a computer

logging.info(f"Starting gensim word2vec run on {today_date}")
logging.info(f"vocab_size: {vocab_size}")
# logging.info(f"sequence_length: {sequence_length}")


# CREATE MODEL
w2v_model = Word2Vec(vector_size=embedding_dim,
                     window=2,
                     min_count=1,
                     sample=1e-5, 
                     alpha=0.03, 
                     workers=cores-1,
                     min_alpha=0.0001,
                     sg=1,
                     compute_loss=True,
                     negative=5
                     )

# CREATE VOCABULARY
t = time.time()

w2v_model.build_vocab(corpus_file=path_to_file,
                      progress_per=10000)

print('Time to build vocab: {} mins'.format(round((time.time() - t) / 60, 2)))

# TRAIN MODEL
t = time.time()
loss_calc = epoch_loss_callback()

trained_word_count, raw_word_count = w2v_model.train(corpus_file=path_to_file,
    total_examples=w2v_model.corpus_count,
    total_words=w2v_model.corpus_total_words,
    epochs=1000,
    report_delay=1,
    compute_loss=True,
    callbacks= [loss_calc]
    )

print('Time to train the model: {} mins'.format(round((time.time() - t) / 60, 2)))

# open file in write mode
with open(r'./losses.dat', 'w') as fp:
    for item in loss_calc.losses:
        # write each item on a new line
        fp.write("%s\n" % item)
    print('Done')
