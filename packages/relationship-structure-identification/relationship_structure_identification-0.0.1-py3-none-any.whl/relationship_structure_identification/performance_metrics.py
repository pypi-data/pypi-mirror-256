#     Copyright (c) <2024> <University of Paderborn>
#     Signal and System Theory Group, Univ. of Paderborn, https://sst-group.org/
#     https://github.com/SSTGroup/relationship_structure_identification
#
#     Permission is hereby granted, free of charge, to any person
#     obtaining a copy of this software and associated documentation
#     files (the "Software"), to deal in the Software without restriction,
#     including without limitation the rights to use, copy, modify and
#     merge the Software, subject to the following conditions:
#
#     1.) The Software is used for non-commercial research and
#        education purposes.
#
#     2.) The above copyright notice and this permission notice shall be
#        included in all copies or substantial portions of the Software.
#
#     3.) Publication, Distribution, Sublicensing, and/or Selling of
#        copies or parts of the Software requires special agreements
#        with the University of Paderborn and is in general not permitted.
#
#     4.) Modifications or contributions to the software must be
#        published under this license. The University of Paderborn
#        is granted the non-exclusive right to publish modifications
#        or contributions in future versions of the Software free of charge.
#
#     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#     EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
#     OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#     NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
#     HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
#     WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#     FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
#     OTHER DEALINGS IN THE SOFTWARE.
#
#     Persons using the Software are encouraged to notify the
#     Signal and System Theory Group at the University of Paderborn
#     about bugs. Please reference the Software in your publications
#     if it was used for them.


import numpy as np
from sklearn.metrics import adjusted_mutual_info_score
import argparse
from pathlib import Path


def calculate_detection_probability(n_subblocks_true, n_subblocks_estimated):
    # for each SCV, return 1 if number of subblocks was estimated correctly, 0 else
    n_estimated_correctly = (n_subblocks_true == n_subblocks_estimated) * 1  # *1 converts bool to int
    return n_estimated_correctly


def calculate_clustering_accuracy(labels_true, labels_pred):
    score = adjusted_mutual_info_score(labels_true, labels_pred)
    return score


if __name__ == '__main__':
    # read arguments of terminal
    parser = argparse.ArgumentParser(description='Print args', fromfile_prefix_chars='@')
    parser.add_argument('--rho', type=float, help='Correlation value.')
    parser.add_argument('--nmontecarlo', type=int, default=50, help='Number of independent simulations.')

    args = parser.parse_args()
    # for running the code locally without using the terminal, uncomment the following line
    # args = parser.parse_args('--nmontecarlo 2 --rho 0.8'.split())

    rho = args.rho
    n_montecarlo = args.nmontecarlo

    p_true = []

    corr_iva = []
    t_iva = []
    p_iva = []
    p_d_b = []
    d_hat_b = []
    p_d_g = []
    d_hat_g = []
    p_d_e = []
    d_hat_e = []

    isi = []
    clustering_accuracy = []

    print('Start calculation of performance metrics...')
    for run in range(n_montecarlo):
        data = np.load(Path(Path(__file__).parent.parent, f'simulations/rho{rho}_run{run}.npy'),
                       allow_pickle=True).item()
        true_data = data['true']
        iva_results = data['iva']

        # true
        cov_true = true_data['scv_cov']
        mixing_true = true_data['A']
        sources_true = true_data['S']
        n_subblocks_true = true_data['d']
        labels_true = true_data['labels']

        # iva
        cov_iva = iva_results['scv_cov']
        mixing_iva = iva_results['A']
        sources_iva = iva_results['S']
        time_iva = iva_results['time']
        isi_iva = iva_results['isi']

        t_iva.append(time_iva)
        isi.append(isi_iva[-1])

        # subblocks
        n_subblocks_b = data['n_subblocks']['bootstrap']
        p_d_b.append(calculate_detection_probability(n_subblocks_true, n_subblocks_b))
        d_hat_b.append(n_subblocks_b)
        n_subblocks_g = data['n_subblocks']['gershgorin']
        p_d_g.append(calculate_detection_probability(n_subblocks_true, n_subblocks_g))
        d_hat_g.append(n_subblocks_g)
        n_subblocks_e = data['n_subblocks']['eigval']
        p_d_e.append(calculate_detection_probability(n_subblocks_true, n_subblocks_e))
        d_hat_e.append(n_subblocks_e)

        # classification
        labels_estimated = data['clustering']
        clustering_accuracy.append(calculate_clustering_accuracy(labels_true, labels_estimated))

    print(f'Save metrics as simulations/metrics_rho{rho}.npy.')
    np.save(Path(Path(__file__).parent.parent, f'simulations/metrics_rho{rho}.npy'),
            {'p_d': {'bootstrap': p_d_b, 'eigval': p_d_e, 'gershgorin': p_d_g},
             'time': t_iva,
             'd_hat': {'true': n_subblocks_true, 'bootstrap': d_hat_b, 'eigval': d_hat_e, 'gershgorin': d_hat_g},
             'clustering': clustering_accuracy, 'isi': isi})
