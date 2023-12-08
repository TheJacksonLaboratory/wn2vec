import os
import sys
import argparse
import logging
import datetime
import time
import nltk

"""
The following code downloads the NLTK wordnet resource. The main command is simply
nltk.download('wordnet')
However, we have noted that on some systems this leads to a certificate verify failed error.
The following solution to this problem was found on StackOverflow 38916452.
"""
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('wordnet')



sys.path.insert(0, os.path.abspath("../src/"))
from wn2vec import WordNetTransformer


today_date = datetime.date.today().strftime("%b_%d_%Y")
logname = f"wn2vec_{today_date}.log"
logging.basicConfig(
    level=logging.INFO,
    filename=logname,
    filemode="w",
    datefmt="%Y-%m-%d %H:%M:%S",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# record start time
start_time = time.time()

parser = argparse.ArgumentParser()
parser.add_argument("-i", type=str, required=True, help="path to filtered marea_file")
parser.add_argument("-o", type=str, required=True, help="path to of output_file")
parser.add_argument(
    "-t",
    "--threshold",
    type=float,
    default=1.0,
    help="threshold (the a number you wish to multiply to the mean of the unique word's frequency and the threshold)",
)

args = parser.parse_args()

marea_input_file = args.i
output_file = args.o
threshold_factor = args.threshold
logging.info(f"wordnet replacement infile: {marea_input_file}; outfile: {output_file}; threshold: {threshold_factor}")
if not os.path.isfile(marea_input_file):
    raise FileNotFoundError(f"Could not find marea [intput] file at {marea_input_file}")
if threshold_factor <= 0:
    raise ValueError(f"--threshold argument must be a float above 0 (default 1), but was {threshold_factor}")


transformer = WordNetTransformer(marea_file=marea_input_file, threshold_multiple=threshold_factor)
threshold = transformer.get_threshold()

replaced_words = transformer.get_replaced_word_count()
total_words = transformer.get_total_word_count()
transformer.transform_and_write(output_file=output_file)

transformer.output_abstract_only()

print(f"[INFO] running run_wn_replacement.py with input file {marea_input_file}.")
print(f"[INFO] outputput file {output_file}.")
print(f"[INFO] threshold_factor {threshold_factor}.")
print(f"[INFO] replacement_threshold {threshold}.")
print(f"[INFO] Number of replaced words: {replaced_words} of {total_words}")

logging.info(f"[INFO] Number of replaced words: {replaced_words} of {total_words}")


"""
example:
> python scripts/run_wn_replacement.py -i dump/pubmed_cr.tsv -o dump/pubmed_cr_wn.tsv --threshold 1
"""
