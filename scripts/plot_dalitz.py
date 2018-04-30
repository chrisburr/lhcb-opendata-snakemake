#!/usr/bin/env python3
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import json

import matplotlib
matplotlib.use('Agg')  # NOQA
from matplotlib import pyplot as plt
import numpy as np
from root_pandas import read_root


with open('config/mass_window.json', 'rt') as fp:
    config = json.load(fp)
sig_mass_low = config['sig_mass_low']
sig_mass_high = config['sig_mass_high']

dalitz_bins = np.linspace(0, 5500, 100)
cp_bins = np.linspace(0, 5500, 50)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-fn', required=True)
    parser.add_argument('--key', required=True)
    parser.add_argument('--bplus-dalitz-fn', required=True)
    parser.add_argument('--bminus-dalitz-fn', required=True)
    parser.add_argument('--cp-plot-fn', required=True)
    parser.add_argument('--integrated-tex-fn', required=True)
    args = parser.parse_args()
    run(args.input_fn, args.key, args.bplus_dalitz_fn, args.bminus_dalitz_fn,
        args.cp_plot_fn, args.integrated_tex_fn)


def savefig(fn):
    plt.colorbar()
    plt.gcf().patch.set_alpha(0)
    plt.savefig(fn, bbox_inches='tight')
    plt.close()


def run(input_fn, key, bplus_dalitz_fn, bminus_dalitz_fn, cp_plot_fn, integrated_tex_fn):
    df = read_root(input_fn, key, columns='')
    df.eval('M12 = sqrt((H1_PE+H2_PE)**2 - (H1_PX+H2_PX)**2 - (H1_PY+H2_PY)**2 - (H1_PZ+H2_PZ)**2)', inplace=True)
    df.eval('M23 = sqrt((H2_PE+H3_PE)**2 - (H2_PX+H3_PX)**2 - (H2_PY+H3_PY)**2 - (H2_PZ+H3_PZ)**2)', inplace=True)
    df.eval('B_Charge = H1_Charge + H2_Charge + H3_Charge', inplace=True)
    df.query(f'({sig_mass_low} < B_M) & (B_M < {sig_mass_high})', inplace=True)

    df_bplus = df.query('B_Charge == 1')
    df_bminus = df.query('B_Charge == -1')

    plt.hist2d(df_bplus['M12'], df_bplus['M23'], bins=dalitz_bins)
    savefig(bplus_dalitz_fn)

    plt.hist2d(df_bminus['M12'], df_bminus['M23'], bins=dalitz_bins)
    savefig(bminus_dalitz_fn)

    bp_counts, xedges, yedges = np.histogram2d(df_bplus['M12'], df_bplus['M23'], bins=cp_bins)
    bm_counts, xedges, yedges = np.histogram2d(df_bminus['M12'], df_bminus['M23'], bins=cp_bins)
    Z = (bp_counts-bm_counts)/(bp_counts+bm_counts)
    X, Y = np.meshgrid(yedges, xedges)
    plt.pcolormesh(X, Y, Z, cmap='RdBu', vmin=-0.1, vmax=0.1)
    savefig(cp_plot_fn)

    N_bplus = len(df_bplus)
    N_bminus = len(df_bminus)
    A_CP = (N_bplus-N_bminus)/(N_bplus+N_bminus)
    # TODO: Include an error
    with open(integrated_tex_fn, 'wt') as fp:
        fp.write(f'$B^+$ yield is {N_bplus}\n\n'
                 f'$B^-$ yield is {N_bminus}\n\n'
                 f'$A_\\text{{CP}}$ = \\SI{{{A_CP*100:.2f}}}{{\percent}}\n')


if __name__ == '__main__':
    parse_args()
