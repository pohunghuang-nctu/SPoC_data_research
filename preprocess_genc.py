import os, sys
import pandas as pd
import math
import argparse


code_prefix = '''
#include <string>
#include <iostream>
#include <bits/stdc++.h>
#include "stdio.h"
using namespace std;

'''


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--data_file', type=str, default='test/spoc-testw.tsv',
        help='data file')
    parser.add_argument(
        '--output_root', type=str, default='output/testw',
        help='root folder of output'
    )
    return parser.parse_args()
    

args = parse_args()
data_file = args.data_file
output_root = args.output_root

assert os.path.exists(data_file), f'data file: {data_file} inexists.'

df = pd.read_csv(data_file, sep='\t')
problems = df['probid'].unique()
problems.sort()

total_num_prob = len(problems)
total_num_sub = len(df['subid'].unique())
total_num_worker = len(df['workerid'].unique())
print(f'problems:{total_num_prob}, subids:{total_num_sub}, workers:{total_num_worker}')
for i, prob in enumerate(problems):
    out_folder = os.path.join(output_root, prob)
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    prob_subset = df[df['probid'] == prob]
    subids = prob_subset['subid'].unique()
    subids.sort()
    for j, sid in enumerate(subids):
        # if prob == '18A' and sid == 47832610:
        #    print('18A/47832610')
        program_df = prob_subset[prob_subset['subid'] == sid]
        workers = program_df['workerid'].unique()
        for x, wid in enumerate(workers):
            pw_df = program_df[program_df['workerid'] == wid]
            pw_df.sort_values(by=['line'])
            codelines = pw_df['code'].tolist()
            texts = pw_df['text'].tolist()
            indents = pw_df['indent'].tolist()
            lines = list()
            for k, line in enumerate(codelines):
                lines.append(f'{" " * 2 * indents[k]}{line} {"// " + texts[k] if isinstance(texts[k], str) else ""}')
                
            program_path = os.path.join(out_folder, f'{sid}-{wid}.cpp')
            with open(program_path, 'w') as ofile:
                ofile.write(code_prefix + '\n'.join(lines))
        
# print(df['probid'].unique())

