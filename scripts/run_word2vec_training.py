"""Train a word2vec model to obtain word embedding vectors.

There are a total of four combination of architectures and training algorithms
that the model can be trained with:

architecture:
  - skip_gram
  - cbow (continuous bag-of-words)

training algorithm
  - negative_sampling
  - hierarchical_softmax
"""
import logging
import os
import sys
import datetime
import tensorflow as tf
import numpy as np
from absl import app
from absl import flags

from wn2vec import WordTokenizer, Word2VecDatasetBuilder, Word2VecModel, EarlyStoppingMonitor

import time


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
logging.getLogger().addHandler(logging.StreamHandler(sys.stderr))


flags.DEFINE_string('arch', 'skip_gram', 'Architecture (skip_gram or cbow).')
flags.DEFINE_string('algm', 'negative_sampling', 'Training algorithm '
                                                 '(negative_sampling or hierarchical_softmax).')
flags.DEFINE_integer('epochs', 1, 'Num of epochs to iterate through corpus.')
flags.DEFINE_integer('batch_size', 256, 'Batch size.')
flags.DEFINE_integer('max_vocab_size', 0, 'Maximum vocabulary size. If > 0, '
                                          'the top `max_vocab_size` most frequent words will be kept in vocabulary.')
flags.DEFINE_integer('min_count', 10, 'Words whose counts < `min_count` will '
                                      'not be included in the vocabulary.')
flags.DEFINE_float('sample', 1e-3, 'Subsampling rate.')
flags.DEFINE_integer('window_size', 10, 'Num of words on the left or right side'
                                        ' of target word within a window.')

flags.DEFINE_integer('hidden_size', 300, 'Length of word vector.')
flags.DEFINE_integer('negatives', 5, 'Num of negative words to sample.')
flags.DEFINE_float('power', 0.75, 'Distortion for negative sampling.')
flags.DEFINE_float('alpha', 0.025, 'Initial learning rate.')
flags.DEFINE_float('min_alpha', 0.0001, 'Final learning rate.')
flags.DEFINE_boolean('add_bias', True, 'Whether to add bias term to dotproduct '
                                       'between syn0 and syn1 vectors.')

flags.DEFINE_integer('log_per_steps', 10000, 'Every `log_per_steps` steps to '
                                             ' log the value of loss to be minimized.')
flags.DEFINE_list(
    'filenames', None, 'Names of comma-separated input text files.')
flags.DEFINE_string('out_dir', 'word2vec_out', 'Output directory.')

FLAGS = flags.FLAGS

def get_train_step_signature(
    arch, algm, batch_size, window_size=None, max_depth=None):
  """Get the training step signatures for `inputs`, `labels` and `progress`  tensor.

  :param arch: string scalar, architecture ('skip_gram' or 'cbow').
  :type arch: str
  :param   algm: training algorithm ('negative_sampling' or 'hierarchical_softmax').
  :type algm: str
  :returns: train_step_signature: a list of three tf.TensorSpec instances, \
    specifying the tensor spec (shape and dtype) for `inputs`, `labels` and  `progress`.
  """
  if arch=='skip_gram':
    inputs_spec = tf.TensorSpec(shape=(batch_size,), dtype='int64')
  elif arch == 'cbow':
    inputs_spec = tf.TensorSpec(
        shape=(batch_size, 2*window_size+1), dtype='int64')
  else:
    raise ValueError('`arch` must be either "skip_gram" or "cbow".')

  if algm == 'negative_sampling':
    labels_spec = tf.TensorSpec(shape=(batch_size,), dtype='int64')
  elif algm == 'hierarchical_softmax':
    labels_spec = tf.TensorSpec(
        shape=(batch_size, 2*max_depth+1), dtype='int64')
  else:
    raise ValueError('`algm` must be either "negative_sampling" or '
        '"hierarchical_softmax".')

  progress_spec = tf.TensorSpec(shape=(batch_size,), dtype='float32')

  train_step_signature = [inputs_spec, labels_spec, progress_spec]
  return train_step_signature


def main(_):
    arch = FLAGS.arch
    algm = FLAGS.algm
    epochs = FLAGS.epochs
    batch_size = FLAGS.batch_size
    max_vocab_size = FLAGS.max_vocab_size
    min_count = FLAGS.min_count
    sample = FLAGS.sample
    window_size = FLAGS.window_size
    hidden_size = FLAGS.hidden_size
    negatives = FLAGS.negatives
    power = FLAGS.power
    alpha = FLAGS.alpha
    min_alpha = FLAGS.min_alpha
    add_bias = FLAGS.add_bias
    log_per_steps = FLAGS.log_per_steps
    filenames = FLAGS.filenames
    out_dir = FLAGS.out_dir

    logging.info("arch={arch}")
    logging.info("algm={algm}")
    logging.info("epochs={epochs}")
    logging.info("batch_size={batch_size}")
    logging.info("max_vocab_size={max_vocab_size}")
    logging.info("min_count={min_count}")
    logging.info("sample={sample}")
    logging.info("window_size={window_size}")
    logging.info("hidden_size={hidden_size}")
    logging.info("negatives={negatives}")
    logging.info("power={power}")
    logging.info("alpha={alpha}")
    logging.info("min_alpha={min_alpha}")
    logging.info("add_bias={add_bias}")
    logging.info("log_per_steps={log_per_steps}")
    logging.info("filenames={filenames}")
    logging.info("out_dir={out_dir}")


    # create out directory if needed
    if not os.path.exists(out_dir):
        # Create a new directory because it does not exist
        os.makedirs(out_dir)
        logging.info(f"created directory for output files at {out_dir}")
    else:
        logging.info(f"Using existing directory for output files at {out_dir}")

    tokenizer = WordTokenizer(
        max_vocab_size=max_vocab_size, min_count=min_count, sample=sample)
    tokenizer.build_vocab(filenames)

    builder = Word2VecDatasetBuilder(tokenizer,
                                     arch=arch,
                                     algm=algm,
                                     epochs=epochs,
                                     batch_size=batch_size,
                                     window_size=window_size)
    dataset = builder.build_dataset(filenames)
    word2vec = Word2VecModel(tokenizer.unigram_counts,
                             arch=arch,
                             algm=algm,
                             hidden_size=hidden_size,
                             batch_size=batch_size,
                             negatives=negatives,
                             power=power,
                             alpha=alpha,
                             min_alpha=min_alpha,
                             add_bias=add_bias)

    train_step_signature = get_train_step_signature(arch, algm, batch_size, window_size, builder._max_depth)
    optimizer = tf.keras.optimizers.SGD(1.0)

    @tf.function(input_signature=train_step_signature)
    def train_step(inputs, labels, progress):
        loss = word2vec(inputs, labels)
        gradients = tf.gradients(loss, word2vec.trainable_variables)

        learning_rate = tf.maximum(alpha * (1 - progress[0]) +
                                   min_alpha * progress[0], min_alpha)

        if hasattr(gradients[0], '_values'):
            gradients[0]._values *= learning_rate
        else:
            gradients[0] *= learning_rate

        if hasattr(gradients[1], '_values'):
            gradients[1]._values *= learning_rate
        else:
            gradients[1] *= learning_rate

        if hasattr(gradients[2], '_values'):
            gradients[2]._values *= learning_rate
        else:
            gradients[2] *= learning_rate

        optimizer.apply_gradients(
            zip(gradients, word2vec.trainable_variables))

        return loss, learning_rate
    num_batches = tf.data.experimental.cardinality(dataset=dataset)
    logging.info(f"number of batches {num_batches}")
    average_loss = 0.
    """
    monitor='val_loss', min_delta=0, patience=0, verbose=0,
    mode='auto', baseline=None, restore_best_weights=False
    """
    restore_best_weights = True
    earlyStopper = EarlyStoppingMonitor(min_delta = 0.001, patience=2, verbose=True)
    shouldStop = False
    for epoch in range(epochs):
        logging.info(f"[INFO] epoch {epoch}/{epochs}")
        for step, (inputs, labels, progress) in enumerate(dataset):
            loss, learning_rate = train_step(inputs, labels, progress)
            average_loss += loss.numpy().mean()
            if step % log_per_steps == 0:
                if step > 0:
                    average_loss /= log_per_steps
                learning_r = learning_rate.numpy()
                logging.info(f"step: {step}; average_loss: {average_loss:.4f}; learning_rate: {learning_r:.4f}")
                logging.info(f"progress: {progress}")
                average_loss = 0.
        shouldStop = earlyStopper.should_stop(average_loss=average_loss, weights=word2vec.weights, epoch=epoch)
        logging.info(earlyStopper.display())
        if shouldStop:
            break
    if restore_best_weights:
        weights = earlyStopper.get_best_weights()
        if weights is None:
            raise ValueError("Unable to retrieve best weights (None)")
    else:
        weights = word2vec.weights


    #syn0_final = word2vec.weights[0].numpy()
    syn0_final = weights[0].numpy()
    np.save(os.path.join(FLAGS.out_dir, 'syn0_final'), syn0_final)
    with tf.io.gfile.GFile(os.path.join(FLAGS.out_dir, 'vocab.txt'), 'w') as f:
        for w in tokenizer.table_words:
            f.write(w + '\n')
    logging.info(f"Done training for input {filenames}")
    logging.info(f"Word embeddings saved to {os.path.join(out_dir, 'syn0_final.npy')}")
    logging.info(f"Vocabulary saved to {os.path.join(out_dir, 'vocab.txt')}")
    print("DONE")


if __name__ == '__main__':
    flags.mark_flag_as_required('filenames')
    app.run(main)
