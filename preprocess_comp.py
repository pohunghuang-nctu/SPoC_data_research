import os, sys
import pandas as pd
import glob
import argparse
import subprocess


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--code_root', type=str, default='output/testw',
        help='data file')
    parser.add_argument(
        '--exec_root', type=str, default='exec/testw'
    )
    
    return parser.parse_args()
    

def compile(cpp_file_path, exec_path):
    cmd = f"g++ -o {exec_path} {cpp_file_path}"
    completed_process = subprocess.run(cmd, shell=True, capture_output=True) 
    return completed_process.returncode, completed_process.stdout, completed_process.stderr   


args = parse_args()
code_root = args.code_root
exec_root = args.exec_root

cpp_files = glob.glob(os.path.join(code_root, '**/*.cpp'))
num_cpps = len(cpp_files)
fail_cnt = 0
for i, cppfile in enumerate(cpp_files):
    # print(f'{i}: {cppfile}')
    exec_path = cppfile.replace(code_root, exec_root).replace('.cpp', '.out')
    if os.path.exists(exec_path):
        continue
    if not os.path.exists(os.path.dirname(exec_path)):
        os.makedirs(os.path.dirname(exec_path))
    ret, out, err = compile(cppfile, exec_path)
    if ret == 0:
        #print(f'compiled pass')
        pass
    else:
        fail_cnt += 1
        print(f'{i}: {cppfile}')
        print(f'{err.decode("utf-8")}')
print(f'{fail_cnt} fail of {num_cpps}')

