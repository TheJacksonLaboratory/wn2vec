#!/bin/bash
#SBATCH --job-name=2007_wn2v
#SBATCH --output=2007_wn2vec.out
#SBATCH --qos=batch
#SBATCH --time=72:00:00
#SBATCH --mem-per-cpu=50G
#SBATCH --mail-user=enock.niyonkuru@jax.org
#SBATCH --mail-type=END,FAIL
### SLURM HEADER

module load python36
source myenv/bin/activate

python ../scripts/wntransformer.py /projects/robinson-lab/wn2vec/word2vec_tf/abst_filter/2007Pubmed_filt.tsv /projects/robinson-lab/wn2vec/word2vec_tf/abst_filter/2007_Wordnet.tsv
