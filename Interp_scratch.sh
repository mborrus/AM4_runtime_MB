#!/bin/bash
#
#SBATCH --array=4-6
#SBATCH --output=./jobfiles/group_regrid%A-%a.out
#SBATCH --job-name=group_Am4
#SBATCH --time=2:00:00
#SBATCH -p serc
#SBATCH --verbose

module load netcdf/4.4.1.1
module load anaconda-cees-beta
#

cd /scratch/users/mborrus/AM4/SST_m8/${SLURM_ARRAY_TASK_ID}

mppnccombine -v -r 19790101.atmos_daily.tile1.nc
mppnccombine -v -r 19790101.atmos_daily.tile2.nc
mppnccombine -v -r 19790101.atmos_daily.tile3.nc
mppnccombine -v -r 19790101.atmos_daily.tile4.nc
mppnccombine -v -r 19790101.atmos_daily.tile5.nc
mppnccombine -v -r 19790101.atmos_daily.tile6.nc
#
fregrid --input_mosaic ./INPUT/C96_mosaic.nc --input_file 19790101.atmos_daily.nc --output_file dailyUTPS.nc --scalar_field ucomp,temp,precip,sphum --nthreads 6 --nlon 144 --nlat 90 --debug

cd /scratch/users/mborrus/AM4/SST_m12/${SLURM_ARRAY_TASK_ID}

mppnccombine -v -r 19790101.atmos_daily.tile1.nc
mppnccombine -v -r 19790101.atmos_daily.tile2.nc
mppnccombine -v -r 19790101.atmos_daily.tile3.nc
mppnccombine -v -r 19790101.atmos_daily.tile4.nc
mppnccombine -v -r 19790101.atmos_daily.tile5.nc
mppnccombine -v -r 19790101.atmos_daily.tile6.nc
#
fregrid --input_mosaic ./INPUT/C96_mosaic.nc --input_file 19790101.atmos_daily.nc --output_file dailyUTPS.nc --scalar_field ucomp,temp,precip,sphum --nthreads 6 --nlon 144 --nlat 90 --debug

cd /scratch/users/mborrus/AM4/SST_m16/${SLURM_ARRAY_TASK_ID}

mppnccombine -v -r 19790101.atmos_daily.tile1.nc
mppnccombine -v -r 19790101.atmos_daily.tile2.nc
mppnccombine -v -r 19790101.atmos_daily.tile3.nc
mppnccombine -v -r 19790101.atmos_daily.tile4.nc
mppnccombine -v -r 19790101.atmos_daily.tile5.nc
mppnccombine -v -r 19790101.atmos_daily.tile6.nc
#
fregrid --input_mosaic ./INPUT/C96_mosaic.nc --input_file 19790101.atmos_daily.nc --output_file dailyUTPS.nc --scalar_field ucomp,temp,precip,sphum --nthreads 6 --nlon 144 --nlat 90 --debug

cd /scratch/users/mborrus/AM4/SST_p8/${SLURM_ARRAY_TASK_ID}

mppnccombine -v -r 19790101.atmos_daily.tile1.nc
mppnccombine -v -r 19790101.atmos_daily.tile2.nc
mppnccombine -v -r 19790101.atmos_daily.tile3.nc
mppnccombine -v -r 19790101.atmos_daily.tile4.nc
mppnccombine -v -r 19790101.atmos_daily.tile5.nc
mppnccombine -v -r 19790101.atmos_daily.tile6.nc
#
fregrid --input_mosaic ./INPUT/C96_mosaic.nc --input_file 19790101.atmos_daily.nc --output_file dailyUTPS.nc --scalar_field ucomp,temp,precip,sphum --nthreads 6 --nlon 144 --nlat 90 --debug

cd /scratch/users/mborrus/AM4/SST_p12/${SLURM_ARRAY_TASK_ID}

mppnccombine -v -r 19790101.atmos_daily.tile1.nc
mppnccombine -v -r 19790101.atmos_daily.tile2.nc
mppnccombine -v -r 19790101.atmos_daily.tile3.nc
mppnccombine -v -r 19790101.atmos_daily.tile4.nc
mppnccombine -v -r 19790101.atmos_daily.tile5.nc
mppnccombine -v -r 19790101.atmos_daily.tile6.nc
#
fregrid --input_mosaic ./INPUT/C96_mosaic.nc --input_file 19790101.atmos_daily.nc --output_file dailyUTPS.nc --scalar_field ucomp,temp,precip,sphum --nthreads 6 --nlon 144 --nlat 90 --debug

cd /scratch/users/mborrus/AM4/SST_p16/${SLURM_ARRAY_TASK_ID}

mppnccombine -v -r 19790101.atmos_daily.tile1.nc
mppnccombine -v -r 19790101.atmos_daily.tile2.nc
mppnccombine -v -r 19790101.atmos_daily.tile3.nc
mppnccombine -v -r 19790101.atmos_daily.tile4.nc
mppnccombine -v -r 19790101.atmos_daily.tile5.nc
mppnccombine -v -r 19790101.atmos_daily.tile6.nc
#
fregrid --input_mosaic ./INPUT/C96_mosaic.nc --input_file 19790101.atmos_daily.nc --output_file dailyUTPS.nc --scalar_field ucomp,temp,precip,sphum --nthreads 6 --nlon 144 --nlat 90 --debug



