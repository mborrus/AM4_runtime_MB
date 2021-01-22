
import os
import AM4py
import subprocess

if __name__ == '__main__':
    #
    input_data_path = os.path.join(os.environ['HOME'], 'Codes', 'AM4_data2', 'AM4_run')
    work_dir = os.path.join(os.environ['HOME'], 'Codes', 'AM4_runtime', 'workdir2')
    job_name = 'AM4_dev'
    batch_job_name = os.path.join(work_dir, 'AM4_batch_example.bs')
    #
    #print('*** input_data_path: ', input_data_path)
    #
    ABS = AM4py.AM4_batch_scripter(input_data_path=imput_data_path, work_dir=work_dir,
                               job_name='AM4_dev', batch_out=batch_job_name )
    #
    print('*** ABS variables:')
    for key,val in ABS.__dict__.items():
    print('{}: {}'.format(key,val))
    #
    zz = ABS.get_input_data(verbose=True)
    #
    my_configs = {'coupler_nml':{'days':10, 'months':0}, 'fv_core_nml':{'npx':193, 'npy':193, 'npz':50}}
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
    #sbatch_output = subprocess.run('sbatch {}'.format(ABS.batch_out), check=True, capture_output=True )
