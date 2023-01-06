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

python ../scripts/wntransformer.py /projects/robinson-lab/wn2vec/current/data/pubmed_filt/100pubmed_filt.tsv  /projects/robinson-lab/wn2vec/current/data/pubmed_wn/100pubmed_wn.tsv





