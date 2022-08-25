#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --qos=batch
#SBATCH --time=48:00:00
#SBATCH --mem-per-cpu=15G
#SBATCH --mail-user=stephen.antogiovanni@jax.org
#SBATCH --mail-type=END,FAIL

module load singularity

singularity exec marea_python.sif python ../scripts/xml2txt.py -x /projects/robinson-lab/wn2vec/data/sample_data/sample_xml -t /projects/robinson-lab/wn2vec/data/sample_data/sample_txt

