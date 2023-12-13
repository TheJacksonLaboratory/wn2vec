import argparse
import datetime
import logging
import multiprocessing
import time
import numpy as np
import pandas as pd
from gensim.models import Word2Vec
from gensim.models.callbacks import CallbackAny2Vec
from tqdm import tqdm

# Configure logging
today_date = datetime.date.today().strftime("%b_%d_%Y")
logname = f"wn2vec_{today_date} {datetime.datetime.now().strftime('%H:%M:%S')}.log"
logging.basicConfig(
    level=logging.INFO,
    filename=logname,
    filemode="w",
    datefmt="%Y-%m-%d %H:%M:%S",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Word2Vec Model Training Script")
parser.add_argument("-i", "--input", type=str, help="Path to input (marea) file")
parser.add_argument("-p", "--prefix", type=str, required=True, help="prefix for output metadata and vector files")
args = parser.parse_args()

# Set up parameters for Word2Vec
EPOCH = 10
embedding_dim = 128
cores = multiprocessing.cpu_count()

# Log start and parameters
logging.info(f"Starting gensim word2vec run on {today_date}")
logging.info(f"epoch: {EPOCH}, input_file: {args.input}")

# Callback class for tracking training progress and loss
class EpochProgressCallback(CallbackAny2Vec):
    """Callback to report progress and loss after each epoch."""
    def __init__(self, total_epochs):
        self.epoch = 1
        self.total_epochs = total_epochs
        self.losses = []
        self.cumu_losses = []
        self.previous_epoch_time = time.time()

    def on_epoch_end(self, model):
        loss = model.get_latest_training_loss()
        cumu_loss = loss if self.epoch == 1 else loss - self.cumu_losses[-1]
        epoch_seconds = time.time() - self.previous_epoch_time
        self.previous_epoch_time = time.time()
        logging.info(f"Epoch {self.epoch}/{self.total_epochs} completed: Loss = {loss}, Cumulative Loss = {cumu_loss}, Epoch Duration = {round(epoch_seconds, 2)} s")
        self.epoch += 1
        self.losses.append(loss)
        self.cumu_losses.append(cumu_loss)

# Create the Word2Vec model
w2v_model = Word2Vec(
    vector_size=embedding_dim,
    window=10,
    min_count=1,
    sample=1e-5,
    alpha=0.03,
    workers=cores - 1,
    min_alpha=0.0001,
    sg=1,
    compute_loss=True,
    negative=5
)

# Build vocabulary
w2v_model.build_vocab(corpus_file=args.input, progress_per=10000)

# Training the model with progress bar and loss tracking
loss_callback = EpochProgressCallback(EPOCH)
with tqdm(total=EPOCH, unit="epoch", desc="Training Progress") as pbar:
    for epoch in range(EPOCH):
        w2v_model.train(
            corpus_file=args.input,
            total_examples=w2v_model.corpus_count,
            total_words=w2v_model.corpus_total_words,
            epochs=1,  # Train for one epoch at a time
            report_delay=1,
            compute_loss=True,
            callbacks=[loss_callback]
        )
        pbar.update(1)

# Extract vectors and words from the model
vectors = w2v_model.wv.vectors  # Word vectors
words = w2v_model.wv.index_to_key  # Corresponding words

# Save vectors and metadata to TSV files
prefix = args.prefix
vector_file = f"{prefix}_vector.tsv"
metadata_file = f"{prefix}_metadata.tsv"
np.savetxt(vector_file, vectors, delimiter='\t')
pd.DataFrame(words).to_csv(metadata_file, sep='\t', header=False, index=False)

