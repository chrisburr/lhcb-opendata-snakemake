#!/usr/bin/env python3
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import re

import numpy as np
from root_numpy import list_trees
from root_pandas import read_root, to_root

mass_dict = {
    'K': 493.677,
    'Pi': 139.57018,
}
pid_cut = 0.5


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-fns', nargs=2, required=True)
    parser.add_argument('--output-fn', required=True)
    parser.add_argument('--products', required=True)
    args = parser.parse_args()
    match = re.match('(K|Pi)(K|Pi)(K|Pi)', args.products)
    if match:
        h1, h2, h3 = match.groups()
    else:
        raise ValueError(f'Failed to parse products: {args.products}')
    run(args.input_fns, args.output_fn, h1, h2, h3)


def run(input_fns, output_fn, h1, h2, h3):
    keys = list_trees(input_fns[0])
    assert len(keys) == 1, keys
    df = read_root(input_fns, keys[0])

    df['H1_isMuon'] = df['H1_isMuon'].astype(np.bool)
    df['H2_isMuon'] = df['H2_isMuon'].astype(np.bool)
    df['H3_isMuon'] = df['H3_isMuon'].astype(np.bool)

    # Sort the columns so that the first is the most kaon-like
    assert sorted([h1, h2, h3]) == [h1, h2, h3], 'Children are ranked from kaon-like to pion-like'
    order = np.argsort(df[['H3_ProbK', 'H2_ProbK', 'H1_ProbK']], axis=1)
    for col in [c for c in df.columns if c.startswith('H1_')]:
        col = col[len('H1_'):]
        cols = [f'H1_{col}', f'H2_{col}', f'H3_{col}']
        df[cols] = df[cols].values[np.arange(order.shape[0])[:, None], order]

    # Compute the PE and mass of all particles
    for head, mass in [('H1', mass_dict[h1]), ('H2', mass_dict[h2]), ('H3', mass_dict[h3])]:
        df.eval(f'{head}_P = sqrt({head}_PX**2 + {head}_PY**2 + {head}_PZ**2)', inplace=True)
        df.eval(f'{head}_PE = sqrt({mass}**2 + {head}_P**2)', inplace=True)
    for component in ['PE', 'PX', 'PY', 'PZ']:
        df.eval(f'B_{component} = H1_{component} + H2_{component} + H3_{component}', inplace=True)
    df.eval(f'B_M = sqrt(B_PE**2 - B_PX**2 - B_PY**2 - B_PZ**2)', inplace=True)

    # if [h1, h2, h3] == ['K', 'K', 'K']:
    # Apply ignore muons
    df.query('~(H1_isMuon | H2_isMuon | H3_isMuon)', inplace=True)
    # Apply an additional selection
    df.query(f'(H1_IPChi2 > 25) & (H2_IPChi2 > 25) & (H3_IPChi2 > 25)', inplace=True)
    # Apply a PID selection
    df.query(f'(H1_Prob{h1} > {pid_cut}) & (H2_Prob{h2} > {pid_cut}) & (H3_Prob{h3} > {pid_cut})', inplace=True)

    to_root(df, output_fn, key=f'B2{h1}{h2}{h3}', mode='w', store_index=False)


if __name__ == '__main__':
    parse_args()
