#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --qos=batch
#SBATCH --time=23:00:00
#SBATCH --mem-per-cpu=10G
#SBATCH --mail-user=stephen.antogiovanni@jax.org
#SBATCH --mail-type=END,FAIL

module load singularity

singularity exec marea_python.sif python ../scripts/pubtate.py -i /projects/robinson-lab/wn2vec/data/pubtator_offset
