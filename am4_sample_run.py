
import os
import AM4py
import subprocess

if __name__ == '__main__':
    #
    input_data_path = os.path.join(os.environ['SCRATCH'], 'AM4', 'AM4_data3', 'AM4_run')
    work_dir = os.path.join(os.environ['SCRATCH'], 'AM4', 'workdir3')
    job_name = 'AM4_dev'
    batch_job_name = os.path.join(work_dir, 'AM4_batch_example.bs')
    n_cpu_atmos = 48
    #
    #print('*** input_data_path: ', input_data_path)
    #
    ABS = AM4py.AM4_batch_scripter(input_data_path=input_data_path, work_dir=work_dir, npes_atmos=n_cpu_atmos,
                               job_name='AM4_dev', batch_out=batch_job_name,
                                verbse=True )
    #
    print('*** ABS variables:')
    for key,val in ABS.__dict__.items():
        print('{}: {}'.format(key,val))
    #
    zz = ABS.get_input_data(verbose=True)
    #
    # NOTE: To do a restart:
    #  move all RESTART files to INPUT
    #  update the start date of the simulation (in nml)
    #  set: fv_core_nml
    #            adjust_dry_mass = .false.
    my_configs = {'coupler_nml':{'days':15, 'months':0}, 'fv_core_nml':{'npx':97, 'npy':97, 'npz':33}}
    #
    my_nml = ABS.make_NML(nml_template='input_yoder_v101.nml', nml_configs=[my_configs],
                      nml_out=os.path.join(ABS.work_dir, 'input.nml') )
    # NML_from_nml('input_yoder_v101.nml')
    #
    #my_nml = NML_from_nml('input_yoder_v101.nml')
    print('** my_nml[fv_core_nml]:' )
    print('** ', my_nml['fv_core_nml'])
    #print(my_nml.keys())
    #
    print('** batch_out: ', ABS.batch_out)
    #
    ABS.write_batch_script()
    #
    sbatch_output = subprocess.run('sbatch {}'.format(ABS.batch_out), shell=True, check=True, capture_output=True )
