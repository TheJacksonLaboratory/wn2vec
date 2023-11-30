#!/bin/bash
#SBATCH --job-name=wntransformer
#SBATCH --output=wntrasformer.out
#SBATCH --qos=batch
#SBATCH --time=72:00:00
#SBATCH --mem-per-cpu=50G
#SBATCH --mail-type=END,FAIL
### SLURM HEADER

source ../venv/bin/activate

python ../scripts/run_wn_replacement.py -i ../data/pubmed_filt.tsv -o ../data/pubmed_wn.tsv





