
import numpy
import scipy
import matplotlib as mpl
import matplotlib.dates as mpd
import pylab as plt
import datetime
import os,sys
#
import subprocess
import requests
import tarfile
import shutil
#
import urllib
import contextlib
# import urllib.request as request
# from contextlib import closing
#
import re
#
import json
#
# we'll probably need this eventually, but maybe we can try to make it optional, if it's going to be a problem...
#import netCDF4
#
#
class NML(dict):
    #
    def __init__(self):
        self.__dict__.update({ky:vl for ky,vl in locals().items() if not ky in ('self', '__class__')})
    
    #
    def assign(self, ky1, ky2, val):
        # a "safe" assignment operator. If the keys do not exist, fail and raise an exception.
        if ky1 in self.keys() and ky2 in self[ky1].keys():
            self[ky1][ky2] = val
            #
            return True
        else:
            err_str = '{} not in self[{}].keys()'.format(ky2, ky1)
            if not(ky1) in self.keys():
                err_str = "{} not in self.keys()"
            #
            raise NameError(err_str)
            return False
    #
    def nml_to_json(self, nml_in=None, json_out=None):
        '''
        # convert nml to dict; save dict as class member; if json_out is not None,
        # export json to json_out
        #
        # NOTE: The format for .nml does not appear to be very strictly defined. Basically, it is not
        #. well defined if key-value pairs are separated by CRLF ('\n') or comma ',' -- oh, and also commas
        #. are allowed (in some cases) withink values. So this might be a work in progress, to be able
        #. to generally define k-v pairs. Right now, its success rests a little bit on, "please, all that
        #. is holy, let them not allow this or that..."
        #
        # @nml_in: filenname of input nml
        # @json_out: filename of output json file.
        #.
        '''
        #
        if nml_in is None:
            nml_in = self.nml
        #
        #nml_dict = {}
        group_name = ''
        #k_group = 0
        #
        values_out = {}
        ky = ''
        
        with open(nml_in) as fin:
            for rw in fin:
                rw = rw.strip()
                #
                # TODO: maye we should retain comments? if so, we'll need to switch the nested
                #. structure to a list (-like), instead of a dict., to allow for multiple commented-out
                #  entries.
                #
                # for a mid-line comment:
                rw = rw.split('!')[0]
                #
                if len(rw)==0 or rw[0] in ['!', '\n']:
                    continue
                #
                if rw[0]=='/':
                    # end of section
                    if not group_name.strip() == '':
                        self[group_name] = values_out
                #
                if rw[0]=='&':
                    # new group:
                    #if not group_name == '':
                    #    self[group_name] = values_out
                    #    #nml_dict[group_name]=values_out
                    #
                    group_name = rw[1:].strip()
                    values_out = {}
                    ky=''
                    val=''
                    #if not group_name in nml_dict.keys():
                    #    nml_dict[group_name]={}
                    continue
                    #
                
                #
                #print('** ', rw)
                #
                # TODO: this logic is almost right, and will probably work most of the time, but
                #. it might be better to be more robust about allowing multi-line entries. Note
                #. this will not work properly for a multi-entry line that end in a multi-line entry.
                if rw.startswith('/'):
                    values_out[ky]=val.strip()
                    continue
                #
                ky_vl = rw.split('=')
                if len(ky_vl) == 1:
                    #print('*** debug: ', val, ky_vl)
                    #val = val + ky_vl[0]
                    val = '{}\n{}'.format(val, rw)
                    continue
                elif len(ky_vl) == 2:
                    if not ky=='':
                        values_out[ky]=val.strip()
                    ky,val = [s.strip() for s in ky_vl]
                elif len(ky_vl) > 2:
                    # there are multiple entries, presumably separated by commas?? so
                    # key=val,key=val,key=val...
                    #print('** DEBUG: ', [s.strip() for s in re.split('=|,', rw) if not s.strip()==''])
                    values_out.update(dict(numpy.reshape([s.strip()
                                        for s in re.split('=|,', rw) if not s.strip()==''], (-1,2))))
                
            #
        #
        #self.nml_dict=nml_dict
        #self.update(nml_dict)
        #
        if not json_out is None:
            with open(json_out, 'w') as fout:
                #json.dump(nml_dict, fout)
                # can we just dump self?
                json.dump(self, fout)
                #json.dump({ky:vl for ky,vl in self.items()})
            #
        #
        return None
        #return nml_dict
    #
    
    #
    def json_to_nml(self, nml_out='input.nml', json_in=None, indent=None, file_mode='w'):
        '''
        # convert json or dict to an nml. export to nml_out.
        # TODO: continue to evaluate how lists, tuples, etc. are encoundered and handled. For example,
        #  we want output to be like, format = 6,8 , not format = [6,8]. so far, i don't see any "[]"
        #. characters in .nml files, so we can probably just get rid of them, but it might be smarter
        #. to just recognize when we have a list type... or to enforce that all values are saved internally
        #  as strings... The latter may become necessary, since there does not appear to be a good standard
        #. for comma, space, etc. separating values (or fields).
        '''
        #
        if json_in is None:
            json_in = self
        #
        if indent is None:
            indent = 4*chr(32)
            #
        #
        if isinstance(json_in, str):
            with open(json_in, 'r') as fin:
                json_in = json.load(fin)
            #
        #
        with open(nml_out, file_mode) as fout:
            for group,entries in json_in.items():
                fout.write('&{}\n'.format(group))
                #
                for entry,val in entries.items():
                    if entry.strip() == '':
                        continue
                    fout.write('{}{} = {}\n'.format(indent, entry, val ))
                fout.write('/\n\n')
                
                #
            #
            
                    
class NML_from_nml(NML):
    def __init__(self, input_nml, output=None):
        #
        nml_out=output
        super(NML_from_nml,self).__init__()
        self.__dict__.update({ky:vl for ky,vl in locals().items() if not ky in ('self', '__class__')})
        #
        # is this useful?
        #with open(input_nml) as fin:
        #    self.nml = fin.read()
        #
        self.nml_to_json(input_nml, json_out=output)
        
    #
class NML_from_json(NML):
    def __init__(self, input_json, output=None):
        #
        json_out = output
        super(NML_from_json,self).__init__()
        self.__dict__.update({ky:vl for ky,vl in locals().items() if not ky in ('self', '__class__')})
        #
        with open(input_json) as fin:
            #self.nml_dict = json.load(fin)
            self.update(json.load(fin))
        #
        if not output is None:
            self.nml = self.json_to_nml(self.nml_json, output)
        #
    #
#
#
class AM4_batch_scripter(object):
    mpi_execs = {'mpirun':{'exec': 'mpirun', 'ntasks':'-np ', 'cpu_per_task':'--cpus-per-proc '},
                 'srun':{'exec':'srun', 'ntasks':'--ntasks=', 'cpu_per_task':'--cpus-per-task='}}
    #
    HPC_configs={
    'mazama_hpc':{'cpus_per_node':24, 'cpu_slots':2, 'cpu_make':'intel', 'cpu_gen':'haswell',
                  'mem_per_node':64, 'modules':['intel/19', 'openmpi_3/', 'gfdl_am4/']},
    'sherlock2_hpc':{'cpus_per_node':24, 'cpu_slots':2, 'cpu_make':'intel', 'cpu_gen':'skylake',
                     'mem_per_node':192, 'slurm_constraint':'CPU_GEN:SKX'},
    'sherlock2_hpc2':{'cpus_per_node':24, 'cpu_slots':2, 'cpu_make':'intel', 'cpu_gen':'skylake',
                      'mem_per_node':384, 'slurm_constraint':'CPU_GEN:SKX'},
    'sherlock3_base':{'cpus_per_node':32, 'cpu_slots':1, 'cpu_make':'AMD', 'cpu_gen':'EPYC_7502',
                      'mem_per_node':256, 'slurm_constraint':'CLASS:SH3_CBASE', 'modules':['am4/singularity_gfdl/2021.1.0']},
    'sherlock3_base_singularity':{'cpus_per_node':32, 'cpu_slots':1, 'cpu_make':'AMD', 'cpu_gen':'EPYC_7502',
                      'mem_per_node':256, 'slurm_constraint':'CLASS:SH3_CBASE', 'modules':['am4/singularity_gfdl/2021.1.0']},
    'sherlock3_perf':{'cpus_per_node':128, 'cpu_slots':2, 'cpu_make':'AMD', 'cpu_gen':'EPYC_7742',
                      'mem_per_node':1024, 'slurm_constraint':'CLASS:SH3_CPERF'},
    'unknown':{'cpus_per_node':24, 'cpu_slots':2, 'cpu_make':'unknown', 'cpu_gen':'unknown',
                  'mem_per_node':64}
    }
    #
    def __init__(self, batch_out=None, work_dir=None, mpi_exec='mpirun',
                 input_data_path=None, input_data_tar=None, input_data_url=None,
                 nml_template='nml_input_template.nml', modules=None,
                diag_table_src='diag_table_v101', field_table_src='field_table_v101', data_table_src='data_table_v101',
                 force_copy_input=0, do_tar=0, hpc_config='mazama_hpc',
                 npes_atmos=48, nthreads_atmos=1, npes_ocean=0, job_name='AM4_run', sbatch_options_str='', current_date='1979,1,1,0,0,0',
                 slurm_partition=None, slurm_time=None,
                 copy_timeout=6000, verbose=0):
        '''
        # parameters? input data file?
        #
        # not sure what this looks like yet, but... This script/class will be called by a wrapper
        #.  script. This process will constitute a step in a larer script (ie, each ~2 hour run in a
        #. twohour queue process).
        #. script
        # 1) review, set up, etc. the working directory
        # 2) Are the input data there?
        # 3) if not, are the input data availble?
        # 4) if not, is the tar available? if not, get it; then open, then copy.
        # 5) evaluate the input/output data. Have we achieved our objectives
        #.  (which we've not yet defined -- runtime, etc.)? Define restart as necessary
        #.   (*** though actually, i guess this will be done by the calling script; this script will
        #.    just receive instructions).
        # 6) copy diag_table nd create input.nml
        # 7) execute MPI command
        #
        # for Mazama (note: the future will probabl hold am4.json files like, am4_mazama.json,
        #. am4_sherlock3.json, etc.)
        #
        # current and local root path(s):
        #
        # @n_tasks: I believe n_tasks needs to be an integer multiple of 6, ie 6 faces to a cube.
        # (so any threads work on a single task/cube face). For now, let's stick with that, particularly
        #. since we'll probably usually use nthreads=1... because, though it would nominally be faster
        #  to do something like --ntasks=n_nodes --cpus-per-task=cpus_per_node , I think MOM6 still
        #  does not work with OpenMP.
        #.
        '''
        #        #
        if isinstance(hpc_config, str):
            if hpc_config.endswith('.json'):
                hpc_config=json.load(hpc_config)
            else:
                hpc_config=self.HPC_configs[hpc_config]
            #
        # else hpc_config better be a dict of HW configs.
        #
        #
        if npes_atmos%6 != 0:
            npes_atmos += npes_atmos%6
            print('*** WARNING: npes_atmos must be a multiple of 6. Increasing tasks -> {} so that npes_atmos%6=0'.format(npes_atmosn_tasks))
        #
        # same for ocean? npes_ocean%6==0 ??? right now, we're not doing ocean, so...
        # TODO: we can also check to see that we don't ask for more threads than we can get, but since
        #. these will almost always be single-threaded, let's hold off...
        #
        cwd = os.getcwd()
        root_path = os.path.dirname(os.path.abspath(cwd))
        default_data_path = os.path.join(root_path, 'AM4_data', 'AM4_run')
        #
        if input_data_path is None:
            input_data_path = default_data_path
        input_data_tar = (input_data_tar or os.path.join(os.path.dirname(input_data_path), 'AM4_run.tar.gz') )
        if work_dir is None:
            work_dir = os.path.join(cwd, 'workdir')
        if batch_out is None:
            batch_out = os.path.join(work_dir, 'am4_batch.sh')
        #
        input_data_url = input_data_url or 'ftp://nomads.gfdl.noaa.gov/users/Ming.Zhao/AM4Documentation/GFDL-AM4.0/inputData/AM4_run.tar.gz'
        # TODO: also download check validations:
        # wget ftp://nomads.gfdl.noaa.gov/users/Ming.Zhao/AM4Documentation/GFDL-AM4.0/inputData/AM4_run.tar.gz.sha256
        # wget ftp://nomads.gfdl.noaa.gov/users/Ming.Zhao/AM4Documentation/GFDL-AM4.0/inputData/AM4_run.tar.gz.sig
        # sha256sum -c AM4_run.tar.gz.sha256
        #gpg --verify AM4_run.tar.gz.sig
        #
        # TODO: How to handle the nml file? here as part of the batch, or in a wrapper that handles both?
        #. or some combination
        #
        if modules is None:
            modules = hpc_config.get('modules', ['intel/19', 'openmpi_3/', 'gfdl_am4/'])
            #modules = ['intel/19', 'openmpi_3/', 'gfdl_am4/']
        if isinstance(modules, str):
            modules = modules.split(',')
        #
        if input_data_path is None:
            input_data_path = '{}/data/AM4_run'.format(root_path)
        input_data_tar = input_data_tar or os.path.join(root_path, 'data', 'AM4_run.tar.gz')
        #
        if isinstance(mpi_exec, dict):
            ky,vl = mpi_exec.items()[0]
            #
            # multi-category dict?
            if isinstance(vl, dict):
                self.mpi_execs.update(mpi_exec)
                mpi_exec = vl
            else:
                # single-entry dict; add this full mpi_exec entry to mpi_execs
                ky = mpi_exec['exec']
                self.mpi_execs[ky] = mpi_exec.copy()
            #
        else:
            mpi_exec = self.mpi_execs[mpi_exec]
        #
        #
        # download, untar, copy input data:
        
        #
        self.__dict__.update({ky:vl for ky,vl in locals().items() if not ky in ('self', '__class__')})
        #
        layout_1 = get_AM4_layouts(self.ntasks_total)[0]
        layout_io_1 = get_AM4_io_layouts(layout_1)[0]
        layout_2 = get_AM4_layouts(self.ntasks_total/6)[0]
        layout_io_2 = get_AM4_io_layouts(layout_2)[0]
        self.__dict__.update({ky:vl for ky,vl in locals().items() if not ky in self.__dict__.keys()})
        
        # write an input.nml file and copy other files?
        #
        #
        # write a batch file:
        # self.write_batch_script()
    #
    # NOTE: these nvcpu calculators will likely not work well for not-simple configurations,
    #. but again, I think most of these jobs will be single-threaded.
    @property
    def cpus_total(self):
        # NOTE: this is cpus, but not tasks. it should tell us how many cores we'll be expecting,
        #. but probably is not something submitted to SLURM unless there are constraints on nodes.
        return self.npes_atmos * self.nthreads_atmos + self.npes_ocean
    @property
    def ntasks_total(self):
        return self.npes_atmos + self.npes_ocean
    @property
    def n_tasks(self):
        return self.ntasks_total
    @property
    def n_threads(self):
        return self.nthreads_atmos
    #
    #def layout_to_str(self, layout):
    #    return '{},{}'.format(*layout)
    #
    @property
    def default_nml_reconfig(self):
        # TODO: check these. if we're actually using ocean... is ocean supposet to be n*x=npes_ocean?
        #.  npes_total???
#         return {'coupler_nml':{'atmos_npes':self.npes_atmos, 'atmos_nthreads':self.nthreads_atmos,
#                               'ocean_npes':self.npes_ocean},
#                'fv_core_nml':{'layout':self.layout_2, 'io_layout':self.layout_io_2},
#                'ice_model_nml':{'layout':self.layout_1, 'io_layout':self.layout_io_1},
#                'land_model_nml':{'layout':self.layout_2, 'io_layout':self.layout_io_2},
#                'ocean_model_nml':{'layout':self.layout_1, 'io_layout':self.layout_io_1},
#                }
        return {'coupler_nml':{'atmos_npes':self.npes_atmos, 'atmos_nthreads':self.nthreads_atmos,
                              'ocean_npes':self.npes_ocean, 'ncores_per_node':self.hpc_config['cpus_per_node'],
                              'current_date':self.current_date},
               'fv_core_nml':{'layout':'{},{}'.format(*self.layout_2),
                              'io_layout':'{},{}'.format(*self.layout_io_2)},
               'ice_model_nml':{'layout':'{},{}'.format(*self.layout_1),
                              'io_layout':'{},{}'.format(*self.layout_io_1)},
               'land_model_nml':{'layout':'{},{}'.format(*self.layout_2),
                              'io_layout':'{},{}'.format(*self.layout_io_2)},
               'ocean_model_nml':{'layout':'{},{}'.format(*self.layout_1),
                              'io_layout':'{},{}'.format(*self.layout_io_1)},
                'atmos_model_nml':{'nxblocks':1, 'nyblocks':self.nthreads_atmos}
               }
    #
    def get_empty_workdir(self, work_dir=None, diag_table_src=None, field_table_src=None, data_table_src=None,
            force_copy=0, verbose=None):
        '''
        # TODO: How do we do restarts, run with different resolution configs, etc.?
        # start here by building a bare bones work_dir, with just the basic input files and an empty INPUT.
        # we will work a little later to tune the workflows for default start, blank start, and restarts.
        # TODO: maybe go through known defaults or templates to create empty input files? INPUT/MOM_input can (I think)
        #  be just a blank file, but some of the others are .nc files, and presumably require structure. We do have a NetCDF
        #  format copier someplace (dycore maybe?).
        #
        # Inputs:
        # @work_dir: working directory (files will be copied to this path; sim will be run in this path.
        # @diag_table_src, field_table_src, data_table_src: source files for {those}_src input files. By default,
        #   we'll keep local copies like field_table_v101.
        # @force_copy: boolean to force copying/over-writing datta_table, field_table, diag_table, and maybe input.nml
        #   Nominally, we maybe have to rewrite input.nml every time anyway -- at least in priciple, even if only to reproduce
        #  it 1:1. We'll be working out those workflows as we go...
        #  *** !!! ***
        #  NOTE: For now, let's ignore input.nml here; we'll just keep that as a separate process (for now anyway).
        '''
        #
        # TODO: consider NOT allowing a local workdir by using the None-like syntax,
        #  work_dir = work_dir or self.work_dir
        #  which will trigger on None or empty (last time I checked anyway).
        if work_dir is None:
            work_dir = self.work_dir
        #
        verbose = verbose or self.verbose
        verbose = verbose or False
        #
        if diag_table_src is None:
            diag_table_src = self.diag_table_src
        if field_table_src is None:
            field_table_src = self.field_table_src
        if data_table_src is None:
            data_table_src = self.data_table_src
        #
        # create workdir + RESTART and INPUT subdirs.
        for pth in ('INPUT', 'RESTART'):
            if not os.path.isdir(os.path.join(work_dir, pth)):
                os.makedirs(os.path.join(work_dir, pth))
        #
        #diag_path = os.path.join(work_dir, 'diag_table')
        #if not os.path.isfile(diag_path) or force_copy:
        #    shutil.copy(diag_table_src, os.path.join(work_dir, 'diag_table'))
        #
        # copy components into workdir:
        for src,dst in [(field_table_src, 'field_table'), (data_table_src, 'data_table'), (diag_table_src, 'diag_table')]:
            pth_dst = os.path.join(work_dir, dst)
            if not os.path.isfile(pth_dst) or force_copy:
                shutil.copy(src, pth_dst)
                if verbose:
                    print('*** VERBOSE: Created input file: {} from source: {}'.format(pth_dst, src))
        
    def get_restart_current_date(self, work_dir=None, default_restart_date=None):
        '''
        # get current_date value for restart from RESTART/coupler.res
        # TODO: allow better granualarity than just work_day? apply some logic to allow full path to coupler.res, but
        #  smart enough to take just work_dir? ??
        '''
        if work_dir is None:
            work_dir = self.work_dir
        default_restart_date = default_restart_date or self.current_date
        #
        # default value:
        #restart_date = '1979,1,1,0,0,0'
        if os.path.isfile(os.path.join(work_dir, 'RESTART', 'coupler.res')):
            coupler_path = os.path.join(work_dir, 'RESTART', 'coupler.res')
        elif os.path.isfile(os.path.join(work_dir, 'INPUT', 'coupler.res')):
            coupler_path = os.path.join(work_dir, 'INPUT', 'coupler.res')
        else:
            print('*** WARNING: coupler_path not available in RESTART or INPUT.  Using default value, {}'.format(default_restart_date))
            #print('*** ERROR: No coupler_path. Use default value, {}'.format(default_current_date))
            return default_restart_date
            
        #
        #if not os.path.isfile(coupler_path):
        #    print('ERROR: no coupler_path')
        #    return restart_date
        #
        with open(coupler_path, 'r') as fin:
            cal_type = fin.readline().split()[0]
            for rw in fin:
                if rw.startswith('\n'):
                    continue
                #
                # ... and keep going! we want the last date. we could also just iterate to EOF and then just read the last line.
                # TODO: unindent this line to do the above?... spin through all rows, then process the last one. this assumes
                #  this file only contains dates.
                restart_date = ','.join(rw.split()[0:6])
            #
        #
        return restart_date
        #
    def get_input_data(self, work_dir=None, input_dir=None, input_tar=None, input_data_url=None,
                       force_copy=None, verbose=None, copy_timeout=None, diag_table_src=None):
        if work_dir is None:
            work_dir = self.work_dir
        force_copy = force_copy or self.force_copy_input
        input_dir = input_dir or self.input_data_path
        input_tar = input_tar or self.input_data_tar
        input_data_url = input_data_url or self.input_data_url
        copy_timeout = copy_timeout or self.copy_timeout
        diag_table_src = diag_table_src or self.diag_table_src
        if verbose is None:
            verbose = self.verbose
        if verbose is None:
            verbose = False
        #
        # root-dir for tar file:
        if not os.path.isdir(os.path.dirname(input_tar)):
            os.makedirs(os.path.dirname(input_tar))
        #
        # It is possible we might create work_dir in advance to add some files, but not copy all the data,
        #. so let's use INPUT as our test case.
        # TODO: better tests to (not) copy
        #input_dir = os.path.join(work_dir, 'INPUT')
        #
        print('*** DEBUG: os.path.isdir(os.path.join(work_dir, \'INPUT\'))={}'.format(os.path.isdir(os.path.join(work_dir, 'INPUT'))))
        #
       # what is a minimum file-count for INPUT? the default input config is ~500 files.
        if not os.path.isdir(work_dir):
            os.makedirs(work_dir)
        #
        if not os.path.isdir(os.path.join(work_dir, 'INPUT')) or len(os.listdir(os.path.join(work_dir, 'INPUT')))<100 or force_copy:
            # work_dir is not there or not complete, so
            # we're going to copy data from the input source to the workdir.
            # Do we have an input source?
            #
            # TODO: check for isdir(.input_path), then for .tar here.
            if not os.path.isdir(input_dir):
                # input data are not available; go get them!
                #
                if verbose:
                    print('*** VERBOSE: os.path.isfile(input_tar)={}'.format(os.path.isfile(input_tar)))
                if not os.path.isfile(input_tar):
                    # No TAR file avilble; we'll have to get it...
                    # TODO: consider downloading data first, then opening and writing file to mitigate
                    #. opportunities for contamination.
                    if verbose: print('*** VERBOSE: fetching data from {}'.format(input_data_url))
                    #
                    # NOTE: requests. does not support ftp, so use urllib or urllib2
                    with contextlib.closing(urllib.request.urlopen(input_data_url)) as url_fin:
                        with open(input_tar, 'wb') as fout:
                            shutil.copyfileobj(url_fin, fout)
                #
                if verbose:
                    print('*** VERBOSE: untarring * {} * to: {} '.format(input_tar, input_dir))
                with tarfile.open(input_tar, 'r:gz') as tar:
                    # this is another one of those cases where a shell call might be easier...
                    tar.extractall(path=os.path.dirname(input_dir))
            #
            if verbose:
                print('*** VERBOSE: copying input data from {} to {}'.format(input_dir, work_dir))
            #
            # Nuke existing workdir? for now, let's not...
            # TODO: shutil.copy2() should work for this, but it's being tempermental, maybe about the
            #. directory. So for now, let's just subprocess the shell command and revisit later. It could
            #. be a versioing problem (subprocess and related libraries are pretty version twitchy).
            # TODO: consider using os.walk() to do this; it will be something like (but syntax details TBD):
            #  for root, dirs, files in os.walk(src, topdown=True/False):
            #        for fn in files:
            #            shutil.copy(join(root,fn), dest_path )
            # or maybe use shutil.copytree()
            #
            #src = input_dir
            #dst = work_dir
            # TODO: The Python copy options just don't seem to work very well (maybe there's a recursive option command or
            #. something to tell it we're copying a directory?). Let's just use a shell command.
            #shutil.copy2(input_dir, work_dir)
            cp_command = 'cp -rf {}/* {}/'.format(input_dir, work_dir)
            try:
                # NOTE: beware the timeout.... I think the default timeout is 60 seconds or something;
                #. this can take a while, so I've been using 6000 seconds as a default.
                #sp_output = subprocess.run(cp_command.split(chr(32)), check=True,
                #           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                sp_output = subprocess.run(cp_command, shell=True, check=True,
                           capture_output=True, timeout=copy_timeout)
            except:
                #print('*** copy error: stdout: {}, sterr: {}'.format(sp_output.stdout, sp_output=stderr) )
                print('*** COPY ERROR: {}'.format(cp_command))
                raise Exception('subprocess, copy error.')
            #
            if verbose:
                print('*** VERBOSE: copy input data complete, from {} to {}'.format(input_dir, work_dir))
            #
            # copy diag_table from a source file. We're going to construct an input.nml separately.
            # NOTE: Again, might be better to do this as a shell command, for a number of reasons.
            shutil.copy(diag_table_src, os.path.join(work_dir, 'diag_table'))
            #
        if not os.path.isdir(os.path.join(work_dir, 'RESTART')):
            os.makedirs(os.path.join(work_dir, 'RESTART'))
        #
    #
    def make_NML(self, nml_template=None, nml_configs=[], nml_out=None, json_out=None):
        '''
        # Some logic to managing and writing nml output.
        # @nml_template: An nml file or .json as a starter place.
        # @ nml_configs: 1 or more dicts (allow json filenames??) with configuration(s); they will be
        #.  integrated, in order, via dict.update(nml_config)
        #
        '''
        # add any default configs:
        # NOTE: putting default_nml_reconfig first allows the user to override.
        nml_configs = [self.default_nml_reconfig] + list(nml_configs)
        nml_template = nml_template or self.nml_template
        
        # determine the correct NML_from{} function, "f_handler":
        if nml_template.endswith('.nml'):
            f_handler = NML_from_nml
            #NML = NML_from_nml(nml_template, output=None)
        elif nml_template.endswith('.json'):
            #NML = NML_from_json(nml_template, output=None)
            f_handler = NML_from_json
        else:
            # guess?
            # TODO: crack it open and look for .nml or
            #NML = NML_from_nml(nml_template, json_out=None)
            with open(nml_template, 'r') as fin:
                f_handler = NML_from_json
                for rw in fin:
                    if rw.startswith('&coupler_nml'):
                        # it is probably a .nml file.
                        f_handler = NML_from_nml
                        break
                    #
        NML = f_handler(nml_template, None)
        #
        for config in nml_configs:
            #
            if isinstance(config, str):
                with open(config, 'r') as fin:
                    config = json.load(config)
                #
            #
            #NML.update(config)
            for ky,d in config.items():
                NML[ky].update(d)
            #
        #
        if not nml_out is None:
            NML.json_to_nml(nml_out=nml_out)
        if not json_out is None:
            with open(json_out, 'w') as fout:
                json.dump(NML, fout)
            #
        self.NML=NML
        #
        return NML
    #
    def write_batch_script(self, fname_out=None, chdir=None, output_out=None, output_err=None,
                           mpi_exec=None, slurm_partition=None, slurm_time=None):
        '''
        # Just as it sounds; write an AM4 batch script. use various inputs (prams, json, dicts?);
        #. fetch, untar, copy input data as necessary, etc.
        # Let's start by just scripting it out (mostly), and then we'll decide what to read in as
        #. input prams, what to read in from JSON (or something), etc. Note that, for now, this will
        #  focus on a SE3 Mazama build/configuration.
        '''
        # TODO: add 'slurm_constraint' if available.
        #
        #fname_out = fname_out or os.path.join(self.work_dir, self.batch_out)
        fname_out = fname_out or self.batch_out
        chdir = chdir or self.work_dir
        output_out = output_out or 'AM4_out_%j.out'
        output_err = output_err or 'AM4_out_%j.err'
        mpi_exec = mpi_exec or self.mpi_exec
        slurm_partition = slurm_partition or self.slurm_partition
        slurm_time = slurm_time or self.slurm_time
        #
        with open(fname_out, 'w') as fout:
            # This section should be pretty universal:
            fout.write('#!/bin/bash\n#\n')
            #
            fout.write('#SBATCH --ntasks={}\n'.format(self.n_tasks))
            fout.write('#SBATCVH --ncpus_per_task={}\n'.format(self.nthreads_atmos))
            if not self.job_name is None or self.job_name=='':
                fout.write('#SBATCH --job-name={}\n'.format(self.job_name))
            #
            fout.write('#SBATCH --chdir={}\n'.format(chdir) )
            fout.write('#SBATCH --output={}\n'.format(output_out))
            fout.write('#SBATCH --error={}\n'.format(output_err))
            #
            if not slurm_partition is None:
                fout.write('#SBATCH --partition={}\n'.format(slurm_partition))
            if not slurm_time is None:
                fout.write('#SBATCH --time={}\n'.format(slurm_time))
            #
            # Module swill be platform dependent. We could handle this section with JSON
            #. if we wanted to.
            fout.write('#\nmodule purge\n#\n')
            #
            for m in self.modules:
                fout.write('module load {}\n'.format(m))
            #
            fout.write('#\n#\n')
            # Universal??? My guess is we can impprove performance by increasing these values on bigger
            #. memory machines.
            # not sure about OMP_THREADS really, but it's worth a shot...
            fout.write('export OMP_THREADS=1\n\n')
            # these probably need to be parameterized somehow, or included in a template... or otherwise
            #. we need to figure out what they should be. I just copied them from GFDL sample scripts.
            fout.write('export KMP_STACKSIZE=512m\n')
            fout.write('export NC_BLKSZ=1M\n')
            fout.write('export F_UFMTENDIAN=big\n')
            #
            # executable will be pretty system/build dependent
            fout.write('EXECUTABLE=${AM4_GFDL_BIN}/${AM4_GFDL_EXE}\n')
            #
            # We can probably make this part pretty universal as well...
            fout.write('#\nulimit -s unlimited\n#\n')
            fout.write('#\ncd {}\n#\n'.format(self.work_dir))
            #
            # NOTE: I don't think we can use threads anyway, so let's just not allow it here.
            #  we'll probaly need to go back and force it to 1 above as well.
#            fout.write('MPI_COMMAND=\"{} {}{} {}{} ${{EXECUTABLE}}\"\n#\n'.format(mpi_exec['exec'],
#                                                            mpi_exec['ntasks'], self.n_tasks,
#                                                            mpi_exec['cpu_per_task'], self.n_threads))
            fout.write('MPI_COMMAND=\"{} {}{} ${{EXECUTABLE}}\"\n#\n'.format(mpi_exec['exec'],
                                                            mpi_exec['ntasks'], self.n_tasks)
                                                            )

            fout.write('echo ${MPI_COMMAND}\n')
            #
            fout.write('${MPI_COMMAND}\n\n')
            # add an error-check:
            for ln in ['if [[ $? -ne 0 ]]; then', 'echo "ERROR: Run failed." 1>&2',
                       '"ERROR: Output from run in {}/fms.out ... or maybe in a log file" 1>&2'.format(self.work_dir),
                       'exit 1', 'fi' ]:
                fout.write('{}\n'.format(ln))
            #
        #
        xx = subprocess.run('chmod 755 {}'.format(fname_out).split(), check=True, capture_output=True)
    #
#
def get_AM4_layouts(n_tasks=24):
    '''
    # compute possible layouts. Include (some) error checking for valid n_tasks?
    '''
    # get all integer factor pairs:
    return numpy.array(sorted([(k,int(n_tasks/k)) for k in range(1, int(numpy.ceil(n_tasks**.5)))
                               if n_tasks%k==0],
                                key = lambda rw: numpy.sum(rw)))
    #
#
def get_AM4_io_layouts(layout):
    '''
    # AM4 io_layouts. the second "y" term must be an integer factor of the "y" term of the input layout.
    #. Don't yet understand the first term, so for now let's limit it to 1.
    '''
    #
    return numpy.array(sorted([(1,int(layout[1]/k)) for k in range(1, int(numpy.ceil(layout[1]**.5)))
                               if layout[1]%k==0],
                              key=lambda rw:numpy.sum(rw)))
    #

          
