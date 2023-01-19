import io
import re
import string
import tqdm
import os
import logging
import datetime
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
import argparse


class Word2VecRunner:

    def __init__(self, input_file, vector, metadata, vocab_size, 
                        embedding_dim, sequence_length, window_size, 
                             BATCH_SIZE , BUFFER_SIZE, num_ns, SEED ):
        #self._input = None
        self._input_file = input_file
        self._vector = vector
        self._metadata = metadata
        self._vocab_size = vocab_size
        self._embedding_dim = embedding_dim
        self._sequence_length = sequence_length
        self._window_size = window_size
        self._BATCH_SIZE = BATCH_SIZE
        self._BUFFER_SIZE = BUFFER_SIZE
        self._num_ns = num_ns
        self._SEED= SEED
        self._lines = []
    
    # Load the TensorBoard notebook extension
    #%load_ext tensorboard


    AUTOTUNE = tf.data.experimental.AUTOTUNE


    #Compile all the steps described above into a function that can be called on a list of vectorized sentences obtained from any text dataset. Notice that the sampling table is built before sampling skip-gram word pairs. You will 
     #use this function in the later sections.

    # Generates skip-gram pairs with negative sampling for a list of sequences
    # (int-encoded sentences) based on window size, number of negative samples
    # and vocabulary size.
    def generate_training_data(sequences, window_size, num_ns, vocab_size, seed):
        # Elements of each training example are appended to these lists.
        targets, contexts, labels = [], [], []

        # Build the sampling table for `vocab_size` tokens.
        sampling_table = tf.keras.preprocessing.sequence.make_sampling_table(vocab_size)

        # Iterate over all sequences (sentences) in the dataset.
        for sequence in tqdm.tqdm(sequences):

            # Generate positive skip-gram pairs for a sequence (sentence).
            positive_skip_grams, _ = tf.keras.preprocessing.sequence.skipgrams(
                sequence,
                vocabulary_size=vocab_size,
                sampling_table=sampling_table,
                window_size=window_size,
                negative_samples=0)

            # Iterate over each positive skip-gram pair to produce training examples
            # with a positive context word and negative samples.
            for target_word, context_word in positive_skip_grams:
                context_class = tf.expand_dims(
                    tf.constant([context_word], dtype="int64"), 1)
                negative_sampling_candidates, _, _ = tf.random.log_uniform_candidate_sampler(
                    true_classes=context_class,
                    num_true=1,
                    num_sampled=num_ns,
                    unique=True,
                    range_max=vocab_size,
                    seed=seed,
                    name="negative_sampling")

                # Build context and label vectors (for one target word)
                negative_sampling_candidates = tf.expand_dims(
                    negative_sampling_candidates, 1)

                context = tf.concat([context_class, negative_sampling_candidates], 0)
                label = tf.constant([1] + [0]*num_ns, dtype="int64")

                # Append each element from the training example to global lists.
                targets.append(target_word)
                contexts.append(context)
                labels.append(label)

            return targets, contexts, labels

    
    def input_file(self, verbose=False):
        """
        opening input file from path and  create text_ds
        """
        input_file = self._input_file
        if not os.path.isfile(input_file):
            raise FileNotFoundError(f"Could not find input file at {input_file}")
        with open(input_file) as f:
            for line in f:
                columns = line.split('\t')
                if len(columns) != 3:
                    raise ValueError(f'Malformed marea line: {line}')
                abstract = columns[2]  #columns[0]: pmid,  columns[1] year, columns[2] abstract text
                self._lines.append(abstract)
        if verbose:
            for line in self._lines[:20]:
                print(line)
        text_ds = tf.data.TextLineDataset(input_file).filter(lambda x: tf.cast(tf.strings.length(x), bool))
        
        return text_ds



    # Now, create a custom standardization function to lowercase the text and
    # remove punctuation.
    def custom_standardization(input_data):
        lowercase = tf.strings.lower(input_data)
        return tf.strings.regex_replace(lowercase,
                                        '[%s]' % re.escape(string.punctuation), '')



    # Use the `TextVectorization` layer to normalize, split, and map strings to
    # integers. Set the `output_sequence_length` length to pad all samples to the
    # same length.
   
    def get_vecotrized_layer(self):
        input_file = self._input_file
        AUTOTUNE = tf.data.experimental.AUTOTUNE

        vectorize_layer = tf.keras.layers.TextVectorization(
            #standardize=self.custom_standardization,
            max_tokens=self._vocab_size,
            output_mode='int',
            output_sequence_length=self._sequence_length)

        text_ds = self.input_file(self)

        vectorize_layer.adapt(text_ds.batch(1024))

        
        # Save the created vocabulary for reference.
        inverse_vocab = vectorize_layer.get_vocabulary()
        print(inverse_vocab[:20])
         
        
        return vectorize_layer, text_ds, inverse_vocab,

    def get_sequences(vectorize_layer, text_ds, inverse_vocab):
        AUTOTUNE = tf.data.experimental.AUTOTUNE
        # Vectorize the data in text_ds.
        text_vector_ds = text_ds.batch(1024).prefetch(AUTOTUNE).map(vectorize_layer).unbatch()

        #Obtain sequences from the dataset
        sequences = list(text_vector_ds.as_numpy_iterator())
        print(len(sequences))


        for seq in sequences[:5]:
            print(f"{seq} => {[inverse_vocab[i] for i in seq]}")

        #Generate training examples from sequences
        targets, contexts, labels = self.generate_training_data(sequences=sequences, 
                                                                window_size=self._window_size, 
                                                                num_ns=self._num_ns,
                                                                vocab_size=self._vocab_size, 
                                                                seed=self._SEED) 




        targets = np.array(targets)
        contexts = np.array(contexts)[:,:,0]
        labels = np.array(labels)

        print('\n')
        print(f"targets.shape: {targets.shape}")
        print(f"contexts.shape: {contexts.shape}")
        print(f"labels.shape: {labels.shape}")

        return targets, contexts, labels

    #Configure the dataset for performance
    def get_dataset(self, targets, contexts, labels):
        AUTOTUNE = tf.data.experimental.AUTOTUNE

        dataset = tf.data.Dataset.from_tensor_slices(((targets, contexts), labels))
        dataset = dataset.shuffle(self._BUFFER_SIZE).batch(self._BATCH_SIZE, drop_remainder=True)
        print(dataset)


        dataset = dataset.cache().prefetch(buffer_size=AUTOTUNE)
        print(dataset)

        return dataset


    class Word2Vec(tf.keras.Model):
        def __init__(self, vocab_size, embedding_dim):
            super(Word2Vec, self).__init__()
            self.target_embedding = layers.Embedding(vocab_size,
                                            embedding_dim,
                                            input_length=1,
                                            name="w2v_embedding")
            self.context_embedding = layers.Embedding(vocab_size,
                                            embedding_dim,
                                            input_length=num_ns+1)

        def call(self, pair):
            target, context = pair
            # target: (batch, dummy?)  # The dummy axis doesn't exist in TF2.7+
            # context: (batch, context)
            if len(target.shape) == 2:
                target = tf.squeeze(target, axis=1)
            # target: (batch,)
            word_emb = self.target_embedding(target)
            # word_emb: (batch, embed)
            context_emb = self.context_embedding(context)
            # context_emb: (batch, context, embed)
            dots = tf.einsum('be,bce->bc', word_emb, context_emb)
            # dots: (batch, context)
            return dots

    def custom_loss(x_logit, y_true):
        return tf.nn.sigmoid_cross_entropy_with_logits(logits=x_logit, labels=y_true)

    def get_embedding(self,dataset, vectorize_layer ): 
       
        word2vec = self.Word2Vec(self._vocab_size, self._embedding_dim)
        word2vec.compile(optimizer='adam',
                        loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),
                        metrics=['accuracy'])

        tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir="logs")
        history_all = word2vec.fit(dataset, epochs=10, callbacks=[tensorboard_callback])


        #docs_infra: no_execute
        #%tensorboard --logdir logs


        weights = word2vec.get_layer('w2v_embedding').get_weights()[0]
        vocab = vectorize_layer.get_vocabulary()

        vector_file = self._vector
        metadata_file = self._metadata
        out_v = io.open(vector_file, 'w', encoding='utf-8')
        out_m = io.open(metadata_file, 'w', encoding='utf-8')

        for index, word in enumerate(vocab):
            if index == 0:
                continue  # skip 0, it's padding.
        vec = weights[index]
        out_v.write('\t'.join([str(x) for x in vec]) + "\n")
        out_m.write(word + "\n")
        out_v.close()
        out_m.close()


        try:
            from google.colab import files
            files.download(vector_file)
            files.download(metadata_file)
        except Exception:
            pass

