#!/bin/bash
#SBATCH --time=120:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=30
#SBATCH --gres gpu:1
#SBATCH --mem=100G
#SBATCH --mail-user=enock.niyonkuru@jax.org
#SBATCH --mail-type=END,FAIL
### SLURM HEADER


module load singularity

singularity exec --nv tensorflow.sif python ../scripts/word2vector.py  /projects/robinson-lab/wn2vec/current/data/pubmed_wn/100000pubmed_wn.tsv   metadata_vectors/100000_wn_vector.tsv metadata_vectors/100000_wn_metadata.tsv