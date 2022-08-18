#!/bin/bash
#SBATCH --job-name=filt_word2vector
#SBATCH --output=filt_wn2vector.out
#SBATCH --qos=batch
#SBATCH --time=72:00:00
#SBATCH --mem-per-cpu=500G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1 
#SBATCH --mail-user=enock.niyonkuru@jax.org
#SBATCH --mail-type=END,FAIL
### SLURM HEADER



source /projects/robinson-lab/wn2vec/word2vec_tf/envs/myenv/bin/activate

python /projects/robinson-lab/wn2vec/word2vec_tf/abst_filter/word2vector.py   /projects/robinson-lab/wn2vec/word2vec_tf/abst_filter/2007Pubmed_filt.tsv  2007Vector.tsv 2007Metadata.tsv
