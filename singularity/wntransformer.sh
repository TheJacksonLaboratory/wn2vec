#!/bin/bash
#SBATCH --job-name=wntransformer
#SBATCH --output=wntrasformer.out
#SBATCH --qos=batch
#SBATCH --time=72:00:00
#SBATCH --mem-per-cpu=50G
#SBATCH --mail-user=enock.niyonkuru@jax.org
#SBATCH --mail-type=END,FAIL
### SLURM HEADER

source ../ myenv/bin/activate

python ../scripts/run_wn_replacement.py -i ../data/pubmed_filt/100pubmed_filt.tsv -o ../data/pubmed_wn/100pubmed_wn.tsv





