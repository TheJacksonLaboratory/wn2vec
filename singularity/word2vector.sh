#!/bin/bash
#SBATCH --job-name=word2vec
#SBATCH --output=word2vec.out
#SBATCH --qos=batch
#SBATCH --time=72:00:00
#SBATCH --mem-per-cpu=50G
#SBATCH --mail-type=END,FAIL
### SLURM HEADER

source venv/bin/activate

python ../scripts/run_word2vec.py -i ../data/pubmed_wn.tsv -v wn_vector -m wn_metadata