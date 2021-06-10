# AM4_runtime
Runtime scripts and analysis codes for NOAA-GFDL AM4. The general idea is to simplify and automate the runtime procedures for AM4; it is very much a work in progress.

That said, these tools can reduce a very complex AM4 workflow to a single, albeit long and with lots of input options, line of code. The `AM4_runner` tool (see below) will actually -- if necessary, download and unpack the principal input data, then configure the `input_nml` (manages layouts, processor counts, etc.), adjust resource requests, and submit a batch job to the scheduler. 

## Overview:
The workflows for running AM4 are... complex. These tools attempt to automate and simplify the process. The main components are:
- **AM4py.py**: Principal working code, where the heavy lifting happens. Most notably:
  - `class NML`: Class to handle the (re-)construction of `input.nml` files for new runs, restarts, etc. Tasks of interest include:
    - Setting `&coupler_nml` values for runtime, number of processors, etc., including adjusting input to get a valid total cpu count (ie, integer multiples of `6`.
    - Setting `layout` entries
    - Adjusting simulation datetime for restarts
  - **class AM4_batch_scripter**:
    - Uses `class NML()`, and other things too, to define a simulation parameters, and write `input.nml` a batch files for submission.
    - Includes some fixed inputs and also `**kwargs` into class scope, so unspecified parameters can also be handled. This includes interpreting any `slurm_{directive}` keyword inputs as SLURM directives. For example, instantiating the class with the parameter `slurm_mem-per-cpu=4g` will add the SLURM directive, `#SBATCH --mem-per-cpu=4g`, to the batch file.
- **AM4_runner.py**: Command line callable scripts to implement `AM4_batch_scripter()`. Some sample commands are provided in-code. As discussed above, this system is designed to accept and pass on `**kwargs`, so any input parameters to `AM4_batch_scripter()` that don't require special handling can be provided here as keywords and, in most cases, will make their way through the workflow. This is a work in progress.
## Notes and examples: 
Python, jupyter notebook, and shell scripts to (really) simplify AM4 runtime operations.
  - Includes code to fetch input data, if it is not present.
  - Processes input parameters to construct a working `input.nml` file (manages layouts, processor counts, etc.). Requirements for `input.nml` may evolove between versions, and (*surprise!*) AM4 can be very sensitive to this. For example, older versions accepted an entry, `cpus-per-node=`, and AM4 will not just ignore the entry; they will break instead.
  - Handles restart process (at least partially).
  - Can submit (or just run) a 1 cpu management job to fetch data (can take a while...), process NML, write batch, then submit much larger job.
  -  Example(s):
      - From a login node, `srun` a handler task to prepare and queue a big job.
    
    srun --partition=serc --constraint=CLASS:SH3_CBASE python am4_runner.py input_data_path=`cd ..;pwd`/AM4_run work_dir=`cd ..;pwd`/workdir nml_template=input_xanadu_2021.01.nml n_cpu_atmos=24 modules=${AM4_MODULE} hpc_config=sherlock3_base_singularity mpi_exec=srun am4_container_pathname=${AM4_CONTAINER_PATHNAME} am4_exe=${AM4_GFDL_EXE} slurm_partition=serc slurm_time=01:00:00 do_batch=False restart=False
      
  - Restrict to Sherlock 3.0 CBASE nodes
  - Define a (new) workdir
  - 24 `atmos` tasks
  - Use `srun` MPI syntax. 
  - Note that the `${AM4_MODULE}`, and other, values are defined in Sherlock LMOD module scripts. 
  - Submit the handler job to the `serc` partition and instruct it to submit the main job to `serc` as well.
  - NOT a RESTART! To restart (and continue) the simulation, run the same command, in the same `workdir`, with `restart=True` (on the TODO list is better automatic handling of restarts).
  - NOTE: All inputs like `slurm_{something}` are interpreted as SLURM directives, `--{something}`.
  - TODO: Add a similar feature for `nml_{something}` inputs



**NOTE:** One syntactical challenge can be module availability for different hardware and on different HPCs. For example, a call to `AM4_runner.py` might depend on an AM4 software module for variables like `$AM4_GFDL_EXE`, `$AM4_CONTAINER_NAME`, etc., and that module might not be available for some hardware (ie, modules are build out for Sherlock 2.0 and 3.0 (Stanford), but if you try to run the script from a Sherlock 1.0 node (either from a public partition or a login node -- which is not for computing), you might get some errors related to modules not being available.

## References:
- **AM4 source:** https://github.com/NOAA-GFDL/AM4
- **AM4 JSS Fork:** https://github.com/jeffersonscientific/AM4
  - NOTE: At this point, the main benefit of this fork is probalby some additional documentation. Other useful elements, like runtime or compile scripts have been moved off to separate repositories (see below).
- **AM4_compilers:** https://github.com/jeffersonscientific/AM4_compilers
  - Scripts and documentation to facilitate compilation. This may be a work in progress. This repo was formed after a successful compile script was... compiled for the Stanford Earth Mazama HPC, and the complexity thereof was fully appreciated. It is likely that there are not (yet) any push-button working scripts. 
  - Expect container-based solutions here as well.
- **FRE-NCtools**: https://github.com/NOAA-GFDL/FRE-NCtools
  - Some tools for working with GFDL models. Should include combining restart files, etc.
- **Namelist guide:** https://www.gfdl.noaa.gov/wp-content/uploads/2017/09/fv3_namelist_Feb2017.pdf

