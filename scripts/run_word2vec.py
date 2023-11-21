import argparse
import datetime
import io
import logging
import multiprocessing
import re
import string
import time
import tqdm

from gensim.models import Word2Vec
from gensim.models.callbacks import CallbackAny2Vec

# Setting up logging
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

# Argument parsing
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, help="path to input (marea) file")
parser.add_argument("-v", "--vector", type=str, help="name of output vector file")
parser.add_argument("-m", "--metadata", type=str, help="name of output metadata file")
parser.add_argument("-model", "--model_name", type=str, default='word2vec.wordvectors', help="name of model")
parser.add_argument("-s", "--vocab_size", type=int, default=100000, help="size of vocabulary for word2vec")
args = parser.parse_args()

# Setting up parameters
vocab_size = args.vocab_size
path_to_file = args.input
vector_file = args.vector
metadata_file = args.metadata
model_name = args.model_name
EPOCH = 10
BATCH_SIZE = 1024
BUFFER_SIZE = 10000
embedding_dim = 128
cores = multiprocessing.cpu_count()

# Logging the start and parameters
logging.info(f"Starting gensim word2vec run on {today_date}")
logging.info(f"vocab_size: {vocab_size}")
logging.info(f"epoch: {EPOCH}")
logging.info(f"input_file: {path_to_file}")
logging.info(f"model_name: {model_name}")


# Callback class to capture training loss after each epoch
class EpochLossCallback(CallbackAny2Vec):
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


# Creating the Word2Vec model
w2v_model = Word2Vec(
    vector_size=embedding_dim,
    window=10,
    min_count=1,
    sample=1e-5, 
    alpha=0.03, 
    workers=cores-1,
    min_alpha=0.0001,
    sg=1,
    compute_loss=True,
    negative=5
)

# Building vocabulary
t = time.time()
w2v_model.build_vocab(corpus_file=path_to_file, progress_per=10000)
print('Time to build vocab: {} mins'.format(round((time.time() - t) / 60, 2)))

# Training the model
t = time.time()
loss_calc = EpochLossCallback()
trained_word_count, raw_word_count = w2v_model.train(
    corpus_file=path_to_file,
    total_examples=w2v_model.corpus_count,
    total_words=w2v_model.corpus_total_words,
    epochs=EPOCH,
    report_delay=1,
    compute_loss=True,
    callbacks=[loss_calc]
)
print('Time to train the model: {} mins'.format(round((time.time() - t) / 60, 2)))

# Saving the losses
with open('./losses.dat', 'w') as fp:
    for item in loss_calc.losses:
        fp.write("%s\n" % item)
    print('Losses saved.')

# Saving the vectors and metadata

## Output the vector and metadata files representing the embeddings

word_vectors = w2v_model.wv
word_vectors.save(model_name)

w2v_model.wv.save_word2vec_format(vector_file, binary=True)
print(f"Vectors saved to {vector_file}")

# Assuming metadata is the vocabulary
with open(metadata_file, 'w') as meta:
    for word in w2v_model.wv.index_to_key:
        meta.write(word + '\n')
print(f"Metadata saved to {metadata_file}")

"""
python run_gensim_word2vec_v1.py -i data/pubmed_filt/1m_abst_all_pubmed_filt.tsv -v vectors_1 -m metadata_1  -model 1m_all_filt_word2vec.wordvectors
"""
