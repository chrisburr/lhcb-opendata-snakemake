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

mass_binning = np.linspace(5050, 6300, 250)
p_binning = np.linspace(0, 5e5, 200)
pid_cut = 0.5


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-fn', required=True)
    parser.add_argument('--mass-fn', required=True)
    parser.add_argument('--p-fn', required=True)
    parser.add_argument('--key', required=True)
    args = parser.parse_args()
    run(args.input_fn, args.mass_fn, args.p_fn, args.key)


def run(input_fn, mass_fn, p_fn, key):
    df = read_root(input_fn, key)

    df['B_M'].hist(bins=mass_binning, histtype='step')
    plt.axvline(sig_mass_low, color='k', linestyle='--')
    plt.axvline(sig_mass_high, color='k', linestyle='--')
    plt.xlabel('B mass [MeV/c²]')
    plt.xlim(mass_binning[0], mass_binning[-1])
    plt.gcf().patch.set_alpha(0)
    plt.savefig(mass_fn, bbox_inches='tight')
    plt.close()

    df.eval('sqrt(B_PX**2 + B_PY**2 + B_PZ**2)').hist(bins=p_binning, histtype='step')
    plt.xlabel('B momentum [MeV/c]')
    plt.xlim(p_binning[0], p_binning[-1])
    plt.gcf().patch.set_alpha(0)
    plt.savefig(p_fn, bbox_inches='tight')
    plt.close()

    for i in range(1, 4):
        df.eval(f'sqrt(H{i}_PX**2 + H{i}_PY**2 + H{i}_PZ**2)').hist(bins=p_binning, histtype='step')
        plt.xlabel(f'H{i} momentum [MeV/c]')
        plt.xlim(p_binning[0], p_binning[-1])
        plt.gcf().patch.set_alpha(0)
        plt.savefig(p_fn.replace('/B_', f'/H{i}_'), bbox_inches='tight')
        plt.close()


if __name__ == '__main__':
    parse_args()
