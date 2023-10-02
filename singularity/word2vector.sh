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

singularity exec --nv tensorflow.sif python ../scripts/run_word2vec.py -i ../data/pubmed_filt.tsv -v filt_vector_file -m filt_metatada_file  
