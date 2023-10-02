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


python  /scripts/filter_by_year.py  -i ../data/pubmed_cr  -o ../data/pubmed_filt.tsv  -y 2015