#!/bin/bash
#SBATCH --qos=long
#SBATCH --time=200:00:00
#SBATCH --mem-per-cpu=500G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mail-user=enock.niyonkuru@jax.org
#SBATCH --mail-type=END,FAIL
### SLURM HEADER


module load singularity

singularity exec --nv tensorflow.sif python ../scripts/word2vector.py  /projects/robinson-lab/wn2vec/current/data/pubmed_filt/2000pubmed_filt.tsv   
metadata_vectors/2000_filt_sumner_vector.tsv metadata_vectors/2000_filt_sumner_metadata.tsv 100000
