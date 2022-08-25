#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --qos=batch
#SBATCH --time=48:00:00
#SBATCH --mem-per-cpu=10G
#SBATCH --mail-user=stephen.antogiovanni@jax.org
#SBATCH --mail-type=END,FAIL

module load singularity

singularity exec marea_python.sif python /projects/robinson-lab/wn2vec/marea1.0/scripts/filter_abstracts.py -m -i /projects/robinson-lab/wn2vec/marea1.0/data/pubmed_txt -n /projects/robinson-lab/wn2vec/marea1.0/data/nltk_data \
			-o /projects/robinson-lab/wn2vec/marea1.0/data/pubmed_rel
