#!/bin/bash
#SBATCH --job-name=abst_filter
#SBATCH --output=2000newFilter.out
#SBATCH --qos=batch
#SBATCH --time=72:00:00
#SBATCH --mem-per-cpu=300G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1 
#SBATCH --mail-user=enock.niyonkuru@jax.org
#SBATCH --mail-type=END,FAIL
### SLURM HEADER



python /projects/robinson-lab/wn2vec/word2vec_tf/abst_filter/newFilter.py   /projects/robinson-lab/wn2vec/marea1.0/data/pubmed_txt  /projects/robinson-lab/wn2vec/wn2vec1.0/data/pubmed_cr/pubmed_cr.tsv 2007

