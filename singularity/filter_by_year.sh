#!/bin/bash
#SBATCH --job-name=filter_by_year
#SBATCH --output=filter_by_year.out
#SBATCH --qos=batch
#SBATCH --time=20:00:00
#SBATCH --mem-per-cpu=300G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1 
#SBATCH --mail-type=END,FAIL
### SLURM HEADER

source ../venv/bin/activate


python  ../scripts/filter_by_year.py  -i ../data/pubmed_cr  -o ../data/pubmed_filt.tsv  -y 2010