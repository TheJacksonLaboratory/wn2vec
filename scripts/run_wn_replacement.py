import os
import sys
import argparse
import numpy as np

sys.path.insert(0, os.path.abspath('../src/'))
from wn2vec import WordNetTransformer

parser = argparse.ArgumentParser()
parser.add_argument('-i', type=str, required=True, help='path to filtered marea_file')
parser.add_argument('-o', type=str, required=True, help='path to of output_file')
parser.add_argument('--threshold', type=float, help="threshold (0-1, default median word threshold)")
args = parser.parse_args()

marea_input_file = args.i
output_file = args.o
threshold = args.threshold
if not os.path.isfile(marea_input_file):
    raise FileNotFoundError(f"Could not find marea [intput] file at {marea_input_file}")

transformer = WordNetTransformer(marea_file=marea_input_file, percentile=threshold)
threshold = transformer.get_threshold()
print(f'Threshold: {threshold} at percentile {100 * threshold}')
replaced_words = transformer.get_replaced_word_count()
print("Number of replaced words: ", replaced_words)
transformer.transform_and_write(output_file=output_file)


"""
example: 
> python ../scripts/run_wn_replacement.py -i ../data/pubmed_filt/100pubmed_filt.tsv -o ../data/pubmed_wn/100pubmed_wn.tsv --threshold 0.3
"""
