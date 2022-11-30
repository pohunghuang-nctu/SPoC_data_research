import os, sys
import glob
import argparse
import subprocess
import json
import collections


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--test_cases_root', type=str, default='testcases',
        help='root folder of test cases')
    parser.add_argument(
        '--test_cases_type', choices=['public', 'hidden', 'custom'], default='public',
        help='the testcases file naming would be <probid>_testcases_<test_cases_type>')
    parser.add_argument(
        '--exec_root', type=str, default='exec/testw'
    )
    
    return parser.parse_args()


def read_tcs(tcf):
    with open(tcf, 'r') as rfile:
        input = True
        tc_list = list()
        tc = {'input': '', 'output': ''}
        for line in rfile:
            if line.startswith('###END'):
                if 'INPUT' in line: ###ENDINPUT###
                    input = False # next line is output
                else: ###ENDOUTPUT###
                    # end of current test case.
                    tc_list.append(tc)
                    input = True # next line is input
                    tc = {'input': '', 'output': ''} # reset tc dict
            else:
                if input:
                    tc['input'] += line
                else:
                    tc['output'] += line
    return tc_list


def do_test(exe_path, tc_dict):
    probid = os.path.dirname(exe_path).split('/')[-1]
    tcs = tc_dict[probid]
    num_tc = len(tcs)
    print(f'total {num_tc} cases to test.')
    pass_cnt = 0
    fail = False
    for i, io in enumerate(tcs):
        input, output = io.values()
        cmd = exe_path
        cp = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, input=input)
        if cp.returncode == 0: # success
            if cp.stdout == output:
                pass_cnt += 1
            else:
                fail = True
        else:
           fail = True
           print(f'return code !=0, ret_code:{cp.returncode}')
    print(f'{pass_cnt}/{num_tc} tcs passed')
    return not fail


args = parse_args()
root = args.test_cases_root
tc_type = args.test_cases_type
exe_root = args.exec_root
tc_files = glob.glob(f'{root}/*/*_testcases_{tc_type}.txt')

tc_dict = dict()
for i, tcf in enumerate(tc_files):
    print(tcf)
    prob = os.path.basename(tcf).split('_')[0]
    tc_dict[prob] = read_tcs(tcf) 
    
with open('test_cases.json', 'w') as jofile:
    sorted_dict = dict(sorted(tc_dict.items()))
    jofile.write(json.dumps(sorted_dict, indent=4))

# run test for each executables
execs = glob.glob(f'{exe_root}/*/*.out')
print(f'total {len(execs)} programs to be tested.')
pass_cnt = 0
for i, exe_path in enumerate(execs):
    prob_id = os.path.dirname(exe_path)
    sub_id, worker_id = os.path.basename(exe_path).replace('.out', '').split('-')
    print(f'problem:{prob_id}, program:{sub_id}, author:{worker_id}')
    result = do_test(exe_path, tc_dict)
    pass_cnt += result
print(f'{pass_cnt} /{len(execs)} tested pass.')

