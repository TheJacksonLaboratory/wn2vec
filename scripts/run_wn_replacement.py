import os
import sys
import argparse
import logging
import datetime
import time
sys.path.insert(0, os.path.abspath('../src/'))
from wn2vec import WordNetTransformer


today_date = datetime.date.today().strftime("%b_%d_%Y")
logname = f"wn2vec_{today_date}.log"
logging.basicConfig(level=logging.INFO, filename=logname, filemode='w', datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# record start time
start_time = time.time()

parser = argparse.ArgumentParser()
parser.add_argument('-i', type=str, required=True, help='path to filtered marea_file')
parser.add_argument('-o', type=str, required=True, help='path to of output_file')
parser.add_argument('--threshold', type=int, help="threshold (0 for mean, 1<threshold <100  for percentile, above 100 for custom threshold)")
args = parser.parse_args()

marea_input_file = args.i
output_file = args.o
threshold = args.threshold
logging.info(f"wordnet replacement infile: {marea_input_file}; outfile: {output_file}; threshold: {threshold}")
if not os.path.isfile(marea_input_file):
    raise FileNotFoundError(f"Could not find marea [intput] file at {marea_input_file}")
if threshold < 0 :
    raise ValueError(f"--threshold argument must be an integer above 0 1  (default 0), but was {threshold}")

transformer = WordNetTransformer(marea_file=marea_input_file, percentile=threshold)
threshold = transformer.get_threshold()
print(f'Threshold: {threshold} ')
replaced_words = transformer.get_replaced_word_count()
total_words = transformer.get_total_word_count()
print(f"Number of replaced words: {replaced_words} of {total_words}")
logging.info(f"Number of replaced words: {replaced_words} of {total_words}")
transformer.transform_and_write(output_file=output_file)


"""
example: 
> python ../scripts/run_wn_replacement.py -i ../data/pubmed_filt/100pubmed_filt.tsv -o ../data/pubmed_wn/100pubmed_wn.tsv --threshold 0
"""
