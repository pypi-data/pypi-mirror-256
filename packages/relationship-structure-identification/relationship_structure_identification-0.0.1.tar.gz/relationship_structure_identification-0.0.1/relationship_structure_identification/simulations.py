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
import argparse
from pathlib import Path
import time

from independent_vector_analysis.consistent_iva import consistent_iva
from independent_vector_analysis.data_generation import _create_covariance_matrix

from relationship_structure_identification.grouping_identification import detect_number_blocks_using_bootstrap, \
    detect_number_blocks_using_gershgorin, detect_number_blocks_using_direct_eigval, cluster_datasets


def mv_laplacian(num_samples, cov):
    """
    Draw samples from a multivariate Laplace distribution.


    Parameters
    ----------
    num_samples : int
        Number of samples

    cov : np.ndarray
        Covariance matrix of the multivariate Laplace distribution, of dimension K x K

    Returns
    -------
    Y : np.ndarray
        Matrix of dimension n_samples x K consisting of the samples of the MV Laplace distribution

    """

    W = np.random.standard_exponential(size=num_samples)
    N = np.random.multivariate_normal(np.zeros(cov.shape[0]), cov, size=num_samples)

    Y = np.sqrt(W[:, np.newaxis]) * N

    return Y


def detect_number_of_blocks(sources, P_fa=0.05, B=1000):
    # detect number of blocks with the three methods for given sources of dimension n_comp x n_samples x n_datasets (K)
    n_c = sources.shape[0]
    n_blocks_bt = np.zeros(n_c, dtype=int)
    n_blocks_g = np.zeros(n_c, dtype=int)
    n_blocks_e = np.zeros(n_c, dtype=int)
    for idx in range(n_c):
        n_blocks_bt[idx] = detect_number_blocks_using_bootstrap(sources[idx, :, :], P_fa=P_fa, B=B)
        n_blocks_g[idx] = detect_number_blocks_using_gershgorin(sources[idx, :, :])
        n_blocks_e[idx] = detect_number_blocks_using_direct_eigval(sources[idx, :, :])

    return n_blocks_bt, n_blocks_g, n_blocks_e


def generate_cov(rho):
    """
    Generate 10 x 10 covariance matrix for 6 SCVs: 1s on the diagonal, rho+n in blocks, 0s outside of blocks, and
    blocks on the positions as defined in our paper.

    Parameters
    ----------
    rho : float
        Correlation value in the blocks

    Returns
    -------
    cov : np.ndarray
        Covariance matrix for all SCVs of dimensions 10 x 10 x 6
    """

    cov = np.zeros((10, 10, 6))

    # common SCV
    cov[:, :, 0] = _create_covariance_matrix(dim=10, correlation_structure='noisy_block',
                                             rho={'blocks': (rho, 0, 10), 'val': 0.0})
    # structured SCVs
    cov[:, :, 1] = _create_covariance_matrix(dim=10, correlation_structure='noisy_block',
                                             rho={'blocks': [(rho, 0, 4), (rho, 4, 6)], 'val': 0.0})

    cov[:, :, 2] = _create_covariance_matrix(dim=10, correlation_structure='noisy_block',
                                             rho={'blocks': [(rho, 0, 3), (rho, 4, 6)], 'val': 0.0})

    cov[:, :, 3] = _create_covariance_matrix(dim=10, correlation_structure='noisy_block',
                                             rho={'blocks': [(rho, 4, 3), (rho, 7, 3)], 'val': 0.0})

    cov[:, :, 4] = _create_covariance_matrix(dim=10, correlation_structure='noisy_block',
                                             rho={'blocks': [(rho, 0, 4), (rho, 4, 3), (rho, 7, 3)], 'val': 0.0})

    cov[:, :, 5] = _create_covariance_matrix(dim=10, correlation_structure='noisy_block',
                                             rho={'blocks': [(rho, 0, 2), (rho, 2, 2), (rho, 4, 3), (rho, 7, 3)],
                                                  'val': 0.0})

    return cov


def simulations(n_samples=1000, rho_c=0.9):
    # n_samples: # samples
    n_c = 6  # source components
    K = 10  # datasets
    N = n_c  # dimension of observations

    # load scv covariance matrix (We wanted to use the same cov in every run. Could also use code from generate_cov.)
    cov = np.load(Path(Path(__file__).parent.parent, f'simulations/scv_cov_rho{rho_c}.npy'))

    # true number of subblocks
    n_subblocks = np.array([1, 2, 2, 2, 3, 4])

    # true clustering labels
    clustering_labels = np.array([0, 0, 0, 0, 1, 1, 1, 1, 1, 1])

    # add noise to cov and generate sources
    sources = np.zeros((n_c, n_samples, K))
    for idx in range(n_c):
        sources[idx, :, :] = mv_laplacian(n_samples, cov=cov[:, :, idx])
        # make sources zero-mean and unit-variance
        sources[idx, :, :] -= np.mean(sources[idx, :, :], axis=0)
        sources[idx, :, :] /= np.std(sources[idx, :, :], axis=0)

    # observations
    mixing = np.random.randn(N, n_c, K)
    observations = np.zeros((N, n_samples, K))
    for k in range(K):
        observations[:, :, k] = mixing[:, :, k] @ sources[:, :, k]

    return cov, sources, mixing, observations, n_subblocks, clustering_labels


if __name__ == '__main__':
    # read arguments of terminal
    parser = argparse.ArgumentParser(description='Print args', fromfile_prefix_chars='@')
    parser.add_argument('--rho', type=float,
                        help='Correlation value.')
    parser.add_argument('--niva', type=int, default=20,
                        help='Number of runs to pick best IVA result.')
    parser.add_argument('--nmontecarlo', type=int, default=50,
                        help='Number of independent simulations.')
    parser.add_argument('--V', type=int, default=1000, help="Number of samples for the generated sources.")
    parser.add_argument('--B', type=int, default=1000,
                        help='Number of bootstrap resamples.')
    parser.add_argument('--Pfa', type=float, default=0.05,
                        help='False alarm probability for bootstrap.')
    parser.add_argument('--nclusters', type=int, default=2,
                        help='Number of clusters (necessary for returning labels to calculate AMI.')

    args = parser.parse_args()
    # for running the code locally without using the terminal, uncomment the following line
    # args = parser.parse_args('--nmontecarlo 2 --niva 2 --rho 0.8'.split())

    rho = args.rho
    n_runs_iva = args.niva
    n_montecarlo = args.nmontecarlo
    V = args.V
    B = args.B
    P_fa = args.Pfa
    n_clusters = args.nclusters

    print(f'Starting simulation.')

    for run in range(n_montecarlo):
        print(f'Start run {run}...')
        cov_true, sources_true, mixing_true, observations, n_subblocks, clustering_labels = simulations(n_samples=V,
                                                                                                        rho_c=rho)

        true_data = {'scv_cov': cov_true, 'S': sources_true, 'A': mixing_true, 'X': observations, 'd': n_subblocks,
                     'labels': clustering_labels}

        # iva
        print('Computing IVA ...')
        t_start = time.time()
        iva_results = consistent_iva(observations, which_iva='iva_l_sos', A=mixing_true, n_runs=n_runs_iva)
        t_end = time.time()
        iva_results['time'] = t_end - t_start

        # number of blocks
        n_blocks_bt, n_blocks_g, n_blocks_e = detect_number_of_blocks(sources_true)

        # clustering result
        clustering_labels = cluster_datasets(iva_results['S'], n_clusters, B, P_fa,
                                             labels=np.arange(iva_results['S'].shape[2]), plot=False)

        print(f'Save run as simulations/rho{rho}_run{run}.npy.')
        np.save(Path(Path(__file__).parent.parent, f'simulations/rho{rho}_run{run}.npy'),
                {'true': true_data,
                 'iva': iva_results,
                 'n_subblocks': {'true': n_subblocks, 'bootstrap': n_blocks_bt, 'eigval': n_blocks_e,
                                 'gershgorin': n_blocks_g},
                 'clustering': clustering_labels})
