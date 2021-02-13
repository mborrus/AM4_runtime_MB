#!/bin/bash
#
#SBATCH --ntasks=1
#SBATCH --output=am4_wrapper_%j.out
#SBATCH --error=am4_wrapper_%j.err
#SBATCH --job-name=AM4_script_wrapper

module purge
module load anaconda/3

# TODO: add parameter input for working_dir

python am4_sample_run.py

